# Hunger-Free-Society
Telegram bot built using python-telegram-bot that links people with leftovers to those who need the food


## Getting Started
1. Create a Telegram bot using the command /newbot with [BotFather](https://t.me/botfather). Get the API key of your bot.
<!-- ![alt text](https://miro.medium.com/max/1266/1*XxKPtfrohg3GX5Sq18w-NA.png "Chat with BotFather") -->
2. Create a Telegram channel.
3. Download the three files in this repo: bot.py (containing your python code for the Telegram bot), requirements.txt (containing the python libraries to be installed), and Procfile (containing the command to execute the python file).
4. Modify the line in the bot.py file `'TOKEN = 'YOURTELEGRAMBOTTOKEN'` to the API key of your bot, and the `chat_id = 'YOURTELEGRAMCHANNEL'` to the link of your Telegram channel.
5. Set up the Google Maps API:
  1. Go to the Google Cloud Platform [console](https://console.cloud.google.com/)
  2. Search for API & Services in the search bar.
  3. Click on the blue plus button saying ENABLE APIS AND SERVICES right below the search bar.
  4. Search for Geocoding API and enable it.
  5. Under API & Services, go to Credentials and select CREATE CREDENTIALS > API key.
6. Modify the line in the bot.py file `GMAPSAPI = 'YOURGOOGLEMAPSAPITOKEN'` to your Google Maps API.
7. Follow the steps [here](https://github.com/liuhh02/python-telegram-bot-heroku) to set up an account and an app on Heroku.
8. You're done! Send `/start` to your bot and it should respond with the following message:
> Hi! I am your posting assistant to help you advertise your leftover food to reduce food waste. To start, please type the location of the leftover food.

## My Implementation
