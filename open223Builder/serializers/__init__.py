from .json_serializer import save as save_json, load as load_json
from .turtle_serializer import save as save_turtle, load as load_turtle

# convenience objects used by window.py
json_serializer = type("JsonSer", (), {"save": save_json, "load": load_json})
turtle_serializer = type("TurtleSer", (), {"save": save_turtle, "load": load_turtle})
