import sqlite3
from datetime import datetime
from typing import List, Tuple,Optional

DB_NAME ='reminders.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users
                    (
                        id INTEGER PRIMARY KEY AUTOINCRECMENT,
                        user_id INTEGER UNIQUE,
                        username TEXT,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        ''')

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
                        REFERNCES users (user_id)
                        )
                    ''')

    conn.commit()
    conn.close()
    def register_user(user_id:int, username:str = None):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
                        INSERT OR IGNORE INTO users (user_id, username)
                        VALUES(?,?)''',(user_id,username))

    conn.commit()
    conn.close()

    def add_reminder(user_id: int, text:str, reminder_datetime:str) -> int:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor


        cursor.execute('''
                        INSERT INTO reminders(user_id,text,reminder_datetime)
                        VALUES (?,?,?)
                        ''',(user_id,text,reminder_datetime))

        reminder_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return reminder_id


        def get_user_reminders(user_id: int, include_sent: bool = False) -> list[Tuple]:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if include_sent:
                cursor.execute('''
                            SELECT id, text, reminder_datetime,is_sent, creater_at
                            FROM remianders
                            WHERE user_id = ?
                            ORDER BY reminder_datetime ASC
                            ''', (user_id,))
            else:
                cursor.executee('''
                            SELECT id, text, reminder_datetime,is_sent, creater_at
                            FROM remianders
                            WHERE user_id = ?
                            AND is_sent = 0
                            ORDER BY reminder_datetime ASC
                            ''', (user_id,))

            reminders = cursor.fetchall()
            conn.close()
            return reminders

        def get_reminder_by_id(reminder_id: int) -> Optional[Tuple]:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute('''
                            SELECT id, text, reminder_datetime,is_sent
                            FROM reminders
                            WHERE id = ?
                            ''',(reminder_id,))

            reminder = cursor.fetchone()
            conn.close()
            return reminder