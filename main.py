from other.utils import get_response, create_buttons, get_request


def handler(event, context):
    """Main function."""
    end_session = 'false'  # По умолчанию.
    text = 'Привет! Я могу подсказать тебе, что надеть на улицу. Начнём?'  # Текст для пользователя.
    tts = f'<speaker audio="alice-sounds-nature-forest-1.opus"> {text}'  # Звук.
    text_by_user = event['request']['original_utterance']
    buttons = create_buttons(['Начнем', True], ['Что ты умеешь?', True])

    agreed, text_by_user, city_was_called, gender_was_called, weather, buttons, text, city, gender, end_session, c, tts = get_request(
        event, text_by_user, text, buttons, end_session, tts)

    return get_response(event, text, agreed, city_was_called, city, gender_was_called, gender, weather, buttons,
                        end_session, tts, c)
