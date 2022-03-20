from types import NoneType
from telebot import types
from validator import validate_age
import telebot
bot = telebot.TeleBot('5175541848:AAHSyM3cKEfmoubtpvi7eMOxHtADMqw8iTU')

stattype = 0
status = False
reg_status = False
first_name = ''
last_name = ''
age = ''
health = ''
chat_id = ''
message_id = ''
gender = ''

@bot.message_handler(content_types=['text'])
def registration(message):
    global status, reg_status, first_name, last_name, age, gender,stattype,chat_id,message_id
    if status == False:
        if message.text == '/start':
            status = True
            chat_id = str(message.from_user.id)
            if not check_func(chat_id):
                if message.from_user.first_name != NoneType:
                    first_name = message.from_user.first_name
                if message.from_user.last_name != NoneType:
                    last_name = message.from_user.last_name
                if message.from_user.first_name != NoneType and message.from_user.last_name != NoneType:
                    question = 'Привет '+ str(last_name) +' '+ str(first_name) + '. Я бот для сбора информации и исользования его лишь в статистике для мед учереждений, так что не бойся меня ;) Перед началом, давайте пройдем небольшую регистрацию\nДля начала, скажи какой у тебя пол?'
                else:
                    question = 'Привет '+ str(message.username) + '. Я бот для сбора информации и исользования его лишь в статистике для мед учереждений, так что не бойся меня ;) Перед началом, давайте пройдем небольшую регистрацию\nДля начала, скажи какой у тебя пол?'
                keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
                key_male = types.InlineKeyboardButton(text='Мужской', callback_data='male') 
                keyboard.add(key_male); #добавляем кнопку в клавиатуру
                key_female= types.InlineKeyboardButton(text='Женский', callback_data='female')
                keyboard.add(key_female)
                stattype = 1
                message_id = bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
            else:
                bot.send_message(message.from_user.id, 'О, я вижу ты снова здесь, как я рад тебя видеть! К сожалению новых функций пока не добавили, но ты заходи время от времени')
                bot.register_next_step_handler(message, registration)
                status = False
        else:
            bot.send_message(message.from_user.id, 'Для того, чтобы начать, напишите /start')
            bot.register_next_step_handler(message, registration)
    else:
        bot.send_message(message.from_user.id, 'Подождите немного, пожалуйста!')
        bot.register_next_step_handler(message, registration)
        

def get_age(message):
    global age,stattype
    if validate_age(str(message.text)):
        age = int(message.text)
        get_health(message)
    else:
        bot.send_message(message.from_user.id, 'Так, так, так. Я хоть и бот, но не настолько глупый, а ну давай по нормальному, скажи, сколько тебе лет')
        bot.register_next_step_handler(message, get_age)

def get_health(message):
    global health, stattype, message_id
    question = 'Почти закончили. Расскажи вкратце, как ты себя чувствуешь?'
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_bad = types.InlineKeyboardButton(text='Совсем плохо((', callback_data='bad') 
    keyboard.add(key_bad); #добавляем кнопку в клавиатуру
    key_nice= types.InlineKeyboardButton(text='Вполне нормально', callback_data='normal')
    keyboard.add(key_nice)
    key_good= types.InlineKeyboardButton(text='Чувствую себя просто отлично', callback_data='great')
    keyboard.add(key_good)
    stattype = 2
    message_id = bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global gender
    global health,stattype, status, last_name, first_name, message_id
    if call.data == 'male' or call.data == 'female':
        bot.edit_message_reply_markup(call.message.chat.id, message_id.message_id, 'Привет '+ str(first_name)+' '+ str(last_name) + '.Я бот для сбора информации и исользования его лишь в статистике для мед учереждений, так что не бойся меня ;) Перед началом, давайте пройдем небольшую регистрацию\nДля начала, скажи какой у тебя пол?',reply_markup=None)
        message_id = ''
        gender = call.data
        bot.send_message(call.message.chat.id, 'Хорошо, так сколько тебе лет?')
        bot.register_next_step_handler(call.message, get_age)
    elif call.data == 'bad' or call.data == 'normal' or call.data == 'great':
        bot.edit_message_reply_markup(call.message.chat.id, message_id.message_id, 'Почти закончили. Расскажи вкратце, как ты себя чувствуешь?',reply_markup=None)
        message_id = ''
        health = call.data
        bot.send_message(call.message.chat.id, 'Хорошо, я сейчас попробую сохранить твои данные')
        if save_data():
            bot.send_message(call.message.chat.id, 'Я все сохранил, спасибо большое!')
            status = False
        else:
            bot.send_message(call.message.chat.id, 'Упс, что - то пошло не так. Попробуйте через время сделать все то же самое, пожааалуйста(((')
            status = False
    elif stattype == 1:
        bot.edit_message_reply_markup(call.message.chat.id, message_id.message_id, 'Привет '+ str(first_name)+' '+ str(last_name) + '.Я бот для сбора информации и исользования его лишь в статистике для мед учереждений, так что не бойся меня ;) Перед началом, давайте пройдем небольшую регистрацию\nДля начала, скажи какой у тебя пол?',reply_markup=None)
        message_id = ''
        bot.send_message(call.message.chat.id, 'Извини, видимо ты ввел что-то не так, попробуй сначала')
        bot.register_next_step_handler(call, registration)
    elif stattype == 2:
        bot.edit_message_reply_markup(call.message.chat.id, message_id.message_id, 'Почти закончили. Расскажи вкратце, как ты себя чувствуешь?',reply_markup=None)
        message_id = ''
        bot.send_message(call.message.chat.id, 'Извини, видимо ты ввел что-то не так')
        bot.register_next_step_handler(call, get_age)

def save_data():
    global stattype
    global reg_status
    global first_name
    global last_name
    global age 
    global health 
    global chat_id 
    global gender 
    with open('DataBase/data.txt', mode = 'a') as data:                            
        data.write(chat_id + '%' + str(first_name) + '#' +str(last_name)+ '#'+ str(age) + '#'+ health + '#' +gender+ '\n' )
        stattype = 0
        reg_status = False
        first_name = ''
        last_name = ''
        age = 0
        health = ''
        chat_id = ''
        gender = ''
        data.close()
        return True
    

def check_func(id):
    check = False                #Проверка: зареган ли клиент
    with open('DataBase/data.txt', mode = 'r') as data:
        for line in data: 
            n = 0     
            while (n<= len(line)-1):
                if line[n] == '%':
                    break
                n = n+1
            if line[:n] == str(id):
                check = True         
        data.close()
    return check


bot.polling(none_stop=True, interval=0)
