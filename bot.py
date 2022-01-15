import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from googlemaps import Client as GoogleMaps
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

LOCATION, PHOTO, DIET, SERVINGS, TIME, CONFIRMATION = range(6)

reply_keyboard = [['Confirm', 'Restart']]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
TOKEN = '5085490474:AAGTfpRP-tU0rIDZ_oeuJU2dJeczVaraK24'
bot = telegram.Bot(token=TOKEN)
chat_id = 'https://t.me/hungerfreesociety'
GMAPSAPI = 'AIzaSyBoKTxJ_rIbsoGIWv1FlPiloAbhGSN0dl4'
gmaps = GoogleMaps(GMAPSAPI)

PORT = int(os.environ.get('PORT', 5000))

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    update.message.reply_text(
        'Hi Volunteers! Welcome to Hunger Free Society,'
        '\n We as a community, try to help you and the society by making your unused leftovers accessible to the needy, ensuring that no person around us sleeps empty stomach. If you are a willing person wanting to contribute towards making the society a better place for all, join us https://t.me/hungerfreesociety '
        '\n To start donating, please type the location of the food that you want to donate')
    return LOCATION


def location(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'Location'
    text = update.message.text
    user_data[category] = text
    logger.info("Location of %s: %s", user.first_name, update.message.text)

    update.message.reply_text('We see! Please send a photo of the leftovers, '
                              'so users will know how the food looks like, or send /skip if you don\'t want to.')
    return PHOTO


def photo(update, context):
    user = update.message.from_user
    user_data = context.user_data
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    category = 'Photo Provided'
    user_data[category] = 'Yes'
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Lovely! Is the food Vegetarian? Non-Vegeterian? Vegan?'
    '\n Please type in the dietary specifications of the food.')

    return DIET


def skip_photo(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'Photo Provided'
    user_data[category] = 'No'
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('Lovely! Is the food Vegetarian? Non-Vegeterian? Vegan?'
    '\n Please type in the dietary specifications of the food.')

    return DIET


def diet(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'Dietary Specifications'
    text = update.message.text
    user_data[category] = text
    logger.info("Dietary Specification of food: %s", update.message.text)
    update.message.reply_text('How many servings are there?')

    return SERVINGS

def servings(update, context):
    user = update.message.from_user
    user_data = context.user_data
    category = 'Number of Servings'
    text = update.message.text
    user_data[category] = text
    logger.info("Number of servings: %s", update.message.text)
    update.message.reply_text('What time will the food be available until?')

    return TIME
    
def time(update, context):
	user = update.message.from_user
	user_data = context.user_data
	category = 'Time to Take Food By'
	text = update.message.text
	user_data[category] = text
	logger.info("Time to Take Food By: %s", update.message.text)
	update.message.reply_text("Thank you for providing the information to Hunger Free Society! Kindly check if the information is correct:"
								"{}".format(facts_to_str(user_data)), reply_markup=markup)

	return CONFIRMATION

def confirmation(update, context):
    user_data = context.user_data
    user = update.message.from_user
    update.message.reply_text("Thank you for visiting Hunger Free Society! \n We will post the information on the channel @" + chat_id + "  now.", reply_markup=ReplyKeyboardRemove())
    if (user_data['Photo Provided'] == 'Yes'):
        del user_data['Photo Provided']
        bot.send_photo(chat_id=chat_id, photo=open('user_photo.jpg', 'rb'), 
		caption="<b>Food is Available!</b> Check the details below: \n {}".format(facts_to_str(user_data)) +
		"\n For more information, message the poster {}".format(user.name), parse_mode=telegram.ParseMode.HTML)
    else:
        del user_data['Photo Provided']
        bot.sendMessage(chat_id=chat_id, 
            text="<b>Food is Available!</b> Check the details below: \n {}".format(facts_to_str(user_data)) +
        "\n For more information, message the poster {}".format(user.name), parse_mode=telegram.ParseMode.HTML)
    geocode_result = gmaps.geocode(user_data['Location'])
    lat = geocode_result[0]['geometry']['location'] ['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    bot.send_location(chat_id=chat_id, latitude=lat, longitude=lng)

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! Hope you had a great experience to join the community as volunteer kindly click on this link, https://t.me/hungerfreesociety  .',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states LOCATION, PHOTO, DIET, SERVINGS, TIME, CONFIRMATION
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            LOCATION: [CommandHandler('start', start), MessageHandler(Filters.text, location)],

            PHOTO: [CommandHandler('start', start), MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            DIET: [CommandHandler('start', start), MessageHandler(Filters.text, diet)],

            SERVINGS: [CommandHandler('start', start), MessageHandler(Filters.text, servings)],

            TIME: [CommandHandler('start', start), MessageHandler(Filters.text, time)],

            CONFIRMATION: [MessageHandler(Filters.regex('^Confirm$'),
                                      confirmation),
            MessageHandler(Filters.regex('^Restart$'),
                                      start)
                       ]

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('https://limitless-cove-52084.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
