from api.app import get_app, init_app
from utils import client, logs
from utils.settings import Settings


def main():
    settings = Settings()
    app = get_app(settings)
    try:
        auth_res = client.auth_user(settings)
        app.state.access_token = client.get_access_token(auth_res)
    except Exception:
        logs.logger.exception("Error occured. Terminating app!")
        raise SystemExit(1)
    init_app(app=app)


if __name__ == "__main__":
    main()
