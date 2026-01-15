#!/usr/bin/env python3
"""
Install generated pydrawing stubs into a Python environment.

This script copies the generated .pyi stubs to complete the empty stubs
that ship with aspose-slides, making full type information available
to IDEs and coding agents.

Usage:
    # Install to current environment
    python install_stubs.py

    # Install to specific venv
    python install_stubs.py /path/to/venv

    # Install to specific site-packages
    python install_stubs.py --site-packages /path/to/site-packages

    # Dry run (show what would be copied)
    python install_stubs.py --dry-run
"""
import argparse
import shutil
import sys
from pathlib import Path


def find_site_packages(venv_path: Path = None) -> Path:
    """Find the site-packages directory."""
    if venv_path:
        # Look for site-packages in the venv
        candidates = list(venv_path.glob("lib/python*/site-packages"))
        if not candidates:
            candidates = list(venv_path.glob("Lib/site-packages"))  # Windows
        if candidates:
            return candidates[0]
        raise FileNotFoundError(f"Could not find site-packages in {venv_path}")
    else:
        # Use current environment
        import site
        paths = site.getsitepackages()
        for p in paths:
            if Path(p).exists():
                return Path(p)
        raise FileNotFoundError("Could not find site-packages in current environment")


def find_aspose_pydrawing(site_packages: Path) -> Path:
    """Find the aspose.pydrawing package directory."""
    pydrawing_path = site_packages / "aspose" / "pydrawing"
    if not pydrawing_path.exists():
        raise FileNotFoundError(
            f"aspose.pydrawing not found at {pydrawing_path}\n"
            "Make sure aspose-slides is installed: pip install aspose-slides"
        )
    return pydrawing_path


def get_stub_source() -> Path:
    """Get the path to our generated stubs."""
    script_dir = Path(__file__).parent
    stub_dir = script_dir / "generated_stubs" / "aspose" / "pydrawing"
    if not stub_dir.exists():
        raise FileNotFoundError(
            f"Generated stubs not found at {stub_dir}\n"
            "Run the stub generators first:\n"
            "  python generate_pydrawing_stubs_v2.py\n"
            "  python enhance_stubs.py\n"
            "  python rectangle_stubs.py"
        )
    return stub_dir


def backup_existing(target_path: Path) -> Path:
    """Create a backup of existing stub file."""
    backup_path = target_path.with_suffix(".pyi.bak")
    if target_path.exists() and not backup_path.exists():
        shutil.copy2(target_path, backup_path)
        return backup_path
    return None


def install_stubs(
    site_packages: Path,
    dry_run: bool = False,
    force: bool = False
) -> dict:
    """
    Install generated stubs to the target site-packages.

    Returns a dict with installation results.
    """
    results = {
        "installed": [],
        "skipped": [],
        "backed_up": [],
        "errors": []
    }

    stub_source = get_stub_source()
    target_base = find_aspose_pydrawing(site_packages)

    # Collect all .pyi files to install
    stub_files = list(stub_source.rglob("*.pyi"))

    print(f"Source: {stub_source}")
    print(f"Target: {target_base}")
    print(f"Files to install: {len(stub_files)}")
    print()

    for stub_file in stub_files:
        # Calculate relative path and target
        rel_path = stub_file.relative_to(stub_source)
        target_file = target_base / rel_path

        # Check if target exists and compare
        if target_file.exists():
            source_lines = len(stub_file.read_text().splitlines())
            target_lines = len(target_file.read_text().splitlines())

            if target_lines >= source_lines and not force:
                print(f"  SKIP: {rel_path} (existing has {target_lines} lines, ours has {source_lines})")
                results["skipped"].append(str(rel_path))
                continue

            # Backup existing
            if not dry_run:
                backup = backup_existing(target_file)
                if backup:
                    results["backed_up"].append(str(backup))

        # Ensure target directory exists
        if not dry_run:
            target_file.parent.mkdir(parents=True, exist_ok=True)

        # Copy the stub
        action = "WOULD INSTALL" if dry_run else "INSTALL"
        source_lines = len(stub_file.read_text().splitlines())
        print(f"  {action}: {rel_path} ({source_lines} lines)")

        if not dry_run:
            try:
                shutil.copy2(stub_file, target_file)
                results["installed"].append(str(rel_path))
            except Exception as e:
                print(f"    ERROR: {e}")
                results["errors"].append({"file": str(rel_path), "error": str(e)})

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Install generated pydrawing stubs into a Python environment."
    )
    parser.add_argument(
        "venv_path",
        nargs="?",
        help="Path to virtual environment (default: current environment)"
    )
    parser.add_argument(
        "--site-packages",
        help="Direct path to site-packages directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without making changes"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite even if existing stubs are larger"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Aspose.pydrawing Stub Installer")
    print("=" * 60)
    print()

    try:
        # Determine site-packages location
        if args.site_packages:
            site_packages = Path(args.site_packages)
        elif args.venv_path:
            site_packages = find_site_packages(Path(args.venv_path))
        else:
            site_packages = find_site_packages()

        print(f"Site-packages: {site_packages}")
        print()

        # Install stubs
        results = install_stubs(
            site_packages,
            dry_run=args.dry_run,
            force=args.force
        )

        # Summary
        print()
        print("=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"  Installed: {len(results['installed'])}")
        print(f"  Skipped:   {len(results['skipped'])}")
        print(f"  Backed up: {len(results['backed_up'])}")
        print(f"  Errors:    {len(results['errors'])}")

        if args.dry_run:
            print()
            print("(Dry run - no changes made)")

        if results["errors"]:
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
