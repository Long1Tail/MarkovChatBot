from config import TOKEN
import telebot, telebot.types
import random

def write_data(data: dict):
    with open('data.txt', 'w', encoding='utf-8') as file:
        for key in data.keys():
            file.write(f'{key}:{';'.join(data[key])}\n')
        file.close()
    
def read_data():
    data = {}
    with open('data.txt', 'r', encoding='utf-8') as file:
        for i in file.readlines():
            key, _ = i.rstrip('\n').split(':')
            args = _.split(';')
            data[key] = args
        file.close()
    return data

bot = telebot.TeleBot(TOKEN)
data = read_data()

not_letters = ',.:;?/\\\"\'[]{}`~!@#$%^&*()_-+=№|'

@bot.message_handler(commands=['start'])
def send_hello(message: telebot.types.Message):
    bot.send_message(message.chat.id, "дарова")

@bot.message_handler(commands=['g', 'gen', 'generate'])
def generate(message: telebot.types.Message):
    print('generated message')
    lenth = random.randint(3, 9)
    tokens = []

    tokens.append(random.choice(list(data.keys())))
    last_token = tokens[0]
    for i in range(lenth-1):
        if last_token not in data.keys():
            break
        
        last_token = random.choice(data[last_token])
        tokens.append(last_token)

    bot.reply_to(message, ' '.join(tokens))

@bot.message_handler(content_types=['text'])
def parse_message(message: telebot.types.Message):
    print('got message')
    text = message.text

    if not text:
        return
    
    for i in not_letters:
        text = text.replace(i, ' ')
    
    while text.find('  ') != -1:
        text = text.replace('  ', ' ')
    
    text = text.lower()

    tokens = text.split()
    for i in range(1, len(tokens)):
        key = tokens[i-1]
        arg = tokens[i]
        if key in data.keys():
            data[key].append(arg)
            continue

        data[key] = [arg]

    write_data(data)


bot.infinity_polling()

write_data(data)