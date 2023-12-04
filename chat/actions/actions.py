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

from langchain.embeddings import HuggingFaceEmbeddings

# Import SQL Lib
import psycopg2

load_dotenv('../.env')

class QuerySQL:
    def __init__(self, cursor) -> None:
        self.cursor = cursor
        self.operators = {
            "eq": "=",
            "lt": "<",
            "gt": ">",
            "le": "<=",
            "ge": ">="
        }
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def query(self, conditions) -> Text:
        # Ensure conditions is a non-empty list
        if not conditions or not isinstance(conditions, list):
            raise ValueError("Invalid conditions")

        # Build the WHERE clause dynamically based on conditions
        where_clause = " AND ".join([f"{col} {self.operators[op]} %s"
                                     for col, op, val in conditions])

        # SQL query with dynamic WHERE clause
        q = f"""SELECT title FROM books WHERE {where_clause}
               ORDER BY RANDOM() LIMIT 5"""

        # Extract values from conditions
        values = [val for col, op, val in conditions]

        # Execute query with the values
        self.cursor.execute(q, values)

        # Fetch results
        results = self.cursor.fetchall()

        # Process results and construct a response
        response = "Here are the results:\n"
        for row in results:
            response += str(row) + "\n"

        return response
    
    # similarity search for descriptions
    def similarity_search(self, conditions) -> Text:
        # Ensure conditions is a non-empty list
        if not conditions or not isinstance(conditions, list):
            raise ValueError("Invalid conditions")
        
        # if similarity serach is not the only condition
        other_entities = ['average_rating', 'publication_year', 'publication_month']
        idx_to_check = 0
        
        if any(tpl[idx_to_check] in other_entities for tpl in conditions):
            pass
        else:
            q = conditions[0][-1]
            q_vector = self.embeddings.embed_query(q)
            
            q = f"""
                SELECT title
                FROM books
                INNER JOIN langchain_pg_embedding
                ON books.book_id = (langchain_pg_embedding.cmetadata ->> 'book_id')::integer
                ORDER BY embedding <-> '{q_vector}'
                LIMIT 5;
            """
            
            # Execute query with the values
            self.cursor.execute(q)

            # Fetch results
            results = self.cursor.fetchall()

            # Process results and construct a response
            response = "Here are the results:\n"
            for row in results:
                response += str(row) + "\n"

            return response


        
        
class ActionQueryDatabase(Action):
    def __init__(self):
        super(ActionQueryDatabase, self).__init__()

        # Establish a connection to the database when the action server starts
        self.connection = psycopg2.connect(
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME')
        )
        
        # Create a cursor to execute SQL queries
        self.cursor = self.connection.cursor()
        
        # single value querying class
        self.querysql = QuerySQL(self.cursor)
        
    def name(self) -> Text:
        return "action_query_database"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get conditions from user input
        message = tracker.latest_message
        
        # Extract tuples of (entity, role, value)
        cond = [(entity["entity"], entity.get("role", ""), entity["value"])
                for entity in message.get("entities", [])]
        
        # entities that will require a different function
        specific_value = ['description']
        idx_to_check = 0
        
        if any(tpl[idx_to_check] in specific_value for tpl in cond):
            response = self.querysql.similarity_search(cond)
            
            # Send the response back to the user
            dispatcher.utter_message(response)        

            return []
        else:
            response = self.querysql.query(cond)
            
            # Send the response back to the user
            dispatcher.utter_message(response)        

            return []

    def __del__(self):
        # Close the database connection when the action server stops
        if self.connection:
            self.cursor.close()
            self.connection.close()