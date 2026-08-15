from datetime import datetime, timedelta
from state import LeaveState


def computation_agent(state: LeaveState):
    """Calculates net leave days excluding weekends and company holidays."""
    start = datetime.strptime(state["start_date"], "%Y-%m-%d")
    end = datetime.strptime(state["end_date"], "%Y-%m-%d")
    holidays = set(state.get("holidays", []))

    current = start
    work_days = 0
    while current <= end:
        # Weekday check (0-4 are Mon-Fri) and not in public holidays list
        if current.weekday() < 5 and current.strftime("%Y-%m-%d") not in holidays:
            work_days += 1
        current += timedelta(days=1)

    if work_days > state["leave_balance"]:
        return {
            "calculated_days": work_days,
            "status": "REJECTED",
            "message": f"Insufficient balance. Requested {work_days} days, balance is {state['leave_balance']}."
        }

    return {
        "calculated_days": work_days,
        "status": "AWAITING_APPROVAL",
        "message": f"Calculated {work_days} working days. Awaiting human confirmation."
    }
