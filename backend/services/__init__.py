"""
Service layer (business use-cases).

Rules of thumb:
- Services coordinate domain objects + storage.
- Services enforce business rules and raise domain exceptions.
- Flask routes should be thin: parse request -> call service -> return response.
"""

