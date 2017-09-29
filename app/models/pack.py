from .models import *
from .pack_card import PackCard
from .card import Card

class Pack():
    #methods
    @staticmethod
    def get_packs(params):
        packs = select_items('packs', params)
        return packs

    @staticmethod
    def get_pack_by_id(id):
        pack = select_item_by_id('packs', id)
        return pack

    @staticmethod
    def create_pack(set_code, player_id, number, open_pack):
        pack = insert_item('packs', {'set_code': set_code, 'player_id': player_id, 'number': number, 'open': open_pack})
        booster_cards = SDKSet.generate_booster(set_code)
        print('Set SDK Call', file=sys.stderr)
        card_ids_used = []
        existing_cards_multiverse_ids = select_items('cards', select=["id"])
        for booster_card in booster_cards:
            while booster_card.multiverse_id in card_ids_used:
                print('Inserting: %i into: %s' % (booster_card.multiverse_id, ','.join(str(e) for e in card_ids_used)), file=sys.stderr)
                replacement_cards = SDKCard.where(set=set_code).where(rarity=booster_card.rarity).all()
                booster_card = random.choice(replacement_cards)
                print('Card SDK Call', file=sys.stderr)
            if booster_card.multiverse_id in existing_cards_multiverse_ids:
                card = existing_cards[0]
            else:
                card = Card.create_card(booster_card.name, booster_card.image_url, booster_card.multiverse_id, booster_card.cmc, json.dumps(booster_card.colors), booster_card.set)
                existing_cards_multiverse_ids.append(booster_card.multiverse_id)
            card_ids_used.append(booster_card.multiverse_id)
            PackCard.create_pack_card(card['id'], pack['id'])
        return pack

    @staticmethod
    def update_packs(values, params):
        pack = update_item('packs', values, params)
        return pack

    @staticmethod
    def update_pack_by_id(id, values):
        return update_packs(values, ["id=%i", id])

    @staticmethod
    def delete_pack(id):
        pack = delete_item_with_id('packs', id)
        return true

    @staticmethod
    def get_available_cards(pack_id):
        pack = select_item_by_id('packs', pack_id)
        pack_cards = select_items('pack_cards', ["pack_id=%i" % pack_id, "deck_id IS NULL"])
        return PackCard.add_card_images_to_pack_cards(pack_cards)

    @staticmethod
    def get_all_cards(pack_id):
        pack = select_item_by_id('packs', pack_id)
        pack_cards = select_items('pack_cards', ["pack_id=%i" % pack_id])
        return pack_cards

    @staticmethod
    def get_pick_number(pack_cards=[]):
        last_pick = max([pack_card["pick_number"] if pack_card["pick_number"] else 0 for pack_card in pack_cards])
        current_pick = last_pick + 1
        return current_pick
