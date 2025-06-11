import os
from app import create_app
env = os.getenv("ENV", "development")

app = create_app(env)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
