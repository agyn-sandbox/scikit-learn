Testing Guide

Overview
- This project uses meson-python as the build backend, which drives Meson and Ninja to
  build native extensions generated with Cython. Tests require a local build of the
  extensions or a prebuilt wheel when available.

Prerequisites
- Python >= 3.10 (see pyproject.toml)
- pip; C/C++ toolchain for native extensions
  - Linux: gcc/g++ and build-essential (or equivalent)
  - macOS: Xcode Command Line Tools (clang), `xcode-select --install`
  - Windows: Microsoft C++ Build Tools (MSVC)
- Build toolchain (meson/ninja/cython)
  - meson-python and Cython are declared in pyproject; pip will install them when
    building from source. Ninja must be available on PATH.
  - Install Ninja as needed:
    - Linux: `sudo apt-get install ninja-build` (Debian/Ubuntu) or `dnf install ninja`
    - macOS: `brew install ninja` or `pip install ninja`
    - Windows: `pip install ninja` (adds `ninja.exe`)
- Test dependencies
  - `pytest`, `pytest-xdist`, `pytest-cov` (and other optional deps are available via
    extras)
- Optional: BLAS/LAPACK libraries for optimized linear algebra
  - Typical providers: OpenBLAS, MKL, Apple Accelerate (macOS)

Setup (source build for testing)
- Install with tests extras to get dependencies:
  - `pip install -e .[tests]`
    - This performs an editable build via meson-python and compiles Cython extensions.
- Verify toolchain availability (optional diagnostics):
  - `meson --version` and `ninja --version`
  - `python -c "import Cython; print(Cython.__version__)"`

Run tests
- Parallel: `pytest --pyargs sklearn -n auto`
- Serial (useful for debugging): `pytest --pyargs sklearn -n 0`
- Coverage: `pytest --pyargs sklearn --cov=sklearn --cov-report=xml`

Wheel fallback (skip local builds)
- If local compilation fails or a native toolchain is unavailable, you can exercise
  tests against prebuilt wheels:
  - Ensure binary wheels are used for core numeric deps:
    - `pip install --upgrade --only-binary=:all: numpy scipy`
  - Install scikit-learn as a wheel when available for your platform:
    - `pip install --upgrade --only-binary=:all: scikit-learn`
  - Install test extras from the published wheel (avoids local rebuild):
    - `pip install --upgrade 'scikit-learn[tests]'`
  - Note: Wheels may not be available for all Python versions/architectures. If pip
    falls back to source builds, re-check your toolchain or pin to a supported
    Python/OS.

BLAS/LAPACK guidance
- scikit-learn relies on NumPy/SciPy which link to BLAS/LAPACK implementations.
  Performance and some parallel behaviors depend on the provider:
  - Linux: wheels typically use OpenBLAS; you can install system OpenBLAS via
    `sudo apt-get install libopenblas-dev` and ensure NumPy/SciPy link against it.
  - macOS: Apple Accelerate is available; OpenBLAS via Homebrew (`brew install
    openblas`) can be used when building from source.
  - Windows: pip wheels for NumPy/SciPy ship with optimized libraries (often MKL).
- To reduce nondeterminism and avoid thread contention in tests, consider limiting
  threads:
  - `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` (POSIX shells)
  - `set OMP_NUM_THREADS=1` etc. on Windows CMD; `$env:OMP_NUM_THREADS=1` in PowerShell
- You can introspect BLAS/LAPACK linkage at runtime:
  - `python -c "import threadpoolctl; print(threadpoolctl.threadpool_info())"`

Troubleshooting
- Build toolchain
  - If Meson reports missing Ninja, install it and ensure it is on PATH.
  - If Cython compilation fails, ensure `Cython>=3.1.2` is installed.
- Compiler
  - Verify your C/C++ compiler is installed and available on PATH.
  - On Windows, ensure MSVC Build Tools match your Python ABI (same architecture).
- BLAS/LAPACK
  - Some tests exercise linear algebra heavily; mismatched or buggy BLAS providers can
    cause failures. Try limiting threads as above or switching providers.
- Environment
  - Ensure NumPy/SciPy versions are compatible with your Python release.
  - If compilation errors occur, run serial tests to isolate issues:
    `pytest --pyargs sklearn -n 0`.
