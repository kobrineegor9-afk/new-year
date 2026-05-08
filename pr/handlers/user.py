from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.crude import add_participant, get_room, update_wish, get_target_info
from utils.game import start_game

router = Router()
@router.message(Command('join'))
async def join_game(message: Message):
    '''пресоедениться к игре : /join ID_игры'''
    args = message.text.split()
    if len(args)< 2:
        await message.answer('укажите ID игры')
        return
    try:
        room_id = int(args[1])
    except ValueError:
        await message.answer('неверный ID игры')

    room = get_room(room_id)
    if not room:
        await message.answer('игра не найдена')
        return
    if room['status'] != 'active':
        await message.answer('игра уже завершена')
        return
    success = add_participant(
        room_id,
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )
    if success:
        await message.answer(
            'вы в игре!'
            'напешите свое пожелание : /wish ваше текст'
            'пример: /wish люблю настолки и комиксы'
        )
    else:
        await message.answer('вы уже в этой игре')

@router.message(Command('wish'))
async def set_wish(message: Message):
    '''установить пожелание : /wish текст пожелания'''
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer('напишите пожелание: /wish люблю кофе и книги')
        return
    wish = args[1]

    from database.models import get_connection
    conn = get_connection()
    room = conn.execute('''
            SELECT r.id FROM rooms r 
            JOIN partipicants p ON r.id = p.room_id
            WHERE p.user_id = ? AND r.status = 'active'
            ORDER BY r.id DESC LIMIT 1
        ''',(message.from_user.id,)).fetchone()
    conn.close()
    if not room:
        await message.answer('вы не состоите в активной игре')
        return
    update_wish(message.from_user.id, room['id'], wish)
    await message.answer('пожелание сохранено!')

@router.message(Command('mytarget'))
async def my_target(message:Message):
    '''узнать своего подопечноо после жеребьевки'''
    from database.models import get_connection
    conn = get_connection()
    room = conn.execute("""
        SELECT r.id FROM rooms r 
        JOIN partipicants p ON r.id = p.room_id
        WHERE p.user_id =? AND r.status = 'finished'
        ORDER BY r.id DESC LIMIT 1
        """,(message.from_user.id,)).fetchone()
    conn.close()
    if not room:
        await message.answer('у вас нет завершенных игр')
        return
    target = get_target_info(message.from_user.id,room['id'])
    if not target:
        await message('информация о подопечном не найдена')
        return
    text = f"вы - тайный санта для: {target['first_name']}"
    if target['username']:
        text += f'(@{target["username"]})'
        if target['wish']:
            text +=f'пожелание :{target["wish"]}'
        else:
            text += 'участник не оставил пожелание'

        await message.answer(text)


