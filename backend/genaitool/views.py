from django.shortcuts import render
import json
from django.http import JsonResponse
import openai
from django.views.decorators.csrf import csrf_exempt
# from openai import OpenAI
# import os
# from langchain.chains import ConversationChain
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import openai
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")

@csrf_exempt 
def get_ai_response(request):
    if request.method == 'POST': 
        # try:
            # Get the raw JSON data from the request body
            json_data = request.body.decode('utf-8')

            # Parse the JSON data
            input_data = json.loads(json_data)
            location_details = {}
            # Access the values from the input data, use get to avoid KeyErrors
            location_details['city'] = input_data.get('city')
            location_details['locality'] = input_data.get('locality', '')
            location_details['area'] = input_data.get('area', '')
            location_details['society'] = input_data.get('society', '')
            location_details['building'] = input_data.get('building', '')
            location_details['address'] = input_data.get('address', '')
            # User priorities is optional; fallback to default priorities if not provided
            given_priorities = input_data.get('user_priorities', [])
            user_priorities = {idx+1:prio for idx,prio in enumerate(given_priorities)}
            print("Here are user priorities: ", user_priorities)
            # Check if the mandatory 'city' field is present
            if not location_details['city']:
                return JsonResponse({'error': 'Missing required data: city'}, status=400)
            
            # Call generate_ai_response with the correct parameters
            response = generate_ai_response(location_details, user_priorities)
            
            # Return the AI response in JSON format
            return JsonResponse({'response': response}, safe=False)

        # except json.JSONDecodeError:
        #     # Handle JSON parsing errors
        #     return JsonResponse({'error': 'Invalid JSON input'}, status=400)

        # except Exception as e:
        #     # Handle any other exceptions and return error message
        #     return JsonResponse({'error': str(e)}, status=500)

    else:
        # Return error for non-POST requests
        error_message = "This is a POST-only endpoint"
        return JsonResponse({'error': error_message}, status=405)


# Step 1: Define the default ranking
# Default ranking list with both categories and topics
default_ranking = [
    ("Basic Infrastructure", "Underground Water Availability"),
    ("Basic Infrastructure", "Electricity Supply"),
    ("Basic Infrastructure", "Drainage System"),
    ("Basic Infrastructure", "Sewage System"),
    ("Basic Infrastructure", "Road Quality"),
    ("Basic Infrastructure", "Public Lighting"),
    ("Legal & Safety Concerns", "Legal Status of the Land"),
    ("Legal & Safety Concerns", "Crime Rate"),
    ("Legal & Safety Concerns", "Emergency Services"),
    ("Legal & Safety Concerns", "Building Safety"),
    ("Environmental Factors", "Air Quality Index (AQI)"),
    ("Environmental Factors", "Proximity to Polluting Industries"),
    ("Environmental Factors", "Noise Levels"),
    ("Environmental Factors", "Green Spaces"),
    ("Environmental Factors", "Flooding Risk"),
    ("Connectivity & Commute", "Public Transport"),
    ("Connectivity & Commute", "Road Connectivity"),
    ("Connectivity & Commute", "Traffic Conditions"),
    ("Connectivity & Commute", "Proximity to Workplaces"),
    ("Social Amenities", "Schools and Educational Institutions"),
    ("Social Amenities", "Healthcare Facilities"),
    ("Social Amenities", "Shopping and Grocery"),
    ("Social Amenities", "Food Outlets"),
    ("Social Amenities", "Entertainment & Leisure"),
    ("Community & Lifestyle", "Peaceful Living"),
    ("Community & Lifestyle", "Social Reviews and Reputation"),
    ("Community & Lifestyle", "Diversity & Inclusivity"),
    ("Community & Lifestyle", "Sense of Community"),
    ("Economic Considerations", "Property Prices"),
    ("Economic Considerations", "Rental Yield and Investment Potential"),
    ("Economic Considerations", "Cost of Living"),
    ("Economic Considerations", "Maintenance Costs"),
    ("Urban Planning and Development", "Future Development Plans"),
    ("Urban Planning and Development", "Zoning Regulations"),
    ("Urban Planning and Development", "Nearby Construction Projects"),
    ("Technology & Utilities", "Internet & Telecom Connectivity"),
    ("Technology & Utilities", "Garbage Collection and Recycling"),
    ("Climate and Weather Considerations", "Temperature Extremes"),
    ("Climate and Weather Considerations", "Wind Patterns"),
    ("Miscellaneous Factors", "Pet-friendliness"),
    ("Miscellaneous Factors", "Cultural and Religious Centers"),
    ("Miscellaneous Factors", "Proximity to Workspaces/Co-working Spaces"),
    ("Miscellaneous Factors", "Public Spaces"),
]

# Function to set priorities based on user input (category and topic-based priorities)
def set_priorities(user_priorities=None):
    """
    This function takes a dictionary of user_priorities and returns a list of all criteria 
    in the correct priority order. It handles cases where the user gives priority to either
    categories or specific topics in "Miscellaneous Factors."

    :param user_priorities: Dictionary where the key is the user priority (1, 2, 3...) 
                            and the value is either a category or a specific topic.
    :return: List of all criteria ordered by priority.
    """
    
    # If no user priorities are provided, return the default ranking
    if not user_priorities:
        return default_ranking
    
    # Initialize the result list for ordered priorities
    ordered_priorities = []
    
    # Keep track of which categories or topics have already been assigned by the user
    assigned_categories = set()
    assigned_topics = set()
    
    # Step 1: Assign user-defined category and topic priorities
    for priority in sorted(user_priorities):
        selection = user_priorities[priority]
        
        # Check if the selection is a category (handle whole categories)
        category_matched = False
        for cat, topic in default_ranking:
            if selection == cat and cat not in assigned_categories:
                ordered_priorities.extend([(cat, t) for c, t in default_ranking if c == cat])
                assigned_categories.add(cat)
                category_matched = True
                break
        
        # If it's not a category, it could be a specific topic (handle topics like Miscellaneous)
        if not category_matched:
            for cat, topic in default_ranking:
                if topic == selection and (cat, topic) not in assigned_topics:
                    ordered_priorities.append((cat, topic))
                    assigned_topics.add((cat, topic))
                    break

    # Step 2: Append the remaining default priorities in their original order
    for cat, topic in default_ranking:
        if (cat not in assigned_categories) and ((cat, topic) not in assigned_topics):
            ordered_priorities.append((cat, topic))
    
    return ordered_priorities


# Example usage
# '''
# user_priorities = {
#     1: "Climate and Weather Considerations",
#     2: "Pet-friendliness",
#     3: "Technology & Utilities"
# }

# # Call the function with user priorities
# result = set_priorities(user_priorities)

# # Output the result
# for i, (category, topic) in enumerate(result, 1):
#     print(f"Rank {i}: {category} - {topic}")

# '''
# Modify the set_priorities function (assuming it's already defined)

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage  # Import the required message format
import os

# Function to generate AI response
def generate_ai_response(location_details, user_priorities):
    api_key_config = os.getenv('OPENAI_API_KEY')
    city=location_details['city'],
    locality=location_details['locality'],
    area=location_details['area'],
    society=location_details['society'],
    building=location_details['building'],
    address=location_details['address']
    # Define LLM object using ChatOpenAI with specific parameters
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.2,  # Low temperature to make the responses more deterministic
        max_tokens=1000,  # Adjust max tokens to limit response length
    )

    # Generate the priority list
    result = set_priorities(user_priorities)
    priorities = ''
    top_two_priorities = []
    for i, (category, topic) in enumerate(result, 1):
        priorities += f"Rank {i}: {category} - {topic}\n"
        if len(top_two_priorities) < 2:
            top_two_priorities.append({category} - {topic})
   
    template = """
You are an expert real estate analyst. Provide a comprehensive, data-driven analysis of the following location for a user considering living or investing there.

**Location Details:**
- City: {city}
- Locality: {locality}
- Area: {area}
- Society: {society}
- Building: {building}
- Address: {address}

**User Priorities (Ranked starting from 1, 1 being highest priority):**
{priorities}

**Instructions:**

1. **Weigh User Preferences:** Prioritize your analysis based on the user's weighted preferences. Focus on the highest-weighted criteria first.

2. **Comparative Analysis:** Compare this location to other neighborhoods in {city} with similar cost of living, prioritizing {top_priority_1} and {top_priority_2}.  Highlight key differences and trade-offs.

3. **Actionable Cons and Mitigation:** For each "Con," suggest specific mitigation strategies.  For example, instead of "High traffic congestion," provide solutions like "High traffic congestion, particularly during peak hours.  Consider using public transportation (bus routes [route1], [route2]) or exploring alternative routes via [specific road names] using navigation apps like Google Maps or Waze."

4. **Data Source Integration (Simulated):**  Simulate querying external data sources.  For example:
    * "Check recent crime statistics from [specific data source URL, e.g., local police department website] for the past three years."
    * "Analyze property price trends from [specific real estate platform, e.g., Zillow, 99acres] for the past five years."
    * "Review school ratings and parent reviews from [website, e.g., GreatSchools]."
    While you cannot access these sources directly, frame your response as if you could, providing specific details you would expect to find.  This will help me validate and augment your response with real data later.

5. **Specific Examples for Pros and Cons:** Provide specific examples to support your claims. For example, instead of "Good schools," provide details like "Good schools, including [School Name 1] ranked [Rank] in the state and [School Name 2] known for its [Specific Program]."

6. **Explain "Why":** Justify your recommendations and the rationale behind each pro and con.

7. **Simulate User Interaction:** Anticipate potential user questions. For instance, if the user prioritizes commute, preemptively address questions about public transport options, parking availability, and typical commute times.

**Output Format:**

* **Top 5 Pros:**  List specific advantages, quantified where possible, with actionable recommendations.
* **Top 5 Cons:** Detail potential drawbacks with suggested mitigations or workarounds.
* **Investment Potential:** Analyze potential property value trends (simulated based on imagined data analysis).
* **Lifestyle Match:** Evaluate suitability for different lifestyles (e.g., families, young professionals, retirees).
* **Overall Recommendation (Highly Recommended / Recommended / Neutral / Not Recommended):**  Clearly state your recommendation.
* **Three Actionable Next Steps:**  Provide concrete steps the user can take to further their research or make a decision.
* **Critical Questions for the User:**  Suggest questions the user should consider or investigate further.


"""
    

    # Create the prompt template
    prompt_template = PromptTemplate(
        template=template, 
        input_variables=["city", "locality", "area", "society", "building", "address","priorities", "data_sources"]
    )

    # **Render** the prompt with actual values
    filled_prompt = prompt_template.format(
        city=city,
        locality=locality,
        area=area,
        society=society,
        building=building,
        address=address,
        priorities=priorities,
        top_priority_1=top_two_priorities[0],
        top_priority_2=top_two_priorities[1],
        # data_sources=data_sources
    )

    # Print the filled-in prompt for debugging
    print("Filled Prompt:")
    print(filled_prompt)

    # Pass the filled prompt as a `HumanMessage` object to the LLM
    response = llm.invoke([HumanMessage(content=filled_prompt)])
  # Wrap the prompt in a `HumanMessage`

    print("AI Response:")
    print(response.content)  # Assuming response has a `content` attribute
    return response.content