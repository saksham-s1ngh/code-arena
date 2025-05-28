from backend.db import Base, engine
from backend.models import User

Base.metadata.create_all(bind=engine)