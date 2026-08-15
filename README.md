# Multi-Agent Leave Management System

A small multi-agent workflow built with **LangGraph** + **SQLite** that automates an employee leave request — from checking balance, to human approval, to saving the record.

---

## How to Run

```bash
# 1. Install dependencies
uv sync

# 2. Run the demo (this also creates/seeds the database on first run)
uv run python demo.py
```

---

## Where the Data Lives

- Database: `leave_management.db` (SQLite file, created automatically)
- Schema + seed data: `init_db.sql` (creates `employees` and `leave_requests` tables, seeds one test employee `EMP001` with 15 days balance and 2 company holidays)
- Demo request (hardcoded for now, in `demo.py`): Employee `EMP001` requesting leave `2026-12-24` to `2026-12-28`

---

## Flow (What Happens When You Run It)

1. **Parallel Retrieval** — two agents run at the same time:
   - `employee_retrieval_agent` → fetches employee name + leave balance
   - `holiday_retrieval_agent` → fetches company holidays

2. **Computation** — `computation_agent` calculates working days (skips weekends + holidays), then checks against balance:
   - If balance is **not enough** → status = `REJECTED`, graph ends here (no human step, no DB write)
   - If balance is **enough** → status = `AWAITING_APPROVAL`, graph pauses

3. **Human-in-the-Loop** — graph pauses (`interrupt_before`, configured in `graph.py`) and waits for terminal input: approve (`y`) or reject (`n`)

4. **Persistence** — if approved, `persistence_agent` inserts the leave request and deducts the balance in SQLite (with commit)

5. **Verification** — demo prints the final DB rows so you can see the write actually happened

---

## Reset Database

in demo.py line 83 change reset=True/False to reset the Database entry

```
    init_db(reset=False)  # will update database on each approval

    init_db(reset=True)  # will reset database and entry will not be saved
```

---

## Project Structure

```
leave-system/
├── state.py           # shared state (TypedDict) passed between all nodes
├── db.py               # SQLite connection + init_db()
├── graph.py             # builds the LangGraph graph (nodes, edges, checkpointer)
├── nodes/
│   ├── retrieval_agents.py        # employee + holiday retrieval (parallel)
│   ├── computation_agent.py       # working-day calculation + balance check
│   ├── human_confirmation_node.py # HITL pass-through node (pause happens in graph.py)
│   └── persistence_agent.py       # DB write on approval
└── demo.py             # CLI runner — the file you actually execute
```
