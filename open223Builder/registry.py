import importlib

def class_to_id(cls) -> str:
    if not isinstance(cls, type):
        cls = type(cls)
    return f"{cls.__module__}.{cls.__name__}"

def id_to_class(class_id: str):
    if not class_id or "." not in class_id:
        raise ValueError(f"Invalid class identifier: {class_id}")
    module, name = class_id.rsplit(".", 1)
    mod = importlib.import_module(module)
    return getattr(mod, name)
