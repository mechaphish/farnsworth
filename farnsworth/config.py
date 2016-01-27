from dotenv import load_dotenv
import os

def set_config_from_env(app, path):
    load_dotenv(path)
    for k in os.environ:
        app.config[k] = os.environ[k]
