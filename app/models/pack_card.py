from .models import *
from .card import Card

class PackCard():
    #methods
    @staticmethod
    def get_pack_cards(params):
        pack_cards = select_items('pack_cards', params)
        return pack_cards

    @staticmethod
    def get_pack_card_by_id(id):
        pack_card = select_item_by_id('pack_cards', id)
        return pack_card

    @staticmethod
    def create_pack_card(card_id, pack_id, deck_id=None, pick_number=None, sideboard=None):
        pack_card = insert_item('pack_cards', {'card_id': card_id, 'pack_id': pack_id, 'deck_id': deck_id, 'pick_number': pick_number, 'sideboard': sideboard})
        return pack_card

    @staticmethod
    def update_pack_card(values, params):
        pack_cards_update = update_item('pack_cards', values, params)
        pack_card = select_first_item('pack_cards', params)
        return pack_card

    @staticmethod
    def update_pack_card_by_id(id, values):
        return PackCard.update_pack_card(values, ["pack_cards.id=%i" % id])

    @staticmethod
    def pick_pack_card(pack_card_id, deck_id, player_id, next_player_id, pick_number):
        pack_card = PackCard.update_pack_card_by_id(pack_card_id, ['pick_number=%i' % pick_number, 'deck_id=%i' % deck_id])
        remaining_cards = select_items('pack_cards', ['pack_id=%i' % pack_card['pack_id'], 'deck_id IS NULL'])
        pack_complete = 0 if len(remaining_cards) > 0 else 1
        pack = update_item('packs', ['player_id=%i' % next_player_id, 'complete=%i' % pack_complete], ['packs.id=%i' % pack_card['pack_id']])
        if pack_complete and pack.number < 3:
          next_pack = update_item('packs', ['open=1'], ['packs.player_id=%i' % player_id, 'packs.number=%i' % (pack.number + 1)])
        return pack_card

    @staticmethod
    def add_card_images_to_pack_cards(pack_cards):
        card_ids = [pack_card['card_id'] for pack_card in pack_cards]
        cards = select_items('cards', ["cards.id in (%s)" % ",".join(list(map(str, card_ids)))])
        card_images = {card['id']: card['image_url'] for card in cards}
        pack_cards = [dict({'image_url': card_images[pack_card['card_id']]}, **pack_card) for pack_card in pack_cards]
        return pack_cards

    @staticmethod
    def delete_pack_card(id):
        pack_card = delete_item_with_id('pack_cards', "id='%i'" % id)
        return true
