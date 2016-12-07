import fileinput
import dill as pickle
import os
import sys
from Question import Question
from Quiz import Quiz
from collections import deque

from printd import printd

class QBase:
    """
    QBase is the data structure that holds all the questions for a quiz.
    Each time the `quiz` command is invoked with a fileName, QBase checks to see if an appropriate .mdq file exists in the given directory, of the form .[fileName].mdq
    If it does, then it sets itself equal to the instance of QBase found in .[filename].mdq
    Else it reads in all the questions from fileName and initializes itself from that
    """
    def __init__(self, fileName):
        # First, check if an mdq file has been made
        self.mdqFileName = "." + fileName + ".mdq"
        if self.mdqFileName in os.listdir():
            readFile = open(self.mdqFileName, 'rb')
            self.questions = pickle.load(readFile)
            printd("Successfully imported {} questions from {}".format(len(self.questions), self.mdqFileName))
        else:
            self.questions = {}
        answer = ""
        questions = {}
        if fileName in os.listdir():
            readFile = open(fileName)
            for line in readFile.readlines():
                if line[0:2] == "# ":
                    if answer != "" and given not in questions.keys():
                        questions[given] = Question(given=given, answer=answer.strip())
                    given = line[2:].strip()
                    answer = ""
                elif not line.isspace():
                    answer += line.strip() + "\n"
            if answer != "" and given not in questions.keys():
                questions[given] = Question(given=given, answer=answer)
            for k,v in questions.items():
                if k in self.questions.keys():
                    questions[k].history = self.questions[k].history
            self.questions = questions
            printd("Successfully updated questions to {} from {}".format(len(self.questions), fileName))
        else:
            printd("Error: File {} not found".format(fileName))
            return

    def getWeak(self):
        for given, answer in self.questions.items():
            if answer.getScore() <= 0.8:
                yield given

    def __exit__(self):
        writeFile = open(self.mdqFileName, 'wb')
        pickle.dump(self.questions, writeFile, pickle.HIGHEST_PROTOCOL)
        printd("Successfully wrote {} questions to {}".format(len(self.questions), self.mdqFileName))
