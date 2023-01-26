import dict
from telebot import types
a=0
spisok = []
lang_button = types.InlineKeyboardMarkup()
for i, j in dict.dictionary.items():
    key = types.InlineKeyboardButton(j, callback_data=i)
    spisok.append(key)
    a+= 1;
    if a == 3:
        a = 0
        lang_button.add(spisok[0], spisok[1], spisok[2])
        spisok = []

#def voice_button():
    # vb = types.InlineKeyboardMarkup()
    # voice = types.InlineKeyboardButton('Озвучить', callback_data='start_voice')
    # vb.add(voice)
    # return vb

