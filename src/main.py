'''
River Raid Game
------------------------------------
'''
import random
import curses
import time

player = {
    "l": 1,
    "c": 1,
    "char": "🐱", # 🐱
    "alive": False
}

enemy = {
    "l": 1,
    "c": 1,
    "char": "🐭", # 🐭
    "alive": False
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

            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            k = stdscr.getch()
            
            move_player(k)

            update_player_score()

        else:
            print('You die!')
            time.sleep(1)
            exit()


def update_player_score():
    global player_score
    if ((player.get('c') == enemy.get('c')) or (player.get('c') == enemy.get('c') - 1) or (player.get('c') == enemy.get('c') + 1)) and (player.get('l') == enemy.get('l')):
        enemy.update({'alive': False})
        player_score += 1

# Check input and move player
def move_player(key):
        if key == ord('w'):
            if player.get('l') != 1:
                player.update({"l": player.get('l') - 1})
        elif key == ord('s'):
            if player.get('l') != curses.LINES - 2:
                player.update({'l': player.get('l') + 1})
        elif key == ord('a'):
            if player.get('c') != 1:
                player.update({'c': player.get('c') - 1})
        elif key == ord('d'):
            if player.get('c') != curses.COLS - 3:
                player.update({'c': player.get('c') + 1})

def add_score_text(stdscr):
    score_text = f"Score: {player_score}"
    stdscr.addstr(0, (curses.COLS // 2) - (len(score_text) // 2), score_text)

def main():
    curses.wrapper(draw_world)

if __name__ == "__main__":
    main()