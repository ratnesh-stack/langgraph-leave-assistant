import sqlite3
from state import LeaveState
from db import DB_NAME


def persistence_agent(state: LeaveState):
    """Applies leave application and updates leave balance in SQLite."""
    if not state.get("user_approved", False):
        return {"status": "REJECTED", "message": "Leave request cancelled by user."}

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Record application
    cursor.execute(
        "INSERT INTO leave_requests (employee_id, start_date, end_date, total_days, status) VALUES (?, ?, ?, ?, ?)",
        (state["employee_id"], state["start_date"], state["end_date"], state["calculated_days"], "APPROVED")
    )
    
    # Deduct balance
    new_balance = state["leave_balance"] - state["calculated_days"]
    cursor.execute(
        "UPDATE employees SET leave_balance = ? WHERE employee_id = ?",
        (new_balance, state["employee_id"])
    )
    
    conn.commit()
    conn.close()

    return {
        "status": "SUCCESS",
        "message": f"Leave approved. Remaining balance: {new_balance}"
    }