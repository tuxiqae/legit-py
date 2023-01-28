from api.app import get_app, init_app
from utils import client, consts


def main():
    client.create_superuser()
    app = get_app()
    init_app(app=app, port=consts.APP_PORT, host=consts.APP_BIND_ADDR)


if __name__ == "__main__":
    main()
