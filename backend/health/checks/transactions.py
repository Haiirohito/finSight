from sqlalchemy import text
from db.session import engine


def check_transactions():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"transactions_service": "ok"}

    except Exception as e:
        return {"transactions_service": "error", "details": str(e)}
