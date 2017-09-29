from .models import *

class Card():
    #methods
    @staticmethod
    def get_cards(params):
        cards = select_items('cards', params)
        return cards

    @staticmethod
    def get_card_by_id(id):
        card = select_item_by_id('cards', id)
        return card

    @staticmethod
    def create_card(name, image_url, multiverse_id, cmc, color_identity, set_code):
        card = insert_item('cards', {'name': name, 'image_url': image_url, 'multiverse_id': multiverse_id, 'cmc': cmc, 'color_identity': color_identity, 'set_code': set_code})
        return card

    @staticmethod
    def delete_card(id):
        card = delete_item_with_id('cards', "id='%i'" % id)
        return true
