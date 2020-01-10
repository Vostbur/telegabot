# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 21:03:23 2020

@author: vostbur@gmail.com
"""

import telebot

bot = telebot.TeleBot("966825665:AAGA4x8809nk8NFnBfd6yGjCJ5-u83wSs-o")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()
     