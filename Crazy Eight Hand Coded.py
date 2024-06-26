import random
from cards import Card

def init_card():
    deck = []
    for suit_id in range (1,5):
        for rank_id in range (1,14):
            new_card = Card(suit_id, rank_id)
            if new_card.rank == '8':
                new_card.value = 50
            deck.append(new_card)
    random.shuffle(deck)

    p_hand = [deck.pop() for _ in range(5)]
    c_hand = [deck.pop() for _ in range(5)]
    up_card = deck.pop()
    active_suit = up_card.suit
    
    return deck, p_hand, c_hand, up_card, active_suit

#The Players Choice
def player_turn():
    global deck, p_hand, blocked, up_card, active_suit
    valid_play = False
    is_eight = False    
    print ("\n Your Hand:  ")
    for card in p_hand:
        print (card.short_name)
    print (f'Upcard : {up_card.short_name}')
    if up_card.rank == '8':
        print (f'Suit is {active_suit}')
    print ('What would you like to do?')
    response = input("Type a card to play or 'Draw' to take a card: ")
    while not valid_play:
        selected_card = None
        while selected_card == None:
            if response.lower() == 'draw':
                valid_play = True
                if len(deck) > 0:
                    card = random.choice(deck)
                    p_hand.append(card)
                    deck.remove(card)
                    print (f' You drew {card.short_name}')
                else: 
                    print ('There are no cards left in the deck')
                    blocked += 1
                return
            else:
                for card in p_hand:
                    if response.upper() == card.short_name:
                        selected_card = card
                if selected_card == None:
                    response = input("You don't have that card Try Again: ")
        if selected_card.rank == '8':
            valid_play = True
            is_eight = True
        elif selected_card.suit == active_suit:
            valid_play = True
        elif selected_card.rank == up_card.rank:
            valid_play = True
        if not valid_play:
            response = input("That's not a legal play. Try Again: ")

    p_hand.remove(selected_card)
    up_card = selected_card
    active_suit = up_card.suit
    print (f'You played {selected_card.short_name}')
    if is_eight:
        get_new_suit()

#New Suit when player plays an 8
def get_new_suit():
    global active_suit
    got_suit = False
    while not got_suit:
        suit = input("Pick a suit (d/h/s/c): ")
        if suit.lower() == 'd':
            active_suit = "Diamonds"
            got_suit = True
        elif suit.lower() == 's':
            active_suit = "Spades"
            got_suit = True
        elif suit.lower() == 'h':
            active_suit = "Hearts"
            got_suit = True
        elif suit.lower() == 'c':
            active_suit = "Clubs"
            got_suit = True
        else:
            print("Not a valid suit. Try again. ")
            print (f'You picked {active_suit}')


#Computer turn
def computer_turn():
    global c_hand, deck, up_card, active_suit, blocked
    options = []
    for card in c_hand:
        if card.rank == '8':
            c_hand.remove(card)
            up_card = card
            print (f" Computer played {card.short_name}")
            #suit totals: [diamonds, hearts, spades, clubs] 
            suit_totals = [0, 0, 0, 0]
            for suit in range(1, 5): 
                for card in c_hand:
                    if card.suit_id == suit:
                        suit_totals[suit-1] += 1
            long_suit = 0
            for i in range (4):
                if suit_totals[i] > long_suit:
                    long_suit = i
            if long_suit == 0: 
                active_suit = "Diamonds"
            if long_suit == 1:
                active_suit = "Hearts"
            if long_suit == 2:
                active_suit = "Spades"
            if long_suit == 3:
                active_suit = "Clubs"
                print (f'Computer Changed to {active_suit}')
            return
        else: 
            if card.suit == active_suit:
                options.append(card)
            elif card.rank == up_card.rank:
                options.append(card)
    if options:
        best_play = max(options, key=lambda x: x.value)
        c_hand.remove(best_play) 
        up_card = best_play 
        active_suit = up_card.suit 
        print (f'Computer played {best_play.short_name}')
    else:
        if len(deck) >0:
            next_card = random.choice(deck)
            c_hand.append(next_card) 
            deck.remove(next_card) 
            print ("Computer drew a card" )
        else:
            print("Computer is blocked")
            blocked += 1 
    print ("Computer has %i cards left" % (len(c_hand)) ) 

#Initialize game
deck, p_hand, c_hand, up_card, active_suit = init_card()
game_done = False
p_total = 0
c_total = 0
blocked = 0

#Main Game Loop
while not game_done:
    blocked = 0 
    player_turn()
    if len(p_hand) == 0:
        game_done = True
        print('\nYou Won!')
    #Display Game Score Here
    p_points =  0
    for card in c_hand:
        p_points += card.value
    p_total += p_points
    print ("You got %i points for computer's hand" %p_points)

    if not game_done:
        computer_turn()
    if len(c_hand) == 0:
        game_done = True
        print('\nComputer Won!')
    # display game score here
    c_points = 0
    for card in p_hand:
        c_points += card.value
    c_total += c_points
    print ("Computer got %i points for your hand" %c_points)

    if blocked >= 2:
        game_done = True
        print ('\n Both Players Blocked, GAME OVER ')
        player_points = 0
        for card in c_hand:
            p_points += card.value
        p_total += p_points
        c_points = 0
        for card in p_hand:
            c_points += card.value
        c_total += c_points
        print ("You got %i points for computer's hand" %p_points)
        print ("Computer got %i points for your hand" %c_points)

    if not game_done:
        play_again = input('Play again (Y/N)?:')
        if play_again.lower().startswith('y'):
            deck, p_hand, c_hand, up_card, active_suit = init_card()
            game_done = False
            blocked = 0
            print ('\n So far you have %i points in total' %p_points)
            print ('And the computer have %i points in total' %c_points)
        else: 
            game_done = True

print ("\n Final Score:")
print ("You: %i Computer: %i" % (p_total, c_total))
if p_total >= c_total:
    print ('You Won!')
else: 
    print ('You lose!')






    




             






