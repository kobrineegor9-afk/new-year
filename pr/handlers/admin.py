from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import Command
from database.crude import create_room, get_room, get_partipicants, finish_room
from utils.game import start_game

router = Router()
@router.message(Command('new game'))
async def new_game(message:Message):
    '''Создать новую игру: /new_game Навзвание'''
    args = message.text.split(maxsplit = 1)
    if len(args)<2 :
        await message.answer('укажите название : /new_game название игры')
        return

    name = args[1]
    room_id = create_room(message.chat.id, name)
    await message.answer(
        f'игра "{name}" создана! '
        f'ID игры: <code>{room_id}</code>'
        f' скажите участникам ввести: /join {room_id}'
    )

@router.message(Command('start'))
async def start_command(message: Message):
    '''провести жеребьевку: /start ID_игры'''
    args = message.text.split()
    if len(args)<2 :
        await message.answer('укажите ID игры : /start_game 1 ')
        return

    try:
        room_id = int(args[1])
    except ValueError:
        await message.answer('неверный ID игры')
        return
    room = get_room(room_id)
    if not room:
        await message.answer('игра не найдена')
        return
    if room['status'] != 'active':
        await message.answer('игра уже завершена')
        return
    partipicants= get_partipicants(room_id)
    if len(partipicants) <3:
        await message.answer('нужно минимум 3 участника ')
        return
    start_game(partipicants)
    finish_room(room_id)

    await message.answer(
        'жеребьевка проведена!'
        'участники могут узнать своего подопечного командой /mytarget'
    )