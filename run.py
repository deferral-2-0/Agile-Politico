from app import app

from config import app_config

config_name = "development"
app = app(config_name)


@app.route('/')
def hello_root():
    """
        Return a simple hello message on the root of the app.
    """
    return "Welcome to politico access Version1 via /api/v1 and " \
        "Version2 via /api/v2 built by @Tevinthuku, credits to Andela"


if __name__ == '__main__':
    """
        the app runs here
    """
    app.run()
