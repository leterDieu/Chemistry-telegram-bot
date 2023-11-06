from binary_cacl import wrap_table, get_element, does_compound_exist
from requests import post
import time
import telepot
# from background import keep_alive


tg_bot_token = 'your_tg_bot_token'
url_template = 'https://api.telegram.org/bot{token}/{method}'
bot = telepot.Bot(tg_bot_token)

url = url_template.format(token=tg_bot_token, method="setMyCommands")
commands = [{'command': '/binary', 'description': 'calculate binary compound.'},
            {'command': '/existence', 'description': 'does formula exist.'},
            {'command': '/element', 'description': 'get element properties by its symbol'}]
post(url, json={'commands': commands})

try:
    start = bot.getUpdates()[-1]['update_id']
except Exception:
    start = 0


def user_ids():
    global start
    response = bot.getUpdates(offset=start + 1)

    if len(response):
        start = response[-1]['update_id']
        data = []
        for mes in response:
            try:
                data.append([
                    mes['message']['chat']['id'],
                    mes['message']['chat']['first_name'],
                    mes['message']['text'], mes['message']['date']
                ])
            except Exception:
                pass

        return data

    return []


# keep_alive()
while True:
    time.sleep(1)

    ui = user_ids()
    for id_, name_, text_, date_ in ui:
        try:

            if '/start' in text_:
                bot.sendMessage(
                    id_,
                    text=
                    f'''Hello, {name_}.\n
                    Consider reading this project's repo: https://github.com/leterDieu/Chemistry-telegram-bot\n
                    Enjoy your session.'''
                )

            if '/binary' in text_:
                try:
                    args_from_text = text_.split()
                    limit1, limit2 = 60, 60
                    if len(args_from_text) > 3:
                        limit1 = int(args_from_text[3])
                    if len(args_from_text) > 4:
                        limit2 = int(args_from_text[4])
                    bot.sendMessage(id_, text=wrap_table(args_from_text[1], float(args_from_text[2]), limit1, limit2))
                except Exception:
                    bot.sendMessage(id_, text='Incorrect input.')

            elif '/existence' in text_:
                try:
                    check_response = does_compound_exist(text_.split()[1])
                    if not check_response[0]:
                        bot.sendMessage(id_, text=check_response[1])
                    else:
                        bot.sendMessage(id_, text=f'True. Hill notation: {check_response[1]}.')
                except Exception:
                    bot.sendMessage(id_, text='Incorrect input.')

            elif '/element' in text_:
                try:
                    bot.sendMessage(id_, text=get_element(text_.split()[1])[1])
                except Exception:
                    bot.sendMessage(id_, text='Incorrect input.')

        except Exception:
            pass
