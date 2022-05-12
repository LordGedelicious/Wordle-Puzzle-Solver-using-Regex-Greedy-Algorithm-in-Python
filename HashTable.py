from HashMap import HashMap
import random


class PriorityHashQueue:
    def __init__(self):
        self.queue = []

    def returnWordIdx(self, index):
        return self.queue[index].get_word()

    def returnMatchValueIdx(self, index):
        return self.queue[index].get_match_value()

    def returnLength(self):
        return len(self.queue)

    def returnContents(self):
        for i in self.queue:
            print(i.get_word(), i.get_match_value())
        print()

    def returnRandomValue(self):
        return self.queue[random.randint(0, self.returnLength() - 1)]

    def returnTopValue(self):
        return self.queue[0]

    def enqueue(self, word, match_value):
        if (self.returnLength() == 0):
            print("enqueue pas len 0")
            print(self.returnLength())
            print()
            self.queue.append(HashMap(word, match_value))
        else:
            newEntry = HashMap(word, match_value)
            for i in range(self.returnLength()):
                if (i == self.returnLength() - 1 or match_value == 0):
                    print("enqueue di awal pas lennya {}".format(
                        self.returnLength()))
                    self.returnContents()
                    self.queue.append(newEntry)
                    break
                elif (match_value > self.queue[i].get_match_value()):
                    print("enqueue di akhir pas lennya {}".format(
                        self.returnLength()))
                    self.returnContents()
                    self.queue.insert(i, newEntry)
                    break

    def dequeue(self, index):
        return self.queue.pop(index)
