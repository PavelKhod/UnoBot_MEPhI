import telebot
from telebot import types
import webbrowser
import logic
bot = telebot.TeleBot('6872862815:AAEDh0fdb15g8XCjghcW4RIJlLOnsEG_i6M')
CHAT_ID = None

@bot.message_handler(commands=['start'])
def main(info):
    bot.send_message(info.chat.id, 'Этот бот предназначен для проведения игры уно в телеграмме. Для запуска игры добавьте бота в свою группу, и напишите /start_game.')

@bot.message_handler(commands=['start_game'])
def main(info):
    if logic.is_playing:
        return
    global CHAT_ID
    CHAT_ID = info.chat.id
    bot.send_message(info.chat.id,
    '''Охаё, они чан) Создай свою игру\n
    '''
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    item2 = types.KeyboardButton("Присоединиться")
    markup.add(item2, item1)
    bot.send_message(info.chat.id, 'Нажмите присоединиться, чтобы войти в игру. Нажмите начать игру, для запуска игры.', reply_markup=markup)

@bot.message_handler(commands=['stats'])
def main(info):
    msg = "Уважаемые игроки:\n"
    for p in logic.player:
        msg += str(p.name) + "\n"
    bot.send_message(info.chat.id, msg)

@bot.message_handler(commands=['stiker'])
def main(info):
    bot.send_sticker(info.chat.id, 'CAACAgIAAxkBAAEBpnZlPXSscqnvN_rM-uZusGxvanFG2wACuCQAArgGAUiH8Vp5cuhbHDAE')

@bot.message_handler(commands=['move'])
def main(info):
    player = info.from_user.first_name
    if len(info.text.split()) > 1:
        move = info.text.split()[1]
        if logic.player[logic.pos].name == player:
            if move.isdigit() and 0 <= int(move) and int(move) < len(logic.player[logic.pos].cards):
                logic.player_hasActed[player] = True
                logic.player_lastMove[player] = int(move)
            else:
                bot.send_message(info.chat.id, 'балбес, напиши нормально')
    else:
        logic.player_hasActed[player] = True
        logic.player_lastMove[player] = -1

@bot.message_handler(commands=['end_game'])
def main(info):
    logic.is_playing = False

@bot.message_handler(commands=['admin'])
def main(info):
    bot.send_message(info.chat.id, 'Писать по всем вопросам:@rbedin25, @shout_0_0, @n3tw4lk3r')

@bot.message_handler(commands=['help'])
def main(info):
    msg = 'Сам себе помаги!\n Но если прям надо то: \n /start_game - запускает игру \n /end_game - заканчивает игру \n /move - выбор карты из руки или взять карту\n /admin - связь с админами'
    bot.send_message(info.chat.id, msg)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Присоединиться":
        if message.from_user.first_name not in logic.player_hasActed:
            bot.send_message(message.chat.id, f'Игрок {message.from_user.first_name} добавлен')
            logic.add_player(message.from_user.first_name)
    if message.text=="Начать игру":
        if logic.is_playing or len(logic.player) == 0:
            return
        global CHAT_ID
        CHAT_ID = message.chat.id
        logic.game()
