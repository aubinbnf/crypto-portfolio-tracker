from db import engine, Base
import models

Base.metadata.create_all(bind=engine)
print("SQLite DB initialized at ./portfolio.db")
