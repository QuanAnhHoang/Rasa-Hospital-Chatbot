# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGreetWithName(Action):
    def name(self) -> Text:
        return "action_greet_with_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = next(tracker.get_latest_entity_values("name"), None)
        if name:
            dispatcher.utter_message(template="utter_chao_hoi_voi_ten", name=name)
        else:
            dispatcher.utter_message(template="utter_chao_hoi_voi_ten", name="None")
        
        return []
