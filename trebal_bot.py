#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileenconding=utf8 :

"""This bot is made to notify users about the daily book from packtpub.
It uses the data scraped by the scraper, which stores it in a text file.
The bot can answer to certain commands, which are defined in the functions."""

import schedule

import time

import telegram

import os

from telegram.ext import Updater, CommandHandler

# The bot token
token = "Your token here. You can obtain a token using the @BotFather."
# Time when the message will be broadcasted.
deliver_time = "10:00"

# Strings that store the message for each command.
m_start = "Welcome to Trebal's daily book bot. This bot is made to "\
"notify you everyday about the free daily book from PacktPub.\n"\
"You can use the command /book to get the information of today's book."\
"Use /help to know all the available commands."

m_about = "This bot has been created by *Ramon de Llano Chamorro*, from "\
"Universitat de Lleida, as a learning assignment.\n▫️_Version: 1.2\nAdded "\
"new commands: subs, help, debug and bcastbook._"

m_help = "You can use the following commands:\n"\
"/start : Initializes the bot and welcomes you.\n"\
"/book : Displays the daily book.\n"\
"/subs : Displays the number of users using the bot.\n"

# This list stores all the users that use the bot.
user_id = []

# ==================== USER FUNCTIONS ==========================================
def start(bot, update, pass_chat_data=True):
    """The default start command, used in most bots. It welcomes the user and
    guides him to the usage of the bot."""

    uid = update.message.chat_id
    bot.sendMessage(chat_id=uid, text=m_start)

    add_user(uid)

def help(bot, update):
    """Displays the standard commands."""

    bot.sendMessage(chat_id=update.message.chat_id, text=m_help,
                    parse_mode=telegram.ParseMode.MARKDOWN)

def about(bot, update):
    """The about command is used to display the information of the bot."""

    bot.sendMessage(chat_id=update.message.chat_id, text=m_about,
                    parse_mode=telegram.ParseMode.MARKDOWN)

def book(bot, update):
    """The main command, used to get the information of the book, previously
    retrieved from the scraper."""

    message = get_book_data()

    bot.sendMessage(chat_id=update.message.chat_id, text=message,
                    parse_mode=telegram.ParseMode.MARKDOWN)

def subs(bot, update):
    """Displays the number of the bot users."""

    message = "Total users: " + str(len(user_id))
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

# ==================== ADMIN FUNCTIONS =========================================
def scrape(bot, update):
    """Scrapes the data from the web, calling the scraper."""

    # Calls the scraper from the host terminal.
    os.system("python scraper.py")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Data scraped successfully",
                    parse_mode=telegram.ParseMode.MARKDOWN)

def bcast_book(bot, update):
    """Broadcasts the daily book"""

    broadcast(get_book_data())

def debug(bot, update):
    """A wildcard function that is used to print information during the
    development of the program, which vary over the time."""

    message = "User ID: " + str(user_id[0])
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

    bot.sendMessage(chat_id=update.message.chat_id, text=message,
                    parse_mode=telegram.ParseMode.MARKDOWN)

# ==================== OTHER FUNCTIONS =========================================
def broadcast(message):
    """Broadcasts a message to all bot users."""

    bot = telegram.Bot(token)

    for uid in user_id:
        bot.sendMessage(chat_id=uid, text=message,
                        parse_mode=telegram.ParseMode.MARKDOWN)

def get_book_data():
    """Reads the information stored in book_data.txt and returns a string to
    be used as a message."""

    r_file = open("book_data.txt", "r")
    title = r_file.readline() + "\n"
    description = r_file.readline() + "\n"
    r_file.close()

    header = "*Today's book (" + time.strftime("%d/%m/%Y") + ")*\n"
    message = header + title + description

    return message

def add_user(uid):
    """Adds a user to the user database if not there."""

    if uid not in user_id:
        user_id.append(uid)

def job():
    """Schedule valid function for the scheduler, which broadcasts the book."""

    os.system("python scraper.py")
    print("Data retrieved.")

    broadcast(get_book_data())
    print("Broadcast delivered.")

def main():
    """Main."""

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))
    dispatcher.add_handler(CommandHandler("book", book))
    dispatcher.add_handler(CommandHandler("subs", subs))

    dispatcher.add_handler(CommandHandler("scrape", scrape))
    dispatcher.add_handler(CommandHandler("bcast_book", bcast_book))
    dispatcher.add_handler(CommandHandler("debug", debug))

    updater.start_polling()

    # Declaration of the schedule
    schedule.every().day.at(deliver_time).do(job)

    while True:
        schedule.run_pending()
        # The sleep prevents the CPU to work unnecessarily.
        time.sleep(1)

if __name__ == "__main__":
    main()
