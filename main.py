import map
import pickle
import curses


class player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        
    def move(self, move_x, move_y) -> None:
        self.x += move_x
        self.y += move_y


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
        

def init_map(file, level) -> list:
    map = []
    for line in file.level:
        map.append(line)

    return map

