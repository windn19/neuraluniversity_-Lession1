from random import randint, choice, shuffle
from pprint import pprint
import os


class Full:
    def __init__(self, num_player=1):
        self.deck = {'П': ['6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т'],
                     'К': ['6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т'],
                     'Б': ['6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т'],
                     'Ч': ['6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т']}
        self.players = [Player(human=False), *[Player() for _ in range(num_player)]]
        self.trump = None
        self.batter_num = 0
        self.cart = None
        self.trump_suit = None

    def change(self, new, change=False):
        if new:
            shuffle(self.players)
            suit = choice([x for x in list(self.deck.keys())])
            card = choice(self.deck[suit])
            self.trump = (suit, card)
            self.trump_suit = self.trump[0]
            self.deck[suit].remove(card)
        for num, player in enumerate(self.players):
            num_cart = 6 - sum(len(x) for x in player.cards.values()) \
                if 6 - sum(len(x) for x in player.cards.values()) > 0 else 0
            if new:
                player.batter = True if num == 0 else False
                player.attack = False if num == 0 else True
            elif change:
                player.batter = not player.batter
                player.attack = not player.attack
            print(num, player.attack, player.batter)
            for _ in range(num_cart):
                try:
                    suit = choice([x for x in list(self.deck.keys()) if self.deck[x]])
                except IndexError:
                    print('Done!')
                    if self.trump:
                        player.cards[self.trump[0]].append(self.trump[1])
                        print(player.cards)
                        self.trump = None
                    break
                card = choice(self.deck[suit])
                player.cards[suit].append(card)
                self.deck[suit].remove(card)

    def __str__(self):
        return str(self.deck)

    @property
    def desk_empty(self):
        return sum(len(x) for x in self.deck.values()) == 0

    @property
    def amound_players(self):
        num = 0
        for player in self.players:
            if player.is_alive:
                num += 1
        return num

    @property
    def game_over(self):
        return self.desk_empty and self.amound_players == 1

    def game(self):
        sample = ['6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т']
        self.change(new=True)
        i = 1
        circle = 0
        con_dist = {'П': [], 'К': [], 'Б': [], 'Ч': []}
        while not self.game_over:
            print(self.deck)
            player = self.players[i % len(self.players)]
            answer = player.move() if circle < 6 else False
            if answer:
                if player.batter:
                    if (con[0] == answer[0] and sample.index(answer[1]) > sample.index(con[1]))\
                            or (con[0] != answer[0] and answer[0] == self.trump_suit):
                        for cart in (con, answer):
                            con_dist[cart[0]].append(cart[1])
                        print(con_dist, circle, self.trump)
                        circle += 1
                    else:
                        player.cards[answer[0]].append(answer[1])
                        print('Fail step')
                        continue
                else:
                    num_set = set()
                    num_con = sum(len(x) for x in con_dist.values())
                    for x in con_dist.values():
                        for num in x:
                            num_set.add(num)
                    print(num_con, num_set, self.trump)
                    if num_con and answer[1] not in num_set:
                        print('Fail step')
                        player.cards[answer[0]].append(answer[1])
                        continue
                con = answer
            else:
                if player.attack:
                    self.change(new=False, change=True)
                else:
                    con_dist[con[0]].append(con[1])
                    for suit in con_dist.keys():
                        player.cards[suit].extend(con_dist[suit])
                    self.change(new=False, change=False)
                con_dist = {'П': [], 'К': [], 'Б': [], 'Ч': []}
                circle = 0
            i += 1


class Player:
    def __init__(self, human=True):
        self.cards = {'П': [], 'К': [], 'Б': [], 'Ч': []}
        self.human = human
        self.batter = None
        self.attack = None

    def __str__(self):
        return f'{self.cards} -- {self.attack} -- {self.batter}'

    @property
    def is_alive(self):
        return sum(len(x) for x in self.cards.values()) == 0

    def move(self):
        print(self)
        cart = input('Твой ход или (б)-бито: ') if self.attack else input('Твой ход или (в) - взять: ')
        while not (cart[-1] in self.cards and cart[:-1] in self.cards[cart[-1]]):
            if cart.isalpha() and (cart.lower() == 'б' or cart.lower() == 'в'):
                return False
            cart = input('Твой ход или (б)-бито: ') if self.attack else input('Твой ход или (в) - взять: ')
        self.cards[cart[-1]].remove(cart[:-1])
        return cart[-1], cart[:-1]


first = Full()
print(first.desk_empty)
first.game()