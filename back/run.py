from app.api import create_app
import os

env = os.getenv("ENV", "development")

app = create_app(env)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
