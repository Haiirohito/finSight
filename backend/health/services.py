from .checks.database import check_database
from .checks.system import check_system
from .checks.transactions import check_transactions
from .checks.budgets import check_budgets


def run_health_checks():

    results = {}

    results.update(check_database())
    results.update(check_system())
    results.update(check_transactions())
    results.update(check_budgets())

    overall_status = "ok"

    for service in results.values():
        if isinstance(service, dict) and service.get("status") == "error":
            overall_status = "error"

    return {"status": overall_status, "services": results}
