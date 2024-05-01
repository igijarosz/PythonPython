from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00ff00"
FOOD_COLOR = "#ff0000"
BG_COLOR = "#000000"
SPEED = 100


class Snake:

    def __init__(self):

        self.body_size = BODY_PARTS
        self.coordinates = []  # przechowuje koordynaty czesci
        self.squares = []  # przechowuje wszystkie czesci weza

        for i in range(0, BODY_PARTS):
            self.coordinates.append([GAME_WIDTH / 2, GAME_HEIGHT / 2])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")


def next_turn(snake: Snake, food: Food) -> None:
    #  koordynaty glowy weza
    x, y = snake.coordinates[0]

    #  przesuwanie w kierunku
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    #  wstawienie nowej czesci weza
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    #  zjadanie jablek i zwiekszanie wyniku
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score:{score}")

        canvas.delete("food")
        food = Food()

    #  usuwanie ostatniej czesci po przesunieciu (jezeli nie zjemy nic)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    #  wykrywanie kolizji
    if check_collisons(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction: str) -> None:
    global direction

    #  sprawdzanie czy zakret jest wykonalny
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    if new_direction == 'right' and direction != 'leftt':
        direction = new_direction
    if new_direction == 'up' and direction != 'down':
        direction = new_direction
    if new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisons(snake: Snake) -> bool:
    """True jezeli wykryje kolizje"""

    # koordynaty glowy weza
    x, y = snake.coordinates[0]

    #  kolizja z krawedzia ekranu
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    #  kolizja z samym soba
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True


def game_over() -> None:
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("Fixedsys", 40), text="GAME OVER",
                       fill="#ffffff")



score = 0
direction = "down"

#  tworzenie okienka i canvasu
window = Tk()
window.title("PythonPython")
window.resizable(False, False)

label = Label(window, text=f"Score: {score}", font=("Fixedsys", 40))
label.pack()
canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

#  centrowanie okienka na ekranie
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#  przypisania klawiszy
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction("down"))
window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))

#  game loop
food = Food()
snake = Snake()

next_turn(snake, food)

window.mainloop()
