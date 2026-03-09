import time
from sqlalchemy import text
from db.session import engine


def check_database():

    try:
        start = time.perf_counter()

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        latency = (time.perf_counter() - start) * 1000

        return {"database": {"status": "ok", "latency_ms": round(latency, 2)}}

    except Exception as e:
        return {"database": {"status": "error", "details": str(e)}}
