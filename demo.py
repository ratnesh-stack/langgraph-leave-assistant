import sqlite3
from graph import app
from db import init_db, DB_NAME


def print_header(title: str):
    """Small helper so every stage banner looks identical — purely cosmetic."""
    print("=" * 50)
    print(title)
    print("=" * 50)


def run_pipeline(thread_config: dict, initial_input: dict):
    """
    Runs Stage 1 (parallel retrieval + computation) and returns the
    state snapshot right after the graph either hits the HIL interrupt
    or auto-rejects. Kept separate from approval/persistence logic so
    the two concerns (graph execution vs. human interaction) don't mix.
    """
    print_header("STAGE 1: Executing Parallel Fetch & Computation")
    for event in app.stream(initial_input, thread_config):
        for node_name, output in event.items():
            print(f"-> Node Finished: {node_name}")
            print(f"   Output Data:   {output}\n")

    return app.get_state(thread_config)


def handle_approval_and_persist(thread_config: dict, state_snapshot):
    """
    Handles everything after the pipeline pauses: shows the human the
    computed request, collects yes/no, resumes the graph, then verifies
    the DB write. Separated from run_pipeline() because this is UI/human
    interaction, not graph logic — different thing to reason about.
    """
    print_header("STAGE 2: Human-in-the-Loop Interruption Paused")
    print(f"Employee Name:    {state_snapshot.values.get('employee_name')}")
    print(f"Leave Balance:    {state_snapshot.values.get('leave_balance')} days")
    print(f"Holidays Found:   {state_snapshot.values.get('holidays')}")
    print(f"Calculated Days:  {state_snapshot.values.get('calculated_days')} working days")
    print(f"Current Message:  {state_snapshot.values.get('message')}")

    while True:
        user_choice = input("\nDo you approve submitting this leave application? (yes/no): ").strip().lower()
        if user_choice in ["yes", "y"]:
            is_approved = True
            break
        elif user_choice in ["no", "n"]:
            is_approved = False
            break
        print("Invalid input! Please enter 'yes' (y) or 'no' (n).")

    # Inject human decision back into the paused graph state
    app.update_state(thread_config, {"user_approved": is_approved})

    print_header("STAGE 3: Resuming Pipeline & Data Persistence")
    for event in app.stream(None, thread_config):
        for node_name, output in event.items():
            print(f"-> Node Finished: {node_name}")
            print(f"   Output Data:   {output}\n")

    verify_persistence()


def verify_persistence():
    """Reads straight from SQLite to prove the graph's write actually landed."""
    print_header("STAGE 4: Verifying SQLite Persistence")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Leave Requests Table:")
    requests = cursor.execute("SELECT * FROM leave_requests").fetchall()
    print(f"  {requests}")

    print("\nUpdated Employee Table:")
    emp_query = "SELECT employee_id, name, leave_balance FROM employees WHERE employee_id='EMP001'"
    emp = cursor.execute(emp_query).fetchall()
    print(f"  {emp}")

    conn.close()

def run_interactive_demo():
    init_db(reset=True)  # Reset DB for a clean demo run
    thread_config = {"configurable": {"thread_id": "interview_demo_session"}}
    initial_input = {
        "employee_id": "EMP001",
        "start_date": "2026-12-24",
        "end_date": "2026-12-28",
    }

    state_snapshot = run_pipeline(thread_config, initial_input)

    if state_snapshot.values.get("status") == "REJECTED":
        print_header("REQUEST REJECTED")
        print(state_snapshot.values.get("message"))
        return

    handle_approval_and_persist(thread_config, state_snapshot)


if __name__ == "__main__":
    run_interactive_demo()