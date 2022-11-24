# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from cgitb import text
from operator import index
import pandas as pd
import numpy as np
import bs4
import pyodbc
import pickle
import re
import requests
import lxml
from typing import Any, Text, Dict, List
from googlesearch import search
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted
from rasa_sdk.events import AllSlotsReset
import time


def all_teams():
    df=pd.read_csv("matches.csv")
    all = list(df['team1'].unique())
    all = ',\n'.join(all)
    return all

def most_winners():
    df=pd.read_csv("matches.csv")
    most = str(df['winner'].value_counts())
    return most

def player_of_match():
    df=pd.read_csv("matches.csv")
    player = str(df['player_of_match'].value_counts()[:10])
    return player


def number_of_matches():
    df=pd.read_csv("matches.csv")
    play = str(df['team1'].value_counts())
    return play

def umpire_count(team_name):
    df=pd.read_csv("matches.csv")
    print(team_name)
    x = df[['date','team1','team2','winner','umpire1','umpire2']][(df["team1"]== team_name) | (df["team2"]== team_name)]
    print(x)
    return pd.concat([x.umpire1,x.umpire2],axis =0).value_counts()[:10]

def most_venue(team_name):
    df=pd.read_csv("matches.csv")
    venue = df['venue'][(df['team1'] == team_name) | (df['team2'] == team_name)].value_counts()
    return venue

def toss_dec(team_name):
    df=pd.read_csv("matches.csv")
    toss = df['toss_decision'][(df['team1'] == team_name) | (df['team2'] == team_name)].value_counts()
    return toss

def winning_perc(team_name):
    df=pd.read_csv("matches.csv")
    a = np.array(df['toss_winner'][df['toss_winner'] == team_name].value_counts())
    b = np.array(df['winner'][(df['toss_winner'] == team_name) & (df['winner'] == team_name)].value_counts())
    out = list((b/a)*100)
    return out

def toss_winner(team_name):
    df=pd.read_csv("matches.csv")
    out = df['toss_winner'][(df['team1'] == team_name) | (df['team2'] == team_name)].value_counts()
    return out






class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_all_teams"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        output = all_teams()
        output1 = 'List of all the companies : ' + output
        dispatcher.utter_message(text=output1)

        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_most_winners"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        output = most_winners()
        output1 = 'Top winners : ' + output
        dispatcher.utter_message(text=output1)

        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_player_of_match"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        output = player_of_match()
        output1 = 'Player of the match : ' + output
        dispatcher.utter_message(text=output1)

        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_number_of_matches"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        output = number_of_matches()
        dispatcher.utter_message(text=output)

        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_umpire_count"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        umpire=tracker.get_slot("umpire_count_slot")
        output=umpire_count(umpire)
        dispatcher.utter_message(text=output)

        return [AllSlotsReset()]
        
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_most_venue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        venue=tracker.get_slot("venue_count_slot")
        output=most_venue(venue)
        dispatcher.utter_message(text=output)

        return [AllSlotsReset()]

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_toss_dec"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        decision=tracker.get_slot("toss_decision_count")
        output=toss_dec(decision)
        dispatcher.utter_message(text=output)

        return [AllSlotsReset()]

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_winning_perc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        winner=tracker.get_slot("winning_percentage_count")
        output=winning_perc(winner)
        dispatcher.utter_message(text=output)

        return [AllSlotsReset()]

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_toss_winner"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        win=tracker.get_slot("toss_winner_count")
        output=toss_winner(win)
        dispatcher.utter_message(text=output)

        return [AllSlotsReset()]





# rasa run --cors "*" --enable-api
# rasa run actions
# rasa run -m models --enable-api --cors "*"
# rasa shell --debug