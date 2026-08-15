-- Employees Table
CREATE TABLE IF NOT EXISTS employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    leave_balance INTEGER NOT NULL
);

-- Company Holidays Table
CREATE TABLE IF NOT EXISTS holidays (
    holiday_date TEXT PRIMARY KEY,
    description TEXT NOT NULL
);

-- Leave Applications Table
CREATE TABLE IF NOT EXISTS leave_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    total_days INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('PENDING', 'APPROVED', 'REJECTED')),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Seed Data: Employees
INSERT OR IGNORE INTO employees (employee_id, name, department, leave_balance) VALUES
('EMP001', 'Alice Smith', 'Engineering', 10),
('EMP002', 'Bob Jones', 'Marketing', 3);

-- Seed Data: Public Holidays
INSERT OR IGNORE INTO holidays (holiday_date, description) VALUES
('2026-12-25', 'Christmas Day'),
('2026-12-26', 'Boxing Day'),
('2026-01-01', 'New Year Day');