import base64
from flask import current_app

from .models import *
from .deck import Deck

class Player():
    #methods
    @staticmethod
    def get_players(params):
        players = select_items('players', params)
        return players

    @staticmethod
    def get_player_by_hash(hash):
        #cipher = AES.new(current_app.config['PLAYER_HASH_KEY'])
        #hash = base64.encodestring(cipher.encrypt("%016d"%id))
        #id = int(cipher.decrypt(base64.decodestring(hash)))
        email = base64.b64decode(hash)
        player = select_first_item('players', ["hash='%s'" % hash])
        return player

    @staticmethod
    def get_player_by_id(id):
        player = select_item_by_id('players', id)
        return player

    @staticmethod
    def create_player(email, pod_id):
        hash_components = "%i%s" % (pod_id, email)
        player_hash = base64.b64encode(hash_components.encode())
        player_hash_string = player_hash.decode('utf-8')
        player = insert_item('players', {'email': email, 'pod_id': pod_id, 'hash': player_hash_string})
        deck = Deck.create_deck(player['id'])
        return player

    @staticmethod
    def delete_player(id):
        player = delete_item_with_id('players', "id='%i'" % id)
        return true

    @staticmethod
    def get_player_pack(player_id):
        packs = select_items('packs', ["player_id = %i" % player_id, "complete = 0", "open = 1"], ['number ASC'], associations=[{'table': 'pack_cards', 'model': 'pack_card', 'join_field_left': 'id', 'join_field_right': 'pack_id'}])
        if packs:
          pack = sorted(packs, key=lambda pack: len(pack['pack_card_ids']), reverse=True)[0]
        else:
          pack = None
        return pack

    @staticmethod
    def get_player_deck(player_id):
        deck = select_first_item('decks', ["player_id=%i" % player_id])
        return deck
