import sqlite3
from datetime import date, timedelta

conn = sqlite3.connect("streaks.db", check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS task_log (
            task_id INTEGER,
            log_date TEXT,
            completed INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS streaks (
            task_id INTEGER UNIQUE,
            current_streak INTEGER,
            last_completed TEXT,
            max_streak INTEGER
        )
    """)
    conn.commit()


def add_task(name):
    c.execute("INSERT OR IGNORE INTO tasks (name) VALUES (?)", (name,))
    conn.commit()


def get_tasks():
    return c.execute("SELECT * FROM tasks").fetchall()


def complete_task(task_id):
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    c.execute(
        "INSERT INTO task_log VALUES (?, ?, 1)",
        (task_id, today)
    )

    streak = c.execute(
        "SELECT current_streak, last_completed, max_streak FROM streaks WHERE task_id=?",
        (task_id,)
    ).fetchone()

    if streak:
        current, last_date, max_streak = streak
        if last_date == yesterday:
            current += 1
        else:
            current = 1
        max_streak = max(max_streak, current)

        c.execute("""
            UPDATE streaks
            SET current_streak=?, last_completed=?, max_streak=?
            WHERE task_id=?
        """, (current, today, max_streak, task_id))
    else:
        c.execute("""
            INSERT INTO streaks VALUES (?, 1, ?, 1)
        """, (task_id, today))

    conn.commit()


def get_streak(task_id):
    result = c.execute(
        "SELECT current_streak, max_streak FROM streaks WHERE task_id=?",
        (task_id,)
    ).fetchone()
    return result if result else (0, 0)


def get_history(task_id):
    return c.execute(
        "SELECT log_date FROM task_log WHERE task_id=? ORDER BY log_date DESC",
        (task_id,)
    ).fetchall()
