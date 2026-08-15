import datetime
import sqlite3
from state import LeaveState
from db import DB_NAME

# 1. RETRIEVAL AGENT A: Employee Info
def employee_retrieval_agent(state: LeaveState):
    """Fetches employee name and current leave balance."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, leave_balance FROM employees WHERE employee_id = ?", (state["employee_id"],))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"status": "FAILED", "message": f"Employee {state['employee_id']} not found."}
    
    return {"employee_name": row[0], "leave_balance": row[1]}

# 2. RETRIEVAL AGENT B: Holiday Info
def holiday_retrieval_agent(state: LeaveState):
    """Fetches company holidays falling between start and end date."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT holiday_date FROM holidays WHERE holiday_date BETWEEN ? AND ?", 
        (state["start_date"], state["end_date"])
    )
    rows = cursor.fetchall()
    conn.close()

    return {"holidays": [r[0] for r in rows]}
