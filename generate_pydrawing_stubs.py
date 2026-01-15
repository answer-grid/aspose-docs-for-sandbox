#!/usr/bin/env python3
"""
Dynamically generate .pyi stubs for aspose.pydrawing by introspecting at runtime.
"""
import inspect
import sys
from typing import Any, List, Set
from pathlib import Path


def get_type_hint(obj: Any, name: str = "") -> str:
    """Try to infer a type hint for an object."""
    if obj is None:
        return "None"

    t = type(obj)
    type_name = t.__name__

    # Map common types
    type_map = {
        'str': 'str',
        'int': 'int',
        'float': 'float',
        'bool': 'bool',
        'bytes': 'bytes',
        'list': 'List[Any]',
        'dict': 'Dict[str, Any]',
        'tuple': 'tuple',
        'NoneType': 'None',
    }

    if type_name in type_map:
        return type_map[type_name]

    # For aspose types, use the full module path
    module = getattr(t, '__module__', '')
    if module.startswith('aspose.'):
        return f"{module}.{type_name}"

    return 'Any'


def get_signature_str(func: Any, class_name: str = "") -> str:
    """Try to extract function signature."""
    try:
        sig = inspect.signature(func)
        params = []
        for pname, param in sig.parameters.items():
            if pname == 'self':
                params.append('self')
            elif param.annotation != inspect.Parameter.empty:
                params.append(f"{pname}: {param.annotation}")
            elif param.default != inspect.Parameter.empty:
                default_type = get_type_hint(param.default)
                params.append(f"{pname}: {default_type} = ...")
            else:
                params.append(f"{pname}")

        return_hint = "Any"
        if sig.return_annotation != inspect.Signature.empty:
            return_hint = str(sig.return_annotation)

        return f"({', '.join(params)}) -> {return_hint}"
    except (ValueError, TypeError):
        return "(self, *args, **kwargs) -> Any"


def is_property(obj: Any, name: str, cls: type) -> bool:
    """Check if an attribute is a property."""
    try:
        class_attr = getattr(type(cls), name, None)
        if isinstance(class_attr, property):
            return True
        # Check for descriptor protocol
        if hasattr(class_attr, '__get__') and not callable(obj):
            return True
    except:
        pass
    return not callable(obj)


def safe_getattr(obj, name, default=None):
    """Safely get attribute, catching crashes."""
    try:
        return getattr(obj, name, default)
    except:
        return default


def safe_dir(obj) -> List[str]:
    """Safely get dir(), catching crashes."""
    try:
        return [x for x in dir(obj) if not x.startswith('_')]
    except:
        return []


def generate_class_stub(cls: type, indent: str = "") -> List[str]:
    """Generate stub for a class."""
    lines = []
    class_name = cls.__name__

    # Get base classes safely
    bases = []
    try:
        for base in cls.__bases__:
            if base.__name__ != 'object':
                base_module = getattr(base, '__module__', '')
                if base_module.startswith('aspose.'):
                    bases.append(f"{base_module}.{base.__name__}")
                else:
                    bases.append(base.__name__)
    except:
        pass

    base_str = f"({', '.join(bases)})" if bases else ""

    # Class docstring
    doc = ""
    try:
        doc = inspect.getdoc(cls) or ""
    except:
        pass
    doc = doc or f"Wrapper for .NET {class_name}"

    lines.append(f"{indent}class {class_name}{base_str}:")
    lines.append(f"{indent}    '''{doc}'''")

    # Get all member names first (safer than getting values)
    member_names = safe_dir(cls)

    if not member_names:
        lines.append(f"{indent}    ...")
        return lines

    # Separate properties and methods by checking names only first
    properties = []
    methods = []
    class_attrs = []  # For static/class attributes like Color.red

    for name in member_names:
        try:
            obj = safe_getattr(cls, name)
            if obj is None:
                continue

            # Skip submodules
            if inspect.ismodule(obj):
                continue

            # Check if it's a class-level attribute (like Color.red)
            # Be careful with isinstance checks as they can crash
            obj_type = type(obj).__name__
            if obj_type == class_name:
                class_attrs.append((name, class_name))
            elif callable(obj):
                methods.append((name, obj))
            else:
                properties.append((name, obj))
        except Exception as e:
            # If we can't inspect it, assume it's a property
            properties.append((name, None))

    # Generate class attributes (like named colors)
    if class_attrs:
        lines.append(f"{indent}    # Class attributes")
        for name, type_name in sorted(class_attrs, key=lambda x: x[0]):
            lines.append(f"{indent}    {name}: ClassVar[{type_name}]")
        lines.append("")

    # Generate properties
    if properties:
        lines.append(f"{indent}    # Properties")
        for name, obj in sorted(properties, key=lambda x: x[0]):
            type_hint = get_type_hint(obj, name)
            lines.append(f"{indent}    @property")
            lines.append(f"{indent}    def {name}(self) -> {type_hint}: ...")
        lines.append("")

    # Generate methods
    if methods:
        lines.append(f"{indent}    # Methods")
        for name, obj in sorted(methods, key=lambda x: x[0]):
            sig = get_signature_str(obj, class_name)
            # Check if it looks like a static/class method
            try:
                if isinstance(inspect.getattr_static(cls, name), staticmethod):
                    lines.append(f"{indent}    @staticmethod")
                    sig = sig.replace("(self, ", "(").replace("(self)", "()")
                elif isinstance(inspect.getattr_static(cls, name), classmethod):
                    lines.append(f"{indent}    @classmethod")
                    sig = sig.replace("(self", "(cls")
            except:
                pass
            lines.append(f"{indent}    def {name}{sig}: ...")

    if not (properties or methods or class_attrs):
        lines.append(f"{indent}    ...")

    return lines


def generate_enum_stub(cls: type, indent: str = "") -> List[str]:
    """Generate stub for an enum-like class."""
    lines = []
    class_name = cls.__name__

    lines.append(f"{indent}class {class_name}:")
    lines.append(f"{indent}    '''Enumeration of {class_name} values.'''")

    members = []
    try:
        members = [(name, getattr(cls, name)) for name in dir(cls)
                   if not name.startswith('_') and name.isupper()]
    except:
        pass

    for name, obj in sorted(members, key=lambda x: x[0]):
        lines.append(f"{indent}    {name}: ClassVar[{class_name}]")

    if not members:
        lines.append(f"{indent}    ...")

    return lines


def generate_module_stub(module: Any, module_name: str) -> str:
    """Generate complete stub for a module."""
    lines = [
        '"""',
        f'Type stubs for {module_name}',
        'Auto-generated by introspection.',
        '"""',
        'from typing import Any, List, Dict, Optional, ClassVar, overload, Tuple, Union',
        'import io',
        '',
    ]

    # Collect imports needed
    imports: Set[str] = set()

    # Get all module members
    classes = []
    functions = []
    constants = []
    submodules = []

    for name in safe_dir(module):
        try:
            obj = safe_getattr(module, name)
            if obj is None:
                continue
        except:
            continue

        try:
            if inspect.ismodule(obj):
                submodules.append(name)
            elif inspect.isclass(obj):
                classes.append((name, obj))
            elif callable(obj):
                functions.append((name, obj))
            else:
                constants.append((name, obj))
        except:
            pass

    # Add submodule imports
    if submodules:
        for sub in sorted(submodules):
            lines.append(f"from . import {sub}")
        lines.append("")

    # Generate constants
    if constants:
        lines.append("# Constants")
        for name, obj in sorted(constants, key=lambda x: x[0]):
            type_hint = get_type_hint(obj, name)
            lines.append(f"{name}: {type_hint}")
        lines.append("")

    # Generate functions
    if functions:
        lines.append("# Functions")
        for name, obj in sorted(functions, key=lambda x: x[0]):
            sig = get_signature_str(obj)
            doc = inspect.getdoc(obj)
            lines.append(f"def {name}{sig}:")
            if doc:
                lines.append(f"    '''{doc}'''")
            lines.append("    ...")
        lines.append("")

    # Generate classes
    if classes:
        lines.append("# Classes")
        for name, cls in sorted(classes, key=lambda x: x[0]):
            try:
                # Check if it's enum-like
                members = safe_dir(cls)
                upper_members = [m for m in members if m.isupper() or m.replace('_', '').isupper()]

                if len(upper_members) > len(members) * 0.5 and len(members) < 50:
                    lines.extend(generate_enum_stub(cls))
                else:
                    lines.extend(generate_class_stub(cls))
                lines.append("")
            except Exception as e:
                lines.append(f"# class {name}: Error generating stub: {e}")
                lines.append(f"class {name}: ...")
                lines.append("")

    return '\n'.join(lines)


def generate_pydrawing_stubs(output_dir: Path):
    """Generate all pydrawing stubs."""
    import aspose.pydrawing as pydrawing

    output_dir.mkdir(parents=True, exist_ok=True)

    # Main module
    print("Generating aspose.pydrawing stubs...")
    main_stub = generate_module_stub(pydrawing, "aspose.pydrawing")
    (output_dir / "__init__.pyi").write_text(main_stub)
    print(f"  Written: __init__.pyi ({len(main_stub.splitlines())} lines)")

    # Submodules
    submodules = ['drawing2d', 'imaging', 'printing', 'text', 'design']
    for sub_name in submodules:
        if hasattr(pydrawing, sub_name):
            sub_module = getattr(pydrawing, sub_name)
            sub_dir = output_dir / sub_name
            sub_dir.mkdir(exist_ok=True)

            print(f"Generating aspose.pydrawing.{sub_name} stubs...")
            sub_stub = generate_module_stub(sub_module, f"aspose.pydrawing.{sub_name}")
            (sub_dir / "__init__.pyi").write_text(sub_stub)
            print(f"  Written: {sub_name}/__init__.pyi ({len(sub_stub.splitlines())} lines)")


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "generated_stubs" / "aspose" / "pydrawing"
    generate_pydrawing_stubs(output_dir)
    print(f"\nStubs written to: {output_dir}")
