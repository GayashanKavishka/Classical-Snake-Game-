import threading
from tkinter import *
import winsound
import random
import pygame
from tkinter import font as tkFont, font
import time

GAME_WIDTH = 1000
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOUR = "#000000"

score = 0
direction = "down"


def play_song(song_file, volume):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play(loops=-1)


class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, canvas):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food, window, canvas, label, high_score):
    global score
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score:{}   High Score:{}".format(score, high_score))
        winsound.PlaySound("music_food.wav", winsound.SND_FILENAME)

        global SPEED
        SPEED -= 2

        canvas.delete("food")
        food = Food(canvas)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over(window, canvas, label)
    else:
        window.after(SPEED, next_turn, snake, food, window, canvas, label, high_score)


def file_read():
    try:
        f = open("score.txt", 'r')
        a = f.read()
        f.close()
        return int(a)
    except FileNotFoundError:
        return 0


def file_write(score):
    f = open("score.txt", 'w')
    f.write(str(score))
    f.close()


def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction
    # winsound.PlaySound("music_move.wav", winsound.SND_FILENAME)


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def stop_song():
    pygame.mixer.music.stop()


def game_over(window, canvas, label):
    stop_song()
    canvas.delete(ALL)
    winsound.PlaySound("music_gameover.wav", winsound.SND_FILENAME)
    canvas.create_text(GAME_WIDTH / 2, 100, font=("consolas", 70), text="GAME OVER !", fill="red", tag="gameover")

    button3 = Button(window, text="PLAY AGAIN", command=lambda: f("PLAY AGAIN", window, canvas, label),
                     width=30, height=5, bg="lightblue", fg="black", font=custom_font,
                     activebackground="blue", activeforeground="yellow", relief="raised")
    button4 = Button(window, text="QUIT", command=lambda: f("QUIT", window, canvas, label), width=30, height=5,
                     bg="lightblue", fg="black", font=custom_font, activebackground="blue", activeforeground="yellow",
                     relief="raised")
    canvas.create_window(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50, window=button3)
    canvas.create_window(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50, window=button4)

    high_score = file_read()
    if score > high_score:
        file_write(score)


def start_game(window):
    global score
    score = 0
    high_score = file_read()

    song_thread = threading.Thread(target=play_song, args=("music_music.wav", 0.2))
    song_thread.start()

    label = Label(window, text="Score:{}   High Score:{}".format(score, high_score), font=("consolas", 40))
    label.pack(anchor=W, side=TOP, padx=50, pady=10)

    canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    window.update()

    window_height = window.winfo_height()
    window_width = window.winfo_width()
    screen_height = window.winfo_screenheight()
    screen_width = window.winfo_screenwidth()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind("<Left>", lambda event: change_direction("left"))
    window.bind("<Right>", lambda event: change_direction("right"))
    window.bind("<Up>", lambda event: change_direction("up"))
    window.bind("<Down>", lambda event: change_direction("down"))

    snake = Snake(canvas)
    food = Food(canvas)

    next_turn(snake, food, window, canvas, label, high_score)


def f(action, window, canvas, label):
    if action == "PLAY" or action == "PLAY AGAIN":
        stop_song()
        label.destroy()
        canvas.destroy()
        start_game(window)
    else:
        window.destroy()


window = Tk()
window.title("Snake game")
window.resizable(False, False)
window.iconbitmap("unnamed.ico")

bold_font = font.Font(family="Helvetica", size=40, weight="bold")
custom_font = tkFont.Font(family="Arial", size=10)

label = Label(window, text="CLASSIC SNAKE GAME", font=bold_font, justify="center")
label.pack(side=TOP, padx=70, pady=10)

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

button1 = Button(window, text="PLAY", command=lambda: f("PLAY", window, canvas, label), width=30, height=5,
                 bg="lightblue", fg="black", font=custom_font, activebackground="blue", activeforeground="yellow",
                 relief="raised")

button2 = Button(window, text="QUIT", command=lambda: f("QUIT", window, canvas, label), width=30, height=5,
                 bg="lightblue", fg="black", font=custom_font, activebackground="blue", activeforeground="yellow",
                 relief="raised")

canvas.create_window(500, 250, window=button1)
canvas.create_window(500, 400, window=button2)

window.mainloop()
