#! /usr/bin/python3

import curses
import sys
import time
import numpy

class Calendar(object):

    def __init__(self):
        self.month = 0
        self.year = 0
        self.origin = time.perf_counter()
        self.pausetime = 0
        self.pauseinit = 0

    def __str__(self):
        return "Year: {} Month: {}".format(self.year, self.month + 1)

    def update(self):
        change = time.perf_counter() - self.origin - self.pausetime
        # month duration in seconds
        dur = 5
        self.year = int(change // (12 * dur))
        self.month = int((change % (12 * dur)) // dur)

    def pause(self):
        self.pauseinit = time.perf_counter()

    def unpause(self):
        self.pausetime += time.perf_counter() - self.pauseinit

class World(object):

    def __init__(self, name, h, w):
        self.name = name
        self.mat = numpy.random.randint(1,size=(h,w)) + 1
        self.h = h
        self.w = w
        self.pops = []
        self.map = {}
        self.col = {}

    def __str__(self):
        return name

    def gen_terr(self): # generate terrain with probability functions
        pass

    def gen_map(self, char_dict):
        for x in range(0,self.w):
            for y in range (0,self.h):
                self.map[(x,y)] = char_dict[self.mat[y,x]]

    def gen_col(self, col_dict):
        for x in range(0,self.w):
            for y in range (0,self.h):
                self.col[(x,y)] = col_dict[self.mat[y,x]]

class Population(object):

    def __init__(self, owner):
        self.name = name
        self.size = 100
        self.growth = 1.2
        self.owner = owner
        self.influence = {self.owner:100}
        self.cap = 10000

    def grow(self):
        self.size = int(self.size*self.growth)
        if self.size > self.cap:
            self.size = self.cap

    def turn(self):
        if len(list(self.influence.keys())) > 1:
            for other in list(self.influence.keys())[1:]:
                if self.influence[other] > self.influence[owner]:
                    self.owner = other

def trace_cursor(k, cursor_y, cursor_x):

    if k == 258:
        cursor_y = cursor_y + 1
    elif k == 336:
        cursor_y = cursor_y + 5
    elif k == 259:
        cursor_y = cursor_y - 1
    elif k == 337:
        cursor_y = cursor_y - 5
    elif k == 261:
        cursor_x = cursor_x + 1
    elif k == 402:
        cursor_x = cursor_x + 5
    elif k == 260:
        cursor_x = cursor_x - 1
    elif k == 393:
        cursor_x = cursor_x - 5
    return(cursor_y, cursor_x)

def gen_world_pad(source):

    world = curses.newpad(source.h+1, source.w+1)
    for i in range(0, source.h):
        for j in range(0, source.w):
            world.addstr(i, j, str(source.map[(j,i)]), source.col[(j,i)])
    return(world)

def cosmogon(stdscr):

    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)

    char_dict = {
        1: "~",
        2: "╬",
        3: "░",
        4: "¶",
        5: "^",
        6: "#",
        7: "ª",
        8: "a",
        9: "A",
        }

    type_dict = {
        1: "water",
        2: "river",
        3: "plains",
        4: "woods",
        5: "mountains",
        6: "farms",
        7: "village",
        8: "town",
        9: "city",
        }

    col_dict = {
        1: curses.color_pair(1),
        2: curses.color_pair(1),
        3: curses.color_pair(2),
        4: curses.color_pair(3),
        5: curses.color_pair(4),
        6: curses.color_pair(2),
        7: curses.color_pair(5),
        8: curses.color_pair(5),
        9: curses.color_pair(5),
        }

    # provisional matrix
    testmat = numpy.array([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1],
        [1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1],
        [1,1,1,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,3,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,3,3,3,3,3,1,1,1,1,1,1,1,1],
        [1,1,3,3,3,3,3,3,3,3,4,4,4,4,4,4,3,3,3,3,2,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,3,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,3,3,3,3,3,4,4,4,4,4,4,4,4,4,3,3,3,2,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,1,1,1,1,1],
        [1,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,3,3,3,3,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,1,1,1,1,1,1],
        [1,1,1,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,2,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,2,2,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,2,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,7,6,3,3,1,1,1,1,1,1,1],
        [1,1,2,2,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,6,2,2,1,1,1,1,1,1,1,1],
        [1,1,3,2,2,2,2,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,3,3,3,3,1,1,1,1,1],
        [1,3,3,3,3,3,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,2,4,4,4,4,4,4,4,4,4,4,4,3,2,2,2,3,3,3,3,3,1,1,1,1,1,1,1],
        [1,3,3,3,3,3,3,3,3,2,2,2,2,4,4,4,4,4,4,4,4,4,4,2,4,4,4,4,4,4,4,4,2,2,2,2,4,4,4,4,3,3,3,3,3,1,1,1,1,1],
        [1,3,3,3,3,3,3,3,3,3,3,4,4,2,4,4,4,4,4,4,4,4,5,2,4,4,4,4,4,4,4,4,2,4,4,4,4,3,3,3,3,3,3,3,1,1,1,1,1,1],
        [1,1,1,3,3,3,3,3,3,4,4,4,4,2,2,2,4,4,4,2,2,2,5,5,4,4,4,4,4,4,2,2,2,4,4,4,4,4,4,4,4,3,3,3,3,3,3,1,1,1],
        [1,1,1,1,3,3,3,3,3,3,3,3,4,4,4,2,2,2,2,2,4,4,4,5,5,4,4,2,2,2,2,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,1,1,1],
        [1,1,3,3,3,3,3,3,4,4,4,4,4,4,2,2,4,4,4,4,4,4,4,5,5,2,2,2,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,1,1,1,1,1,1,1],
        [1,1,3,3,3,3,3,3,4,4,4,4,4,2,2,4,4,4,4,4,4,4,5,5,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
        [1,3,3,3,3,3,3,3,3,4,4,4,4,2,4,4,4,4,4,4,4,4,2,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,1,1,1,1],
        [1,3,3,3,2,2,2,2,2,4,4,2,2,2,4,4,4,4,4,4,4,2,2,5,5,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,1,1,1,1],
        [1,1,1,2,2,3,3,3,2,2,2,2,4,4,4,4,4,4,4,4,4,2,4,5,4,4,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,2,2,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,2,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1],
        [1,1,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,2,2,3,3,3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,7,6,4,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1],
        [1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,6,2,2,2,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ])

    # Create a new world
    world = World("Alpha", 30, 50)
    # Use the provitional matrix
    world.mat = testmat 
    world.gen_map(char_dict)
    world.gen_col(col_dict)
    world_pad = gen_world_pad(world)

    # World is paused
    calendar = Calendar()
    paused = 1
    calendar.pause()

    # Loop where k is the last character pressed
    while True:

        # Pause and unpause
        if k == 112:
            if paused == 1: 
                # if paused, unpause
                calendar.unpause()
                stdscr.nodelay(True)
                paused = 0
            else:
                # if unpaused, pause
                calendar.pause()
                stdscr.nodelay(False)
                paused = 1

        # Quit to menu
        if k == 113:
            main_menu(stdscr)

        # Initialization
        curses.curs_set(True)
        curses.napms(41)
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # The cursor will be moving in the pad
        pheight, pwidth = world_pad.getmaxyx()

        cursor_y, cursor_x = trace_cursor(k, cursor_y, cursor_x)

        cursor_x = max(0, cursor_x)
        cursor_x = min(pwidth-2, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(pheight-2, cursor_y)

        # Declaration of strings
        view = " Viewing: {}".format(type_dict[world.mat[cursor_y,cursor_x]])
        statusbarstr = " Quit 'q' | Pause 'p' | Last: {} Pos: {}, {}"
        statusbarstr = statusbarstr.format(k , cursor_y, cursor_x)
        calstr = str(calendar)

        # Update and print date
        if paused == 0:
            calendar.update()
        stdscr.addstr(0, 0, " "+ world.name +", "+ calstr, curses.color_pair(5))

        # Render information
        stdscr.addstr(height-4, 0, view)

        # Render status bar
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(4))

        # Move the cursor
        world_pad.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Refresh the world
        world_pad.refresh( 0,0, 5,5, height-5,width-20)

        # Get next input
        k = stdscr.getch()

def main_menu(stdscr):

    k = 0
    cursor_x = 0
    cursor_y = 0

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while True:

        if k == 10 and cursor_y == (height // 2) + 2:
            sys.exit()

        if k == 10 and cursor_y == (height // 2) + 1:
            cosmogon(stdscr)

        # Initialization
        curses.curs_set(False)
        stdscr.nodelay(False)
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1

        cursor_x = (width // 2)

        cursor_y = max(int((height // 2) + 1), cursor_y)
        cursor_y = min(int((height // 2) + 2), cursor_y)

        # Strings
        statusbarstr = " Miguel Romero 2020 | github.com/romeromig"
        title = "COSMOGON"
        subtitle = "We are the chosen ones"

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_y = int((height // 2) - 2)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y-2, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y, start_x_subtitle, subtitle)
        if cursor_y == (height // 2) + 1:
            stdscr.addstr(start_y + 3, (width // 2) - 2, 'Begin', curses.A_STANDOUT)
        else:
            stdscr.addstr(start_y + 3, (width // 2) - 2, 'Begin')
        if cursor_y == (height // 2) + 2:
            stdscr.addstr(start_y + 4, (width // 2) - 2, 'Exit', curses.A_STANDOUT)
        else:
            stdscr.addstr(start_y + 4, (width // 2) - 2, 'Exit')

        # Move the cursor
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()


def main():
    curses.wrapper(main_menu)

if __name__ == "__main__":
    main()
