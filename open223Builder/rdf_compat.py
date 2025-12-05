from rdflib import URIRef

# Replace this namespace with the WaTr base you use
WATR = "https://w3id.org/watr/ontology#"
PYPES_NS = "https://we3lab.org/pypes#"

# Map your PyPES classes to WaTr URIs here. Start small and expand.
# Example (uncomment and adjust once you decide the target WaTr classes):
# from pype_schema import node, connection, tag
# from library import InletConnectionPoint, OutletConnectionPoint, BidirectionalConnectionPoint, FluidWater, FluidAir, Pipe
# PYPES_TO_WATR = {
#     node.Boiler: URIRef(WATR + "Boiler"),
#     node.Valve: URIRef(WATR + "Valve"),
#     connection.Pipe: URIRef(WATR + "Pipe"),
#     InletConnectionPoint: URIRef(WATR + "Inlet"),
#     OutletConnectionPoint: URIRef(WATR + "Outlet"),
#     FluidWater: URIRef(WATR + "Water"),
#     FluidAir: URIRef(WATR + "Air"),
# }
PYPES_TO_WATR = {}
WATR_TO_PYPES = {v: k for k, v in PYPES_TO_WATR.items()}

def to_uri(cls):
    return PYPES_TO_WATR.get(cls)

def from_uri(uri):
    return WATR_TO_PYPES.get(uri)

def python_class_predicate():
    return URIRef(PYPES_NS + "pythonClass")
