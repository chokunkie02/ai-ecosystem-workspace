def get_db():
    db = "Database Connection Dependency Injection Mock"
    try:
        yield db
    finally:
        pass
