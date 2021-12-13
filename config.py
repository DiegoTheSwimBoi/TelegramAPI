TOKEN ='Insert Token Here'

s_regin="public"

#BOT WILL REACT ON USER-STATIC-WORDS OR EMOJI
command={
  "news":["📰  Новости","Новости","новости","НОВОСТИ","news","News","NEWS","📰"],
  "hello":["Привет","Привет.","Привет!","ПРИВЕТ","Hi","Hi.","Hi!","HI","Hello","Hello.","Hello!","HELLO","😃","😄","😆","😁","😸","😹","😺"],
  "random":["🎲  Рандом","Рандом","рандом","РАНДОМ","random","Random","RANDOM","rnd","Rnd","RND","🎲"],
  "help":["/h","/help","?","📖"],
  "delete":["❌","🚫","отписаться"],
  "sub":["subscribe","подписаться"],
  
}

food={"пиво":"🍺","виноград":"🍇","дыня":"🍈","арбуз":"🍉","мандарин":"🍊","лимон":"🍋","банан":"🍌"}


help_message=f'Команда:  {command["random"][0]}  -  выдаст вам рандомное число. \nКоманда:  {command["news"][0]} - выдаст вам новость. \nМы будем рядом. Обращайтесь за помощью'

admin_message=f'Мы рады приветствовать в нашей среде 😊. Обращайтесь за помощью:\nКоманда:  {command["delete"][1]}'







