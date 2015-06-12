# Introduction #

This is a Python framework to fight poker bots against each other.  It supports bots in C++ and Java using [protocol buffers](http://code.google.com/apis/protocolbuffers/docs/overview.html).  For how to use C++ and Java see LanguagesThatAreNotPython.  I recommend that you try this introduction page first to get vaguely familiar with the Python side before using another language.

It's a little rough around the edges and may contain bugs.

To try it out, click on the source tab up top, check it out over SVN and run 'python main.py' in the folder you checked out.  You can [download Python](http://www.python.org/download/releases/2.6.1/) for your operating system if you don't already have it.

# Most Basic Bot #

```
from bot import Bot
from poker_game import Action

class FoldBot(Bot):
    def turn(self):
        print "Bot %d events in queue:" % self.id
        for event in self.event_queue:
            print event
        self.event_queue = []
        return Action('fold')
```

This bot ignores whatever is happening and folds every time.  A fancier bot would use some of the other actions.

The actions and events are instances of objects with the specified properties implemented as member variables.  The type of each is stored in the .type variable.  For instance the following Action:
```
Action('raise',amount=2)
```

Has the following properties:
```
Action.type == 'raise'
Action.amount == 2
```

Events are similar, your bot receives an event for everything that goes on at the table (except cards dealt to other players).  Events can be broadcast to all players, or sent to specific ones.  The 'deal' event is sent to each player individually, since it contains the cards that player is dealt.  The 'bad\_bot' event is the only other non-broadcast event in the Python interface (there is a 'your\_turn' event in the protocol buffer one).

## Actions ##

  * type 

&lt;properties&gt;


  * 'fold',
    * fold means you quit this round
  * 'call',
    * call means you match the current high bet
  * 'raise' amount
    * raise means you match the current high bet and add some amount to it
  * 'check' (not available on first round, except for the big blind)
    * a check is just a pass

## Events ##

  * type 

&lt;properties&gt;


  * 'join' player\_id credits
  * 'new\_round'
  * 'button' player\_id
  * 'big\_blind' player\_id
  * 'small\_blind' player\_id
  * 'deal' cards
  * 'flop' cards
  * 'turn' card
    * fourth community card
  * 'river' card
    * fifth community card
  * 'action' player\_id=number action=Action
  * 'adjust\_credits'  player\_id=number amount=number (positive or negative)
  * 'win' player\_id=number rank=number amount=number
    * there is also an adjust\_credits event for this
> > > in the case that there are multiple winners
> > > the rank will indicate who won first, second etc (int, starts at zero)
  * 'end\_of\_round'
  * 'quit' player\_id=number
  * 'bad\_bot' message=string action=Action
    * last action by your bot was determined to be invalid

## Basic Types ##

  * player\_id := number
  * action := Action
  * credits := number
  * message := string
  * card := (value, 'suit') where value is a number 2-14 and suit is a string from ['d', 'h', 's', 'c']
cards := [card, card, ...]