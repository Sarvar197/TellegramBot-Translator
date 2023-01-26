from googletrans import Translator
import telebot
import keyboard
import sqlite3
import dict
transl = Translator()



# Подключение к боту
bot = telebot.TeleBot('5814415159:AAGdWU1_b7VcZh40Fw1a8hvc1gtkRmjo324')

# Присоединяемся к базе данных
connection = sqlite3.connect('example.db',  check_same_thread=False)
print('started') # Показываем в терминале, что процесс запущен

sql_con = connection.cursor()

#Запуск Бота
@bot.message_handler(commands=['start'])
def process_start_command(message):
    #mycursor = connection.cursor()

    sql = "SELECT * FROM users WHERE id = ?"
    adr = (str(message.from_user.id),)
    sql_con.execute(sql, adr)
    myresult = sql_con.fetchall()
    print(myresult)


    if myresult is None or myresult == [] or myresult == ():
        #mycursor = connection.cursor()
        sql = 'INSERT INTO users (id,lang) VALUES (?,?)'
        user_id = message.from_user.id
        sql_con.execute(sql,user_id)
        connection.commit()
        bot.send_message(message.from_user.id, 'Зарегистрирован')
    else:
        bot.send_message(message.from_user.id, 'Ваш бот уже зарегистрирован ')

    bot.send_message(message.from_user.id, 'Привет, я бот-переводчик. Для начала работы выбери команду в разделе меню ')

@bot.message_handler(commands=['choose'])
def process_start_command(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Выберите язык:',reply_markup=keyboard.lang_button)

@bot.message_handler(commands=['info'])
def process_info_command(message):
    user_id = message.from_user.id
    contact = 'Контакт для жалоб и предложений @translator_service'
    bot.send_message(user_id, contact)

@bot.callback_query_handler(lambda c: c.data)
def process_callback(callback_query):
    if callback_query.data in dict.languages:

        lang = callback_query.data

        #mycursor = connection.cursor()
        sqlite3 = 'UPDATE users SET lang = ? WHERE id = ?'
        user_id = (lang, str(callback_query.from_user.id))
        sql_con.execute(sqlite3, user_id)
        bot.send_message(callback_query.from_user.id, "Вы выбрали язык: " + dict.dictionary[lang])

@bot.message_handler()
def echo_message(message):
    print('перевод осуществлён')

    sql = "SELECT * FROM users WHERE id = ?"
    user_id = (message.from_user.id,)
    sql_con.execute(sql, user_id)
    result = sql_con.fetchall()
    lang = result[0][1]
    word = transl.translate(message.text, dest=lang).text

    bot.send_message(message.from_user.id, word)

if __name__ == '__main__':
    bot.polling()