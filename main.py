import os
import random
import datetime
import json
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
# from azure.storage.blob import BlobServiceClient

# Azure Text Analytics configuration
language_key = os.environ.get('LANGUAGE_KEY')
language_endpoint = os.environ.get('LANGUAGE_ENDPOINT')
text_analytics_client = None

# Azure Storage configuration
# connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
# container_name = "bot_data"

def authenticate_text_analytics_client():
    ta_credential = AzureKeyCredential(language_key)
    return TextAnalyticsClient(endpoint=language_endpoint, credential=ta_credential)

# def authenticate_blob_storage_client():
#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#     return blob_service_client

def get_random_question():
    with open("questions.json", "r") as f:
        questions = json.load(f)
    return random.choice(questions)

def get_random_answer():
    possible_answers = [
        "I'm glad to hear that!",
        "Thanks for sharing your thoughts!",
        "We appreciate your feedback!",
        "That's interesting! Thanks for letting us know."
    ]
    return random.choice(possible_answers)

def analyze_sentiment_and_store(question, sentiment_result, user_id):
    sentiment = sentiment_result.sentiment
    positive_responses = ["Thank you for your positive feedback!", "We're glad you enjoyed it!"]
    negative_responses = ["We're sorry to hear that. We'll work on improving!", "Thank you for your feedback. We'll take it into consideration."]

    if sentiment == "positive":
        return random.choice(positive_responses)
    else:
        return random.choice(negative_responses)

def process_user_message(user_message, user_id):
    global text_analytics_client
    if text_analytics_client is None:
        text_analytics_client = authenticate_text_analytics_client()

    # Get random question
    question = get_random_question()

    # Analyze sentiment and perform opinion mining on user's response
    response_sentiment_result = text_analytics_client.analyze_sentiment([user_message], show_opinion_mining=True)[0]

    # Generate response based on sentiment
    response = analyze_sentiment_and_store(question, response_sentiment_result, user_id)

    return response

# Example usage
user_message = "The food and service were great!"
user_id = "user123"
response = process_user_message(user_message, user_id)
print(response)
