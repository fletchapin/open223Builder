from rdflib import Graph, URIRef, Literal, RDF, RDFS, Namespace
from PyQt5.QtWidgets import QGraphicsScene
from registry import class_to_id
from rdf_compat import to_uri, python_class_predicate

# Import your item classes
from items import SystemItem
try:
    from items import ConnectableItem, ConnectionPoint, Connection, Property, PhysicalSpace, DomainSpace
except Exception:
    ConnectableItem = None
    ConnectionPoint = None
    Connection = None
    Property = None
    PhysicalSpace = None
    DomainSpace = None

PYPES = Namespace("https://we3lab.org/pypes#")


def _subject(item) -> URIRef:
    inst = getattr(item, "inst_uri", None)
    return URIRef(str(inst)) if inst else URIRef(f"https://we3lab.org/pypes/inst/{id(item)}")


def _add_common(g: Graph, subj: URIRef, item):
    lbl = getattr(item, "label", None)
    cmt = getattr(item, "comment", None)
    if lbl:
        g.add((subj, RDFS.label, Literal(lbl)))
    if cmt:
        g.add((subj, RDFS.comment, Literal(cmt)))
    cls = getattr(item, "type_uri", None) or type(item)
    if isinstance(cls, type):
        uri = to_uri(cls)
        if uri:
            g.add((subj, RDF.type, uri))
        else:
            g.add((subj, python_class_predicate(), Literal(class_to_id(cls))))


def save(scene: QGraphicsScene, path: str):
    g = Graph()
    g.bind("pypes", PYPES)

    for item in scene.items():
        subj = _subject(item)
        try:
            if PhysicalSpace and isinstance(item, PhysicalSpace):
                _add_common(g, subj, item)
                continue
            if ConnectableItem and isinstance(item, ConnectableItem):
                _add_common(g, subj, item)
                parent = item.parentItem()
                if parent is not None:
                    g.add((subj, PYPES.parent, _subject(parent)))
                continue
        except Exception:
            continue

    for item in scene.items():
        try:
            if ConnectionPoint and isinstance(item, ConnectionPoint):
                s = _subject(item)
                _add_common(g, s, item)
                parent = getattr(item, "connectable", None) or item.parentItem()
                if parent is not None:
                    g.add((s, PYPES.parent, _subject(parent)))
                medium_cls = getattr(item, "medium", None)
                if isinstance(medium_cls, type):
                    m_uri = to_uri(medium_cls)
                    if m_uri:
                        g.add((s, PYPES.medium, m_uri))
                    else:
                        g.add((s, python_class_predicate(), Literal(class_to_id(medium_cls))))
                g.add((s, PYPES.relativeX, Literal(float(getattr(item, "relative_x", 0.5)))))
                g.add((s, PYPES.relativeY, Literal(float(getattr(item, "relative_y", 0.5)))))
        except Exception:
            continue

    for item in scene.items():
        try:
            if Connection and isinstance(item, Connection):
                s = _subject(item)
                _add_common(g, s, item)
                src = getattr(item, "source", None)
                tgt = getattr(item, "target", None)
                if src:
                    g.add((s, PYPES.source, _subject(src)))
                if tgt:
                    g.add((s, PYPES.target, _subject(tgt)))
        except Exception:
            continue

    for item in scene.items():
        try:
            if Property and isinstance(item, Property):
                s = _subject(item)
                _add_common(g, s, item)
                parent = item.parentItem()
                if parent is not None:
                    g.add((s, PYPES.parent, _subject(parent)))
                unit = getattr(item, "unit", None)
                if unit is not None:
                    g.add((s, PYPES.unit, URIRef(str(unit))))
                qk = getattr(item, "quantity_kind", None)
                if qk is not None:
                    g.add((s, PYPES.quantityKind, URIRef(str(qk))))
                value = getattr(item, "value", None)
                if value is not None:
                    g.add((s, PYPES.value, Literal(value)))
        except Exception:
            continue

    for item in scene.items():
        try:
            if isinstance(item, SystemItem):
                s = _subject(item)
                g.add((s, RDF.type, PYPES.System))
                _add_common(g, s, item)
                for m in getattr(item, "members", []):
                    g.add((s, PYPES.member, _subject(m)))
        except Exception:
            continue

    g.serialize(path, format="turtle")


def load(scene: QGraphicsScene, path: str) -> bool:
    # Stub loader (keep your current RDF loader if you have one).
    return True
