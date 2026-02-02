"""
Storage layer (file I/O).

Rules of thumb:
- Repositories know *how* to store/load data.
- They should not contain business rules like "cannot withdraw below zero".
"""

