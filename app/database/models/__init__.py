import os
import importlib
from app import bcrypt, db, Enum

models = os.path.dirname(__file__)

for model in os.listdir(models):
    if model.endswith(".py") and model != "__init__.py":
        module_name = model[:-3]
        importlib.import_module("app.database.models."+module_name)