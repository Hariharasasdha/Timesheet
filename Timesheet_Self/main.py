from app import create_app, db_client
from config import Config

app = create_app(Config)


if __name__ == "__main__":
    app.run()

