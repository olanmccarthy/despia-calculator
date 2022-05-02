import requests
import json
import random
import copy
from card import Card
from constants import adlib, albion, aluber, tragedy, chain, snow, albaz, kitt, merc, gryphon, girl, fusion, bir, lost, opening, called, dracoback, adventure, foolish, patchwork, poly, rite, allure

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
        handCopy = copy.deepcopy(hand)

        # 1. Choose between using rite or normal summoning aluber
        if aluber in hand and fusion not in hand and opening not in hand and (girl in hand or rite in hand or foolish in hand):
            self.chooseBetweenAluberOrRite += 1

        

    def run(self):
        # Combo Logic
        for i in range(self.loopAmount):
            random.shuffle(self.deck)
            hand = self.deck[-5:]
            deckcopy = self.deck[5:]

            # Check hands
            self.checkHand(hand, deckcopy)

        # Print Stats
        print(f"Main deck total: {len(self.deck)}")

        print (f"Amount of times you are forced to choose between normal summoning Aluber or using Brave: {(self.chooseBetweenAluberOrRite / self.loopAmount) * 100}%")

