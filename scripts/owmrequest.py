import requests


def get_string_telegram(JsonFile):  # декоратор возврата строки из апи функции
    def api_string_for_telegram(*args, **kwargs):
        weather = []
        date = JsonFile()
        for i in date['list']:
            weather.append(str(i['dt_txt'][:16]) + " " + '\n' + "Влажность " + str(i['main']['humidity']) + "%" + '\n'
                           + "Давление " + str(i['main']['pressure']) + " мм рт. ст. " + '\n' +
                           "Температура " + "+" +
                           str(round(i['main']['temp'])) + " " + '\n'
                           + "Скорость ветра " +
                           str(i['wind']['speed']) + " " + "м/c"
                           + " " +
                           str(get_wind_direction(i['wind']['deg'])) + '\n'
                           + str(i['weather'][0]['description']) +
                           '\n' + "Вероятность осадков "
                           + str(i['pop']) + "%")
        return weather
    return api_string_for_telegram

# Определяет с какой стороны летит ветер


def get_wind_direction(deg) -> str:
    l = ['С ', 'СВ', ' В', 'ЮВ', 'Ю ', 'ЮЗ', ' З', 'СЗ']
    for i in range(0, 8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res

# Проверка наличия в базе информации о нужном населенном пункте (опциональное использование)


def get_city_id(s_city_name) -> int:
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
        pass
    assert isinstance(city_id, int)
    return city_id

# Запрос текущей погоды (вывод в консоль для дебага)


def request_current_weather(city_id) -> None:
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])
        print("data:", data)
    except Exception as e:
        print("Exception (weather):", e)
        pass

# Прогноз


def TelegramInformation(city_id=468902) -> str:
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                       params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    return 'city: ' + data['city']['name'] + "\n" + data['city']['country']

# получение json в функции и обработка строки json в декораторе


@get_string_telegram
def request_forecast(city_id=468902) -> str:
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print('city:', data['city']['name'], data['city']['country'])
    except Exception as e:
        print("Exception (forecast):", e)
        data = None
    return data


# city_id for Yaroslavl
city_id = 468902
appid = "dca30b363934f02b817e916cb61ab3f3"   # OpenWeatherMap API

weather_str = request_forecast(city_id)
print("Все работает")
