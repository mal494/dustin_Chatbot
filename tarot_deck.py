import random

class MajorArcana:
    def __init__(self):
        self.cards = [
            {"name": "The Magician", "value": 1},             
            {"name": "The High Priestess", "value": 2},             
            {"name": "The Empress", "value": 3},             
            {"name": "The Emperor", "value": 4},             
            {"name": "The Hierophant", "value": 5},             
            {"name": "The Lovers", "value": 6},             
            {"name": "The Chariot", "value": 7},             
            {"name": "Strength", "value": 8},             
            {"name": "The Hermit", "value": 9},             
            {"name": "Wheel of Fortune", "value": 10},             
            {"name": "Justice", "value": 11},             
            {"name": "The Hanged Man", "value": 12},             
            {"name": "Death", "value": 13},             
            {"name": "Temperance", "value": 14},             
            {"name": "The Devil", "value": 15},             
            {"name": "The Tower", "value": 16},             
            {"name": "The Star", "value": 17},             
            {"name": "The Moon", "value": 18},             
            {"name": "The Sun", "value": 19},             
            {"name": "Judgement", "value": 20},             
            {"name": "The World", "value": 21}        
            ]

    def draw_card(self):
        """Picks a random card from the deck."""
        if not self.cards:
            return "Deck is empty!"
        card = random.choice(self.cards)
        return f"You drew: {card['name']} (Value: {card['value']})"
        
if __name__ == "__main__":     
    deck = MajorArcana()     
    print(deck.draw_card())