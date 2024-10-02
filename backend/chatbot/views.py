from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables, including the OpenAI API key
load_dotenv()

# Define the agents for each category
CLASS_AGENT_PAIRS = {
    "Basic Infrastructure": "Expert Civil Engineer / Professional Home Inspector",
    "Legal Concerns": "Expert Real Estate Attorney",
    "Safety Concerns": "Homeowner’s Insurance Specialist",
    "Environmental Factors": "Expert Environmental Consultant",
    "Connectivity & Commute": "Expert Transportation Planner of the city",
    "Social Amenities": "Senior Local Government Official / Community Center Director",
    "Community & Lifestyle": "Experienced Local Real Estate Agent",
    "Economic Considerations": "Professional Financial Advisor",
    "Urban Planning and Development": "Senior Local Government Official",
    "Technology": "IT Infrastructure Consultant",
    "Utilities": "Senior Representatives from local utility companies",
    "Climate and Weather Considerations": "Local Climate Scientist",
    "Miscellaneous Factors": "Professional General Advisor"
}

# Initialize the LLM (ChatOpenAI) for both classification and response generation
def initialize_llm():
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.3,  # Adjust temperature for balanced responses
        max_tokens=500
    )

# 1. Shared function to classify the question using LLM
def classify_user_question(user_question):
    """
    Takes the user's question, uses an LLM to classify it into one of the predefined categories, 
    and returns the classified category and the corresponding agent.
    """
    llm = initialize_llm()  # Initialize the LLM

    # Create the classification prompt
    classification_prompt = f"""
    You are an expert in understanding a question regarding real estate and urban planning. Your task is to classify the following question into one of these categories:
    1. Basic Infrastructure
    2. Legal Concerns
    3. Safety Concerns
    4. Environmental Factors
    5. Connectivity & Commute
    6. Social Amenities
    7. Community & Lifestyle
    8. Economic Considerations
    9. Urban Planning and Development
    10. Technology
    11. Utilities
    12. Climate and Weather Considerations
    13. Miscellaneous Factors
    
    Question: "{user_question}"
    Please return only the most relevant category from the list above.
    """

    # Generate the classification response using the LLM
    response = llm.generate([classification_prompt])
    classified_category = response.generations[0][0].text.strip()

    # Find the corresponding agent for the classified category
    agent = CLASS_AGENT_PAIRS.get(classified_category, "Professional General Advisor")

    return classified_category, agent

# 2. API to classify the user's question and return the category and agent
@csrf_exempt
def classify_question(request):
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)

            # Ensure that the 'question' field is provided
            user_question = data.get('question')
            if not user_question:
                return JsonResponse({'error': 'Missing required field: question'}, status=400)

            # Call the shared function to classify the question
            classified_category, agent = classify_user_question(user_question)

            # Return the classification and agent information
            return JsonResponse({'classified_category': classified_category, 'agent': agent})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON input'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'This is a POST-only endpoint'}, status=405)

# 3. API to generate the response based on the classified category and agent
@csrf_exempt
@csrf_exempt
def generate_agent_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            classified_category = data.get('category')
            user_question = data.get('question')
            city = data.get('city')
            location_details = data.get('locationDetails', {})
            user_priorities = data.get('userPriorities', [])

            if not classified_category or not user_question:
                return JsonResponse({'error': 'Missing required fields: category or question'}, status=400)

            agent = CLASS_AGENT_PAIRS.get(classified_category, "Professional General Advisor")
            llm = initialize_llm()

            context = f"City: {city}, Location Details: {location_details}, User Priorities: {user_priorities}"

            agent_prompt = f"""
            You are a {agent}. A user has asked a question about "{classified_category}". 
            Here is the context - {context}
            
            Question: "{user_question}"
            
            Provide the response in a professional and informative tone.
            """

            response = llm.generate([agent_prompt])
            agent_response = response.generations[0][0].text.strip()

            return JsonResponse({'agent': agent, 'response': agent_response})

        except json.JSONDecodeError:
            logger.error('Invalid JSON input')
            return JsonResponse({'error': 'Invalid JSON input'}, status=400)
        except Exception as e:
            logger.error(f'Error in generate_agent_response: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'This is a POST-only endpoint'}, status=405)