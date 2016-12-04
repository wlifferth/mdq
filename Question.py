from collections import deque

class Question:
    def __init__(self, given, answer):
        self.given = given
        self.answer = answer
        self.history = deque(maxlen=10)
 
    def getScore(self):
        weights = [.1, .1, .2, .2, .3, .4, .6, .7, .8, .8]
        if not self.history:
            return -1
        else:
            weightedSum =  sum([score * weight for score, weight in zip(self.history, weights[:len(self.history)])]) / sum(weights[:len(self.history)])
        if len(self.history) < 3 and weightedSum > .2:
            return weightedSum - .2
        return weightedSum

    def getRight(self):
        self.history.extend([1])

    def getWrong(self):
        self.history.extend([0])

    def getProgress(self):
        length = 40
        given = self.given if len(self.given) < length else self.given[:length - 3] + "..."
        if len(self.history) > 0:
            return "{:40s}{:3.2f}:".format(given, self.getScore()) + "#" * int(10 * self.getScore())
        return "{:40s} NYT:".format(given)
