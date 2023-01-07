import os

from alisabot import create_app, db
from alisabot.models.user import User


"""Интерфейс командной строки Flask/Точка входа в приложение."""
"""Точка входа в приложение/интерфейс командной строки Flask."""

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {"db": db, "User": User}
