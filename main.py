#!/usr/bin/env python3
"""main.py: a sorting game for your brain to enjoy!"""
__author__ = "Sameh Abouelsaad"
__copyright__ = "Copyright 2021"
__credits__ = []
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Sameh Abouelsaad"
__email__ = "samehabouelsaad@gmail.com"
__status__ = "Development"

import random
from tkinter import StringVar, Tk, Button, messagebox, Label, IntVar
from tkinter.constants import ANCHOR

# you can configure the numbers of blocks and the time limit
COLUMNS = 5
ROWS = 5
TIME = 120
# you can configure the fonts used in the game
NUMBER_FONT_TUPLE = ("Comic Sans MS", 40, "bold")
TIME_FONT_TUPLE = ("Courier", 20, "bold")

def gameover():
    messagebox.showinfo("Sorry!", f"we got a loser!")
    mainWindow.destroy()

def show_help(*_):
    messagebox.showinfo("Help", 
    "The Rules:\n1- Press the visible number to start the game\n2- Hover over the blocks to discover the numbers\n3- Press the numbers in ascending order to won\n4- You should clear all blocks before you ran out of time or lives\n5- share a screen shot with your time if you can win :D")
    mainWindow.unbind('<Enter>')

def update_remain_time(*_):
    global timer_id
    remaining = remain_time.get()
    if remaining == 0:
        gameover()
    remain_time.set(remaining - 1)
    timer_id = mainWindow.after(1000, update_remain_time)

def check_order(ev=None):
    global game_started
    if not game_started:
        game_started = True
        for button in buttons:
            button.config(activeforeground='black', activebackground='white', fg='grey', bg='grey')
        mainWindow.after(1000, update_remain_time)
    pressed_number = int(ev.widget["text"])
    if sorted_list[-1] == pressed_number:
        ev.widget.config(state="disabled")
        sorted_list.pop()
        if len(sorted_list) == 0:
            mainWindow.after_cancel(timer_id)
            messagebox.showinfo("Congrats!", f"You won!\nyou took {TIME - remain_time.get()} sec to order {COLUMNS * ROWS} numbers!")
            mainWindow.destroy()

    else:
        lives_remaining = lives.get()
        if len(lives_remaining) > 2:
            lives.set(lives_remaining[:-2])
        else:
            lives.set(lives.get()[:-2])
            mainWindow.after_cancel(timer_id)
            gameover()

def create_game_gui():
    index = 0
    for x in range(ROWS):
        for y in range(COLUMNS):
            button = Button(mainWindow, text=str(number_list[index]), width=5)
            if not number_list[index] == sorted_list[-1]:
                button.config(activeforeground='white', activebackground='white', fg='grey', bg='grey')
            button.config(font=NUMBER_FONT_TUPLE)
            button.grid(row=x, column=y)
            buttons.append(button)
            index += 1

    label1 = Label(mainWindow, text='⏱', font=TIME_FONT_TUPLE, height=2)
    label1.grid(row=ROWS, column=0, pady=10)

    label2 = Label(mainWindow, textvariable=remain_time, font=TIME_FONT_TUPLE)
    label2.grid(row=ROWS, column=1, pady=10, sticky='w')

    label3 = Label(mainWindow, textvariable=lives, font=NUMBER_FONT_TUPLE, fg='red')
    label3.grid(row=ROWS, column=COLUMNS-1, pady=10)

    for button in buttons:
        button.bind("<Button-1>", check_order)

if __name__ == '__main__':
    number_list = random.sample(range(999), COLUMNS*ROWS)
    sorted_list = sorted(number_list, reverse=True)

    game_started = False
    timer_id = None
    buttons = []

    mainWindow = Tk()
    mainWindow.title("Sorting Game")

    remain_time = IntVar(value=TIME)
    lives = StringVar(value='❤️❤️❤️')

    create_game_gui()
    mainWindow.bind('<Enter>', show_help)
    
    mainWindow.mainloop()
