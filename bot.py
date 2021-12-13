import  telebot
from telebot import types
import config
import random
import bd
import jsonNews

bot = telebot.TeleBot(config.TOKEN)


#Telebot: Welcome message /start

@bot.message_handler(commands=['start'])
def welcome(message):
    sti= open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id,sti)
    bot.send_message(message.chat.id,"Здарова, <b> дружище </b>. \n  Давно не виделись".format(message.from_user, bot.get_me()),parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1= types.KeyboardButton("Привет")
    item2= types.KeyboardButton("📰  Новости")
    item3= types.KeyboardButton("🎲  Рандом")
    markup.add(item1,item2,item3)
    if bd.HasUser(message.chat.id):
        subs=bd.getSubsByUserID(message.chat.id)
        if subs:
            catId=[]
            for i in range(len(subs)):
                catId.insert(i,subs[i][0])
            news(message,catId)
    bot.send_message(message.chat.id,"Что надо?",reply_markup=markup)

def news(message,catId):
    dataFetch=jsonNews.getNews()
    bot.send_message(message.chat.id,"Подписки")
    for i in range(len(dataFetch)):
        #print(dataFetch[i]['category'],catId)
        if dataFetch[i]['category'] in catId:
            bot.send_message(message.chat.id,dataFetch[i]['title']+"\n"+dataFetch[i]['img']+"\n"+dataFetch[i]['description'])
        #print(dataFetch[i]['title'])
    


#Telebot: What do you want?

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type=="private":
        getMsgTOLower=message.text.lower()
        if message.text in config.command["hello"]:
            bot.send_message(message.chat.id, message.text)
        elif message.text in config.command["news"]:
            bot.send_message(message.chat.id,'Выбрана категория "Новости"...')
            sti= open('static/bruh.webp', 'rb')
            bot.send_sticker(message.chat.id,sti)
            markup2=types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Зарегистрироваться",callback_data='reg')
            item2 = types.InlineKeyboardButton("Есть аккаунт",callback_data='enter')
            markup2.add(item1,item2)
            bot.send_message(message.chat.id,'Выберите действие:', reply_markup=markup2)
        elif getMsgTOLower in config.food:
            bot.send_message(message.chat.id,config.food[getMsgTOLower])
        elif message.text in config.command["random"]:
            bot.send_message(message.chat.id,str(random.randint(0,100)))
        elif getMsgTOLower in config.command["help"]:
            bot.send_message(message.chat.id,config.help_message)
        elif bd.getUserByID(message.chat.id) and config.s_regin=="protected":
            getCategory = bd.getAllCategories()
            if message.text in getCategory:
                bot.send_message(message.chat.id,bd.insertSub(message.chat.id,message.text))
            if getMsgTOLower in config.command["delete"]:
                delete(message)
        else:
            bot.send_message(message.chat.id,"ХЗ! Я не понимаю тебя 😖 \n  Держи 🍺 - это поможет \n Или пропиши '/help' ")
        

#Telebot: InlineKeyboard
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    User = bd.HasUser(call.from_user.id)
    try:
        if call.message:
            if call.data=='reg':
                
                if(len(User)==0):
                    bot.send_message(call.from_user.id,"Произошла регистрация")
                    markup3=types.InlineKeyboardMarkup(row_width=2)
                    item1 = types.InlineKeyboardButton("Да",callback_data='yes')
                    item2 = types.InlineKeyboardButton("Нет",callback_data='no')
                    markup3.add(item1,item2)
                    bot.send_message(call.from_user.id,'Вы готовы передать свои данные ? ', reply_markup=markup3)
                else:
                    bot.send_message(call.from_user.id,"Пользователь с таким логином уже есть в сети")
            elif call.data=='enter':
                bot.send_message(call.from_user.id,"Авторизация")
                msg = bot.send_message(call.from_user.id, "Введите ваш уникальный код: ")
                bot.register_next_step_handler(msg, Auth)

            elif call.data in bd.getAllCategoriesID():
                cat=bd.getSubsByUserID(call.from_user.id)
                print(bd.getAllCategoriesID())
                if len(cat)>0 and len(User)>0:
                    for i in range(len(cat)):
                        if f"{call.data}" == f"{cat[i][0]}":
                            bot.send_message(call.from_user.id,bd.deleteSub(call.data,call.from_user.id))
                else:
                    bot.send_message(call.from_user.id,"У вас еще нет подписок")
                
                msg = bot.send_message(call.from_user.id, "Введите ваш уникальный код: ")
                config.s_regin="public"
                bot.register_next_step_handler(msg, Auth)
            else:
                bot.send_message(call.from_user.id,"Произошла ошибка")
            
            if call.data=="yes":
                bot.send_message(call.from_user.id,"Для регистрации необходимо создать уникальный код, который будет использован в качестве пароля. ")
                msg = bot.send_message(call.from_user.id, "Введите уникальный код: ")
                bot.register_next_step_handler(msg, Take_Token)
            elif call.data=="no":  
                bot.send_message(call.from_user.id,"Хорошо. Тогда потом. 😸")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Обрабатывается запрос...", reply_markup=None )
        
        
    except Exception as e:
        print(repr(e))

#Telebot: Check In
def Take_Token(message):
    msg = format(message.text)
    bot.send_message(message.chat.id, bd.insertUser(message.chat.id,msg))
    YourNews(message)

#Telebot: Auth
def Auth(message):
    msg = format(message.text)
    response=bd.authUser(message.chat.id,msg)
    if(response):
        YourNews(message)
    else:
        bot.send_message(message.chat.id, "Не правильно ведён пароль")

#Telebot: Newsroom Enter
def YourNews(message):
    config.s_regin="protected"
    
    bot.send_message(message.chat.id, "Добро пожаловать")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    getCategory = bd.getAllCategories()
    for item in getCategory:
        markup.add(types.KeyboardButton(item))
    markup.add(types.KeyboardButton("Отписаться"))
    bot.send_message(message.chat.id, "Вам предложены различные новости: ", reply_markup=markup)

def delete(message):
    getCategoryByID = bd.getSubsByUserID(message.chat.id)
    if len(getCategoryByID)>0:
        markup3=types.InlineKeyboardMarkup(row_width=len(getCategoryByID))
        for i in range(len(getCategoryByID)):
            markup3.add(types.InlineKeyboardButton(getCategoryByID[i][1],callback_data=getCategoryByID[i][0]))
        bot.send_message(message.chat.id,"Вы можете отписаться", reply_markup=markup3)
    else: 
        bot.send_message(message.chat.id,"У вас еще нет подписок")
        msg = bot.send_message(message.chat.id, "Введите ваш уникальный код: ")
        config.s_regin="public"
        bot.register_next_step_handler(msg, Auth)

    
  

bot.polling(non_stop=True)


