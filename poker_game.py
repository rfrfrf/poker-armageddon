import random
import copy
import logging
import collections

from cards import Deck, n_card_rank

# TODO: basic game
# TODO: side-pot splitting
# TODO: correct handling of heads_up -> button selection etc
# TODO: logging module
# TODO: player wrapper with credits, id, __str__ etc, move action sanitizing into there
# TODO: example bot
# TODO: protocol bot

class KeywordObject(object):
    def __init__(self, type, **kwargs):
        self.type = type
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
        print "created: %s" % self.__str__()
            
    def __str__(self):
        result = "<%s type=%s%s>"
        attributes = ""
        for k,v in sorted(self.__dict__.iteritems()):
            if k.startswith('_') or k == 'type':
                continue
            attributes += " %s=%s" % (k, v)
        return result % (self.__class__.__name__, self.type, attributes)

# event format:
# <type> <properties>
# 'join' player_id credits
# 'new_round'
# 'button' player_id
# 'big_blind' player_id
# 'small_blind' player_id
# 'deal' cards
# 'flop' cards
# 'turn' card  # fourth community card
# 'river' card # fifth community card
# 'action' player <Action>
# 'adjust_credits'  player (+/-)amount
# 'win' player rank amount -> there is also an adjust_credits event for this
#                             in the case that there are multiple winners
#                             the rank will indicate who won first, second etc (int)
# 'end_of_round'
# 'quit' player_id
# 'bad_bot' message <Action> -> last action by your bot was determined to be invalid
# 
class Event(KeywordObject):
    pass

# action format:
# 'fold',
#    fold means you quit this round
# 'call', 
#    call means you match the current high bet
# 'raise' amount
#    raise means you match the current high bet and add some amount to it
# 'check' (not available on first round, except for the big blind)
#    a check is just a pass
        
class Action(KeywordObject):
    pass

class Pot(object):
    def __init__(self):
        self.current_bet = 0
        self.player_total = {}
        self.all_in = {}
        
    @property
    def total(self):
        return sum(amount for amount in self.player_total.values())
        
    def bet(self, player, amount, all_in=False):
        self.player_total.setdefault(player, 0)
        player_bet = self.player_total[player] + amount
        if self.all_in:
            if self.all_in.get(player, False):
                raise AlreadyAllIn(player)
            self.all_in[player] = True
        else:
            if player_bet > self.current_bet:
                # raise
                self.current_bet = player_bet
            elif player_bet < self.current_bet:
                raise InsufficientBet(player, amount)
            else:
                # call
                pass
        self.player_total[player] = player_bet
        
    def split(self, hand_ranks):
        if len(self.all_in) == 0:
            # case with no all in players, easy
            # see if there was a tie
            raise NotImplementedError
            max_rank = max(hand_ranks)
            results = []
            winners = [player for hand_rank, player in hand_ranks if hand_rank == max_rank]
            # TODO: if not evenly divisible, extra credits go to the player
            # first after the dealer button
            credits = self.total / len(winners)
            for winner in winners:
                results.append((winner, credits))
            return results
        else:
            hand_ranks = list(revered(sorted(hand_ranks)))
            raise NotImplementedError 
        
class WinByDefault(Exception):
    def __init__(self, winner):
        self.winner = winner
        
class InsufficientBet(Exception):
    def __init__(self, player, amount):
        self.player = player
        self.amount = amount
        
class AlreadyAllIn(Exception):
    def __init__(self, player):
        self.player = player

class PokerGame(object):
    def __init__(self, bots, initial_credits=10000, num_decks=1,
            small_blind_amount=10):
        self.players = []
        self.credits = {}
        self.id = {}
        self.deck = Deck()
        # big blind amount is 2x small_blind_amount
        self.small_blind_amount = small_blind_amount
        random.seed() # seed with, hopefully, /dev/urandom
        for id, bot in enumerate(bots):
            bot_instance = bot(id=id, credits=initial_credits, small_blind_amount=self.small_blind_amount, big_blind_amount=self.big_blind_amount)
            self.players.append(bot_instance)
            self.id[bot_instance] = id
            self.credits[bot_instance] = initial_credits
        self.active_players = copy.copy(self.players)
        
    @property
    def big_blind_amount(self):
        return self.small_blind_amount * 2

    def run(self):
        assert(len(self.active_players) > 0)
        
        round_num = 1
        # button is random and goes to the next player (higher index) each round,
        # looping around at the end
        button = random.choice(self.active_players)
        
        # send out join messages
        for player in self.active_players:
            for other_player in self.active_players:
                if player is not other_player:
                    event = Event('join', player_id=self.id[player], credits=self.credits[player])
                    self.send_event(other_player, event)
        
        print "Start of Game State:"
        self.print_state()
                        
        while len(self.active_players) > 1:
            button = self.active_players[(self.active_players.index(button)+1) % len(self.active_players)]
            # determine next blinds, remove any players that are at 0 credits
            # or can't pay the blind
            button = self.remove_losers(button)
            self.broadcast_event(Event('new_round'))
            print "Round:",round_num
            round = Round(self, button)
            round.run()
            print "End of Round State:"
            self.print_state()
            self.broadcast_event(Event('end_of_round'))
            round_num += 1
        print "Game Over"
        winner = self.active_players[0]
        print "Game Winner: %s with credits %d" % (winner, self.credits[winner])
            
    def print_state(self):
        for player in self.active_players:
            print "\t",player,"with credits",self.credits[player]
            
    def remove_losers(self, button):
        # find anyone with no money
        for player in self.active_players:
            if self.credits[player] <= 0:
                if player == button:
                    # figure out next button
                    i = self.active_players.index(player)
                    button_index = (i+1) % len(self.active_players)
                    button = self.active_players[button_index]
                self.remove_loser(player)
                
        return button
    
    def broadcast_event(self, event):
        print "Broadcast Event: %s" % event
        for player in self.active_players:
            player.event_queue.append(event)
            
    def send_event(self, player, event):
        print "Event to player %d: %s" % (self.id[player], event)
        player.event_queue.append(event)
            
    def remove_loser(self, player):
        self.active_players.remove(player)
        self.broadcast_event(Event('quit', player_id=self.id[player]))
        
    def adjust_credits(self, player, amount):
        self.credits[player] += amount
        self.broadcast_event(Event('adjust_credits', player_id=self.id[player], amount=amount))
        
class Round(object):
    def __init__(self, game, button):
        self.game = game
        # make a copy of the deck for this round and shuffle it
        self.deck = copy.copy(game.deck)
        self.deck.shuffle()
        self.players = copy.copy(game.active_players)
        self.button = button
        self.pot = Pot()
        self.all_in = collections.defaultdict(bool)
        
    def run(self):
        self.game.broadcast_event(Event('button', player_id=self.game.id[self.button]))
        # do the blinds
        small_blind, big_blind = self.calculate_blinds(self.button)
        self.game.broadcast_event(Event('small_blind', player_id=self.game.id[small_blind]))
        self.bet(small_blind, self.game.small_blind_amount)
        self.game.broadcast_event(Event('big_blind', player_id=self.game.id[big_blind]))
        self.bet(big_blind, self.game.big_blind_amount)
        
        hole_cards = {}
        # deal each player 2 cards
        for player in self.players:
            hole_cards[player] = self.deck.take(2)
            self.game.send_event(player, Event('deal', cards=hole_cards[player]))
        
        try:
            # first round of betting, no 'check' allowed unless you're the big
            # blind and nobody raised
            self.betting_round(1, self.button, self.pot)
        
            # flop
            community_cards = self.deck.take(3)
            self.game.broadcast_event(Event('flop', cards=community_cards))
        
            self.betting_round(2, self.button, self.pot)
        
            # turn
            turn = self.deck.take_one()
            self.game.broadcast_event(Event('turn', card=turn))
            community_cards.append(turn)
        
            self.betting_round(3, self.button, self.pot)
        
            # river
            river = self.deck.take_one()
            self.game.broadcast_event(Event('river', card=river))
            community_cards.append(river)
        
            # final betting round
            self.betting_round(4, self.button, self.pot)
        except WinByDefault, e:
            player = e.winner
            credits = self.pot.total
            # TODO: win should indicate amount won, (gained over previous round)
            self.game.broadcast_event(Event('win', player_id=self.game.id[player], rank=1, amount=credits))
            self.game.adjust_credits(player, credits)
        else:
            ranking = self.determine_ranking(community_cards, hole_cards)
            for player, credits in self.pot.split(ranking):
                self.game.broadcast_event(Event('win', player_id=self.game.id[player], amount=credits))
                self.game.adjust_credits(player, credits)
                
    def run_turn(self, player):
        try:
            return player.turn()
        except Exception, e:
            self.game.send_event(player, Event('bad_bot', message='bot threw an exception: ' + str(e), action=None))
            return Action('fold')
            
    def get_player(self, index):
        return self.players[index % len(self.players)]
            
    def calculate_blinds(self, button):
        i = self.players.index(button)
        if len(self.players) == 2:
            small_blind = button
            big_blind = self.get_player(i+1)
        else:
            small_blind = self.get_player(i+1)
            big_blind = self.get_player(i+2)
        return small_blind, big_blind
        
    def bet(self, player, amount):
        if self.game.credits[player] < amount:
            self.all_in[player] = True
            amount = self.game.credits[player]
        # if the player is all in, indicate that to the pot
        self.pot.bet(player, amount, self.all_in[player])
        self.game.adjust_credits(player, -amount)
        
    def next_player(self, player):
        return self.get_player(self.players.index(player)+1)
        
    def betting_round(self, n, button, pot):
        player_bets = {}
        has_bet = {}
        
        for player in self.players:
            player_bets[player] = 0
            
        small_blind, big_blind = self.calculate_blinds(button)
        if n == 1:
            current_player = self.get_player(self.players.index(big_blind) + 1)
            player_bets[small_blind] = self.game.small_blind_amount
            player_bets[big_blind] = self.game.big_blind_amount
            current_bet = self.game.big_blind_amount
        else:
            current_player = self.get_player(self.players.index(button) + 1)
            current_bet = 0
            
        while True:
            # if player is all in, he does not get another turn
            if self.all_in[current_player]:
                print "Player is all in, skipping", current_player
                current_player = self.next_player(current_player)
                continue
            
            action = current_player.turn()
            def warn(message):
                self.game.send_event(current_player, Event('bad_bot', message=message, action=action))
                
            if action is None or \
                  getattr(action, 'type', None) not in ['fold', 'call', 'raise', 'check'] or \
                  action.type == 'raise' and not hasattr(action, 'amount'):
                warn('invalid action, folding')
                action = Action('fold')
            
            # check that the bet is good
            if action.type == 'call':
                if current_bet == 0:
                    warn('tried to call on zero bet, folding')
                    action = Action('fold')
                elif current_bet == player_bets[current_player]:
                    warn('tried to call but had already bet that amount, should have checked, checking')
                    action = Action('check')
                else:
                    amount_to_bet = current_bet-player_bets[current_player]
                    if self.game.credits[current_player] < amount_to_bet:
                        amount_to_bet = self.game.credits[current_player]
                        self.all_in[current_player] = True
                    self.bet(current_player, amount_to_bet)
                    player_bets[current_player] += amount_to_bet
                    has_bet[player] = True
                    
            if action.type == 'raise':
                if action.amount <=0 or self.game.credits[current_player] < action.amount:
                    warn('invalid raise, folding')
                    action = Action('fold')
                else:
                    amount_to_bet = action.amount
                    if self.game.credits[current_player] == amount_to_bet:
                        amount_to_bet = self.game.credits[current_player]
                        self.all_in[current_player] = True
                    elif self.game.credits[current_player] < amount_to_bet:
                        warn('tried to raise more than player possesses, betting maximum')
                        amount_to_bet = self.game.credits[current_player]
                        self.all_in[current_player] = True
                    current_bet += amount_to_bet
                    self.bet(current_player, amount_to_bet)
                    player_bets[current_player] += amount_to_bet
                    has_bet = {player: True}
                    
            if action.type == 'check':
                # can only check if current bet is zero
                if current_bet != 0:
                    warn('tried to check after bet was made, folding')
                    action = Action('fold')
                else:
                    self.game.broadcast_event(Event('check', player_id=self.game.id[current_player]))
                    has_bet[player] = True
                
            if action.type == 'fold':
                self.game.broadcast_event(Event('fold', player_id=self.game.id[current_player]))
                next_player = self.next_player(current_player)
                self.players.remove(current_player)
                current_player = next_player
            else:
                current_player = self.next_player(current_player)
                
            if len(self.players) == 1:
                winner = self.players[0]
                print "Player %s won when everyone else folded" % winner
                raise WinByDefault(winner)
                
            # break out of this loop if all players have bet
            for player in self.players:
                if player not in has_bet and not self.all_in[player]:
                    break
            else:
                break
        print "End of betting round %d" % n
            
    def determine_ranking(self, community_cards, hole_cards):
        # determine the best hand for each player
        hand_ranks = []
        for player in self.players:
            cards = community_cards + hole_cards[player]
            print "Player: %s with %s using cards %s" % (player, hand_rank, cards)
            hand_ranks.append((n_card_rank(cards), player))
        return hand_ranks
            