from __future__ import annotations
import abc
import typing
import map
import pickle
import curses
import random
import csv
import json


class player:
    def __init__(self, name: str) -> None:
        self.x = 0
        self.y = 0
        self.items = []
        self.story_stage = 0
        self.lives = 3
        self.name = name
        
    def move(self, move_x: int, move_y: int) -> None:
        if map.map1[move_x][move_y] != 5:
            self.x += move_x
            self.y += move_y
            move_y = 0
            move_x = 0


class interactable:
    def __init__(self,question: str, choice1: str, choice2: str, result1: str, result2: str) -> None:
        # probably just change how the entire thing works and hardcode indexes for story events
        self.question = question
        self.choice1 = choice1
        self.choice2 = choice2
        self.result1 = result1
        self.result2 = result2

    def check(self, choice: str) -> str:
        if choice == self.choice1:
            return self.result1
        if choice == self.choice2:
            return self.result2
        else:
            return "Invalid choice"


class story:
    def __init__(self) -> None:
        pass

class fight:
    def __init__(self) -> None:
        pass
        

def init_questions() -> dict:
    out = {}
    with open('story.csv', newline='') as question_list:
        questioncsv = csv.reader(question_list, delimiter=':', quotechar='"')
        next(questioncsv)
        questions =[interactable(line[0], line[1], line[2], line[3], line[4]) for line in questioncsv]
        counter = 0
        for q in questions:
            out[counter] = q
            counter += 1

    return out


def init_intro() -> dict:
    out = {}
    with open('intro.csv', newline='') as intro:
        introcsv = csv.reader(intro, delimiter=':', quotechar='"')
        next(introcsv)
        counter = 0
        for line in introcsv:
            out[counter] = line
            counter += 1

    return out


def init_story() -> dict:
    out = {}
    with open('story.csv', newline='') as story:
        storycsv = csv.reader(story, delimiter=':', quotechar='"')
        next(storycsv)
        counter = 0
        for line in storycsv:
            out[counter] = line
            counter += 1

    return out


def init_fights() -> dict:
    out = {}
    with open('fights.csv', newline='') as fights:
        fightcsv = csv.reader(fights, delimiter=':', quotechar='"')
        next(fightcsv)
        counter = 0
        for line in fightcsv:
            out[counter] = line
            counter += 1

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

def display_story(player: player, story: dict, index: int) -> None:
    story_text = story[index]
    for line in story_text:
        pass # do something about this later, rest of the display functions are honestly the same
    pass


def display_intro(player: player, intro: dict, index: int) -> None:
    pass


def display_fight(player: player, fight: dict, index: int) -> None:
    pass


def interact(player: player, question: str, choice1: str, choice2: str, result1: str, result2: str) -> str:
    pass
    # display question and choices
    # get user input
    # return result
    # also handle invalid input and other cases where the the type of interaction is not a question
    return ''


def main(stdscr) -> None:
    stdscr.clear()
    main_win = curses.newwin(24, 60, 20, 0)
    text_win = curses.newwin(24, 20, 0, 0)

    while True: # game loop: build the rest in here
        if text_win.getstr() == "quit": # save and exit
            # temp sol: change local_data to global save
            local_data = {}
            save(local_data)
            break
        pass


curses.wrapper(main)


if __name__ == "__main__":
    main(stdscr=curses.initscr())