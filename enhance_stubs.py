#!/usr/bin/env python3
"""
Enhance pydrawing stubs with detailed member info for key classes.
Introspects one class at a time to handle crashes gracefully.
"""
import subprocess
import sys
from pathlib import Path

INTROSPECT_SCRIPT = '''
import sys
try:
    import aspose.pydrawing as pd
    cls = getattr(pd, "{class_name}")

    members = []
    for name in dir(cls):
        if name.startswith('_'):
            continue
        try:
            obj = getattr(cls, name)
            obj_type = type(obj).__name__
            is_callable = callable(obj)
            is_class_attr = obj_type == "{class_name}"
            members.append((name, "method" if is_callable else ("classvar" if is_class_attr else "property")))
        except:
            members.append((name, "property"))

    for name, kind in sorted(members):
        print(f"{{kind}}:{{name}}")
except Exception as e:
    print(f"ERROR:{{e}}", file=sys.stderr)
    sys.exit(1)
'''

def introspect_class(class_name: str) -> dict:
    """Introspect a single class in a subprocess."""
    script = INTROSPECT_SCRIPT.format(class_name=class_name)

    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=10,
        env={"DYLD_FALLBACK_LIBRARY_PATH": "/opt/homebrew/lib"}
    )

    if result.returncode != 0:
        return None

    members = {"methods": [], "properties": [], "classvars": []}
    for line in result.stdout.strip().split('\n'):
        if ':' in line:
            kind, name = line.split(':', 1)
            if kind == "method":
                members["methods"].append(name)
            elif kind == "classvar":
                members["classvars"].append(name)
            else:
                members["properties"].append(name)

    return members


def generate_detailed_stub(class_name: str, members: dict) -> str:
    """Generate detailed stub for a class."""
    lines = [
        f"class {class_name}:",
        f"    '''System.Drawing.{class_name} wrapper.'''",
    ]

    # Class variables (like Color.red, Color.blue)
    if members["classvars"]:
        lines.append("    ")
        lines.append("    # Named values")
        for name in sorted(members["classvars"]):
            lines.append(f"    {name}: ClassVar[{class_name}]")

    # Properties
    if members["properties"]:
        lines.append("    ")
        lines.append("    # Properties")
        for name in sorted(members["properties"]):
            lines.append(f"    @property")
            lines.append(f"    def {name}(self) -> Any: ...")

    # Methods
    if members["methods"]:
        lines.append("    ")
        lines.append("    # Methods")
        for name in sorted(members["methods"]):
            if name in ('from_argb', 'from_known_color', 'from_name'):
                lines.append(f"    @staticmethod")
                lines.append(f"    def {name}(*args) -> {class_name}: ...")
            else:
                lines.append(f"    def {name}(self, *args) -> Any: ...")

    if not any(members.values()):
        lines.append("    ...")

    return '\n'.join(lines)


def main():
    key_classes = [
        'Color', 'Point', 'PointF', 'Size', 'SizeF',
        'Rectangle', 'RectangleF', 'Font', 'Image', 'Bitmap',
        'Pen', 'Brush', 'SolidBrush', 'Graphics'
    ]

    output_dir = Path(__file__).parent / "generated_stubs" / "aspose" / "pydrawing"

    detailed_stubs = {}

    for class_name in key_classes:
        print(f"Introspecting {class_name}...", end=" ", flush=True)
        try:
            members = introspect_class(class_name)
            if members:
                detailed_stubs[class_name] = generate_detailed_stub(class_name, members)
                total = len(members["methods"]) + len(members["properties"]) + len(members["classvars"])
                print(f"OK ({total} members)")
            else:
                print("FAILED")
        except Exception as e:
            print(f"ERROR: {e}")

    # Update main stub file with detailed versions
    main_stub_path = output_dir / "__init__.pyi"
    current_stub = main_stub_path.read_text()

    for class_name, detailed in detailed_stubs.items():
        # Replace the simple stub with the detailed one
        simple_pattern = f"class {class_name}:\n    '''Wrapper for System.Drawing.{class_name}'''\n    def __init__(self, *args, **kwargs) -> None: ..."
        current_stub = current_stub.replace(simple_pattern, detailed)

    main_stub_path.write_text(current_stub)
    print(f"\nUpdated: {main_stub_path}")


if __name__ == "__main__":
    main()
