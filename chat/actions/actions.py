# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import os
from dotenv import load_dotenv

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Import SQL Lib
import psycopg2

load_dotenv('../.env')


class ActionQueryDatabase(Action):

    def name(self) -> Text:
        return "action_query_database"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract relevant information from user input
        user_input = tracker.latest_message.get('text')
        
        # Establish a connection to the database
        connection = psycopg2.connect(
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME')
        )
        
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        
        # Example SQL query
        q = f"SELECT * FROM books WHERE average_rating = {float(user_input)} LIMIT 5"
        
        # Execute the query
        cursor.execute(q)
        
        # Fetch the results
        results = cursor.fetchall()
        
        # Process results and construct a response
        response = "Here are the results:\n"
        for row in results:
            response += str(row) + "\n"

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Send the response back to the user
        dispatcher.utter_message(response)

        return []
