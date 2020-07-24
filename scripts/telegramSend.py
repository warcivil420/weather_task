import telebot
import owmrequest as req
bot = telebot.TeleBot('1331637578:AAGuUhHFAL9DiyDmGU8eh6CE7k_7XGnQVVs')
date = []

for i in req.weather_str:
	date.append(i.split(" ")[0])

print(date[0])
@bot.message_handler(commands=['start'])
def start(message):
	send_mess = f"<b>Привет {message.from_user.first_name} </b>! \n напиши сюда числа в формате ХХХХ-ХХ-ХХ, например 2020-07-24 мы знаем погоду в дате от {str(date[0])} до {str(date[len(date)-1])} " 
	bot.send_message(message.chat.id, send_mess, parse_mode = 'html')


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.text in date: 
        for i in range(len(date)-1):
            if(message.text in date[i]):
                bot.send_message(message.chat.id, req.weather_str[i])
    else:
        bot.send_message(message.chat.id, 'Прости друг я тебя не понимаю')


bot.polling(none_stop=True)	
