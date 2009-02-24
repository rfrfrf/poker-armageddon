from bot import Bot
from poker_game import Action

class ExampleBot(Bot):
    def turn(self):
        self.output("my turn")
        self.output("%d events in queue" % len(self.event_queue))
        self.event_queue = []
        if self.id == 1:
            return Action('fold')
        else:
            return Action('raise', amount=20)
    
    def output(self, msg):
        print "ExampleBot(%d): %s" % (self.id, msg)