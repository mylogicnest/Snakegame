import turtle
import time
import random

# Game settings
delay = 0.1
score = 0
high_score = 0

# Create the game window
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

# Create the snake's head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Create the food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Create the score display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0",
          align="center", font=("Arial", 16, "normal"))

# Snake movement functions
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

# Keyboard controls
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

# Snake body
segments = []

# Main game loop
while True:
    screen.update()

    # Check collision with the wall
    if (head.xcor() > 290 or head.xcor() < -290 or
            head.ycor() > 290 or head.ycor() < -290):

        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        score = 0
        delay = 0.1
        pen.clear()
        pen.write(
            f"Score: {score}  High Score: {high_score}",
            align="center",
            font=("Arial", 16, "normal")
        )

    # Check if snake eats the food
    if head.distance(food) < 20:
        x = random.randrange(-270, 271, 20)
        y = random.randrange(-270, 271, 20)
        food.goto(x, y)

        # Add a new body segment
        segment = turtle.Turtle()
        segment.speed(0)
        segment.shape("square")
        segment.color("green")
        segment.penup()
        segments.append(segment)

        score += 10
        if score > high_score:
            high_score = score

        delay = max(0.04, delay - 0.002)

        pen.clear()
        pen.write(
            f"Score: {score}  High Score: {high_score}",
            align="center",
            font=("Arial", 16, "normal")
        )

    # Move the snake's body
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Check collision with the snake's body
    for segment in segments:
        if segment.distance(head) < 10:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            for part in segments:
                part.goto(1000, 1000)
            segments.clear()

            score = 0
            delay = 0.1
            pen.clear()
            pen.write(
                f"Score: {score}  High Score: {high_score}",
                align="center",
                font=("Arial", 16, "normal")
            )
            break

    time.sleep(delay)