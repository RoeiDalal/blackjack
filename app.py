import re
from unittest import result
from flask import Flask, render_template, request, url_for
import pymongo
import random
import datetime
import pandas as pd
from bson.json_util import dumps

mongodb_uri="mongodb://root:password@mongo:27017/"
client = pymongo.MongoClient(mongodb_uri, 27017, username='root', password='password')

path="static/cards/"

db = client["blackjack_db"]
records = db["records"]

cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
hand = {}

card_values = {"2":1,"3":1,"4":1,"5":1,"6":1,"7":0,"8":0,"9":0,"10":-1,"11":-1,"12":-1,"13":-1,"14":-1}
counter = 0

hard_df = pd.read_excel(r'basic.xlsx', sheet_name='hard')
soft_df = pd.read_excel(r'basic.xlsx', sheet_name='soft')
split_df = pd.read_excel(r'basic.xlsx', sheet_name='split')
cards_df = pd.read_excel(r'basic.xlsx', sheet_name='cards')
header = ["2","3","4","5","6","7","8","9","10","11","12","13","14"]
hard_df.columns = header
soft_df.columns = header
split_df.columns = header
cards_df.columns = header

app = Flask(__name__)

def distribute_cards():
    dealer = random.choice(cards)
    hand['dealer'] = dealer
    card1 = random.choice(cards)
    hand['card1'] = card1
    card2 = random.choice(cards)
    hand['card2'] = card2

def sum_cards(card1, card2):
    if card1 >= 10 and card1 <14:
        card1 = 10
    if card2 >= 10 and card2 <14:
        card2 = 10
    if card1 == 14:
        card1 = 11
    if card2 == 14:
        card2 = 11
    return card1+card2

def check_hand(card1, card2):
    if card1 == card2:
        return "split"
    elif card1 == 14 or card2 == 14:
        return "soft"
    else:
        return "hard"

def check_result(card1, card2, dealer, answer, type):
    if type == "split":
        if split_df.loc[card1-2][str(dealer)]:
            if answer == "split":
                return True, "split"
            else:
                return False, "split"
        else:
            type = "hard"
            
    elif type == "soft":
        if card1 == 14:
            result = soft_df.loc[card2-2][str(dealer)]
            return result == answer, result
        elif card2 == 14:
            result = soft_df.loc[card1-2][str(dealer)]
            return result == answer, result

    if type == "hard":
        player = sum_cards(card1,card2)
        result = hard_df.loc[player-4][str(dealer)]
        return result == answer, result

def get_card_image(num):
    return cards_df.loc[random.randint(0,3)][str(num)]

def count_records(records):
    i = 0
    for record in records:
        i+=1
    return i

def update_counter(round_count):
    num= counter+round_count
    return num

@app.route('/')
def main():
    return render_template('main.html',header="Blackjack") 

@app.route('/game', methods=['POST'])
def set_game():
    type = check_hand(hand['card1'],hand['card2'])
    record = {}
    record['timestemp'] = datetime.datetime.now()
    record['type'] = type
    record['card1'] = hand['card1']
    record['card2'] = hand['card2']
    sum = sum_cards(record['card1'],record['card2'])
    record['player'] = sum
    record['dealer'] = hand['dealer']
    record['answer'] = request.form['button']
    record['correct'],answer = check_result(record['card1'], record['card2'], record['dealer'],record['answer'],type)
    round_count = card_values[str(hand['card1'])] + card_values[str(hand['card2'])] + card_values[str(hand['dealer'])]
    global counter
    counter = round_count + counter
    #records.insert_one(record)
    distribute_cards()
    dealer = path+get_card_image(hand['dealer'])
    card1 = path+get_card_image(hand['card1'])
    card2 = path+get_card_image(hand['card2'])
    return render_template('game.html',header="Blackjack", dealer=dealer, card1=card1, card2=card2, correct=record['correct'], counter=counter, answer=answer)

@app.route('/game', methods=['GET'])
def get_game():
    distribute_cards()
    dealer = path+get_card_image(hand['dealer'])
    card1 = path+get_card_image(hand['card1'])
    card2 = path+get_card_image(hand['card2'])
    return render_template('game.html',header="Blackjack", dealer=dealer, card1=card1, card2=card2)

@app.route('/stats')
def stats():
    total_hard = records.count_documents({"type":"hard"})
    total_soft = records.count_documents({"type":"soft"})
    total_split = records.count_documents({"type":"split"})
    correct_hard = records.count_documents({"type":"hard","correct":True})
    correct_soft = records.count_documents({"type":"soft","correct":True})
    correct_split = records.count_documents({"type":"split","correct":True})
    return render_template('stats.html',header="statistics",total_hard=total_hard,correct_hard=correct_hard,total_soft=total_soft,correct_soft=correct_soft,total_split=total_split,correct_split=correct_split)

@app.route('/rules')
def rules():
    return render_template('rules.html',header="Blackjack") 

app.run(host='0.0.0.0', port=8080)