import time

from poker_game import PokerGame

def main():
   from example_bot import ExampleBot
   bots = [ExampleBot, ExampleBot]
   game = PokerGame(bots=bots)
   start_time = time.time()
   outcome = game.run()
   end_time = time.time()
   print "Result:", outcome
   print "Time elapsed:", (end_time - start_time), "seconds"

if __name__ == "__main__":
    import sys
    sys.exit(main())