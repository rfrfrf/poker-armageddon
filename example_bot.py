from bot import Bot
from poker_game import Action

class ExampleBot(Bot):
    def turn(self):
        print "Bot %d events in queue:" % self.id
        for event in self.event_queue:
            print event
        self.event_queue = []
        if self.id == 1:
            return Action('fold')
        else:
            return Action('raise', amount=20)