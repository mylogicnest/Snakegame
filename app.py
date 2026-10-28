"""
Snake Game (frontend client). It talks to the Flask backend in app.py
through the API: GET /api/scores and POST /api/scores.

1. Start the backend first:  python3 app.py
2. Then, in a second terminal:  python3 snakegame.py
"""
import time
import random
import threading
import tkinter
import turtle

import requests

API_URL = "http://127.0.0.1:5001/api/scores"
START_DELAY = 0.07
MIN_DELAY = 0.03


# ---------- API calls (pointer c: frontend <-> backend integration) ----------
def fetch_high_score():
    """Ask the backend for the best score so far."""
    try:
        response = requests.get(API_URL, timeout=2)
        response.raise_for_status()
        scores = response.json()
        return scores[0]["score"] if scores else 0
    except requests.exceptions.RequestException:
        print("Backend not reachable, starting with high score 0.")
        return 0


def submit_score(player, value):
    """Send the finished game's score to the backend."""
    try:
        response = requests.post(
            API_URL, json={"player": player, "score": value}, timeout=2
        )
        response.raise_for_status()
        print("Score saved:", response.json())
    except requests.exceptions.RequestException:
        print("Could not save the score (is app.py running?).")


# ---------- Game setup ----------
player = input("Enter your name: ").strip() or "Anonymous"

delay = START_DELAY
score = 0
high_score = fetch_high_score()

screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

segments = []


def update_score():
    pen.clear()
    pen.write(
        f"{player}   Score: {score}   High Score: {high_score}",
        align="center",
        font=("Arial", 16, "normal"),
    )


def place_food():
    """Put the food on the same grid as the snake, never on the snake."""
    while True:
        x = random.randrange(-280, 281, 20)
        y = random.randrange(-280, 281, 20)
        on_snake = head.distance(x, y) < 20 or any(
            s.distance(x, y) < 20 for s in segments
        )
        if not on_snake:
            food.goto(x, y)
            return


update_score()


# ---------- Controls ----------
def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)


screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")


def game_over():
    """Send the score to the backend (in the background), then reset."""
    global score, delay

    if score > 0:
        # Background thread so the game doesn't freeze while waiting
        threading.Thread(
            target=submit_score, args=(player, score), daemon=True
        ).start()

    time.sleep(0.5)
    head.goto(0, 0)
    head.direction = "stop"

    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    place_food()
    score = 0
    delay = START_DELAY
    update_score()


# ---------- Main loop ----------
try:
    while True:
        screen.update()

        # Wall collision
        if (head.xcor() > 290 or head.xcor() < -290 or
                head.ycor() > 290 or head.ycor() < -290):
            game_over()

        # Eating food
        if head.distance(food) < 20:
            segment = turtle.Turtle()
            segment.speed(0)
            segment.shape("square")
            segment.color("green")
            segment.penup()
            segment.goto(1000, 1000)
            segments.append(segment)

            score += 10
            if score > high_score:
                high_score = score
            delay = max(MIN_DELAY, delay - 0.002)
            place_food()
            update_score()

        # Move the body
        for i in range(len(segments) - 1, 0, -1):
            segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())
        if segments:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # Body collision
        for segment in segments:
            if segment.distance(head) < 10:
                game_over()
                break

        time.sleep(delay)

except (turtle.Terminator, tkinter.TclError):
    # Window was closed, exit quietly
    print("Game closed.")