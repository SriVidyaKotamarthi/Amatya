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

def get_data_sources_list(city):
    if city == 'Bengaluru':
        return """
        1. Government and Public Sector Data Sources
            a. Urban Planning and Zoning
            Bangalore Development Authority (BDA): Information on zoning regulations, land-use patterns, approved layouts, and future development plans.
            Bruhat Bengaluru Mahanagara Palike (BBMP): Data on wards, property tax, civic infrastructure (roads, sewage, drainage), and building plans.
            Karnataka State Town Planning Department: For detailed town and country planning documents, urban development schemes.
            National Urban Information System (NUIS): Offers urban planning maps, GIS layers, and satellite imagery for cities like Bengaluru.
            b. Real Estate and Land Ownership
            Karnataka Land Records (Bhoomi): For property ownership, encumbrances, legal status of land (whether encroached or authorized), and other cadastral data.
            Karnataka Registration and Stamps Department: Data on land transaction details, property prices, and valuation trends.
            Revenue Department of Karnataka: Information on unauthorized land occupations and legal disputes related to land.
            c. Environment and Pollution
            Karnataka State Pollution Control Board (KSPCB): Data on air quality (AQI), water quality, industrial pollution, and environmental clearances.
            Central Pollution Control Board (CPCB): Provides air and water quality monitoring data, noise pollution levels, and reports on environmental violations.
            India Meteorological Department (IMD): Provides data on weather patterns, climate, and natural hazards (like flood zones).
            d. Infrastructure and Public Utilities
            Bangalore Water Supply and Sewerage Board (BWSSB): Data on water supply, sewage systems, and drainage infrastructure.
            Bangalore Electricity Supply Company (BESCOM): Data on power supply, outages, tariffs, and electric grid status.
            Karnataka Renewable Energy Development Ltd. (KREDL): For information on renewable energy infrastructure in the locality.
            e. Transport and Connectivity
            Bangalore Metropolitan Transport Corporation (BMTC): Bus routes, schedules, and public transport connectivity data.
            Namma Metro (Bangalore Metro Rail Corporation Limited): Data on metro routes, stations, upcoming lines, and accessibility.
            Karnataka Road Transport Department: Vehicle registrations, road tax data, and traffic congestion studies.
            Indian Railways: Data on railway stations, connectivity, and traffic near railway zones.
            f. Crime and Safety
            Bengaluru City Police: Crime statistics by locality, presence of police stations, law and order situation, and community policing initiatives.
            National Crime Records Bureau (NCRB): Detailed crime data, including local crime rates, types of crimes, and safety trends.
            g. Healthcare and Education
            Ministry of Health and Family Welfare: Data on public hospitals, clinics, health centers, and vaccination coverage.
            Department of Public Instruction, Karnataka: Data on government and private schools, their ratings, facilities, and performance.
            National Health Mission (NHM): Availability of health infrastructure, public health initiatives, and emergency services in a locality.
        2. Private Sector and Open-Data Platforms
            a. Real Estate Marketplaces
            MagicBricks, 99acres, Housing.com, CommonFloor: Detailed reviews of localities, property prices, rental yields, trends in property valuation, and resident feedback.
            PropTiger: Property data, real estate trends, upcoming projects, and locality insights.
            b. Property Analytics Platforms
            CRE Matrix, Square Yards: Data on property investment, market appreciation rates, property price indices, and rental yield comparisons.
            Zillow (for global cities) or Local Platforms: Location-specific heat maps for property valuation.
            c. Pollution and Environment Tracking
            BreezoMeter, AQICN.org: Real-time air quality index, pollution hotspots, historical air and water quality trends.
            OpenWeatherMap, AccuWeather: Local climate and weather data, micro-climate analysis for the area.
            d. Traffic and Mobility Data
            Google Maps, Waze: Real-time traffic congestion data, typical travel times, public transport efficiency, and local commute conditions.
            TomTom Traffic Index: Offers historical traffic data for Bengaluru, including congestion levels and time delays during peak hours.
            e. Social Reviews and Feedback
            Google Reviews, Zomato, TripAdvisor: Ratings and reviews of local amenities such as food outlets, entertainment, public services, and more.
            Facebook Groups, Reddit, Quora: Community feedback and discussion forums on specific localities.
        3. Open-Source Data and APIs
            a. OpenStreetMap (OSM)
            Detailed mapping data, including infrastructure, public amenities, road networks, points of interest, and geospatial insights on the locality.
            b. Bhuvan (ISRO)
            Provides high-resolution satellite imagery, urban planning data, and land-use patterns.
            c. Geospatial Data Platforms
            Mapbox, Carto: Offer APIs and datasets for urban geography, traffic movement, and infrastructure mapping.
        4. Academic and Research Institutions
            a. Indian Institute of Science (IISc)
            Research on air pollution, water bodies, urban sprawl, and the environmental impact of industrial zones in Bengaluru.
            b. Indian Institute of Management Bangalore (IIMB)
            Studies on real estate economics, urban governance, and socio-economic development.
            c. Institute for Social and Economic Change (ISEC)
            Reports on urbanization, economic development, infrastructure planning, and housing markets in Bengaluru.
        5. Civic Tech and NGO Platforms
            a. IChangeMyCity (Janaagraha)
            Crowdsourced data on civic issues, complaints about roads, garbage, safety, and drainage in different localities.
            b. Swaniti Initiative:
            Offers data-driven reports on public infrastructure, healthcare, and social amenities at the locality level.
            c. NGOs like Citizen Matters:
            Provide detailed journalism on urban issues, including mobility, pollution, healthcare access, and social life in Bengaluru.
            d. Transparent Chennai:
            Although Chennai-focused, this platform provides methodologies for assessing local amenities that can be applied to Bengaluru.
        6. Crowdsourced and IoT Data
            a. Yulu, Bounce (Bike and EV Sharing Platforms)
            Usage patterns, availability of shared mobility services, and infrastructure readiness for sustainable transport.
            b. Smart City Data (Bengaluru Smart City Ltd.)
            Offers data on smart city initiatives, including IoT-enabled services like smart parking, public WiFi, and waste management.
            c. Locality-Specific Social Media and Resident Forums
            Platforms like Nextdoor or Local WhatsApp Groups: Provide real-time resident feedback, community engagement, and alerts on civic issues.
        7. Historical and Cultural Context
            Heritage Data from Bangalore History Society or Urban Researchers: Information on heritage conservation, cultural landmarks, and historical relevance of the locality.
            Census Data: Demographics, socio-economic conditions, population density, literacy rates, and employment levels.
        """
    elif city == 'Delhi':
        return """"""
    elif city == 'Chennai':
        return """"""
    elif city == 'Kolkata':
        return """"""
    elif city == 'Mumbai':
        return """"""
    elif city == 'Hyderabad':
        return """"""
    elif city == 'Pune':
        return """"""
    else:
        return """"""

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

# def generate_ai_response(city, locality, area, building, street, user_priorities):
#     api_key_config = os.getenv('OPENAI_API_KEY')
#     # Define LLM object using ChatOpenAI with specific parameters
#     llm = ChatOpenAI(
#         model_name="gpt-3.5-turbo",
#         temperature=0.2,  # Low temperature to make the responses more deterministic
#         max_tokens=1000,  # Adjust max tokens to limit response length
#     )

#     # Generate the priority list
#     result = set_priorities(user_priorities)
#     priorities = ''
#     for i, (category, topic) in enumerate(result, 1):
#         priorities += f"Rank {i}: {category} - {topic}\n"
    
#     # Generate data sources
#     data_sources = get_data_sources_list(city)

#     # Define the prompt template
#     template = """You are an expert assistant to help the users with choosing the right location for living. \
#     You will do this by providing Pros and Cons of the place of their choice provided the following details.
#     City of choice : {city};
#     Locality: {locality};
#     Area: {area};
#     Building: {building};
#     Street: {street};
#     If any of the above details is 'None' ignore it and only consider the details that are provided.
#     The criteria to consider for providing the inputs are 
#     1. Basic Infrastructure
#     Underground Water Availability: Reliable and clean water supply, including borewell or municipal water access.
#     Electricity Supply: Uninterrupted electricity availability, the presence of power backup systems, and whether the locality is prone to frequent power cuts.
#     Drainage System: Efficient drainage to prevent waterlogging or flooding during rains.
#     Sewage System: Proper sewage and waste management systems to ensure hygiene and avoid pollution.
#     Road Quality: Well-paved, maintained roads within the locality and access to main roads.
#     Public Lighting: Adequate street lighting for safety during nighttime.
#     2. Legal & Safety Concerns
#     Legal Status of the Land: Ensure that the land is not encroached upon, and the property has clear titles. Check whether it's on unauthorized occupation or illegal land.
#     Crime Rate: Assess the safety of the neighborhood by looking at crime statistics and speaking to residents.
#     Emergency Services: Proximity to police stations, fire stations, and other emergency services.
#     Building Safety: Check for structural integrity, fire safety, earthquake resistance, etc.
#     3. Environmental Factors
#     Air Quality Index (AQI): Evaluate the air pollution levels in the locality, especially if there are industries nearby.
#     Proximity to Polluting Industries: Ensure the locality is not near factories or plants that emit air or water pollutants.
#     Noise Levels: Check if the area is free from excessive noise, whether from nearby roads, railway tracks, construction, or industries.
#     Green Spaces: Proximity to parks, trees, or other natural features for a healthier living environment.
#     Flooding Risk: Evaluate whether the locality is prone to flooding, especially during the monsoon.
#     4. Connectivity & Commute
#     Public Transport: Proximity to bus stops, metro stations, railway stations, or other forms of public transportation.
#     Road Connectivity: Access to main roads and highways, and proximity to major transport routes.
#     Traffic Conditions: Assess the traffic congestion in the area and whether traffic jams are frequent.
#     Proximity to Workplaces: Consider how far the locality is from your office or business hub, as well as general traffic during commute hours.
#     5. Social Amenities
#     Schools and Educational Institutions: Proximity to good schools, colleges, and daycare centers if applicable.
#     Healthcare Facilities: Access to hospitals, clinics, pharmacies, and specialized medical centers.
#     Shopping and Grocery: Availability of grocery stores, supermarkets, convenience stores, and vegetable markets nearby.
#     Food Outlets: Proximity to restaurants, cafés, street food, and other dining options.
#     Entertainment & Leisure: Access to malls, cinemas, parks, gyms, sports clubs, and recreational centers.
#     6. Community & Lifestyle
#     Peaceful Living: Check whether the locality is quiet and free from disturbances, like late-night parties, industrial noise, or loud commercial activity.
#     Social Reviews and Reputation: Gather feedback from current or past residents about their experience living in the area.
#     Diversity & Inclusivity: Whether the locality is welcoming to people of different backgrounds, cultures, and income levels.
#     Sense of Community: Is there an active residents' association, social events, or a good sense of neighborhood cooperation?
#     7. Economic Considerations
#     Property Prices: Evaluate the cost of buying or renting, including market trends and the potential for appreciation or depreciation.
#     Rental Yield and Investment Potential: If you’re buying, consider future rental yields and whether the area is seeing growth.
#     Cost of Living: Consider the cost of utilities, groceries, transportation, and services in the locality.
#     Maintenance Costs: Check if the upkeep of society/building (if applicable) is reasonable and whether shared services are well-managed.
#     8. Urban Planning and Development
#     Future Development Plans: Research upcoming infrastructure projects like metro lines, roads, or commercial spaces, which could affect property values.
#     Zoning Regulations: Check the zoning laws of the locality to ensure it aligns with your preferences (residential, mixed-use, or commercial zoning).
#     Nearby Construction Projects: Evaluate whether ongoing or planned construction projects might cause disruption or noise in the future.
#     9. Technology & Utilities
#     Internet & Telecom Connectivity: Availability of high-speed internet services and strong mobile network coverage.
#     Garbage Collection and Recycling: Efficiency of waste collection and recycling systems in the locality.
#     10. Miscellaneous Factors
#     Pet-friendliness: If you have pets, ensure that the locality and housing society allow pets and are pet-friendly.
#     Cultural and Religious Centers: Proximity to temples, churches, mosques, or other places of worship that might be significant to you.
#     Proximity to Workspaces/Co-working Spaces: Especially important for freelancers or remote workers.
#     Public Spaces: Access to libraries, community halls, or other public gathering spaces.
#     11. Climate and Weather Considerations
#     Temperature Extremes: Some areas may experience microclimates, so check for heatwaves, humidity, or cooler temperatures.
#     Wind Patterns: Some localities may be windier, which could affect comfort and energy use.

#     The order of importance for providing Pros and Cons on the above criteria is     
#     {priorities}
    
#     The data sources to be considered for providing the correct top suggestions are as below:
#     {data_sources}
    
#     Analyze the data in comparision to other areas of the city. When showing the results include the 
#     names of areas that you compared with. 
#     After analyzing all the available data from the sources mentioned, provide the response in the following format.
#     Response:
#     Pros:  List out all the pros (top 20 points)
#     Cons: List out all the cons (top 20 points)
#     Final Recommendation: For {city}-{locality}-{area}-{building}-{street} :
#     provide your final judgement to go for it or not.Please mention the area name. 
#     """
#     # Create the prompt
#     prompt = PromptTemplate(template=template, input_variables=["city", "locality", "area", "building", "street", "priorities", "data_sources"])
#     print(prompt)

#     # Combine prompt and LLM
#     llm_chain = prompt | llm

#     # **Fix**: Pass a dictionary with named arguments
#     response = llm_chain.invoke({
#         "city": city,
#         "locality": locality,
#         "area": area,
#         "building": building,
#         "street": street,
#         "priorities": priorities,
#         "data_sources": data_sources
#     })

#     print(response.content)
#     return response.content


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
    # Generate data sources
    # data_sources = get_data_sources_list(city)

    # Define the prompt template
    # ******************************** Self Given Prompt **********************
    # template = """You are an expert assistant to help the users with choosing the right location for living. 
    # You will do this by providing Pros and Cons of the place of their choice provided the following details.
    # City of choice : {city};
    # Locality: {locality};
    # Area: {area};
    # Society: {society};
    # Building: {building};
    # Address: {address};
    # If any of the above details is not given ignore it and only consider the details that are provided.
    
    # The criteria to consider for providing the inputs are 
    # 1. Basic Infrastructure
    # Underground Water Availability: Reliable and clean water supply, including borewell or municipal water access.
    # Electricity Supply: Uninterrupted electricity availability, the presence of power backup systems, and whether the locality is prone to frequent power cuts.
    # Drainage System: Efficient drainage to prevent waterlogging or flooding during rains.
    # Sewage System: Proper sewage and waste management systems to ensure hygiene and avoid pollution.
    # Road Quality: Well-paved, maintained roads within the locality and access to main roads.
    # Public Lighting: Adequate street lighting for safety during nighttime.
    # 2. Legal & Safety Concerns
    # Legal Status of the Land: Ensure that the land is not encroached upon, and the property has clear titles. Check whether it's on unauthorized occupation or illegal land.
    # Crime Rate: Assess the safety of the neighborhood by looking at crime statistics and speaking to residents.
    # Emergency Services: Proximity to police stations, fire stations, and other emergency services.
    # Building Safety: Check for structural integrity, fire safety, earthquake resistance, etc.
    # 3. Environmental Factors
    # Air Quality Index (AQI): Evaluate the air pollution levels in the locality, especially if there are industries nearby.
    # Proximity to Polluting Industries: Ensure the locality is not near factories or plants that emit air or water pollutants.
    # Noise Levels: Check if the area is free from excessive noise, whether from nearby roads, railway tracks, construction, or industries.
    # Green Spaces: Proximity to parks, trees, or other natural features for a healthier living environment.
    # Flooding Risk: Evaluate whether the locality is prone to flooding, especially during the monsoon.
    # 4. Connectivity & Commute
    # Public Transport: Proximity to bus stops, metro stations, railway stations, or other forms of public transportation.
    # Road Connectivity: Access to main roads and highways, and proximity to major transport routes.
    # Traffic Conditions: Assess the traffic congestion in the area and whether traffic jams are frequent.
    # Proximity to Workplaces: Consider how far the locality is from your office or business hub, as well as general traffic during commute hours.
    # 5. Social Amenities
    # Schools and Educational Institutions: Proximity to good schools, colleges, and daycare centers if applicable.
    # Healthcare Facilities: Access to hospitals, clinics, pharmacies, and specialized medical centers.
    # Shopping and Grocery: Availability of grocery stores, supermarkets, convenience stores, and vegetable markets nearby.
    # Food Outlets: Proximity to restaurants, cafés, street food, and other dining options.
    # Entertainment & Leisure: Access to malls, cinemas, parks, gyms, sports clubs, and recreational centers.
    # 6. Community & Lifestyle
    # Peaceful Living: Check whether the locality is quiet and free from disturbances, like late-night parties, industrial noise, or loud commercial activity.
    # Social Reviews and Reputation: Gather feedback from current or past residents about their experience living in the area.
    # Diversity & Inclusivity: Whether the locality is welcoming to people of different backgrounds, cultures, and income levels.
    # Sense of Community: Is there an active residents' association, social events, or a good sense of neighborhood cooperation?
    # 7. Economic Considerations
    # Property Prices: Evaluate the cost of buying or renting, including market trends and the potential for appreciation or depreciation.
    # Rental Yield and Investment Potential: If you’re buying, consider future rental yields and whether the area is seeing growth.
    # Cost of Living: Consider the cost of utilities, groceries, transportation, and services in the locality.
    # Maintenance Costs: Check if the upkeep of society/building (if applicable) is reasonable and whether shared services are well-managed.
    # 8. Urban Planning and Development
    # Future Development Plans: Research upcoming infrastructure projects like metro lines, roads, or commercial spaces, which could affect property values.
    # Zoning Regulations: Check the zoning laws of the locality to ensure it aligns with your preferences (residential, mixed-use, or commercial zoning).
    # Nearby Construction Projects: Evaluate whether ongoing or planned construction projects might cause disruption or noise in the future.
    # 9. Technology & Utilities
    # Internet & Telecom Connectivity: Availability of high-speed internet services and strong mobile network coverage.
    # Garbage Collection and Recycling: Efficiency of waste collection and recycling systems in the locality.
    # 10. Miscellaneous Factors
    # Pet-friendliness: If you have pets, ensure that the locality and housing society allow pets and are pet-friendly.
    # Cultural and Religious Centers: Proximity to temples, churches, mosques, or other places of worship that might be significant to you.
    # Proximity to Workspaces/Co-working Spaces: Especially important for freelancers or remote workers.
    # Public Spaces: Access to libraries, community halls, or other public gathering spaces.
    # 11. Climate and Weather Considerations
    # Temperature Extremes: Some areas may experience microclimates, so check for heatwaves, humidity, or cooler temperatures.
    # Wind Patterns: Some localities may be windier, which could affect comfort and energy use.

    # The criteria to consider for providing the inputs are ...
    
    # The order of importance for providing Pros and Cons on the above criteria is     
    # {priorities}
    
    # The data sources to be considered for providing the correct top suggestions are as below:
    # {data_sources}
    
    # Analyze the data in comparison to other areas of the city. When showing the results include the 
    # names of areas that you compared with. 
    
    # Response:
    # Pros:  List out all the pros (top 20 points). 
    # Do not include sub headings. The points should be specific to the location(mention name of the location like area, locality as ans when required) and in comaparision to other locations, crisp, clear, short and simple.
    # Cons: List out all the cons (top 20 points) The points should be specific to the location and in comaparision to other locations, crisp, clear, short and simple.
    # Recommendation: Keep it simple clear and short with reasoning.Provide your final judgement to go for it or not. Please mention the location details to give more confidence in the results.
    # """
    # ************************************** Google suggested ***************
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
    # top_two_priorities = list(priorities.values())[:2]

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
    response = llm([HumanMessage(content=filled_prompt)])  # Wrap the prompt in a `HumanMessage`

    print("AI Response:")
    print(response.content)  # Assuming response has a `content` attribute
    return response.content