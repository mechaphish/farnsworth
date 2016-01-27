from dotenv import load_dotenv
import os

def set_config_from_env(app, path):
    app.config.setdefault('LISTEN', '0.0.0.0')
    if os.path.isfile(path):
        load_dotenv(path)
        for k in os.environ:
            app.config[k] = os.environ[k]
