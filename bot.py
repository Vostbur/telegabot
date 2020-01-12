# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 2020
@author: vostbur@gmail.com
"""
import re
import sqlite3
import os
import telebot

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"))
USER_ID = int(os.environ.get('TELEGRAM_ID'))

prompt = """/start, /help - this help
/add TASK_NAME - append a new task
/del TASK_NAME - delete a task by the full name or part of the task name
/list - show all active tasks"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global prompt
    bot.reply_to(message, prompt)

@bot.message_handler(content_types=['text'])
def todo(message):
    global USER_ID, prompt
    if message.from_user.id == USER_ID:
        db_filename = "dbase.db"
        db_exists = os.path.exists(db_filename)
        
        query_schema = "create table if not exists tasks(\
                         name text not NULL primary key)"
        query_select = "select * from tasks"
        query_insert = "insert into tasks (name) values (?)"
        query_delete = "delete from tasks where name = (?)"
        
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        if not db_exists:
            conn.execute(query_schema)
        
        pattern = re.compile(r"/\w+")
        
        def list_tasks(cur):
            cur.execute(query_select) 
            return cur.fetchall()   
            
        tasks = list_tasks(cursor)
        
        text = message.text
        match = pattern.search(text)
        command = match[0] if match else ""
        text = pattern.sub("", text).strip()
    
        if command == "/add":
            with conn:
                try:
                    conn.execute(query_insert, (text,))
                    tasks.append((text,))
                except sqlite3.IntegrityError:
                    bot.send_message(message.chat.id, "Task '{text}' already exists.")
        
        elif command == "/list":
            for i in tasks:
                bot.send_message(message.chat.id, "".join(list(i)))
        
        elif command == "/del":
            tmp_set = [i for i in tasks if text in i[0]]
            if tmp_set:
                if len(tmp_set) > 1:
                    bot.send_message(message.chat.id, "Exits simular tasks:" + \
                                     "; ".join([i[0] for i in tmp_set]))
                else:
                    with conn:
                        conn.execute(query_delete, tmp_set[0])
                        tasks.remove(tmp_set[0])
            else:
                bot.send_message(message.chat.id, "Task not found")
    
        else:
            bot.send_message(message.chat.id, prompt)
        
        conn.close()

bot.polling()     