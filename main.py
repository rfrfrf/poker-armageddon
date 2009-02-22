import time

from poker_game import PokerGame

def main():
   from example_bots.example_bot import ExampleBot
   #from example_bots.protobot.cpp.foldbot_cpp import FoldBot
   from example_bots.protobot.java.foldbot_java import FoldBot
   bots = [ExampleBot, FoldBot]
   game = PokerGame(bots=bots)
   start_time = time.time()
   outcome = game.run()
   end_time = time.time()
   print "Result:", outcome
   print "Time elapsed:", (end_time - start_time), "seconds"

if __name__ == "__main__":
    import sys
    sys.exit(main())
