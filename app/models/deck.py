from .models import *
from .pack_card import PackCard

class Deck():
    #methods
    @staticmethod
    def get_decks(params):
        decks = select_items('decks', params)
        return decks

    @staticmethod
    def get_deck_by_id(id):
        deck = select_item_by_id('decks', id)
        return deck

    @staticmethod
    def get_deck_by_player_id(player_id):
        deck = select_first_item('decks', ["player_id=%i" % player_id])
        return deck

    @staticmethod
    def create_deck(player_id):
        deck = insert_item('decks', {'player_id': player_id})
        return deck

    @staticmethod
    def delete_deck(id):
        deck = delete_item_with_id('decks', id)
        return true

    @staticmethod
    def get_cards(deck_id):
        deck = select_item_by_id('decks', deck_id)
        deck_cards = select_items('pack_cards', ["deck_id=%i" % deck_id], ["pack_cards.pick_number ASC"])
        return PackCard.add_card_images_to_pack_cards(deck_cards)
