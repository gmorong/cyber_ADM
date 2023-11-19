from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram import*
import logging
import sqlite3

#id администратора (получить можно тут @getmyid_bot)
ADMIN =1316382049
##1316382049
#627268282

#Некоторые переменные
kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(types.InlineKeyboardButton(text="Рассылка"))
kb.add(types.InlineKeyboardButton(text="/НовыеМежДисКоманды"))

#Инициализация проекта
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token="6927325839:AAHTK2fDoWdJ0u6vBT0y-PeVg0MK76YIuKY") #Тут надо указать API бота, для этого переходим в @BotFather регистрируем нового бота и получаем API
dp = Dispatcher(bot, storage=storage)

#Создание базы данных
conn = sqlite3.connect('db5.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, block INTEGER);""")
conn.commit()

#Объявление States
class dialog(StatesGroup):
    spam = State()



class meinfo(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    
#Команда /start

@dp.message_handler(commands=['start'])
async def start(message: Message):
  cur = conn.cursor()
  cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
  result = cur.fetchone()
  if message.from_user.id == ADMIN:
    await message.answer('Добро пожаловать в Админ-Панель!', reply_markup=kb)
  else:
      if result is None:
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
        entry = cur.fetchone()
        if entry is None:
          cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
          conn.commit()
          await message.answer('Привет, я ПИШ-bot!')

#Команды
@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):
  await dialog.spam.set()
  await message.answer('Напиши текст рассылки.\n\nПример:\nВниамние! Новое мероприятие!\nКраткое содержание мироприятия и информация о нём\nРегиятриция: ссылка на гугл форму\n\nДля отмены напиши "Назад"')

@dp.message_handler(state=dialog.spam)
async def start_spam(message: Message, state: FSMContext):
  if message.text == 'Назад':
    await message.answer('Главное меню', reply_markup=kb)
    await state.finish()
  else:
    cur = conn.cursor()
    cur.execute(f'''SELECT user_id FROM users''')
    spam_base = cur.fetchall()
    for z in range(len(spam_base)):
          await bot.send_message(spam_base[z][0], message.text)
          await state.finish()
    await message.answer('Рассылка завершена', reply_markup=kb)

@dp.message_handler(commands = ["НовыеМежДисКоманды"], state=None)      
async def enter_meinfo(message: types.Message):
    if message.chat.id == ADMIN:               
        await message.answer("Введите список всех Команд и ссылки на их беседы :3\nПример:\n\nКоманда №1: разработка программ\nКрасткое описание: команда по разработке команд\nСсылка: https://t.me/+XNsZnp9SPw1kYTli\n\nКоманда №2: разработка программ\nКрасткое описание: команда по разработке команд\nСсылка: https://t.me/+LAy6QVitMntkNjJi")        

        await meinfo.Q3.set()                                  

@dp.message_handler(state=meinfo.Q3)                             
async def answer_q122(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)                     

    await message.answer("Всё сохранено :3")

    data = await state.get_data()               
    answer3 = data.get("answer3")         
    if message.chat.id ==ADMIN:
        joinedFile = open("comands.txt","w", encoding="utf-8")       
        joinedFile.write(str(answer3))
        await message.answer(f'{answer3}')

    await state.finish()

########################

@dp.message_handler(commands="vopros", commands_prefix="/")
async def cmd_dezign(message: types.Message):
    await message.delete()
    await message.answer(text = "Вы можете задать вопросы:\n1. По тел.: +7 (831) 436 63 07\n2. По эл. почте: nntu@nntu.ru\n3. В группе ВК: https://vk.com/nntualekseeva\nИли поискать на сайте: www.nntu.ru")

@dp.message_handler(commands="napravlenie", commands_prefix="/")
async def cmd_OsDop(message: types.Message):
    await message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Осн.Программа", callback_data="OsPr"))
    keyboard.add(types.InlineKeyboardButton(text="Доп.Программа", callback_data="DopPr"))
    await message.answer("Выберите программу обучения: ", reply_markup=keyboard)

@dp.message_handler(commands="profori", commands_prefix="/")
async def cmd_OsProfOr(message: types.Message):
    await message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Осн. Программа", callback_data="OsnProf"))
    keyboard.add(types.InlineKeyboardButton(text="Доп. Программа", callback_data="DopProf"))
    await message.answer("Давайте начнём профориентцию! ;)\nНа какую программу вы хотите пойти (Основную или Дополнительную)? ", reply_markup=keyboard)

#######################

@dp.message_handler(commands="commands", commands_prefix="/")
async def cmd_dezign(message: types.Message):
    await message.delete()
    link1 = open('comands.txt', encoding="utf-8") 
    link = link1.read()
    await message.answer(text = f"{link}")


#ОсПрограммаОбуч
@dp.callback_query_handler(text="OsPr")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="2022", callback_data="2022"))
    keyboard.add(types.InlineKeyboardButton(text="2023", callback_data="2023"))
    keyboard.add(types.InlineKeyboardButton(text="2024", callback_data="2024"))
    keyboard.add(types.InlineKeyboardButton(text="2025", callback_data="2025"))
    await call.message.answer("Выберите год поступления: ", reply_markup=keyboard)

@dp.callback_query_handler(text="2022")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Нет информации")

@dp.callback_query_handler(text="2023")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("• 14.04.01 Ядерная энергетика и теплофизика\nВысокотемпературные газовые ядерные реакторные установки\n\n• 14.04.02 Ядерная физика и технологии \nЯдерное топливо и основное оборудование высокотемпературных газовых реакторов\n\n• 22.04.01 Материаловедение и технологии материалов\nМатериалы для высокотемпературных ядерных реакторов\n\n• 09.04.01 Информатика и вычислительная техника\nЦифровые технологии управления технологическими процессами атомных станций нового поколения")

@dp.callback_query_handler(text="2024")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("• 13.04.02 Электроэнергетика и электротехника\nКибербезопасность электроэнергетических систем атомных станций\n\n•18.04.01 Химическая технология\nТехника и технологии водородной энергетик\n\n• 15.04.05 Конструкторско-технологическое обеспечение машиностроительных производств\nКонструкторско-технологическое обеспечение атомных электростанций с ВТГР")

@dp.callback_query_handler(text="2025")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("• 13.04.02 Электроэнергетика и электротехника\nАвтономные электрогенерирующие комплексы на основе водорода\n\n• 13.04.03 Энергетическое машиностроение\nЭнергетические установки на водородном топливе\n\n• 15.04.04 Автоматизация технологических процессов и производств\nАвтоматизация технологических процессов и производств в задачах управления объектами атомной промышленности \n\n• 22.04.02 Металлургия\nАддитивные технологии и производства")

#ДопПрограммаОбуч
@dp.callback_query_handler(text="DopPr")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="2022", callback_data="2O22"))
    keyboard.add(types.InlineKeyboardButton(text="2023", callback_data="2O23"))
    keyboard.add(types.InlineKeyboardButton(text="2024", callback_data="2O24"))
    keyboard.add(types.InlineKeyboardButton(text="2025", callback_data="2O25"))
    await call.message.answer("Выберите год поступления: ", reply_markup=keyboard)

@dp.callback_query_handler(text="2O22")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("• Вычислительная гидродинамика и теплообмен реакторных установок (в пакете ЛОГОС)")

@dp.callback_query_handler(text="2O23")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("• Методы и средства измерений теплотехнических параметров ЯЭУ\n• Применение лазерных технологий в машиностроении\n• Расчет прочности, динамики и ресурса, средств транспортировки водорода\n• Разработка программного обеспечения реального времени для ОС QNX Neutrino\n• Администрирование и оптимизация Astra Linux для систем мониторинга и управления")

@dp.callback_query_handler(text="2O24")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("• Устойчивое развитие и ESG-трансформация\n• Энергетические установки, работающие на водородном топливе\n• Цифровое моделирование электроэнергетических систем АЭС\n• Системы цифрового управления технологическим оборудованием АС\n• R&D менеджмент")

@dp.callback_query_handler(text="2O25")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Нет информации")

#Профориентация Основная программа
@dp.callback_query_handler(text="OsnProf")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Энергетика и физика", callback_data="EnPhi"))
    keyboard.add(types.InlineKeyboardButton(text="Технологии и машиностроение", callback_data="TechMash"))
    await call.message.answer("Давайте начнём профориентцию! ;)\nЧто вам больше нравится?\n\n• Энергетика и физика\n• Технологии и машиностроение ", reply_markup=keyboard)

@dp.callback_query_handler(text="EnPhi")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Ядерная энергетика", callback_data="YadEn"))
    keyboard.add(types.InlineKeyboardButton(text="Электроэнергетика", callback_data="ElEn"))
    await call.message.answer("Продолжим!\nКакая из отраслей вам кажется привлекательней?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="YadEn")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт одно из данных направлений:\n\n• Ядерная энергетика и теплофизика\n• Ядерная физика и технологии\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

@dp.callback_query_handler(text="ElEn")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="ДА!", callback_data="Enmach"))
    keyboard.add(types.InlineKeyboardButton(text="Нет :с", callback_data="Elandel"))
    await call.message.answer("Остался последний вопрос!\nВам нравится конструирование?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="Enmach")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Энергетическое машиностроение\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="Elandel")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Электроэнергетика и электротехника\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

@dp.callback_query_handler(text="TechMash")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Информатика", callback_data="Infor"))
    keyboard.add(types.InlineKeyboardButton(text="Машиностроение", callback_data="MechStroy"))
    await call.message.answer("Продолжим!\nКакая область вам ближе?", reply_markup=keyboard)

@dp.callback_query_handler(text="Infor")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Разработка программ/приложений", callback_data="RazPrPril"))
    keyboard.add(types.InlineKeyboardButton(text="Создание эффективных алгоритмов", callback_data="SozEfAl"))
    await call.message.answer("Что вас привлекает больше?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="RazPrPril")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Информатика и вычислительная техника\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="SozEfAl")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Автоматизация технологических процессов и производств\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

@dp.callback_query_handler(text="MechStroy")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Да", callback_data="Yean"))
    keyboard.add(types.InlineKeyboardButton(text="Нет", callback_data="Nope"))
    await call.message.answer("Продолжим!\nВам нравится изучать различные природные материалы?", reply_markup=keyboard)

@dp.callback_query_handler(text="Yean")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Да", callback_data="yeah1"))
    keyboard.add(types.InlineKeyboardButton(text="Нет", callback_data="nope1"))
    await call.message.answer("Вам нравится выявлять причинно следственные связи?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="yeah1")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Материаловедение и  технологии материалов\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="nope1")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Металлургия\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

@dp.callback_query_handler(text="Nope")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Да", callback_data="yeah2"))
    keyboard.add(types.InlineKeyboardButton(text="Нет", callback_data="nope2"))
    await call.message.answer("Вам нравится химия?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="yeah2")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Химические технологии\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv 
@dp.callback_query_handler(text="nope2")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Конструкторско-технологическое обеспечение машиностроительных производств\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Профориентация Основная программа

@dp.callback_query_handler(text="DopProf")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Да", callback_data="yeah4"))
    keyboard.add(types.InlineKeyboardButton(text="Нет", callback_data="nope4"))
    await call.message.answer("Вам нравится IT сфера?", reply_markup=keyboard)

@dp.callback_query_handler(text="yeah4")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Разрабатывать", callback_data="razrab1"))
    keyboard.add(types.InlineKeyboardButton(text="Поддерживать", callback_data="podder1"))
    await call.message.answer("Вам больше нравится разрабатывать или поддерживать?", reply_markup=keyboard)

@dp.callback_query_handler(text="razrab1")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Создавать", callback_data="sozd32"))
    keyboard.add(types.InlineKeyboardButton(text="Рассчитывать", callback_data="rass32"))
    await call.message.answer("В разработке вам больше нравится создавать, или рассчитывать?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="sozd32")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Разработка программного обеспечения реального времени для ОС QNX Neutrino\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="rass32")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Цифровое моделирование электроэнергетических систем АЭС\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

@dp.callback_query_handler(text="podder1")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Сайта", callback_data="site"))
    keyboard.add(types.InlineKeyboardButton(text="Оборудования АС", callback_data="ObAS"))
    await call.message.answer("Поддерживать работу сайта или оборудования АС?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="site")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Администрирование и оптимизация Astra Linux для систем мониторинга и управления\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="ObAS")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Системы цифрового управления технологическим оборудованием АС\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#=================================================================================================================================
@dp.callback_query_handler(text="nope4")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Рассчитывать", callback_data="rasnope"))
    keyboard.add(types.InlineKeyboardButton(text="Анализировать", callback_data="analiz"))
    keyboard.add(types.InlineKeyboardButton(text="Применять", callback_data="prim1"))
    await call.message.answer("Что вам больше нравится?", reply_markup=keyboard)

@dp.callback_query_handler(text="rasnope")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Расчет гидродинамики", callback_data="resgid"))
    keyboard.add(types.InlineKeyboardButton(text="Измерение теплотехнических параметров ЯЭУ", callback_data="izmteppar"))
    keyboard.add(types.InlineKeyboardButton(text="Расчет прочности", callback_data="resproch"))
    await call.message.answer("Что вас интересует?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="resgid")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Вычислительная гидродинамика и теплообмен реакторных установок\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="izmteppar")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Методы и средства измерений теплотехнических параметров ЯЭУ\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="resproch")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Расчет прочности, динамики и ресурса, средств транспортировки водорода\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

@dp.callback_query_handler(text="analiz")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Развитием компании", callback_data="razvidcomp"))
    keyboard.add(types.InlineKeyboardButton(text="Исследовать новые возможности для компании", callback_data="isslednewvoz"))
    await call.message.answer("Чем вы бы хотели заниматься?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="razvidcomp")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Устойчивое развитие и ESG-трансформация\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="isslednewvoz")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• R&D менеджмент\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

@dp.callback_query_handler(text="prim1")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Применением лазеров", callback_data="PrimLaz"))
    keyboard.add(types.InlineKeyboardButton(text="Установкой оборудования на водородном топливе", callback_data="UstObVodTop"))
    await call.message.answer("Чем бы хотели заняться?", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="PrimLaz")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Применение лазерных технологий в машиностроении\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Otv
@dp.callback_query_handler(text="UstObVodTop")
async def send_Os(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти на сайт", url='https://www.nntu.ru/structure/view/podrazdeleniya/pish/proekt-programma-partnery'))
    keyboard.add(types.InlineKeyboardButton(text="Подать заявку", url='https://ips.nntu.ru/content/zayavka/zayavka'))
    await call.message.answer("Вам подойдёт данное направление:\n\n• Энергетические установки, работающие на водородном топливе\n\n• Вы можете найти информацию о направлении у нас на сайте или отправть заявку на обучние!", reply_markup=keyboard)

#Конец файла
if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)

















