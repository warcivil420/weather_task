import telebot
import owmrequest as req
bot = telebot.TeleBot('1331637578:AAGuUhHFAL9DiyDmGU8eh6CE7k_7XGnQVVs')

date = [i.split(" ")[0] for i in req.weather_str]

print(date[0])

@bot.message_handler(commands=['start'])
def start(message):
	send_mess = req.TelegramInformation() + "\n" + f"<b>Привет {message.from_user.first_name} </b>! \n напиши сюда числа в формате ХХХХ-ХХ-ХХ, например 2020-07-24 мы знаем погоду в дате от {str(date[0])} до {str(date[len(date)-1])} "
	bot.send_message(message.chat.id, send_mess, parse_mode = 'html')


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text in date: 
        for received_date in range(len(date)):
            if(message.text.replace(' ', '') == date[received_date]):
                bot.send_message(message.chat.id, req.weather_str[received_date])
    else:
        bot.send_message(message.chat.id, f"напиши сюда числа в формате ХХХХ-ХХ-ХХ, например 2020-07-24 я могу  показать прогноз погоды с {date[0]} до {str(date[len(date)-1])}")
bot.polling(none_stop=True)	
