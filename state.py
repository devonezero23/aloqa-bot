from aiogram.dispatcher.filters.state import State, StatesGroup


class Register(StatesGroup):
    number = State()
    
class Connection(StatesGroup):
    answer_msg = State()
   