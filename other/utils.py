from weather.get_info import get_city_coords, get_weather
from recommendations.main import get_rec


def get_response(event, text, agreed, city_was_called, city, gender_was_called, gender, weather, buttons, end_session,
                 tts, c):
    """Выдает ответ для пользователя."""
    response = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'tts': tts,
            'end_session': end_session,
            'buttons': buttons,
        },
        "session_state": {
            "agreed": agreed,
            "city_was_called": city_was_called,
            "city": city,
            'gender_was_called': gender_was_called,
            'gender': gender,
            'weather': weather,
            'count': c
        }
    }
    return response


def create_buttons(*args: list):
    """Функция, которая создает кнопки."""
    buttons = []
    for button in args:
        buttons.append({'title': button[0], 'hide': button[1]})
    return buttons


def get_ping_response(event, text):
    """Ping."""
    response = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
        },
    }
    return response


def check_var(event):
    if 'agreed' in event['state']['session']:
        agreed = event['state']['session']['agreed']
    else:
        agreed = False

    if 'city_was_called' in event['state']['session']:
        city_was_called = event['state']['session']['city_was_called']
    else:
        city_was_called = False

    if 'city' in event['state']['session']:
        city = event['state']['session']['city']
    else:
        city = None

    if 'gender_was_called' in event['state']['session']:
        gender_was_called = event['state']['session']['gender_was_called']
    else:
        gender_was_called = False

    if 'gender' in event['state']['session']:
        gender = event['state']['session']['gender']
    else:
        gender = None

    if 'weather' in event['state']['session']:
        weather = event['state']['session']['weather']
    else:
        weather = {}

    if 'count' in event['state']['session']:
        c = event['state']['session']['count']
    else:
        c = 0
    return agreed, city_was_called, city, gender_was_called, gender, weather, c


def get_request(event, text_by_user, text, buttons, end_session, tts):
    """Получает запрос от пользователя."""
    agreed, city_was_called, city, gender_was_called, gender, weather, c = check_var(event)

    if 'request' in event and 'original_utterance' in event['request'] and len(
            event['request']['original_utterance']) > 0:
        buttons = []
        if 'YANDEX.WHAT_CAN_YOU_DO' in event['request']['nlu']['intents']:
            text = 'Я умею подсказывать одежду, которую вы можете надеть на улицу. Чтобы начать, просто скажите мне, ' \
                   'готовы вы или нет.'
            buttons = create_buttons(['Готов', True], ['Не готов', True])
            agreed, city_was_called, city, gender_was_called, gender, weather, c = False, False, None, False, None, {}, 0
        elif not agreed:
            if text_by_user == "ping":
                text = 'ок'
                return get_ping_response(event, text)
            elif 'YANDEX.WHAT_CAN_YOU_DO' in event['request']['nlu']['intents']:
                text = 'Я умею подсказывать одежду, которую вы можете надеть на улицу. Чтобы начать, просто скажите мне, ' \
                       'готовы вы или нет.'
                buttons = create_buttons(['Готов', True], ['Не готов', True])
                c = 0
            elif 'YANDEX.HELP' in event['request']['nlu']['intents']:
                text = 'Если вы хотите получить рекомендации, просто скажите да.'
                buttons = create_buttons(['Да', True], ['Нет', True])
                c = 0
            elif 'YANDEX.CONFIRM' in event['request']['nlu']['intents']:
                text = 'Хорошо, тогда назовите свой город.'
                agreed = True
                c = 0
            elif 'YANDEX.REJECT' in event['request']['nlu']['intents']:
                text = 'Очень жаль, жду вас в другой раз.'
                end_session = 'true'
                c = 0
            else:
                if c == 0:
                    text = 'Не совсем вас поняла, вы готовы или нет?'
                    buttons = create_buttons(['Да', True], ['Нет', True])
                    c += 1
                elif c == 1:
                    text = 'Извините, я снова ничего не поняла. Вы всегда можете попросить помощи, если она требуется.'
                    buttons = create_buttons(['Помоги', True])
                    c += 1
                elif c == 2:
                    text = 'Я опять вас не понимаю. Если вы хотите получить рекомендации, просто скажите да.'
                    buttons = create_buttons(['Да', True], ['Нет', True])
        elif not city_was_called:
            lat, lon = get_city_coords(text_by_user)
            weather = get_weather(lat, lon)
            if 'YANDEX.HELP' in event['request']['nlu']['intents']:
                weather = {}
                text = 'Похоже вы застряли. Просто корректно назовите свой город, чтобы продолжить.'
                c = 0
            elif get_weather(lat, lon) is not None and len(text_by_user) > 2:
                city_was_called = True
                city = text_by_user.capitalize()
                text = 'Теперь скажите мужчина вы или женщина.'
                buttons = create_buttons(['Мужчина', True], ['Женщина', True])
                c = 0
            else:
                weather = {}
                if c == 0:
                    text = 'Простите я вас не понимаю.'
                    c += 1
                elif c == 1:
                    text = 'Похоже вы назвали не город, или такого города не существует. Вы всегда можете обратиться ко мне за помощью.'
                    buttons = create_buttons(['Помоги', True])
                    c += 1
                elif c == 2:
                    text = 'Я снова вас не понимаю. Просто корректно назовите свой город, чтобы продолжить.'
        elif not gender_was_called:
            if 'YANDEX.HELP' in event['request']['nlu']['intents']:
                text = 'Похоже вы застряли. Просто скажите кто вы, мужчина или женщина.'
                buttons = create_buttons(['Мужчина', True], ['Женщина', True])
                c = 0
            elif text_by_user.lower() in ['мужчина', 'женщина']:
                gender_was_called = True
                gender = text_by_user.capitalize()
                text = get_rec(weather.get('temp'), city.lower().capitalize(), gender)
                buttons = create_buttons(['Да', True], ['Нет', True])
                c = 0
            else:
                if c == 0:
                    text = 'Извините, я вас не поняла. Скажите точно, мужчина вы или женщина.'
                    buttons = create_buttons(['Мужчина', True], ['Женщина', True])
                    c += 1
                elif c == 1:
                    text = 'Я снова вас не понимаю. Может вам нужна помощь?'
                    buttons = create_buttons(['Помоги', True])
                    c += 1
                elif c == 2:
                    text = 'Похоже вы застряли. Просто скажите кто вы, мужчина или женщина.'
                    buttons = create_buttons(['Мужчина', True], ['Женщина', True])
        elif gender_was_called:
            if 'YANDEX.HELP' in event['request']['nlu']['intents']:
                text = 'Если вы хотите получить ещё рекомендации, просто скажите да. А если вы хотите, чтобы программа завершилась, скажите нет.'
                buttons = create_buttons(['Да', True], ['Нет', True])
                c = 0
            elif 'YANDEX.CONFIRM' in event['request']['nlu']['intents']:
                text = 'Хорошо, тогда назовите свой город.'
                city_was_called = False
                city = None
                gender_was_called = False
                gender = None
                weather = {}
                c = 0
            elif 'YANDEX.REJECT' in event['request']['nlu']['intents']:
                text = 'Очень жаль, жду вас в другой раз.'
                end_session = 'true'
                c = 0
            else:
                text = 'Извините, я вас не поняла, если вам нужна помощь, вы всегда можете попросить.'
                buttons = create_buttons(['Помоги', True])
        tts = f'<speaker audio="alice-sounds-game-ping-1.opus"> {text}'

    return agreed, text_by_user, city_was_called, gender_was_called, weather, buttons, text, city, gender, end_session, c, tts
