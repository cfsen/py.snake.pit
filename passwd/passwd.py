import os
import random

class passwd_trainer:
    def __init__(self):
        self.passwd = None
        self.difficulty = 0
        self.streak = 0
        self.threshold = 3
        self.mask = []

    def status(self):
        print(f"Streak: {self.streak} | Difficulty: {self.difficulty}")

    def generate_mask(self):
        self.mask = [x for x in range(len(self.passwd))]
        random.shuffle(self.mask)

    def scramble_pwd(self):
        t = list(self.passwd)
        if(self.difficulty >= len(self.passwd)):
            for k,x in enumerate(t):
                t[k] = "*"
        elif(self.difficulty >= 1 and self.difficulty < len(self.passwd)):
            for x in range(self.difficulty):
                t[self.mask[x]] = "*"
        print("".join(t))

    def update_state(self, i):
        if(i == self.passwd): self.streak += 1
        else: self.streak -= 1

        if(self.streak == self.threshold):
            self.difficulty += 1
            self.streak = 0
        elif(self.streak == -self.threshold):
            self.difficulty -= 1
            self.streak = 0

if(__name__ == "__main__"):
    p = passwd_trainer()
    while True:
        os.system("cls")
        print("(Quit at any time using: \":q!\")")

        if(p.passwd is None):
            print("Set a password to practice (will be displayed in plain text):")
            p.passwd = input()
            if(p.passwd == ":q!"): break
            p.generate_mask()
            continue

        p.status()
        p.scramble_pwd()
        i = input()
        if(i == ":q!"): break
        p.update_state(i)
