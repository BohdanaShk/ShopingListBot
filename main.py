import telebot

API_TOKEN = "2111677038:AAFbvZx9qQHc6fMudfg4HIUOTTrWKtdEeEw"
shopping_bot = telebot.TeleBot(API_TOKEN)

# telebot.types.ReplyKeyboardMarkup
# telebot.types.InlineKeyboardMarkup
commands = ['Add to list ', 'Get from list', 'Delete from list']
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row(*commands)


shopping_list = []
current_operation = None


@shopping_bot.message_handler(commands=["start"])
def start(message):
    shopping_bot.reply_to(message, 'Welcome to shopping bot', reply_markup=keyboard)


@shopping_bot.message_handler(content_types=['text'])
def command(message):
    global current_operation
    global shopping_list
    if message.text == 'Add to list':
        current_operation = 'add'
        shopping_bot.reply_to(message, 'Now you can add items to the list')
    elif message.text == 'Get from list':
        current_operation = 'get'
        shopping_bot.reply_to(message, ','.join(shopping_list))
    elif message.text == 'Delete from list':
        current_operation = 'del'
        inline_kb = telebot.types.InlineKeyboardMarkup()
        for elem in shopping_list:
            inline_kb.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
        shopping_bot.reply_to(message, 'Now you can delete items', reply_markup=inline_kb)
    else:
        if current_operation == 'add':
            shopping_list.append(message.text)
            shopping_bot.reply_to(message, f'successfully added {message.text}')


@shopping_bot.callback_query_handler(func=lambda x: True)
def callback_handler(call):
    global shopping_list
    index_to_remove = None
    for i in range(len(shopping_list)):
        if shopping_list[i] == call.data:
            index_to_remove = i
            break
    if index_to_remove is not None:
        del shopping_list[index_to_remove]

    print(shopping_list)


shopping_bot.polling()
