import os
import importlib

models = os.path.dirname(__file__)

for model in os.listdir(models):
    if model.endswith(".py") and model != "__init__.py":
        module_name = model[:-3]
        importlib.import_module("app.models."+module_name)