# Import necessary libraries
import random
import curses

# Initialize the screen
s = curses.initscr()

# Set the cursor state. 0 means invisible.
curses.curs_set(0)

# Get the width and height of the screen
sh, sw = s.getmaxyx()

# Create a new window using screen height and width
w = curses.newwin(sh, sw, 0, 0)

# Draw a border around the window
w.box()

# Accept keypad input
w.keypad(True)

# Control the speed of the game
w.timeout(100)

# Initialize the score
score = 0

# Add the score to the screen
w.addstr(0, 0, 'Score: ' + str(score))

# Initial snake position
snk_x = sw//4
snk_y = sh//2

# Initial snake body parts
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

# Initial food position
food = [sh//2, sw//2]

# Create a list to store the positions of the obstacles
obstacles = []

# Generate random positions for the obstacles
for _ in range(10):  # Change this number to control the number of obstacles
    while True:
        obstacle = [random.randint(1, sh-2), random.randint(1, sw-2)]
        if obstacle not in obstacles and obstacle not in snake and obstacle != food:
            obstacles.append(obstacle)
            break

# Draw the obstacles on the screen
for obstacle in obstacles:
    w.addch(obstacle[0], obstacle[1], '#')

# Add the food to the screen
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

# Initial direction the snake moves towards
key = curses.KEY_RIGHT

# Infinite loop for game movement
while True:
    # Get the next key
    next_key = w.getch()
    # If a key is pressed, use it as the next key
    key = key if next_key == -1 else next_key

    # Calculate the new head of the snake
    new_head = [snake[0][0], snake[0][1]]

    # Move the snake
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # Wrap the snake's position if it hits the border
    new_head[0] = new_head[0] % (sh - 1)
    new_head[1] = new_head[1] % (sw - 1)

    # Insert new head of the snake
    snake.insert(0, new_head)

    # Check if game over (snake runs into itself or an obstacle)
    if snake[0] in snake[1:] or snake[0] in obstacles:
        # Clear the window
        w.clear()
        # Display game over message
        w.addstr(sh // 2, sw // 2, 'Game Over!')
        # Refresh the window to show the message
        w.refresh()
        # Wait for a few seconds to let the player see the message
        curses.napms(2000)
        # End the window
        curses.endwin()
        # Quit the game
        quit()

    # Check if snake has eaten the food
    if snake[0] == food:
        # If so, set food to None
        food = None
        # Increase the score
        score += 1
        # Update the score on the screen
        w.addstr(0, 0, 'Score: ' + str(score))
        while food is None:
            # Create new food
            nf = [
                random.randint(1, sh - 1),
                random.randint(1, sw - 1)
            ]
            # If the new food position is not part of the snake, place it on the screen
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        # If not, keep moving the snake
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    # Add the new head of the snake to the screen
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
