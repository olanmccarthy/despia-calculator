import requests
import json
import random
import copy
import scipy.stats as ss
from card import Card
from constants import adlib, albion, aluber, tragedy, chain, snow, albaz, kitt, merc, gryphon, girl, fusion, bir, lost, opening, called, dracoback, adventure, foolish, patchwork, poly, rite, allure, crossout

class Calculator:
    def __init__(self, deckList, loopAmount):
        self.loopAmount = loopAmount

        # Brave variant stats
        self.chooseBetweenAluberOrRite = 0
        self.brandedFusionGotAshed = 0
        self.bravePreventedFusionFromBeingAshed = 0
        self.endOnGryphonPlusJade = 0
        self.endOnGryphonJadeLost = 0
        self.howManyBraveCardsInHandWhenAluber = 0
        self.noWayToFuse = 0

        # Pure variant stats
        self.crossOutPreventedFusionFromBeingAshed = 0
        
        # Common Stats
        self.endOnJadeLost = 0
        self.calledByPreventedFusionFromBeingAshed = 0
        self.endOnJadeAlone = 0

        with open(deckList) as f:
            deck_ids = f.read().splitlines()
        deck_ids.pop(0)
        deck_ids.pop(0)
        self.decksize = deck_ids.index("#extra")
        deck_ids = deck_ids[:self.decksize]
        deck = []
        deckmonsters = {}
        self.monsterbridges = {}

        # Convert card ids to card objects
        for id in deck_ids:
            response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={id}")
            info = json.loads(response.text)
            resp = info["data"][0]
            try:
                card = Card(resp["name"], resp["type"], resp["race"], resp["attribute"], resp["atk"], resp["def"], resp["level"])
            except KeyError:
                # Card is not a monster
                card = Card(resp["name"], resp["type"], resp["race"])
            deck.append(card)
            if "Monster" in resp["type"]:
                deckmonsters[resp["name"]] = {"ATK": resp["atk"],"DEF": resp["def"], "Attribute": resp["attribute"],"Type": resp["race"], "Level": resp["level"]}

        self.deck = deck

        for card in deckmonsters:
            self.monsterbridges[card] = []
            for key in deckmonsters:
                score = self.getScore(deckmonsters[card],deckmonsters[key])
                if score == 1:
                    self.monsterbridges[card].append(key)

    def getScore(self, card,comparison):
        score = 0
        for key in card:
            if card[key] == comparison[key]:
                score = score + 1
        return score

    def checkHand(self, hand, deck):
        if albion in hand:
            # This is not strictly how albion works but its a trek to do properly
            self.drawNewCard(albion, hand, deck)

        handCopy = copy.deepcopy(hand)

        # 1. Choose between using rite or normal summoning aluber
        if aluber in hand and fusion not in hand and opening not in hand and (girl in hand or rite in hand or foolish in hand):
            self.chooseBetweenAluberOrRite += 1

        # 3a. How often do you draw brave engine/called by as well as a way to access fusion
        if (opening in hand or fusion in hand) and (girl in hand or rite in hand or foolish in hand or called in hand):
            self.bravePreventedFusionFromBeingAshed += 1 

    def drawNewCard(self, card, hand, deck):
        # Draw a new card from deck and remove current card
        self.removeFromHand([card], hand)
        hand.append(deck[0])
        deck = deck[1:]
        
    
    def removeFromHand(self, cards, hand):
        #removes the first instance of a card in cards from hand and nothing else
        for card in cards:
            if card in hand:
                hand.remove(card)
                return

    def run(self):
        # Combo Logic
        for i in range(self.loopAmount):
            random.shuffle(self.deck)
            hand = self.deck[-5:]
            deckcopy = self.deck[5:]

            # Check hands
            self.checkHand(hand, deckcopy)

        # 2. How often does your branded fusion get ash blossomed going first
        # 3. How often does the brave engine prevent you branded fusion getting ashed going first?
        # 8. How often does crossout designator+ called by prevent your branded fusion getting ash blossomed in the pure variant?
        # Assume for this you always have access to branded fusion, what chance do you have of drawing girl, rite, foolish, called by or crossout in hand
        amountOfCounters = self.deck.count(girl) + self.deck.count(rite) + self.deck.count(foolish) + self.deck.count(called) + self.deck.count(crossout)
        hpd = ss.hypergeom(len(self.deck), amountOfCounters, 5)
        answerToAsh = hpd.pmf(1) + hpd.pmf(2) + hpd.pmf(3)

        # Print Stats
        print(f"Main deck total: {len(self.deck)}")

        print (f"Amount of times you are forced to choose between normal summoning Aluber or using Brave: {(self.chooseBetweenAluberOrRite / self.loopAmount) * 100}%")

        print(f"Assuming you have fusion, the amount of times you should be able to stop your Fusion from being Ash'd {answerToAsh * 100}%")

        print(f"Amount of times you draw brave plus access to fusion {(self.bravePreventedFusionFromBeingAshed/self.loopAmount) * 100}%")
