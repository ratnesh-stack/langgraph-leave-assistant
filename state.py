from typing import TypedDict

class LeaveState(TypedDict):
    # Inputs
    employee_id: str
    start_date: str
    end_date: str
    
    # Retrieved Data
    employee_name: str
    leave_balance: int
    holidays: list[str]
    
    # Computation & Decision Results
    calculated_days: int
    user_approved: bool
    status: str
    message: str

