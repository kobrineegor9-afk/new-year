from typing import Optional,List,Dict, Any
from database.models import get_connection

def create_room(chat_id: int, name: str) -> int:
    conn= get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO rooms (chat_id, name) VALUES (?,?)',
        (chat_id, name)
    )
    conn.commit()
    room_id = cursor.lastrowid
    conn.close()
    return room_id

def get_room(room_id:int) ->Optional[Dict[str,Any]]:
    conn= get_connection()
    room = conn.execute(
        'SELECT * FROM rooms WHERE id = ?',
        (room_id,)
    ).fetchone()
    conn.close()
    return dict(room) if room else None

def finish_room(room_id: int):
    conn = get_connection()
    coon = conn.execute(
        "UPDATE rooms SET status = 'finished' WHERE id = ?",
        (room_id,)
    )
    conn.commit()
    conn.close()

def add_partipicant(room_id: int, user_id: int, username:Optional[str],first_name: str) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            'INSERT INTO partipicants (room_id , user_id, username,first_name)VALUES (?,?,?,?)',
            (room_id, user_id,username, first_name)
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def update_wish(user_id: int,room_id:int , wish:str):
    conn = get_connection()
    conn.execute(
        'UPDATE partipicants SET wish = ? WHERE user_id = ? AND room_id = ?',
        (wish, user_id, room_id)
    )
    conn.commit()
    conn.close()

def get_partipicants(room_id:int) -> List[Dict[str, Any]]:
    conn = get_connection()
    partipicants = conn.execute(
        'SELECT * FROM partipicants WHERE room_id =?',
        (room_id,)
    )
    conn.commit()
    conn.close()

def set_target(partipicant_id:int, target_id:int):
    conn = get_connection()
    conn.execute(
        'UPDATE partipicants SET target_id = ? where id =?',
        (target_id, partipicant_id)
    )
    conn.commit()
    conn.close()
def get_target_info(user_id: int, room_id:int ) -> Optional[Dict[str,Any]]:
    conn = get_connection()
    result = conn.execute('''
         SELECT t.first_name, t.username, t.wish
         FROM partipicants p 
         JOIN partipicants t ON p.target_id = t.id
         WHERE p.user_id = ? AND p.room_id = ?
         ''', (user_id, room_id)).fetchone()
    conn.close()
    return dict(result) if result else None

