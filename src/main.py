from api.app import get_app, init_app
from utils import client, consts, logs


def main():
    app = get_app()
    try:
        auth_res = client.auth_admin()
        app.state.access_token = client.get_access_token(auth_res)
    except Exception:
        logs.logger.exception("Error occured. Terminating app!")
        raise SystemExit(1)
    init_app(app=app, port=consts.APP_PORT, host=consts.APP_BIND_ADDR)


if __name__ == "__main__":
    main()
