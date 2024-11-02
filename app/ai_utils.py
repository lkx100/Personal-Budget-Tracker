import requests
import os
import json
import google.generativeai as genai

def generate_ai_suggestion(expense_list):
    # Replace with your actual API key and endpoint
    api_key = os.getenv('AIzaSyDOqBteSfy31I3BT3frMM7gtaBIuBP2Ids')
    api_url = ''

    expenses_formatted = ""

    for expense in expense_list:
        expenses_formatted += f"Date: {expense['date']}, Category: {expense['category__name']}, Amount: {expense['amount']}\n"
    
    # genai.configure(api_key=os.environ["AIzaSyDOqBteSfy31I3BT3frMM7gtaBIuBP2Ids"])
    # model = genai.GenerativeModel("gemini-1.5-flash")
    # response = model.generate_content(f"Given the following expense data:\n{expenses_formatted}\nProvide personalized spending advice in Brief.")
    # response = model.generate_content(f"Tell me about hyderabad.")
    print(response.text)
    # Format the expense data

    prompt = f"Given the following expense data:\n{expenses_formatted}\nProvide personalized spending advice in Brief."

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    data = {
        'prompt': prompt,
        'max_tokens': 100,
    }



    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        suggestion = result['choices'][0]['text']
        return suggestion.strip()
    except Exception as e:
        print(f"AI suggestion error: {e}")
        return "Unable to generate suggestion at this time."