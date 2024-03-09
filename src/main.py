'''
Cat and Mouse Game
------------------------------------
'''
import random
import curses
import time

player = {
    "l": 1,
    "c": 1,
    "char": "🐱",
    "alive": False
}

enemy = {
    "l": 1,
    "c": 1,
    "char": "🐭",
    "alive": False
}

barrier = {
    "char": "🚧",
    "drawed": False,
    "count": 20,
    "positions": set()
}


player_score = 0

def draw_player(stdscr):
    stdscr.addstr(player.get("l"), player.get("c"), player.get('char'))

def draw_enemy(stdscr):
    if not enemy.get("alive"):
        enemy.update({"l": random.randint(1, curses.LINES - 5), "c": random.randint(1, curses.COLS - 5), "alive": True})
        stdscr.addstr(enemy.get("l"), enemy.get("c"), enemy.get('char'))
    else:
        stdscr.addstr(enemy.get("l"), enemy.get("c"), enemy.get('char'))

def draw_barrier(stdscr):
    if not barrier.get('drawed'):
        for _ in range(barrier.get('count')):
            barrier_c = random.randint(1, curses.COLS - 5)
            barrier_l = random.randint(1, curses.LINES - 5)
            if (barrier_l, barrier_c) not in barrier["positions"] and (barrier_l, barrier_c) != (player.get('l'), player.get('c')) and (barrier_l, barrier_c) != (enemy.get('l'), enemy.get('c')):
                stdscr.addstr(barrier_l, barrier_c, barrier.get('char'))
                barrier["positions"].add((barrier_l, barrier_c))
        barrier.update({'drawed': True})
    else:
        for loc in barrier["positions"]:
            stdscr.addstr(loc[0], loc[1], barrier.get('char'))


def draw_world(stdscr):
    global player_score
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(False)
    player.update({"l": curses.LINES // 2, "c": curses.COLS // 2, "alive": True})
    

    # Loop where k is the last character pressed
    while (k != ord('q')):
        if player.get("alive"):
            # Initialization
            stdscr.clear()
            add_score_text(stdscr)
            draw_enemy(stdscr)
            draw_player(stdscr)
            draw_barrier(stdscr)

            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            k = stdscr.getch()
            
            move_player(k)

            update_player_score()

        else:
            stdscr.addstr(0, 0, 'You die!')
            stdscr.refresh()
            time.sleep(1)
            break

def update_player_score():
    global player_score
    if ((player.get('c') == enemy.get('c')) or (player.get('c') == enemy.get('c') - 1) or (player.get('c') == enemy.get('c') + 1)) and (player.get('l') == enemy.get('l')):
        enemy.update({'alive': False})
        player_score += 1
        curses.beep()

# Check input and move player
def move_player(key):
    new_l, new_c = player.get('l'), player.get('c')
    if key == ord('w'):
        new_l -= 1
    elif key == ord('s'):
        new_l += 1
    elif key == ord('a'):
        new_c -= 1
    elif key == ord('d'):
        new_c += 1

    # Check if the new position is within a 1-cell radius of a barrier
    too_close_to_barrier = False
    for loc in barrier["positions"]:
        if abs(loc[0] - new_l) < 1 and abs(loc[1] - new_c) <= 1:
            too_close_to_barrier = True
            break

    # Update the player's position if not too close to a barrier
    if not too_close_to_barrier:
        player.update({"l": new_l, "c": new_c})

def add_score_text(stdscr):
    score_text = f"Score: {player_score}"
    stdscr.addstr(0, (curses.COLS // 2) - (len(score_text) // 2), score_text)

def main():
    curses.wrapper(draw_world)

if __name__ == "__main__":
    main()