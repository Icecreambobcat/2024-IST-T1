from __future__ import annotations
import typing
import pickle
import curses
import random
import csv
import time
import os
from curses import wrapper, textpad


class player:
    def __init__(self, name: str) -> None:
        """

        Player class to store local runtime data for the player

        Properties:

        items: list[str] - list of items the player has
        story_index: int - index of the current story text
        lives: int - number of lives the player has
        name: str - name of the player

        """
        self.items = []
        self.story_index = 0
        self.lives = 3
        self.name = name
        
    def packege_data(self) -> dict[str, typing.Any]:
        return {
            'items': self.items,
            'story_index': self.story_index,
            'lives': self.lives,
            'name': self.name
        }


class question:
    def __init__(self, question: list[str], choice1: str, choice2: str, result1: str, result2: str, pointer1: int, pointer2: int, index: int) -> None:
        """
        
        Class to store questions, choices, and results for the game as well as point to the next event

        Properties:

        question: list[str] - the question to be asked
        choice1: str - the first choice
        choice2: str - the second choice
        result1: str - the result of the first choice
        result2: str - the result of the second choice
        pointer1: int - the index of the next event if the first choice is chosen
        pointer2: int - the index of the next event if the second choice is chosen
        index: int - the index of the current event

        """
        self.question = question
        self.choice1 = choice1
        self.choice2 = choice2
        self.result1 = result1
        self.result2 = result2
        self.pointer1 = pointer1
        self.pointer2 = pointer2
        self.index = index

    def check(self, choice: str) -> list[str | int]:
        if choice == self.choice1:
            return [self.result1, self.pointer1]
        if choice == self.choice2:
            return [self.result2, self.pointer2]
        else:
            return ["Invalid input", self.index]


class story:
    def __init__(self, text: list[str], index: int, pointer: int) -> None:
        """
        
        Class to contain text screen events

        Properties:

        text: list[str] - the text to be displayed
        index: int - the index of the current event
        pointer: int - the index of the next event

        """
        self.text = text
        self.index = index
        self.pointer = pointer

class fight:
    def __init__(self, text_list: list[str], outcome1: list[str], outcome2: list[str], outcome3: list[str], index: int, pointer1: int, pointer2: int, pointer3: int) -> None:
        """

        Class to contain fight events
        
        Properties:

        text_list: list[str] - the text to be displayed
        outcome1: list[str] - the outcome of the first choice
        outcome2: list[str] - the outcome of the second choice
        outcome3: list[str] - the outcome of the third choice
        index: int - the index of the current event
        pointer1: int - the index of the next event if the first choice is chosen
        pointer2: int - the index of the next event if the second choice is chosen
        pointer3: int - the index of the next event if the third choice is chosen
        
        """
        self.text = text_list
        self.outcome1 = outcome1
        self.outcome2 = outcome2
        self.outcome3 = outcome3
        self.index = index
        self.pointer1 = pointer1
        self.pointer2 = pointer2
        self.pointer3 = pointer3
        

class intro:
    def __init__(self, text: list[str], index: int, pointer: int) -> None:
        """
        
        Class to contain intro events

        Properties:

        text: list[str] - the text to be displayed
        index: int - the index of the current event
        pointer: int - the index of the next event

        """
        self.text = text
        self.index = index
        self.pointer = pointer


def init_all() -> dict[int, typing.Any]:
    out = {}

    """
    
    Function to initialize all data from csv files

    This function takes the outputs of the other functions and combines them into one dictionary
    
    """

    def init_questions() -> dict[int, question]:
        out = {}
        with open('questions.csv', 'r') as file:
            questions_csv = csv.reader(file)
            next(questions_csv)   
            for line in questions_csv:
                obj = question(line[0].split('#'), line[1], line[2], line[3], line[4], int(line[5]), int(line[6]), int(line[7]))
                out [obj.index] = obj

        return out

    def init_intro() -> dict[int, intro]:
        out = {}
        with open('intro.csv', 'r', newline= '') as file:
            intro_csv = csv.reader(file, delimiter= ':')
            next(intro_csv)
            for line in intro_csv:
                obj = intro(line[0].split('#'), int(line[1]), int(line[2]))
                out[obj.index] = obj

        return out

    def init_story() -> dict[int, story]:
        out = {}
        with open('story.csv', 'r') as file:
            story_csv = csv.reader(file)
            next(story_csv)
            for line in story_csv:
                obj = story(line[0].split('#'), int(line[1]), int(line[2]))
                out[obj.index] = obj

        return out

    def init_fights() -> dict[int, fight]:
        out = {}
        with open('fights.csv', 'r') as file:
            fights_csv = csv.reader(file)
            next(fights_csv)
            for line in fights_csv:
                obj = fight(line[0].split('#'), line[1].split('#'), line[2].split('#'), line[3].split('#'), int(line[4]), int(line[5]), int(line[6]), int(line[7]))
                out[obj.index] = obj

        return out


    for directory in [init_questions(), init_intro(), init_story(), init_fights()]:
        for key in directory.keys():
            out[key] = directory[key]

    return out


def save(local_data: dict[str, typing.Any]) -> None | int:
    try:
        with open('save.txt', 'wb') as save_file:
            pickle.dump(local_data, save_file)
    except Exception:
        return 0


def read() -> dict[str, typing.Any] | None:
    try:
        with open('save.txt', 'rb') as save_file:
            local_data = pickle.load(save_file)
            if local_data is None or not dict:
                return None
            else: return local_data
    except Exception:
        return None


def roll_dice(d: int, count: int, type: str) -> int:
    # where d is sides, count is number of dice, and type is how to combine results
    if d and count is int and type is str:
        if type == "sum":
            return sum([random.randint(1, d) for i in range(count)])
        elif type == "max":
            return max([random.randint(1, d) for i in range(count)])
        elif type == "min":
            return min([random.randint(1, d) for i in range(count)])
        else:
            return 0
    else: 
        return 0


def recreate_player(data: dict[str, typing.Any]) -> player:
    p = player(data['name'])
    p.items = data['items']
    p.story_index = data['story_index']
    p.lives = data['lives']
    return p


def display(index: int, window: curses.window) -> None:

    obj = text_store[index]
    out = []

   # if obj.__class__.__name__ == "story":
   #     for w in obj.text:
   #         out.append(w)
   #     for lines in out:
   #         window.addstr(lines) # figure how to make it look good
   # elif text_store[index].__class__.__name__ == "question":
   #     for w in obj.question:
   #         out.append(w)
   #     for lines in out:
   #         window.addstr(lines) # figure how to make it look good
   # elif text_store[index].__class__.__name__ == "fight":
   #     for w in obj.text:
   #         out.append(w)
   #     for lines in out:
   #         window.addstr(lines)
    if text_store[index].__class__.__name__ == "intro":
        counter = 0
        for w in obj.text:
            out.append(w)
        for lines in out:
            counter += 1
            window.addstr(counter - 1, 0, lines)
            window.refresh()
   # else:
   #     raise Exception("Invalid object type")
   #     # what else though


def main(stdscr) -> None:

    def set_terminal_size():
        # For macOS
        os.system('osascript -e \'tell application "Terminal" to tell front window to set {rows, columns} to {26, 104}\'')

        # For some Windows systems
        # os.system('mode con: cols=104 lines=26')

        # For some Unix-based systems
        # os.system('resize -s 26 104')

    set_terminal_size()

    global main_win, text_win, main_border, text_border, input_win, text_store

    global text_store
    text_store = init_all()

    local_data = {}

    save_data = read()

    if save_data != None:
        local_data: dict[str, typing.Any] = save_data
    else:
        local_data['first_play'] = True
        local_data['name'] = ""
        local_data['items'] = []
        local_data['story_index'] = 0
        local_data['lives'] = 3

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    red_black = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    green_black = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    invert = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    cyan_black = curses.color_pair(4)

    stdscr.clear()
    curses.cbreak()
    
    main_win = curses.newwin(24, 60, 1, 43)
    text_win = curses.newwin(24, 40, 1, 1)
    input_win = curses.newwin(10, 40, 15, 1)
    main_border = curses.newwin(26, 62, 0, 42)
    text_border = curses.newwin(26, 42, 0, 0)

    input_box = textpad.Textbox(input_win, insert_mode=True)


    main_win.attron(cyan_black)
    text_win.attron(green_black)
    text_border.attron(green_black)
    input_win.attron(red_black)


    main_border.border()
    text_border.border()

    main_border.refresh()
    text_border.refresh()

    main_win.addstr(0, 0, "Welcome to the game!\nPress any key to continue and type 'quit' to save and exit.")
    text_win.addstr(0, 0, "You'll type your input here.\nPress Ctrl+G to confirm inputs.")

    main_win.refresh()
    text_win.refresh()


    input_win.move(0, 0)
    text_win.getch()
    

    if local_data['first_play'] == True:
        text_win.addstr(3, 0, "Please enter your name:", red_black)
        text_win.refresh()
        while True: 
            input_box.edit()
            name = input_box.gather().strip()
            input_win.clear()

            if name.lower() == "quit":
                curses.nocbreak()
                stdscr.keypad(False)
                save(local_data)
                quit()

            elif name != "":
                local_data['first_play'] = False
                local_data['name'] = name
                input_win.clear()
                break

            elif name == "":
                text_win.addstr(4, 0, "Please enter a valid name.\nNo blank names, nameless wanderer.", red_black)
                text_win.refresh()
                continue



    while True: # game loop: build the rest in here
        text_win.clear()
        main_win.clear()
        main_win.refresh()
        text_win.refresh()

        # incorporate display function right here
        display(local_data['story_index'], main_win)

        input_box.edit()
        key = input_box.gather().strip().lower()
        input_win.clear()
        if key.lower().strip() == "quit": # save and exit
            curses.nocbreak()
            save(local_data)
            quit()
        elif key.lower().strip() == "save":
            save(local_data)
            



if __name__ == "__main__":
    wrapper(main)