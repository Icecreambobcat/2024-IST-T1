import map
import pickle
import curses
import random
import sys
import csv


class player:
    def __init__(self, name) -> None:
        self.x = 0
        self.y = 0
        self.items = []
        self.story_stage = 0
        self.lives = 3
        self.name = name
        self.first_play = True
        
    def move(self, move_x, move_y) -> None:
        if map.map1[move_x][move_y] != 5:
            self.x += move_x
            self.y += move_y
            move_y = 0
            move_x = 0


class interactable:
    def __init__(self,question, choice1, choice2, result1, result2) -> None:
        self.question = question
        self.choice1 = choice1
        self.choice2 = choice2
        self.result1 = result1
        self.result2 = result2

    def check(self, choice) -> str:
        if choice == self.choice1:
            return self.result1
        if choice == self.choice2:
            return self.result2
        else:
            return "Invalid choice"
        

def init_questions() -> dict:
    out = {}
    with open('story.csv', newline='') as question_list:
        questioncsv= csv.reader(question_list, delimiter=':', quotechar='"')
        questions =[interactable(line[0], line[1], line[2], line[3], line[4]) for line in questioncsv]
        counter = 0
        for q in questions:
            out[counter] = q
            counter += 1

    return out


def init_intro() -> list:
    out = []
    with open('intro.csv', newline='') as intro:
        for line in intro:
            out.append(line)

    return out


def init_story() -> dict:
    out = {}
    with open('story.csv', newline='') as story:
        storycsv = csv.reader(story, delimiter=':', quotechar='"')
        counter = 0
        for line in storycsv:
            out[counter] = line
            counter += 1

    return out


def save(local_data: dict) -> None:
    try:
        with open('save.bin', 'wb') as save_file:
            pickle.dump(local_data, save_file)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


def read() -> dict:
    try:
        with open('save.bin', 'rb') as save_file:
            local_data = pickle.load(save_file)
        return local_data
    except FileNotFoundError:
        print("The file 'save.bin' does not exist.")
        return {}
    except pickle.UnpicklingError:
        print("An error occurred while loading data.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}


def roll_dice(d, count, type) -> int:
    # where d is sides, count is number of dice, and type is how to combine results
    if d and count is int and type is str:
        if type == "sum":
            return sum([random.randint(1, d) for i in range(count)])
        if type == "max":
            return max([random.randint(1, d) for i in range(count)])
        if type == "min":
            return min([random.randint(1, d) for i in range(count)])
        else:
            return 0
    else: 
        return 0


def fight(scene) -> None:
    # implement a basic fight system where it's essentially a SPR reskin
    # maybe could also implement with battle class idk
    # considering what story node the player is at display different dialogue
        pass


def main(stdscr) -> None:
    stdscr.clear()
    main_win = curses.newwin(24, 60, 20, 0)
    text_win = curses.newwin(24, 20, 0, 0)

    while True:
        if text_win.getstr() == "quit":
            # temp sol
            local_data = {}
            save(local_data)
            break
        pass


curses.wrapper(main)


if __name__ == "__main__":
    main(stdscr=curses.initscr())