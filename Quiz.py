from printd import printd
from correctMessages import correctMessages
import random

class Quiz:
    def __init__(self, qBase):
        self.qBase = qBase
        self.right = 0
        self.wrong = 0
        self.menu()
        self.take()
        self.grade()
           
    def menu(self):
        printd("How would you like to be tested?")
        printd("[0] Multiple Choice")
        choices = list("0")
        self.qType = input(">>>> ")
        while(self.qType not in choices):
            printd("Sorry that wasn't a valid option. Try again.")
            self.qType = input(">>>> ")
        printd("The quiz is currently {} questions long.".format(len(self.qBase.questions)))
        printd("Would you like to limit its size?")
        printd("[0] No limit (take the whole quiz)")
        printd("[1] Limit to 10 questions")
        printd("[2] Limit to 20 questions")
        choices = list("0123")
        limitChoice = input(">>>> ")
        while(limitChoice not in choices):
            printd("Sorry that wasn't a valid option. Try again.")
            limitChoice = input(">>>> ")
        if limitChoice == '1' and len(self.qBase.questions) > 10:
            self.limit = 10
            self.questions = random.sample(list(self.qBase.questions.keys()), 10)
        elif limitChoice == '2' and len(self.qBase.questions) > 20:
            self.limit = 20
            self.questions = random.sample(list(self.qBase.questions.keys()), 20)
        else:
            self.limit = len(self.qBase.questions)
            self.questions = self.qBase.questions.keys()

    def take(self):
        for given in self.questions:
            printd("\n")
            printd("="*40)
            printd("\n")
            if not self.askMC(given):
                return

    def askMC(self, given):
            printd("GIVEN: " + given)
            answers = random.sample(list(self.qBase.questions.values()), 4)
            answers[random.randint(0, 3)] = self.qBase.questions[given]
            options = list("ABCDQ")
            for x in range(0, 4):
                printd(options[x] + ": " + answers[x].answer)
            choice = input(">>>> ").upper()
            while choice not in options:
                printd("Sorry that wasn't an option--try again")
                choice = input(">>>> ").upper()
            if choice == "Q":
                return False
            if answers[options.index(choice)].answer == self.qBase.questions[given].answer:
                printd(random.choice(correctMessages))
                self.right += 1
                self.qBase.questions[given].getRight()
            else:
                printd("Sorry, that was wrong")
                printd("Correct answer: " + self.qBase.questions[given].answer)
                self.wrong += 1
                self.qBase.questions[given].getWrong()
            return True

    def grade(self):
        self.total = self.right + self.wrong
        if self.total == 0:
            printd("You didn't finish a single question.")
        else:
            printd("You got {} out of {} correct.".format(self.right, self.total))
            printd("This is {0:.2f}%".format(100 * self.right / self.total))
        choices = list("01")
        printd("Print question rating results?")
        printd("[0] No")
        printd("[1] Yes")
        choice = input(">>>> ")
        while(choice not in choices):
            printd("Sorry that wasn't a valid option. Try again.")
            choice = input(">>>> ")
        if choice == '1':
            questions = list(self.qBase.questions.values())
            questions = sorted(questions, key=lambda q: q.getScore())
            for question in questions:
                printd(question.getProgress())
