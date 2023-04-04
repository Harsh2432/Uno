import random

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} {self.value}"

class Deck:
    def __init__(self):
        self.cards = []

        for color in ["Red", "Green", "Blue", "Yellow"]:
            for value in range(0, 10):
                self.cards.append(Card(color, value))
                if value != 0:
                    self.cards.append(Card(color, value))

        wild_card = Card("Wild", "")
        wild_draw4 = Card("Wild Draw 4", "")
        self.cards += [wild_card] * 4 + [wild_draw4] * 4

        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck, count=1):
        for i in range(count):
            self.hand.append(deck.draw_card())

    def play_card(self, card_index, discard_pile):
        card = self.hand.pop(card_index)
        discard_pile.append(card)
        return card

    def choose_color(self):
        color = input("\nChoose a color (Red, Green, Blue, Yellow): ")
        while color.lower() not in ["red", "green", "blue", "yellow"]:
            color = input("Invalid color. Choose a color (Red, Green, Blue, Yellow): ")
        return color.lower().capitalize()

    def __str__(self):
        return f"\n{self.name}'s hand: {', '.join(map(str, self.hand))}"

class UNO:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.discard_pile = []
        self.current_player_index = 0
        self.direction = 1
        self.game_over = False

        # Deal cards to players
        for i in range(7):
            for player in self.players:
                player.draw(self.deck)

        # Place top card of deck in discard pile
        self.discard_pile.append(self.deck.draw_card())

    def play(self):
        while not self.game_over:
            current_player = self.players[self.current_player_index]

            print(f"\nCurrent card: {self.discard_pile[-1]}")
            print(current_player)

            if self.discard_pile[-1].color == "Wild":
                color = current_player.choose_color()
                self.discard_pile[-1].color = color

            valid_cards = [card for card in current_player.hand if self.is_playable(card)]

            if len(valid_cards) > 0:
                print("Playable cards:")
                for i, card in enumerate(valid_cards):
                    print(f"{i}: {card}")
                card_index = int(input("\nChoose a card to play: "))
                while card_index not in range(len(valid_cards)):
                    card_index = int(input("Invalid choice. Choose a card to play: "))

                played_card = current_player.play_card(current_player.hand.index(valid_cards[card_index]), self.discard_pile)
                if played_card.value == "Draw 2":
                    self.next_player().draw(self.deck, count=2)
                elif played_card.value == "Draw 4":
                    self.next_player().draw(self.deck, count=4)
                    self.discard_pile[-1].color = current_player.choose_color()
                elif played_card.value == "Reverse":
                    self.direction *= -1
                elif played_card.value == "Skip":
                    self.next_player_index()

                if len(current_player.hand) == 0:
                    print(f"{current_player.name} wins!")
                    self.game_over = True

            else:
                print("\nNo playable cards. Drawing a card...")
                current_player.draw(self.deck)
                if self.is_playable(current_player.hand[-1]):
                    print(f"Drew {current_player.hand[-1]}. Playing it.")
                    current_player.play_card(-1, self.discard_pile)
                else:
                    print(f"Drew {current_player.hand[-1]}. Can't play it. Ending turn.")
                if len(current_player.hand) == 0:
                    print(f"\n{current_player.name} wins!")
                    self.game_over = True

            self.next_player_index()

    def next_player_index(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)

    def next_player(self):
        self.next_player_index()
        return self.players[self.current_player_index]

    def is_playable(self, card):
        top_card = self.discard_pile[-1]
        if card.color == top_card.color or card.value == top_card.value or card.color == "Wild":
            return True
        return False

game = UNO(["Harsh", "Anurag", "Vipul"])
game.play()