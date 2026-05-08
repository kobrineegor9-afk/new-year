import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

DB_NAME = 'reminders.db'


def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER UNIQUE,
                       username TEXT,
                       created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   ''')

    # Таблица напоминаний
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS reminders
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       text TEXT,
                       reminder_datetime TIMESTAMP,
                       is_sent INTEGER DEFAULT 0,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (user_id) 
                       REFERENCES users (user_id)
                       )
                   ''')

    conn.commit()
    conn.close()


def register_user(user_id: int, username: str = None):
    """Регистрация нового пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   INSERT OR IGNORE INTO users (user_id, username)
        VALUES (?, ?) ''', (user_id, username))

    conn.commit()
    conn.close()


def add_reminder(user_id: int, text: str, reminder_datetime: str) -> int:
    """Добавить новое напоминание"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   INSERT INTO reminders (user_id, text, reminder_datetime)
                   VALUES (?, ?, ?)
                   ''', (user_id, text, reminder_datetime))

    reminder_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return reminder_id


def get_user_reminders(user_id: int, include_sent: bool = False) -> List[Tuple]:
    """Получить все напоминания пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if include_sent:
        cursor.execute('''
                       SELECT id, text, reminder_datetime, is_sent, created_at
                       FROM reminders
                       WHERE user_id = ?
                       ORDER BY reminder_datetime ASC
                       ''', (user_id,))
    else:
        cursor.execute('''
                       SELECT id, text, reminder_datetime, created_at
                       FROM reminders
                       WHERE user_id = ?
                         AND is_sent = 0
                       ORDER BY reminder_datetime ASC
                       ''', (user_id,))

    reminders = cursor.fetchall()
    conn.close()
    return reminders


def get_reminder_by_id(reminder_id: int) -> Optional[Tuple]:
    """Получить напоминание по ID"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT id, user_id, text, reminder_datetime, is_sent
                   FROM reminders
                   WHERE id = ?
                   ''', (reminder_id,))

    reminder = cursor.fetchone()
    conn.close()
    return reminder


def delete_reminder(reminder_id: int, user_id: int) -> bool:
    """Удалить напоминание"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   DELETE
                   FROM reminders
                   WHERE id = ?
                     AND user_id = ?
                   ''', (reminder_id, user_id))

    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def mark_reminder_as_sent(reminder_id: int):
    """Отметить напоминание как отправленное"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   UPDATE reminders
                   SET is_sent = 1
                   WHERE id = ?
                   ''', (reminder_id,))

    conn.commit()
    conn.close()


def get_pending_reminders() -> List[Tuple]:
    """Получить все неотправленные напоминания, время которых уже наступило"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT id, user_id, text, reminder_datetime
                   FROM reminders
                   WHERE is_sent = 0
                     AND reminder_datetime <= datetime('now', 'localtime')
                   ORDER BY reminder_datetime ASC
                   ''')

    reminders = cursor.fetchall()
    conn.close()
    return reminders


def delete_all_reminders(user_id: int) -> int:
    """Удалить все напоминания пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   DELETE
                   FROM reminders
                   WHERE user_id = ?
                     AND is_sent = 0
                   ''', (user_id,))

    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted