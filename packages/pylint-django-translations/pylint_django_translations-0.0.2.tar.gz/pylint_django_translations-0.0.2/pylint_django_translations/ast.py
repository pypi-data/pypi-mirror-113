"Identify classes in the AST"
from astroid.node_classes import NodeNG
from astroid.nodes import ClassDef


def is_translatable_model(node: NodeNG) -> bool:
    "Identify Translable model classes"
    return isinstance(node, ClassDef) and node.basenames == ["Translatable"]


def is_translatablemeta_subclass(node: NodeNG) -> bool:
    "Identify TranslatableMeta classes inside Django models"
    return (
        node.name == "TranslatableMeta"
        and isinstance(node, ClassDef)
        and isinstance(node.parent, ClassDef)
    )
