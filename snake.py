import curses
import random

# Constants for the game
SCREEN_HEIGHT = 20
SCREEN_WIDTH = 60
SNAKE_CHAR = '#'
FOOD_CHAR = '*'
DELAY = 100  # milliseconds between movements

# Direction vectors
DIRECTIONS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)
    stdscr.timeout(DELAY)

    # Initial snake coordinates and direction
    snake = [(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2 + i) for i in range(3)]
    direction = curses.KEY_LEFT
    food = place_food(snake)

    while True:
        key = stdscr.getch()
        if key in DIRECTIONS:
            direction = key

        head_y, head_x = snake[0]
        move_y, move_x = DIRECTIONS.get(direction, (0, 0))
        new_head = ((head_y + move_y) % SCREEN_HEIGHT, (head_x + move_x) % SCREEN_WIDTH)

        # Check collision with self
        if new_head in snake:
            break

        snake.insert(0, new_head)
        if new_head == food:
            food = place_food(snake)
        else:
            snake.pop()

        draw_game(stdscr, snake, food)

    stdscr.nodelay(False)
    stdscr.addstr(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2 - 5, "Game Over")
    stdscr.getch()


def draw_game(stdscr, snake, food):
    stdscr.clear()
    for y, x in snake:
        stdscr.addch(y, x, SNAKE_CHAR)
    fy, fx = food
    stdscr.addch(fy, fx, FOOD_CHAR)
    stdscr.refresh()


def place_food(snake):
    while True:
        pos = (random.randint(0, SCREEN_HEIGHT - 1), random.randint(0, SCREEN_WIDTH - 1))
        if pos not in snake:
            return pos


if __name__ == '__main__':
    curses.wrapper(main)
