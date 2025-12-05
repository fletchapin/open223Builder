import json
from typing import Any, Dict
from registry import class_to_id
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QPointF

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


def _pos(item) -> Dict[str, float]:
    try:
        p: QPointF = item.scenePos()
        return {"x": float(p.x()), "y": float(p.y())}
    except Exception:
        return {"x": 0.0, "y": 0.0}


def _size(item) -> Dict[str, float]:
    try:
        br = item.boundingRect()
        return {"w": float(br.width()), "h": float(br.height())}
    except Exception:
        return {"w": 0.0, "h": 0.0}


def save(scene: QGraphicsScene, path: str):
    data: Dict[str, Any] = {
        "version": 1,
        "nodes": [],
        "spaces": [],
        "connection_points": [],
        "connections": [],
        "properties": [],
        "systems": [],
    }

    for item in scene.items():
        try:
            inst_uri = getattr(item, "inst_uri", None)
            type_cls = getattr(item, "type_uri", type(item))
            cls_id = class_to_id(type_cls if isinstance(type_cls, type) else type(item))
            label = getattr(item, "label", "")
            comment = getattr(item, "comment", "")
        except Exception:
            continue

        if PhysicalSpace and isinstance(item, PhysicalSpace):
            data["spaces"].append({
                "inst_uri": str(inst_uri),
                "class": cls_id,
                "label": label,
                "comment": comment,
                **_pos(item),
                **_size(item),
            })
            continue

        if ConnectableItem and isinstance(item, ConnectableItem):
            parent = item.parentItem()
            data["nodes"].append({
                "inst_uri": str(inst_uri),
                "class": cls_id,
                "label": label,
                "comment": comment,
                **_pos(item),
                **_size(item),
                "parent": str(getattr(parent, "inst_uri", None)) if parent else None,
            })
            continue

        if ConnectionPoint and isinstance(item, ConnectionPoint):
            medium_cls = getattr(item, "medium", None)
            medium_id = class_to_id(medium_cls) if isinstance(medium_cls, type) else None
            cp_parent = item.connectable if hasattr(item, "connectable") else item.parentItem()
            data["connection_points"].append({
                "inst_uri": str(inst_uri),
                "class": class_to_id(getattr(item, "type_uri", type(item)) if isinstance(getattr(item, "type_uri", None), type) else type(item)),
                "parent": str(getattr(cp_parent, "inst_uri", None)) if cp_parent else None,
                "medium": medium_id,
                "relative_x": float(getattr(item, "relative_x", 0.5)),
                "relative_y": float(getattr(item, "relative_y", 0.5)),
                "label": label,
                "comment": comment,
            })
            continue

        if Connection and isinstance(item, Connection):
            source = getattr(item, "source", None)
            target = getattr(item, "target", None)
            medium = getattr(source, "medium", None) if source else None
            medium_id = class_to_id(medium) if isinstance(medium, type) else None
            data["connections"].append({
                "inst_uri": str(inst_uri),
                "class": cls_id,
                "source_cp": str(getattr(source, "inst_uri", None)) if source else None,
                "target_cp": str(getattr(target, "inst_uri", None)) if target else None,
                "medium": medium_id,
                "label": label,
                "comment": comment,
            })
            continue

        if SystemItem and isinstance(item, SystemItem):
            data["systems"].append({
                "inst_uri": str(inst_uri),
                "label": label,
                "comment": comment,
                "members": [str(getattr(m, "inst_uri", None)) for m in getattr(item, "members", [])],
            })
            continue

        if Property and isinstance(item, Property):
            unit = getattr(item, "unit", None)
            qk = getattr(item, "quantity_kind", None)
            data["properties"].append({
                "inst_uri": str(inst_uri),
                "class": class_to_id(getattr(item, "type_uri", type(item)) if isinstance(getattr(item, "type_uri", None), type) else type(item)),
                "parent": str(getattr(item.parentItem(), "inst_uri", None)) if item.parentItem() else None,
                "identifier": getattr(item, "identifier", None),
                "unit": str(unit) if unit is not None else None,
                "quantity_kind": str(qk) if qk is not None else None,
                "value": getattr(item, "value", None),
                "label": label,
                "comment": comment,
            })
            continue

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load(scene: QGraphicsScene, path: str) -> bool:
    import json
    from registry import id_to_class
    from commands import CompoundCommand
    try:
        from commands import AddItemCommand, AddConnectionPointCommand, AddPropertyCommand
    except Exception:
        AddItemCommand = AddConnectionPointCommand = AddPropertyCommand = None
    try:
        from items import ConnectionPoint, Property
    except Exception:
        ConnectionPoint = Property = None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    created = {}
    cmd = CompoundCommand("Load JSON")

    for bucket in ("spaces", "nodes"):
        for n in data.get(bucket, []):
            cls = id_to_class(n["class"])
            try:
                item = cls() if callable(cls) else None
                if item is None:
                    continue
                item.inst_uri = n["inst_uri"]
                item.label = n.get("label") or getattr(item, "label", "")
                item.comment = n.get("comment") or ""
                if hasattr(item, "setPos"):
                    item.setPos(n.get("x", 0.0), n.get("y", 0.0))
                if AddItemCommand:
                    add_cmd = AddItemCommand(scene, item)
                    if add_cmd.execute():
                        cmd.add_command(add_cmd)
                else:
                    scene.addItem(item)
                created[n["inst_uri"]] = item
            except Exception:
                continue

    for cpd in data.get("connection_points", []):
        try:
            parent = created.get(cpd.get("parent"))
            if not parent or not ConnectionPoint:
                continue
            cp_cls = id_to_class(cpd["class"])
            medium_cls = id_to_class(cpd["medium"]) if cpd.get("medium") else None
            cp = ConnectionPoint(connectable=parent, type_uri=cp_cls, medium=medium_cls, position=(cpd.get("relative_x", 0.5), cpd.get("relative_y", 0.5)))
            cp.inst_uri = cpd["inst_uri"]
            cp.label = cpd.get("label") or getattr(cp, "label", "")
            cp.comment = cpd.get("comment") or ""
            if AddConnectionPointCommand:
                add_cp = AddConnectionPointCommand(connection_point=cp)
                if add_cp.execute():
                    cmd.add_command(add_cp)
            else:
                scene.addItem(cp)
            created[cpd["inst_uri"]] = cp
        except Exception:
            continue

    for pd in data.get("properties", []):
        try:
            parent = created.get(pd.get("parent"))
            if not parent or not Property:
                continue
            prop = Property.new(prop_data=pd, parent=parent)
            if AddPropertyCommand:
                add_prop = AddPropertyCommand(parent_item=parent, property=prop)
                if add_prop.execute():
                    cmd.add_command(add_prop)
            else:
                scene.addItem(prop)
            created[pd["inst_uri"]] = prop
        except Exception:
            continue

    for cd in data.get("connections", []):
        try:
            conn_cls = id_to_class(cd["class"])
            source_cp = created.get(cd.get("source_cp"))
            target_cp = created.get(cd.get("target_cp"))
            if not (source_cp and target_cp):
                continue
            conn = conn_cls(source=source_cp, target=target_cp)
            conn.inst_uri = cd["inst_uri"]
            if AddItemCommand:
                add_conn = AddItemCommand(scene, conn)
                if add_conn.execute():
                    cmd.add_command(add_conn)
            else:
                scene.addItem(conn)
            created[cd["inst_uri"]] = conn
        except Exception:
            continue

    return True
