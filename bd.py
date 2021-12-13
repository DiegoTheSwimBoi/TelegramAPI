import sqlite3 



try:
    con = sqlite3.connect('database.db')
    cursor=con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"chat_code"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)
    con.commit()
except sqlite3.Error:
    print("Err table create")
finally:
    con.close()
	
try:
    con = sqlite3.connect('database.db')
    cursor=con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)
    con.commit()
    GetUser = cursor.execute(""" SELECT * FROM "categories" """).fetchall()
    if(len(GetUser)<5):
        arr=['Вечерний поезд', 'EDM', 'Rock n Roll', '8-bit', 'Covers']
        for i in range(len(arr)):
            cursor.execute(""" INSERT INTO "categories" (name) VALUES (?)
            """,(arr[i],))
            con.commit()
except sqlite3.Error:
    print("Err table create and insert")
finally:
    con.close()
	
	
	
try:
    con = sqlite3.connect('database.db')
    cursor=con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "subscriptions" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"category_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)
    con.commit()
except sqlite3.Error:
    print("Err table create")
finally:
    con.close()
	
	
def getAllCategories():

    cat=[]

    try:
        con = sqlite3.connect("database.db")
        cursor=con.cursor()

        GetUser = cursor.execute(""" SELECT * FROM "categories" """).fetchall()
        if(len(GetUser)==0):
            print("Категории не найдены")
        else:
            for i in range(len(GetUser)):
                # print(GetUser[i][0])
                cat.insert(GetUser[i][0],GetUser[i][1])  
            con.commit()
            return cat
    except sqlite3.Error:
        print("Err DB insert")
    finally:
        con.close() 

def getAllCategoriesID():

    cat=[]

    try:
        con = sqlite3.connect("database.db")
        cursor=con.cursor()

        GetUser = cursor.execute(""" SELECT id FROM "categories" """).fetchall()
        if(len(GetUser)==0):
            print("Категории не найдены")
        else:
            for i in range(len(GetUser)):
                # print(GetUser[i][0])
                cat.append(str(GetUser[i][0]))  
            con.commit()
            return cat
    except sqlite3.Error:
        print("Err DB insert")
    finally:
        con.close() 


def HasUser(code):
    try:
        con = sqlite3.connect("database.db")
        cursor=con.cursor()

        GetUser = cursor.execute(""" SELECT "chat_code" FROM "users" where "chat_code"=? """,(code,)).fetchall()
        return GetUser
    except sqlite3.Error:
        print("No")
        return "Произошла ошибка"
    finally:
        con.close() 



def insertUser(code,password):
    try:
        con = sqlite3.connect("database.db")
        
        cursor=con.cursor()

        GetUser = cursor.execute(""" SELECT "chat_code" FROM "users" where "chat_code"=? """,(code,)).fetchall()
        if(len(GetUser)>0):
            return "Пользователь с таким логином уже есть в сети"
        else:
            cursor.execute(""" INSERT INTO "users" (chat_code,password) VALUES (?,?)
            """,(code,password))
            con.commit()
            return "Зарегистрирован"        
    except sqlite3.Error:
        print("No")
    finally:
        con.close() 

def authUser(code,password):
    try:
        con = sqlite3.connect("database.db")
        
        cursor=con.cursor()

        GetUser = cursor.execute(""" SELECT "chat_code" FROM "users" where "chat_code"=? AND "password"=? """,(code,password)).fetchall()
        if(len(GetUser)>0):
            return True
        else:
            return False  
    except sqlite3.Error:
        print("No")
    finally:
        con.close() 



def getAllUsers():

    cat=[]

    try:
        con = sqlite3.connect("database.db")
        cursor=con.cursor()

        

        GetUser = cursor.execute(""" SELECT * FROM "users" """).fetchall()
        if(len(GetUser)==0):
            print("Категории не найдены")
            cat.insert(1,"Категории не найдены")
        else:
            for i in range(len(GetUser)):
                # print(GetUser[i][0])
                cat.insert(GetUser[i][0],{GetUser[i][1],GetUser[i][2]})
            con.commit()
            return cat
    except sqlite3.Error:
        print("Err DB ")
    finally:
        con.close() 

def getUserByID(userId):
    try:
        con = sqlite3.connect("database.db")
        cursor=con.cursor()
        t = (f'{userId}',)
        GetUser = cursor.execute(""" SELECT "id" FROM "users" where "chat_code"=? """,t).fetchall()
        con.commit()
        if(len(GetUser)>0):
            return True
        else:
            return False
    except sqlite3.Error:
        print("Err DB ")
    finally:
        con.close() 



def insertSub(user,category):	
    try:
        
        con = sqlite3.connect("database.db")
        cursor=con.cursor()
        message=''
        t = (f'{user}',)
        cursor.execute(""" SELECT "category_id" FROM "subscriptions" where "user_id"=? """,t)
        UserSubs=cursor.fetchall() 
        catId = cursor.execute(""" SELECT "id" FROM "categories" where "name"=? """,(f'{category}',)).fetchone()
        if len(UserSubs)>0:
            if catId not in UserSubs:
                cursor.execute(""" INSERT INTO "subscriptions" (user_id,category_id) VALUES (?,?)
                """,(user,catId[0]))
                con.commit()
                message="Подписан"
            else: message="Уже подписан"
        else: 
            cursor.execute(""" INSERT INTO "subscriptions" (user_id,category_id) VALUES (?,?)
            """,(user,catId[0]))
            con.commit()
            message="Подписан"
        return message

    except sqlite3.Error:
        print("err")
        return "Произошла ошибка на сервере"
    finally:
        con.close()   



def getSubsByUserID(user):
    cat={}

    try:
        con = sqlite3.connect("database.db")
        cursor=con.cursor()
        t = (f'{user}',)
        cursor.execute(""" SELECT category_id,name FROM "subscriptions" INNER JOIN categories ON categories.id=subscriptions.category_id where subscriptions.user_id=? """,t)
        UserSubs=cursor.fetchall()
        if(len(UserSubs)==0):
            print("Категории не найдены")
        else:
            for i in range(len(UserSubs)):
                # print(GetUser[i][0])
                cat[i]=[UserSubs[i][0],UserSubs[i][1]]
            con.commit()
        
        return cat
    except sqlite3.Error:
        print("Err DB insert")
    finally:
        con.close()     


def deleteSub(id,user):
    try:
        con = sqlite3.connect("database.db")
        cursor=con.cursor()
        t = (f'{id}',f'{user}')
        cursor.execute(""" DELETE FROM "subscriptions" where "category_id"=? and user_id=? """,t).fetchall()
        con.commit()
        return "Отписан"
    except sqlite3.Error:
        print("No")
    finally:
        con.close()   







