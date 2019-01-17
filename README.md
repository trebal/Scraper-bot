# scraper-bot
This basic project consists in a python web scraper combined with a python telegram bot. The first gets the information and the bot shows to the users. It is made to scrape the title and description of the daily free book from packtpub.

To use this program, you will need the modules "urllib2" and "bs4" for the scraper, and the "schedule" for the bot.
To change the deliver time of the bot, change the variable "deliver_time" (line 22) from the file "trebal_bot.py".
Do not forget to change the value of the variable "token" (line 20) from the file "trebal_bot.py" in order to use your own bot.
You will need your own token to run it. You can obtain it from the BotFather in Telegram.

To run it, just put the bot and the scraper in the same folder. Execute in a terminal "python trebal_bot.py" and it will run automatically. The scraper is called from the bot, but it can also be executed to obtain the data. The scraper also runs without arguments, and downloads the information into a file called "book_data".
