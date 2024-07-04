import threading
from tkinter import *
import winsound
import random
import pygame
from tkinter import font as tkFont, font
import time



GAME_WIDTH = 1000
GAME_HEIGHT = 600
SPEED = 150
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "blue"
FOOD_COLOR = "yellow"
BACKGROUND_COLOUR = "#000000"

score = 0
direction = "down"


def play_song(song_file,volume):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play(loops=-1)

class Snake :
    def __init__(self,canvas):
        self.body_size = BODY_PARTS
        self.cordinates = []
        self.squares = []

        for i in range(0,BODY_PARTS):
            self.cordinates.append([0,0])

        for x,y in self.cordinates:
            square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR,tag = "sanke")
            self.squares.append(square)



class Food:
    def __init__(self,canvas):

        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x,y]

        canvas.create_oval(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill = FOOD_COLOR,tag = "food")






def next_turn(snake,food,window,canvas,labal,sc):
    x,y = snake.cordinates[0]
    global score
    if direction == "up":
       y -= SPACE_SIZE
    elif direction == "down":
       y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    snake.cordinates.insert(0,(x,y))

    square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill = SNAKE_COLOR)
    snake.squares.insert(0,square)

    if(x == food.coordinates[0] and y == food.coordinates[1]):

        global score
        score += 1
        labal.config(text="Score:{}   High Score:{}".format(score,sc))
        global SPEED
        winsound.PlaySound("music_food.wav",winsound.SND_FILENAME)

        SPEED= SPEED-3

        canvas.delete("food")

        food = Food(canvas)
    else:
        del snake.cordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1];


    if check_collisions(snake):
        game_over(canvas,labal )
    else:
        window.after(SPEED, next_turn, snake, food,window,canvas,labal,sc)

def file_read():
    f = open("score.txt",'r')
    a = f.read()
    f.close()
    return int(a)

def file_write(score):
    f = open("score.txt",'w')
    f.write(score)
    f.close()

def change_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction
    #winsound.PlaySound("music_move.wav", winsound.SND_FILENAME)

def check_collisions(snake):

    x,y = snake.cordinates[0]

    if (x< 0 or x >= GAME_WIDTH) or (y<0 or y >= GAME_HEIGHT) :
        return True

    for body_part  in snake.cordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    else:

        return False

def stop_song():
    pygame.mixer.music.stop()




def game_over(canvas,labal):
    stop_song()
    canvas.delete(ALL);
    winsound.PlaySound("music_gameover.wav", winsound.SND_FILENAME)
    canvas.create_text(canvas.winfo_width()/2,100, font =("consolas",70),text="GAME OVER !",fill="red",tag="gameover")
    button3 = Button(window,text="PLAY AGAIN",command= lambda: f("PLAY AGAIN",window,canvas,labal),width=30 , height=5,bg="lightblue", fg="black",font=custom_font,
             activebackground="blue",  # Color when button is clicked
             activeforeground="yellow",  # Text color when button is clicked
             relief="raised",)
    button4 = Button(window, text="QUIT", command=lambda: f("QUIT", window,canvas,labal), width=30, height=5, bg="lightblue",
                     fg="black", font=custom_font,
                     activebackground="blue",  # Color when button is clicked
                     activeforeground="yellow",  # Text color when button is clicked
                     relief="raised", )

    canvas.create_window(GAME_WIDTH/2,GAME_HEIGHT/2-50,window = button3)
    canvas.create_window(GAME_WIDTH/2,GAME_HEIGHT/2+50,window = button4)
    a = file_read()
    if (score > a):
        file_write(str(score))




def start_game(window):
    global score
    score = 0
    sc = file_read()
    song_thread = threading.Thread(target=play_song, args=("music_music.wav", 0.2))
    song_thread.start()
    labal = Label(window, text="Score:{}   High Score:{}".format(score,sc), font=("consplas", 40))
    # labal1 = Label(window,text = "Controls by ARROW KEYS",font =("consplas",30),justify="center",height =10)
    labal.pack(anchor=W, side=TOP, padx=50, pady=10)

    canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    window.update()


    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind("<a>", lambda event: change_direction("left"))
    window.bind("<A>", lambda event: change_direction("left"))
    window.bind("<Left>", lambda event: change_direction("left"))

    window.bind("<d>", lambda event: change_direction("right"))
    window.bind("<D>", lambda event: change_direction("right"))
    window.bind("<Right>", lambda event: change_direction("right"))

    window.bind("<w>", lambda event: change_direction("up"))
    window.bind("<W>", lambda event: change_direction("up"))
    window.bind("<Up>", lambda event: change_direction("up"))

    window.bind("<s>", lambda event: change_direction("down"))
    window.bind("<S>", lambda event: change_direction("down"))
    window.bind("<Down>", lambda event: change_direction("down"))

    snake = Snake(canvas)
    food = Food(canvas)

    next_turn(snake, food,window,canvas,labal,sc)

def f(x,window,canvas,labal):
    if(x == "PLAY" ):
        stop_song()
        labal.destroy()
        canvas.destroy()
        start_game(window)
    elif(x == "PLAY AGAIN"):
        stop_song()
        labal.destroy()
        canvas.destroy()
        global SPEED
        SPEED = 150
        start_game(window)
    else:
        window.destroy()
window = Tk()
window.title("Snake game")
window.resizable(False, False)  # Window can't be resize

window.iconbitmap("unnamed.ico")
song_thread = threading.Thread(target=play_song, args=("music_music.wav", 0.2))
song_thread.start()

bold_font = font.Font(family="Helvetica", size=40, weight="bold")
custom_font = tkFont.Font(family="Arial", size=10,)

labal = Label(window, text="ClASSIC SNAKE GAME", font=bold_font,justify="center")
    # labal1 = Label(window,text = "Controls by ARROW KEYS",font =("consplas",30),justify="center",height =10)
labal.pack(side=TOP, padx=70, pady=10)

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

button1 = Button(window,text="PLAY",command=lambda :f("PLAY",window,canvas,labal),width=30 , height=5,bg="lightblue", fg="black",font=custom_font,
        activebackground="blue",  # Color when button is clicked
        activeforeground="yellow",  # Text color when button is clicked
        relief="raised",)

button2 = Button(window,text="QUIT",command= lambda: f("QUIT",window,canvas,labal),width=30 , height=5,bg="lightblue", fg="black",font=custom_font,
        activebackground="blue",  # Color when button is clicked
        activeforeground="yellow",  # Text color when button is clicked
        relief="raised",)


canvas.create_window(500,250,window = button1)
canvas.create_window(500,400,window = button2)




window.mainloop()

