#!/usr/bin/env python
"""
Environment verification script for devcontainer setup.

Run after entering the devcontainer:
    uv run python scripts/check_env.py

Or if venv is activated:
    python scripts/check_env.py
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def check_python():
    """Check Python version and virtual environment."""
    print("🐍 PYTHON")
    print(f"   Version:    {sys.version.split()[0]}")
    print(f"   Executable: {sys.executable}")

    if ".venv" in sys.executable:
        print("   ✅ Running in .venv (uv environment)")
        return True
    else:
        print("   ⚠️  Not running in .venv - run 'uv sync' first")
        return False


def check_gpu():
    """Check CUDA availability and GPU devices."""
    print("\n🎮 GPU / CUDA")

    try:
        import torch
    except ImportError:
        print("   ❌ PyTorch not installed")
        return False

    if not torch.cuda.is_available():
        print("   ❌ CUDA not available")
        print("   → Check: nvidia-smi in terminal")
        print("   → Check: GPU passthrough in devcontainer.json")
        return False

    print(f"   ✅ CUDA version: {torch.version.cuda}")
    print(f"   ✅ cuDNN version: {torch.backends.cudnn.version()}")
    print(f"   ✅ GPU count: {torch.cuda.device_count()}")

    for i in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(i)
        mem_gb = props.total_memory / (1024**3)
        print(f"      GPU {i}: {props.name} ({mem_gb:.1f} GB)")

    # Quick compute test
    try:
        x = torch.randn(1000, 1000, device="cuda")
        _ = torch.matmul(x, x)
        print("   ✅ GPU compute test passed")
        return True
    except Exception as e:
        print(f"   ❌ GPU compute test failed: {e}")
        return False


def check_gdal():
    """Check GDAL and geospatial libraries."""
    print("\n🌍 GEOSPATIAL (GDAL)")

    # Check system GDAL first
    try:
        result = subprocess.run(
            ["gdal-config", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        system_gdal_version = result.stdout.strip()
        print(f"   ✅ System GDAL: {system_gdal_version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   ❌ System GDAL not found (check Dockerfile)")

    # Check Python GDAL bindings
    try:
        from osgeo import gdal
        print(f"   ✅ Python GDAL: {gdal.__version__}")
        gdal_ok = True
    except ImportError:
        print("   ⚠️  Python GDAL bindings not installed")
        gdal_ok = False

    # Optional Python geospatial packages
    geo_packages = ["rasterio", "geopandas", "shapely"]
    installed = []
    missing = []
    for pkg in geo_packages:
        try:
            m = __import__(pkg)
            installed.append(f"{pkg} {m.__version__}")
        except ImportError:
            missing.append(pkg)

    if installed:
        print(f"   ✅ Geospatial: {', '.join(installed)}")
    if missing:
        print(f"   ⚠️  Missing: {', '.join(missing)} (uv sync --extra dev --extra geo)")

    return gdal_ok


def check_packages():
    """Check core ML and data science packages."""
    print("\n📦 CORE PACKAGES")

    packages = [
        "torch",
        "torchvision",
        "numpy",
        "scipy",
        "pandas",
        "polars",
        "matplotlib",
        "seaborn",
        "tqdm",
        "jupyter",
    ]

    all_ok = True
    for pkg in packages:
        try:
            m = __import__(pkg)
            version = getattr(m, "__version__", "installed")
            print(f"   ✅ {pkg}: {version}")
        except ImportError:
            print(f"   ❌ {pkg}: NOT INSTALLED")
            all_ok = False

    return all_ok


def check_dev_tools():
    """Check development tools."""
    print("\n🔧 DEV TOOLS")

    tools = [
        ("pytest", "pytest"),
        ("ruff", "ruff"),
        ("black", "black"),
    ]

    all_ok = True
    for pkg, name in tools:
        try:
            m = __import__(pkg)
            version = getattr(m, "__version__", getattr(m, "VERSION", "installed"))
            print(f"   ✅ {name}: {version}")
        except ImportError:
            print(f"   ⚠️  {name} not installed (install with: uv sync --extra dev)")
            # Dev tools are optional, don't fail
    return all_ok


def check_data_mounts():
    """Check for common data mount points."""
    print("\n💾 DATA MOUNTS")

    # Common mount points - customize for your lab
    mount_points = [
        Path("/run/media"),
        Path("/run/data_raid5"),
    ]

    found_any = False
    for mount in mount_points:
        if mount.exists():
            try:
                n_items = len(list(mount.iterdir()))
                print(f"   ✅ {mount} ({n_items} items)")
                found_any = True
            except PermissionError:
                print(f"   ⚠️  {mount} exists but not readable")

    if not found_any:
        print("   ℹ️  No data mounts found (may be expected)")
        print("      Configure in .devcontainer/devcontainer.json")

    return True  # Not a failure condition


def main():
    """Run all environment checks."""
    print("\n" + "=" * 60)
    print(f"ENVIRONMENT CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = {
        "Python": check_python(),
        "GPU": check_gpu(),
        "GDAL": check_gdal(),
        "Packages": check_packages(),
        "Dev Tools": check_dev_tools(),
        "Data Mounts": check_data_mounts(),
    }

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    critical_checks = ["Python", "GPU", "Packages"]
    critical_ok = all(results[k] for k in critical_checks)

    for name, passed in results.items():
        status = "✅" if passed else "❌"
        critical = "(critical)" if name in critical_checks else ""
        print(f"   {status} {name} {critical}")

    print()
    if critical_ok:
        print("✅ ALL CRITICAL CHECKS PASSED - Environment ready!")
        print()
        print("Next steps:")
        print("  1. Start exploring in notebooks/")
        print("  2. Put reusable code in lib/")
        print("  3. Entry point scripts go in scripts/")
        print()
        print("💡 Tip: Open default.code-workspace to see data mounts in explorer")
    else:
        print("❌ SOME CRITICAL CHECKS FAILED")
        print()
        print("Common fixes:")
        print("  - Run 'uv sync' to install dependencies")
        print("  - Check GPU passthrough in devcontainer.json")
        print("  - Run 'nvidia-smi' to verify GPU access")

    print("=" * 60 + "\n")

    return 0 if critical_ok else 1


if __name__ == "__main__":
    sys.exit(main())
