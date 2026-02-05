from config import TOKEN
import telebot, telebot.types
import random

def write_data(data: dict[str, set], name: str):
    with open(f'{name}.txt', 'w', encoding='utf-8') as file:
        for key in data.keys():
            file.write(f'{key}:{';'.join(data[key])}\n')
        file.close()
    
def write_all_data(beginnings: dict[str, set], middle: dict[str, set], endings: dict[str, set]):
    write_data(beginnings, 'beg')
    write_data(middle, 'mid')
    write_data(endings, 'end')


def read_data(name: str):
    data = {}
    with open(f'{name}.txt', 'r', encoding='utf-8') as file:
        for i in file.readlines():
            key, _ = i.rstrip('\n').split(':')
            args = set(_.split(';'))
            data[key] = args
        file.close()
    return data

bot = telebot.TeleBot(TOKEN)
beg = read_data('beg')
mid = read_data('mid')
end = read_data('end')

def generate_sentence(beg: dict[str, set[str]], mid: dict[str, set[str]], end: dict[str, set[str]]):
    word = random.choice(list(beg.keys()))
    res = [word]
    word = random.choice(list(beg[word]))
    while(True):
        res.append(word)
        if word in end.keys() and (word not in mid.keys() or random.randint(1, 6) == 6 or not mid[word]):
            res.append(random.choice(list(end[word])))
            break
        word = random.choice(list(mid[word]))

    text = ' '.join(res)
    text = text[0].capitalize() + text[1:]
    return text

def split_into_sentences(text: str):
    s = []
    token = ''
    for i in text:
        if i in ['.', '?', '!', '\n']:
            s.append(token)
            token = ''
            continue
        token += i
    s.append(token.lower())
    return s

def get_rid_of_litter(text: str):
    res = ''
    for i in text:
        if i.isalnum() or i == ' ':
            res += ' '
    while res.find('  ') != -1:
        res = res.replace('  ', ' ')
    
    return res

not_letters = ',:;/\\\"\'[]{}`~!@#$%^&*()-+=№|—'

@bot.message_handler(commands=['start'])
def send_hello(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Привет! Скажешь что-нибудь?")

@bot.message_handler(commands=['g', 'gen', 'generate', 'get_me_some_nonsense'])
def generate(message: telebot.types.Message):
    length = 1
    tokens = []
    for i in range(length):
        tokens.append(generate_sentence(beg, mid, end))
    reply = '\n'.join(tokens)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(content_types=['text'])
def parse_message(message: telebot.types.Message):
    text = message.text
    if not text:
        return
    
    sentences = split_into_sentences(text)
    for i in sentences:
        if not i:
            continue
        
        tokens = get_rid_of_litter(i).split()
        if len(tokens) < 2:
            continue

        if tokens[0] not in beg.keys():
            beg[tokens[0]] = set()
        beg[tokens[0]].add(tokens[1])

        for j in range(1, len(tokens) - 1):
            if tokens[j-1] not in mid.keys():
                mid[tokens[j-1]] = set()
            mid[tokens[j-1]].add(tokens[j])
        
        if tokens[-2] not in end.keys():
            end[tokens[-2]] = set()
        end[tokens[-2]].add(tokens[-1])
    write_all_data(beg, mid, end)


bot.infinity_polling()