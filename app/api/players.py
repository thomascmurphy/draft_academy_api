"""
 Simple API endpoint for returning players
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
from ..models import Player, Pack, Deck, Pod, PackCard
import pdb
import sys

players = Blueprint('players', __name__, url_prefix='/api/v1/players')

# @players.route('/<player_hash>', methods=['GET'])
# def get_player(player_hash):
#     player = Player.get_player_by_hash(player_hash)
#     return jsonify({'player': player}), 201

@players.route('', methods=['GET'])
def get_players():
    email = request.args.get('email')
    query = []
    if email:
      query = ["email = '%s'" % email]
    players = Player.get_players(query)
    pod_hashes = {player['pod_id']: player['hash'] for player in players}
    pod_ids = set([player['pod_id'] for player in players])
    pods = Pod.get_pods(["pods.id in (%s)" % ",".join(list(map(str, pod_ids)))])
    pods = [dict({'player_hash': pod_hashes[pod['id']]}, **pod) for pod in pods]
    return jsonify({'players': players, 'pods': pods}), 201

@players.route('/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.get_player_by_id(player_id)
    pod = Pod.get_pod_by_id(player['pod_id'])
    return jsonify({'player': player, 'pod': pod}), 201

@players.route('/<player_hash>/deck', methods=['GET'])
def get_player_deck_by_hash(player_hash):
    player = Player.get_player_by_hash(player_hash)
    deck = Player.get_player_deck(player['id'])
    deck_cards = Deck.get_cards(deck['id'])
    return jsonify({'player': player, 'deck': deck, 'deck_cards': deck_cards}), 201

# @players.route('/<int:player_id>/deck', methods=['GET'])
# def get_player_deck_by_id(player_id):
#     player = Player.get_player_by_id(player_id)
#     deck = Player.get_player_deck(player['id'])
#     cards = Deck.get_cards(deck['id'])
#     return jsonify({'player': player, 'deck': deck, 'cards': cards}), 201

@players.route('/<player_hash>/pack', methods=['GET'])
def get_player_pack_by_hash(player_hash):
    player = Player.get_player_by_hash(player_hash)
    pack = Player.get_player_pack(player['id'])
    pack_cards = Pack.get_available_cards(pack['id']) if pack else []
    return jsonify({'player': player, 'pack': pack, 'pack_cards': pack_cards}), 201

# @players.route('/<int:player_id>/pack', methods=['GET'])
# def get_player_pack_by_id(player_id):
#     player = Player.get_player_by_id(player_id)
#     pack = Player.get_player_pack(player_id)
#     cards = Pack.get_available_cards(pack['id'])
#     return jsonify({'player': player, 'pack': pack, 'cards': cards}), 201

@players.route('/pick', methods=['POST'])
def create_pick():
    pack_card_id = int(request.json['pack_card_id'])
    pack_card = PackCard.get_pack_card_by_id(pack_card_id)
    pack = Pack.get_pack_by_id(pack_card['pack_id'])
    player = Player.get_player_by_id(pack['player_id'])
    pod = Pod.get_pod_by_id(player['pod_id'])
    player_ids = pod['player_ids']
    next_player_id = player_ids[(player_ids.index(player['id']) + 1)%len(player_ids)]
    deck = Deck.get_deck_by_player_id(player['id'])
    #pick_number = Pack.get_pick_number(Pack.get_all_cards(pack['id']))
    deck_cards = Deck.get_cards(deck['id'])
    pick_number = len(deck_cards) + 1
    pack_card = PackCard.pick_pack_card(pack_card_id, deck['id'], player['id'], next_player_id, pick_number)

    pack = Player.get_player_pack(player['id'])
    pack_cards = Pack.get_available_cards(pack['id']) if pack else []
    deck_cards = Deck.get_cards(deck['id']) if deck else []
    return jsonify({'player': player, 'pack': pack, 'pack_cards': pack_cards, 'deck_cards': deck_cards}), 201

@players.route('/<player_hash>/card_images', methods=['GET'])
def get_player_card_images_by_hash(player_hash):
    player = Player.get_player_by_hash(player_hash)
    pod_id = player['pod_id']
    pod_players = Player.get_players(['pod_id=%i' % pod_id])
    pod_player_ids = [player['id'] for player in pod_players]
    pod_packs = Pack.get_packs(['packs.player_id IN (%s)' % ",".join(list(map(str, pod_player_ids)))])
    pod_pack_ids = [pack['id'] for pack in pod_packs]
    pod_pack_cards = PackCard.get_pack_cards(['pack_cards.pack_id IN (%s)' % ",".join(list(map(str, pod_pack_ids)))])
    pod_pack_cards_with_images = PackCard.add_card_images_to_pack_cards(pod_pack_cards)
    card_image_urls = [card['image_url'] for card in pod_pack_cards_with_images]
    return jsonify({'card_image_urls': card_image_urls}), 201

