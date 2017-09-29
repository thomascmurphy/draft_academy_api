"""
 Simple API endpoint for returning pods
"""
import ast
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
from ..models import Pod, Pack, PackCard, Player, Deck

pods = Blueprint('pods', __name__, url_prefix='/api/v1/pods')
import pdb

@pods.route('', methods=['GET'])
def get_pods():
    email = request.args.get('email')
    query = []
    if email:
      players = Player.get_players(["email = '%s'" % email])
      pod_ids = [player['pod_id'] for player in players]
      query = ["pods.id in (%s)" % ",".join(list(map(str, pod_ids)))]
    pods = Pod.get_pods(query)
    return jsonify({'pods': pods}), 201

@pods.route('/<int:pod_id>', methods=['GET'])
def get_pod(pod_id):
    pod = Pod.get_pod_by_id(pod_id)
    players = Player.get_players(["pod_id=%i" % pod_id])
    player_ids = [player['id'] for player in players]
    decks = Deck.get_decks(["player_id IN (%s)" % ','.join(list(map(str, player_ids)))])
    packs = Pack.get_packs(["player_id IN (%s)" % ','.join(list(map(str, player_ids)))])
    pack_ids = [pack['id'] for pack in packs]
    pack_cards = PackCard.get_pack_cards(["pack_id IN (%s)" % ','.join(list(map(str, pack_ids)))])
    pack_cards = PackCard.add_card_images_to_pack_cards(pack_cards)
    return jsonify({'pod': pod, 'players': players, 'packs': packs, 'decks': decks, 'pack_cards': pack_cards}), 201

@pods.route('', methods=['POST'])
def create_pod():
    pod_json = request.json['pod']
    name = pod_json['name']
    pack_1_set = pod_json['pack_1_set']
    pack_2_set = pod_json['pack_2_set']
    pack_3_set = pod_json['pack_3_set']
#     player_emails = ast.literal_eval(request.json['player_emails'])
    player_emails = filter(None, request.json['player_emails'])
    pod = Pod.create_pod(name, pack_1_set, pack_2_set, pack_3_set, player_emails)
    return jsonify({'pod': pod}), 201

@pods.route('/<int:pod_id>', methods=['DELETE'])
def delete_pod(pod_id):
    pod = Pod.delete_pod(pod_id)
    return jsonify(pod), 201

@pods.route('/<int:pod_id>/picks', methods=['POST'])
def create_pick(pod_id):
    deck_id = request.form['deck_id']
    pack_card_id = request.form['pack_card_id']
    pack_card = PackCard.get_pack_card_by_id(pack_card_id)
    pack = Pack.get_pack_by_id(pack_card['pack_id'])
    all_pack_cards = Pack.get_all_cards(pack['id'])
    pick = PackCard.update_pack_card_by_id(pack_card_id, {'deck_id': deck_id})
    if len(Pack.get_available_cards(pack['id'])) == 0:
        Pack.update_pack_by_id(pack['id'], {'complete': True})
    return jsonify({'pick': pick}), 201

@pods.route('/<int:pod_id>/pack/<int:pack_number>/picks/<int:pick_number>', methods=['GET'])
def view_picks(pod_id, pack_number, pick_number):
    pod = Pod.get_pod_by_id(pod_id)
    players = Player.get_players(["pod_id=%i", pod_id])
    player_ids = [player['id'] for player in players]
    packs = Pack.get_packs(["player_id IN (%s)" % ','.join(player_ids), "number=%i" % pack_number])
    pack_ids = [pack['id'] for pack in packs]
    picks = PackCard.get_pack_cards(["pack_id IN (%s)" % ','.join(pack_ids), "pick=%i" % pick_number])
    return jsonify({'players': players, 'packs': packs, 'picks': picks}), 201
