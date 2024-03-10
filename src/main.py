'''
Cat and Mouse Game
------------------------------------
'''
import random
import curses
import time

# Initialize player, enemy, and barrier
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
    "count": 10,
    "positions": set()
}

# Initialize player score and level
player_score = 0
player_level = 1

def draw_player(stdscr):
    """Draw the player on the screen."""
    stdscr.addstr(player.get("l"), player.get("c"), player.get('char'))

def draw_enemy(stdscr):
    """Draw the enemy on the screen."""
    new_l = random.randint(1, curses.LINES - 5)
    new_c = random.randint(1, curses.COLS - 5)
    if not enemy.get("alive"):
        if not too_close_to_barrier(new_l, new_c):
            enemy.update({"l": new_l, "c": new_c, "alive": True})
            stdscr.addstr(enemy.get("l"), enemy.get("c"), enemy.get('char'))
        else:
            draw_enemy(stdscr)
    else:
        stdscr.addstr(enemy.get("l"), enemy.get("c"), enemy.get('char'))

def draw_barrier(stdscr):
    """Draw the barrier on the screen."""
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
    """Draw the game world on the screen."""
    global player_score
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(False)
    player.update({"l": curses.LINES // 2, "c": curses.COLS // 2, "alive": True})
    

    # Loop where q is the last character pressed
    while (k != ord('q')):
        if player.get("alive"):
            # Initialization
            stdscr.clear()
            draw_score_and_level(stdscr)
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
            stdscr.clear()
            stdscr.refresh()
            time.sleep(1)
            break

def update_player_score():
    """Update player's score and level based on the game progress."""
    global player_score, player_level
    if ((player.get('c') == enemy.get('c')) or (player.get('c') == enemy.get('c') - 1) or (player.get('c') == enemy.get('c') + 1)) and (player.get('l') == enemy.get('l')):
        enemy.update({'alive': False})
        player_score += 1
        curses.beep()
        if player_score % 10 == 0:
            player_level = player_score // 10 + 1
            barrier.update({'drawed': False,'count': barrier.get('count') + player_score}) # Increasing the degree of difficulty of the game based on the level
            curses.flash()  # Flash screen to indicate level up

def move_player(key):
    """Move the player based on the user input."""
    new_l, new_c = player.get('l'), player.get('c')
    if key == ord('w'):
        if new_l != 1:
            new_l -= 1
    elif key == ord('s'):
        if new_l != curses.LINES - 2:
            new_l += 1
    elif key == ord('a'):
        if new_c != 1:
            new_c -= 1
    elif key == ord('d'):
        if new_c != curses.COLS - 3:
            new_c += 1

    # Update the player's position if not too close to a barrier
    if not too_close_to_barrier(new_l, new_c):
        player.update({"l": new_l, "c": new_c})

def too_close_to_barrier(l, c):
    """Check if the player is too close to a barrier."""
    too_close_to_barrier = False
    for loc in barrier["positions"]:
        if abs(loc[0] - l) < 1 and abs(loc[1] - c) <= 1:
            too_close_to_barrier = True
            break
    return too_close_to_barrier

def draw_score_and_level(stdscr):
    """Draw the player's score and level on the screen."""
    score_text = f"Score: {player_score}"
    level_text = f"Level: {player_level}"
    stdscr.addstr(0, (curses.COLS // 2) - ((len(score_text) // 2) + (len(level_text) // 2)), score_text + ' - ' + level_text)

def main():
    """Main function to run the game."""
    curses.wrapper(draw_world)

if __name__ == "__main__":
    main()