import map
import pickle
import curses
import csv
from curses import wrapper


class player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        
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
        questions =[interactable(line[0], line[1], line[3], line[4], line[5]) for line in questioncsv]
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


def save() -> None:

    local_data = NotImplemented
    # note to implement dict for local data saves 

    with open('save.bin', 'wb') as save:
        save.write(pickle.dumps(local_data))


def read() -> None:
    with open('save.bin', 'rb') as save:
        local_data = pickle.loads(save)

    NotImplemented = local_data


def roll_dice(d, count, type) -> int:
    # where d is sides, count is number of dice, and type is how to combine results
    pass


def fight(scene) -> None:
    # implement a basic fight system where it's essentially a SPR reskin
    # considering what story node the player is at display different dialogue
    pass