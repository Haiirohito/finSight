from sqlalchemy import text
from db.session import engine


def check_budgets():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"budgets_service": "ok"}
    except Exception as e:
        return {"budgets_service": "error", "details": str(e)}
