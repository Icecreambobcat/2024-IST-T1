from __future__ import annotations
import typing
import map
import pickle
import curses
import random
import csv


class player:
    def __init__(self, name: str) -> None:
        """

        Player class to store local runtime data for the player

        Properties:

        x: int - x coordinate of the player
        y: int - y coordinate of the player
        items: list[str] - list of items the player has
        story_index: int - index of the current story text
        lives: int - number of lives the player has
        name: str - name of the player

        """
        self.x = 0
        self.y = 0
        self.items = []
        self.story_index = 0
        self.lives = 3
        self.name = name
        
    def move(self, move_x: int, move_y: int) -> None:
        if map.map1[move_x][move_y] != 5:
            self.x += move_x
            self.y += move_y
            move_y = 0
            move_x = 0

    def packege_data(self) -> dict[str, typing.Any]:
        return {
            'x': self.x,
            'y': self.y,
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


def init_all() -> dict[int, dict[int, object]]:
    out = {}

    """
    
    Function to initialize all data from csv files

    This function takes the outputs of the other functions and combines them into one dictionary
    
    """

    def init_questions() -> dict:
        out = {}
        with open('questions.csv', 'r') as file:
            questions_csv = csv.reader(file)
            next(questions_csv)   
            for line in questions_csv:
                obj = question(line[0].split('#'), line[1], line[2], line[3], line[4], int(line[5]), int(line[6]), int(line[7]))
                out [obj.index] = obj

        return out

    def init_intro() -> dict:
        out = {}
        with open('intro.csv', 'r') as file:
            intro_csv = csv.reader(file)
            next(intro_csv)
            for line in intro_csv:
                obj = intro(line[0].split('#'), int(line[1]), int(line[2]))
                out[obj.index] = obj

        return out

    def init_story() -> dict:
        out = {}
        with open('story.csv', 'r') as file:
            story_csv = csv.reader(file)
            next(story_csv)
            for line in story_csv:
                obj = story(line[0].split('#'), int(line[1]), int(line[2]))
                out[obj.index] = obj

        return out

    def init_fights() -> dict:
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


def save(local_data: dict[str, typing.Any]) -> None:
    try:
        with open('save.bin', 'wb') as save_file:
            pickle.dump(local_data, save_file)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


def read() -> dict[str, typing.Any]:
    try:
        with open('save.bin', 'rb') as save_file:
            local_data = pickle.load(save_file)
            if local_data is None:
                return {'key': None}
            else: return local_data
    except FileNotFoundError:
        print("The file 'save.bin' does not exist.")
        return {}
    except pickle.UnpicklingError:
        print("An error occurred while loading data.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}


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


def move_player(player: player, mvmt: str) -> None:
    if mvmt == "up":
        move_x = 0
        move_y = -1
    elif mvmt == "down":
        move_x = 0
        move_y = 1
    elif mvmt == "left":
        move_x = -1
        move_y = 0
    elif mvmt == "right":
        move_x = 1
        move_y = 0
    player.move(player.x + move_x, player.y +  move_y)


def recreate_player(data: dict[str, typing.Any]) -> player:
    p = player(data['name'])
    p.x = data['x']
    p.y = data['y']
    p.items = data['items']
    p.story_index = data['story_index']
    p.lives = data['lives']
    return p


def display(index: int, window: curses.window) -> None:
    if text_store[index].__class__.__name__ == "story":
        out = []
        for w in text_store[index].text:
            out.append(w)
        for lines in out:
            window.addstr(lines) # figure how to make it look good
        pass
    elif text_store[index].__class__.__name__ == "question":
        for w in text_store[index].question:
            pass
        pass
    elif text_store[index].__class__.__name__ == "fight":
        pass
    elif text_store[index].__class__.__name__ == "intro":
        pass
    else:
        pass


def main(stdscr) -> None:
    stdscr.clear()
    main_win = curses.newwin(24, 60, 20, 0)
    text_win = curses.newwin(24, 20, 0, 0)

    save_data = read()

    if save_data and save_data != {}:
        local_data = save_data 
    elif save_data['first_run'] == True:
        local_data = {
            'first_run' : False
        }
    elif save_data == {}: # if error
        # prompt user to repair files or build new save
        # should prompt user to rm -rf the directory and reinstall
        # automate through zsh script
        return None


    global text_store
    text_store = init_all()

    while True: # game loop: build the rest in here

        # when am i gonna write the game lmao

        if text_win.getstr() == "quit": # save and exit
            # temp sol: change local_data to global save
            local_data = {}
            save(local_data)
            break
        pass


curses.wrapper(main)


if __name__ == "__main__":
    main(stdscr=curses.initscr())