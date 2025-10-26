Testing Guide

Prerequisites
- Python >= 3.11
- pip; C/C++ build toolchain for native extensions
- Dependencies: pytest, pytest-xdist, pytest-cov; numpy, scipy
- Optional: BLAS/LAPACK libraries for optimized linear algebra (e.g., OpenBLAS, MKL)

Setup
- pip install -e .
- pip install pytest pytest-xdist pytest-cov numpy scipy

Run tests
- pytest --pyargs sklearn -n auto
- Coverage: pytest --pyargs sklearn --cov=sklearn --cov-report=xml

Troubleshooting
- Extension builds may require BLAS/LAPACK; if builds fail or tests crash, try running serially to debug: `pytest --pyargs sklearn -n 0`.
- Ensure your Python environment uses compatible numpy/scipy versions for your Python release.
- If compilation errors occur, verify your C/C++ toolchain is correctly installed and available on PATH.
