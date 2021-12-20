
import os, requests, uuid, json

# Не забудьте заменить своим ключом значение subscription_key! 
subscription_key = 'b3825972b6f24045bb7a74e9b6efa6f5' #7a2387d7-ca29-47dc-a4c6-143a60c8e568
location = 'northeurope' #   http://127.0.0.1:5000/
# Не забудьте заменить своим местоположением значение location!
# Наш маршрут Flask поставит два аргумента: text_input и language_output.
# При нажатии кнопки перевода текста в приложении Flask запрос Ajax возьмет эти значения из нашего веб-приложения и будет использовать их в запросе.
def get_translation(text_input, language_output):
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + language_output
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # В теле можно передать несколько объектов.
    body = [{
        'text' : text_input
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()
