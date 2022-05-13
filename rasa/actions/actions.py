from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from typing import Any, Text, Dict, List

import arrow

import numpy as np
import pandas as pd
from py2neo import Node,Relationship,Graph,Path,Subgraph
from py2neo import NodeMatcher, RelationshipMatcher

city_db = {
    'brussels': 'Europe/Brussels', 
    'zagreb': 'Europe/Zagreb',
    'london': 'Europe/Dublin',
    'lisbon': 'Europe/Lisbon',
    'amsterdam': 'Europe/Amsterdam',
    'seattle': 'US/Pacific'
}

attribute_db = {
    'birth year': 'birth_year',
    'eye color': 'eye_color',
    'height': 'height',
    'homeworld': 'homeworld',
    'weight': 'mass',
    'name': 'name',
    'skin color': 'skin_color',
    'species': 'species'
}

neo4j_url = 'http://localhost:7474/'
user = 'neo4j'
pwd = 'test'

class ActionTellTime(Action):
    
    def name(self) -> Text:
        return "action_tell_time"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()
       
        if not current_place:
            msg = f"It's {utc.format('HH:mm')} utc now."
            dispatcher.utter_message(text=msg)
            return []

        place_string = city_db.get(current_place, None)
        if not place_string:
            msg = f"I didn't recognise {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []

        msg = f"It's {utc.to(city_db[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)

        return []

class ActionQueryCharacter(Action):
    
    def name(self) -> Text:
        return "action_query_character"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        current_character = next(tracker.get_latest_entity_values("character"), None)

        graph = Graph(neo4j_url,  auth=(user, pwd))

        node_matcher = NodeMatcher(graph)
        node = node_matcher.match("Characters").where(f"toLower(_.name) = toLower('{current_character}')").first()

        if not node:
            msg = f"We didn't find {current_character}. \nMaybe you spelled it wrong. \nCan you try again?"
            dispatcher.utter_message(text=msg)
            return []

        if node:
            msg = f"{node['name']}: \nBirth year: {node['birth_year']} \nEye color: {node['eye_color']} \nGender: {node['gender']} \nHair color: {node['hair_color']} \nHeight: {node['height']} \nHomeworld: {node['homeworld']} \nWeigth: {node['mass']} \nSkin color {node['skin_color']} \nSpecies: {node['species']}"
            dispatcher.utter_message(text=msg)
            return []
        
        return []

class ActionQueryPlanet(Action):
    
    def name(self) -> Text:
        return "action_query_planet"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        current_planet = next(tracker.get_latest_entity_values("planet"), None)

        graph = Graph(neo4j_url,  auth=(user, pwd))

        node_matcher = NodeMatcher(graph)
        node = node_matcher.match("Planets").where(f"toLower(_.name) = toLower('{current_planet}')").first()

        if not node:
            msg = f"We didn't find {current_planet}. \nMaybe you spelled it wrong. \nCan you try again?"
            dispatcher.utter_message(text=msg)
            return []

        if node:
            msg = f"{node['name']}: \nClimate: {node['climate']} \nDiameter: {node['diameter']} \nGravity type: {node['gravity']} \nYear length: {node['orbital_period']} \nPopulation: {node['population']} \nDay length: {node['rotation_period']} \nSurface water: {node['surface_water']} \nTerrain {node['terrain']}"
            dispatcher.utter_message(text=msg)
            return []
        
        return []

class ActionQueryCharacterAttribute(Action):
    
    def name(self) -> Text:
        return "action_query_character_attribute"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        current_character = next(tracker.get_latest_entity_values("character"), None)
        current_attribute = next(tracker.get_latest_entity_values("attribute"), None)

        attribute_string = attribute_db.get(current_attribute, None)
        if not attribute_string:
            msg = f"I didn't recognise {current_attribute}. Maybe you spelled it wrong. We will be able to match it better in the future."
            dispatcher.utter_message(text=msg)
            return []

        return []