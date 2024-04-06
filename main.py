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
        name: str - name of the player

        """
        self.items = []
        self.story_index = 0
        self.name = name
        
    def packege_data(self) -> dict[str, typing.Any]:
        return {
            'items': self.items,
            'story_index': self.story_index,
            'name': self.name
        }


class question:
    def __init__(self, question: list[str], choice1: str, choice2: str, result1: str, result2: str, index: int, pointer1: int, pointer2: int) -> None:
        """
        
        Class to store questions, choices, and results for the game as well as point to the next event

        Properties:

        question: list[str] - the question to be asked
        choice1: str - the first choice
        choice2: str - the second choice
        result1: str - the result of the first choice
        result2: str - the result of the second choice
        index: int - the index of the current event
        pointer1: int - the index of the next event if the first choice is chosen
        pointer2: int - the index of the next event if the second choice is chosen

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
        with open('Store/questions.csv', 'r', newline= '') as file:
            questions_csv = csv.reader(file, delimiter= ':')
            next(questions_csv)   
            for line in questions_csv:
                obj = question(line[0].split('#'), line[1], line[2], line[3], line[4], int(line[5]), int(line[6]), int(line[7]))
                out [obj.index] = obj

        return out

    def init_intro() -> dict[int, intro]:
        out = {}
        with open('Store/intro.csv', 'r', newline= '') as file:
            intro_csv = csv.reader(file, delimiter= ':')
            next(intro_csv)
            for line in intro_csv:
                obj = intro(line[0].split('#'), int(line[1]), int(line[2]))
                out[obj.index] = obj

        return out

    def init_story() -> dict[int, story]:
        out = {}
        with open('Store/story.csv', 'r', newline= '') as file:
            story_csv = csv.reader(file, delimiter= ':')
            next(story_csv)
            for line in story_csv:
                obj = story(line[0].split('#'), int(line[1]), int(line[2]))
                out[obj.index] = obj

        return out

    def init_fights() -> dict[int, fight]:
        out = {}
        with open('Store/fights.csv', 'r', newline= '') as file:
            fights_csv = csv.reader(file, delimiter= ':')
            next(fights_csv)
            for line in fights_csv:
                obj = fight(line[0].split('#'), line[1].split('#'), line[2].split('#'), line[3].split('#'), int(line[4]), int(line[5]), int(line[6]), int(line[7]))
                out[obj.index] = obj

        return out


    for directory in [init_questions(), init_intro(), init_story(), init_fights()]:
        for key in directory.keys():
            out[key] = directory[key]

    return out


def save(local_data: dict[str, typing.Any]) -> None:
    try:
        with open('Store/save.bin', 'wb') as save_file:
            pickle.dump(local_data, save_file)
    except Exception:
        text_win.clear()
        text_win.refresh()
        curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK)
        for c in "Save failed. Please try again.":
            text_win.addstr(c, curses.color_pair(9) | curses.A_BOLD)
            text_win.refresh()
            time.sleep(0.01)
        
        time.sleep(2)

        for i in range (5):
            text_win.clear()
            text_win.addstr(f'Returning in: {i+1}...', curses.color_pair(9) | curses.A_BOLD)
            text_win.refresh()
            time.sleep(1)
        return


def read() -> dict[str, typing.Any]:
    try:
        with open('Store/save.bin', 'rb') as save_file:
            local_data = pickle.load(save_file)
            if local_data is None or not dict:
                return {}
            else: return local_data
    except Exception:
        return {}

def roll_dice(d: int, count: int, type: str) -> int:
    # where d is sides, count is number of dice, and type is how to combine results
    if type == "sum":
        return sum([random.randint(1, d) for i in range(count)])
    elif type == "max":
        return max([random.randint(1, d) for i in range(count)])
    elif type == "min":
        return min([random.randint(1, d) for i in range(count)])
    else:
        return 0

def recreate_player(data: dict[str, typing.Any]) -> player:
    try:
        p = player(data['name'])
        p.items = data['items']
        p.story_index = data['story_index']
        return p
    except Exception:
        return player("")


def display(index: int, window: curses.window) -> None:

    obj = text_store[index]
    out = []

    def sp(line: str, window: curses.window) -> None:
        for c in line:      
            window.addstr(c)
            window.refresh()
            time.sleep(0.02)


    if obj.__class__.__name__ == "story":
        for w in obj.text:
            out.append(w)
        for lines in out:
            sp(lines, window)
            window.addstr('\n')
    elif text_store[index].__class__.__name__ == "question":
        for w in obj.question:
            out.append(w)
        for lines in out:
            sp(lines, window)
            window.addstr('\n')
        sp(f"1. {obj.choice1}", window)
        window.addstr('\n')
        sp(f"2. {obj.choice2}", window)
        window.addstr('\n')
        sp("Please enter your choice: (int)", window)
    elif obj.__class__.__name__ == "fight":
        for w in obj.text:
            out.append(w)
        for lines in out:
            sp(lines, window)
            window.addstr('\n')
    elif obj.__class__.__name__ == "intro":
        for w in obj.text:
            out.append(w)
        for lines in out:
            sp(lines, window)
            window.addstr('\n')
    else:
        sp("Files corrupted. Please reinstall the game.", window)
        

def scroll_print(line: str, window: curses.window) -> None:
    window.addstr(line)
    window.refresh()
    time.sleep(0.01)
    

def main(stdscr) -> None:

    def set_terminal_size():
        # For macOS
        os.system('osascript -e \'tell application "Terminal" to set size of window 1 to {740, 400}\'')

    def gather_input() -> None:
        global key
        key = 'Placeholder'

        while key == 'Placeholder' or key == '':
            input_win.clear()
            input_box.edit()
            key = input_box.gather().strip().lower()
            input_win.clear()

            if key == '':
                text_win.clear()
                item_ref()
                text_win.addstr('\n\n')

                for c in "No blank inputs, adventurer.":
                    text_win.addstr(c, red_black | curses.A_BOLD)
                    text_win.refresh()
                    time.sleep(0.02)

        if key.lower().strip() == "quit": # save and exit
            curses.nocbreak()
            save(local_data)
            quit()

        elif key.lower().strip() == "save":
            save(local_data)


    set_terminal_size()

    curses.cbreak()

    stdscr.clear()
    stdscr.refresh()

    stdborder = curses.newwin(26, 104, 0, 0)
    stdborder.border()
    stdborder.refresh()

    tempwin = curses.newwin(24, 102, 1, 1)
    tempwin.nodelay(True)

    for c in r"""
          ___           ___           ___           ___      
         /  /\         /  /\         /  /\         /  /\         Game by:
        /  /::\       /  /:/        /  /::\       /  /:/         Icecreambobcat
       /  /:/\:\     /  /:/        /__/:/\:\     /  /:/          ft. Moshyking as the voice actor
      /  /:/  \:\   /  /:/        _\_ \:\ \:\   /  /::\____      (Planned for 1.0.0, at least)
     /__/:/ \__\:| /__/:/     /\ /__/\ \:\ \:\ /__/:/\:::::\     (As for now, we're at 0.5.0 :skull:)
     \  \:\ /  /:/ \  \:\    /:/ \  \:\ \:\_\/ \__\/~|:|~~~~     
      \  \:\  /:/   \  \:\  /:/   \  \:\_\:\      |  |:|         As the dusk rolls over
       \  \:\/:/     \  \:\/:/     \  \:\/:/      |  |:|         Evening falls upon the land
        \__\::/       \  \::/       \  \::/       |__|:|         The stars twinkle in the sky
            ~~         \__\/         \__\/         \__\|         Find your truth. Find your way.
                      
            Press any alphanumeric key to continue...       
                   
            

                            Sure hope you have a great time playing,
                            because I sure as hell didn't enjoy making this.
                            - The Developer
                   
                   """:
        tempwin.addstr(c)
        time.sleep(0.002)
        tempwin.refresh()

    while tempwin.getch() != -1:
        pass

    tempwin.nodelay(False)
    txt = tempwin.getkey()
    if not txt.isalnum(): # because launching it in the mac terminal has this dumb bug of pressing some weird key
        tempwin.getch()

    tempwin.clear()
    tempwin.refresh()
    stdborder.clear()
    stdborder.refresh()

    global main_win, text_win, main_border, text_border, input_win, text_store

    global text_store
    text_store = init_all()

    local_data = {}

    save_data = read()

    if save_data != {}:
        local_data: dict[str, typing.Any] = save_data

    else:
        local_data['first_play'] = True
        local_data['player'] = player('')

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    red_black = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    green_black = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    yellow_black = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    cyan_black = curses.color_pair(4)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    blue_black = curses.color_pair(5)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    white_black = curses.color_pair(6)


    stdscr.clear()

    main_win = curses.newwin(24, 60, 1, 43)
    text_win = curses.newwin(24, 40, 1, 1)
    input_win = curses.newwin(10, 40, 15, 1)
    main_border = curses.newwin(26, 62, 0, 42)
    text_border = curses.newwin(26, 42, 0, 0)

    input_box = textpad.Textbox(input_win, insert_mode=True)


    main_win.attron(cyan_black)
    text_win.attron(green_black)
    text_border.attron(green_black)
    main_border.attron(cyan_black)


    main_border.border()
    text_border.border()

    main_border.refresh()
    text_border.refresh()

    main_win.nodelay(True)
    text_win.nodelay(True)
    input_win.nodelay(True)

    if local_data['first_play'] == True:
        for c in "Welcome to the game!\nPress any key to continue and type 'quit' to save and exit.\n\nIf you already have a save file, please type 'recreate'.":
            main_win.addstr(c)
            main_win.refresh()
            time.sleep(0.01)

    if local_data['first_play'] == False:
        for c in f"Welcome back, {local_data['name']}!\nSure hope you're ready for more adventure.\nTo reset, quit and run 'reset.py'.":
            main_win.addstr(c)
            main_win.refresh()
            time.sleep(0.01)

    for c in "You'll type your input here.\nPress Ctrl+G to confirm inputs.\nType 'save' to well, save.":
        text_win.addstr(c)
        text_win.refresh()
        time.sleep(0.01)
    
    main_win.refresh()
    text_win.refresh()

    input_win.move(0, 0)

    while input_win.getch() != -1:
        pass


    text_win.nodelay(False)

    if local_data['first_play'] == True:
        text_win.getch()

    text_win.nodelay(True)

    input_win.attron(white_black)



    if local_data['first_play'] == True:
        text_win.addstr('\n\n')

        for c in "Please enter your name:\nMaximum 16 characters.":
            text_win.addstr(c, red_black | curses.A_BOLD)
            text_win.refresh()
            time.sleep(0.01)

        while True: 
            input_win.clear()
            input_box.edit()
            name = input_box.gather().strip()
            input_win.clear()

            if name.lower() == "quit":
                curses.nocbreak()
                save(local_data)
                quit()

            elif name.lower() == "recreate":
                recreate = recreate_player(save_data)
                if recreate.name == "" or len(recreate.name) > 16:
                    text_win.clear()
                    text_win.addstr("Please enter your name:\nMaximum 16 characters.")
                    text_win.addstr('\n\n')
                    for c in "No save file found/savename too long.\nPlease enter your name.":
                        text_win.addstr(c, red_black | curses.A_BOLD)
                        text_win.refresh()
                        time.sleep(0.01)
                    continue

                local_data['first_play'] = False
                local_data['player'] = recreate
                local_data['name'] = local_data['player'].name
                input_win.clear()
                break

            elif name != "" and len(name) <= 16:
                local_data['first_play'] = False
                local_data['player'] = player(name)
                local_data['name'] = local_data['player'].name
                input_win.clear()
                break

            elif name == "" or len(name) > 16:
                text_win.clear()
                text_win.addstr("Please enter your name:\nMaximum 16 characters.")
                text_win.addstr('\n\n')

                for c in "Please enter a shorter name.\nNo blank names either, nameless.":
                    text_win.addstr(c, red_black | curses.A_BOLD)
                    text_win.refresh()
                    time.sleep(0.01)
                continue


    def item_ref() -> None:
        text_win.clear()
        for c in "Items: ":
            scroll_print(c, text_win)

        for item in local_data['player'].items:
            text_win.addstr('\n')

            for c in item:
                scroll_print(c, text_win)


    main_win.attron(red_black | curses.A_BOLD)

    for c in f"\n\nPress any key to continue...\n\nMay your journey be eventful, ":
        scroll_print(c, main_win)

    while input_win.getch() != -1:
        pass

    main_win.attron(yellow_black | curses.A_UNDERLINE)
    name_ln = f"{local_data['name']}"
    for c in name_ln:
        scroll_print(c, main_win)

    while input_win.getch() != -1:
        pass

    main_win.attroff(yellow_black | curses.A_UNDERLINE)
    main_win.attron(red_black | curses.A_BOLD)
    main_win.addstr("!")
    main_win.refresh()
    main_win.attroff(red_black | curses.A_BOLD)
    main_win.attron(cyan_black)
    input_win.move(0, 0)
    input_win.nodelay(False)
    input_win.getch()
    input_win.nodelay(True)

    
    while True: # game loop: build the rest in here
        main_win.nodelay(True)
        text_win.nodelay(True)
        input_win.nodelay(True)

        main_win.clear()
        main_win.refresh()

        index = local_data['player'].story_index
        obj = text_store[index]

        display(index, main_win)
        item_ref()

        if obj.__class__.__name__ == 'story' and obj.pointer == obj.index:
            for c in "\n\nWell, that does it.\nGo home to your kids, they're still waiting for you.\n\nPress any key to quit.":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            input_win.getch()
            input_win.nodelay(True)
            break

        if obj.__class__.__name__ == 'intro' and obj.pointer == obj.index:
            for c in "\n\nWell, that does it.\nGo home to your kids, they're still waiting for you.\n\nPress any key to quit.":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            input_win.getch()
            input_win.nodelay(True)
            break

        if obj.__class__.__name__ == 'question' and obj.pointer1 == obj.index and obj.pointer2 == obj.index:
            for c in "\n\nWell, that does it.\nGo home to your kids, they're still waiting for you.\n\nPress any key to quit.":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            input_win.getch()
            input_win.nodelay(True)
            break

        if obj.__class__.__name__ == 'fight' and obj.pointer1 == obj.index and obj.pointer2 == obj.index and obj.pointer3 == obj.index:
            for c in "\n\nWell, that does it.\nGo home to your kids, they're still waiting for you.\n\nPress any key to quit.":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            input_win.getch()
            input_win.nodelay(True)
            break

        if obj.__class__.__name__ == 'intro':
            for c in "\n\nPress any key to continue...\n\nPress ESC to save and quit.":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            esc = input_win.getch()
            if esc == 27:
                break
            elif esc != -1:
                local_data['player'].story_index = obj.pointer
                continue
            input_win.nodelay(True)
            
        elif obj.__class__.__name__ =='story':
            for c in "\n\nPress any key to continue...\n\nPress ESC to save and quit.":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)
                
            while input_win.getch() != -1:
                pass
            
            input_win.nodelay(False)
            esc = input_win.getch()
            if esc == 27:
                break
            elif esc != -1:
                local_data['player'].story_index = obj.pointer
                continue
            input_win.nodelay(True)

        elif obj.__class__.__name__ == 'question':
            gather_input()
            output = ''
            if key == '1':
                output = obj.choice1
            elif key == '2':
                output = obj.choice2
            result = obj.check(output)

            if result == ["Invalid input", index]:
                for c in "\n\nInvalid input. Please try again.":
                    text_win.addstr(c, red_black | curses.A_BOLD)
                    text_win.refresh()
                    time.sleep(0.01)
                time.sleep(2)
                continue
            if result == [obj.result1, obj.pointer1]:
                main_win.addstr('\n\n')
                for c in obj.result1:
                    scroll_print(c, main_win)

                main_win.addstr('\n\n')
                for c in "Press any key to continue...":
                    scroll_print(c, main_win)
                
                while input_win.getch() != -1:
                    pass

                input_win.nodelay(False)
                input_win.getch()
                input_win.nodelay(True)

                local_data['player'].story_index = obj.pointer1

            elif result == [obj.result2, obj.pointer2]:
                main_win.addstr('\n\n')
                for c in obj.result2:
                    scroll_print(c, main_win)

                main_win.addstr('\n\n')
                for c in "Press any key to continue...":
                    scroll_print(c, main_win)

                while input_win.getch() != -1:
                    pass

                input_win.nodelay(False)
                input_win.getch()
                input_win.nodelay(True)

                local_data['player'].story_index = obj.pointer2

    
        elif obj.__class__.__name__ == 'fight':
            for c in "\n\nPress any key to continue...\n\nPress ESC to save and quit.":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)
            
            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            esc = input_win.getch()
            if esc == 27:
                break
            input_win.nodelay(True)

            main_win.clear()
            main_win.refresh()

            for c in "Roll for initiative!":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            for c in "\nPress any key to roll 2d20...":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            input_win.getch()
            input_win.nodelay(True)

            roll = roll_dice(20, 2, "max")

            for c in f"\nYou rolled a {roll}!":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)
            

            for c in "\n\nRoll for stealth!":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            for c in "\nPress any key to roll 2d6...":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            input_win.getch()
            input_win.nodelay(True)

            roll2 = roll_dice(6, 2, "min")

            for c in f"\nYou rolled a {roll2}!":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            for c in "\n\nRoll for damage!":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            for c in "\nPress any key to roll 3d4...":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            input_win.getch()
            input_win.nodelay(True)

            roll3 = roll_dice(4, 3, "sum")

            for c in f"\n\nYou rolled a {roll3}!":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            if roll + roll2 + roll3 >= 36:
                out = 1
            elif roll + roll2 + roll3 >= 20:
                out = 2
            else:
                out = 3

            for c in "\n\nPress any key to continue...":
                main_win.addstr(c)
                main_win.refresh()
                time.sleep(0.01)

            while input_win.getch() != -1:
                pass

            input_win.nodelay(False)
            input_win.getch()
            input_win.nodelay(True)

            if 'Cheat dice' in local_data['player'].items:
                main_win.clear()
                for c in "You have some weighted dice!\nWould you like to use it? (y/n)":
                    scroll_print(c, main_win)
                
                while True:
                    gather_input()
                    if key == 'y':
                        local_data['player'].items.remove('Cheat dice')
                        out = 1
                        break
                    elif key == 'n':
                        pass
                        break
                    else:
                        for c in "Invalid input. item not used.":
                            text_win.addstr(c, red_black | curses.A_BOLD)
                            text_win.refresh()
                            time.sleep(0.01)
                        time.sleep(2)
                        text_win.clear()
                        item_ref()
                        continue

            if out == 1:
                local_data['player'].story_index = obj.pointer1

                main_win.addstr('\n\n')
                for c in obj.outcome1:
                    scroll_print(c, main_win)

                main_win.addstr('\n\n')
                for c in "Press any key to continue...":
                    scroll_print(c, main_win)

                while input_win.getch() != -1:
                    pass

                input_win.nodelay(False)
                input_win.getch()
                input_win.nodelay(True)

            elif out == 2:
                local_data['player'].story_index = obj.pointer2
                
                main_win.addstr('\n\n')
                for c in obj.outcome2:
                    scroll_print(c, main_win)

                main_win.addstr('\n\n')
                for c in "Press any key to continue...":
                    scroll_print(c, main_win)
                
                while input_win.getch() != -1:
                    pass

                input_win.nodelay(False)
                input_win.getch()
                input_win.nodelay(True)

            elif out == 3:
                local_data['player'].story_index = obj.pointer3

                main_win.addstr('\n\n')
                for c in obj.outcome3:
                    scroll_print(c, main_win)
                    
                main_win.addstr('\n\n')
                for c in "Press any key to continue...":
                    scroll_print(c, main_win)

                input_win.nodelay(False)
                input_win.getch()
                input_win.nodelay(True)

                while input_win.getch() != -1:
                    pass

            else: 
                text_win.addstr('\n\n')
                for c in "Invalid result. Please try again.":
                    text_win.addstr(c, red_black | curses.A_BOLD)
                    text_win.refresh()
                    time.sleep(0.01)

                time.sleep(2)

        input_win.move(0, 0)

    
    save(local_data)
    quit()


        
            
def reset() -> None:
    directory = os.getcwd()
    os.system(f'cd {directory} && rm -f save.dat && touch save.dat')


def launch() -> None:
    directory = os.getcwd()
    os.system(f'osascript -e \'tell application "Terminal" to do script "cd {directory} && python3 main.py && exit"\'')


if __name__ == "__main__":
    wrapper(main)