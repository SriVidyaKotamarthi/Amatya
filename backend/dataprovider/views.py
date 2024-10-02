from django.shortcuts import render

# Create your views here.
city_localities = {
    'Bengaluru': [
        'Banashankari', 'Bannerghatta Road', 'Basavanagudi', 'Bellandur', 'Benson Town',
        'BTM Layout', 'Chandapura', 'Cooke Town', 'Devanahalli', 'Electronic City',
        'Frazer Town', 'HSR Layout', 'Indiranagar', 'Jayanagar', 'Koramangala',
        'Malleshwaram', 'Marathahalli', 'Nagarbhavi', 'Rajajinagar', 'Sadashivanagar',
        'Sarjapur Road', 'Ulsoor', 'Whitefield', 'Yelahanka'
    ],
    'Delhi': [
        'Connaught Place', 'Karol Bagh', 'Lajpat Nagar', 'Greater Kailash', 'Hauz Khas',
        'Vasant Kunj', 'Saket', 'Dwarka', 'Janakpuri', 'Rohini', 'Pitampura',
        'Rajouri Garden', 'South Extension', 'Khan Market', 'Mayur Vihar', 'Preet Vihar'
    ],
    'Chennai': [
        'Adyar', 'T. Nagar', 'Velachery', 'Anna Nagar', 'Besant Nagar', 'Mylapore',
        'Kodambakkam', 'Nungambakkam', 'Tambaram', 'Guindy', 'Perungudi', 'Thiruvanmiyur',
        'Saidapet', 'Porur', 'Madipakkam'
    ],
    'Mumbai': [
        'Andheri', 'Bandra', 'Juhu', 'Powai', 'Borivali', 'Goregaon', 'Malad',
        'Kandivali', 'Dadar', 'Parel', 'Worli', 'Colaba', 'Versova', 'Vile Parle',
        'Santacruz'
    ],
    'Pune': [
        'Koregaon Park', 'Viman Nagar', 'Kothrud', 'Hinjewadi', 'Baner', 'Aundh',
        'Wakad', 'Kalyani Nagar', 'Hadapsar', 'Magarpatta', 'Bavdhan', 'Pimple Saudagar',
        'Pimpri', 'Chinchwad', 'Nigdi'
    ],
    'Ahmedabad': [
        'Satellite', 'Bopal', 'Vastrapur', 'Thaltej', 'Navrangpura', 'Prahlad Nagar',
        'Maninagar', 'Paldi', 'Bodakdev', 'Ambawadi', 'Ellis Bridge', 'Gota',
        'Naranpura', 'Shahibaug', 'Memnagar'
    ],
    'Hyderabad': [
        'Banjara Hills', 'Jubilee Hills', 'Madhapur', 'Gachibowli', 'Kondapur', 
        'Hitech City', 'Manikonda', 'Kukatpally', 'Begumpet', 'Secunderabad',
        'Somajiguda', 'Mehdipatnam', 'Ameerpet', 'Dilsukhnagar', 'Himayatnagar'
    ],
    'Kolkata': [
        'Salt Lake', 'New Town', 'Garia', 'Ballygunge', 'Jadavpur', 'Tollygunge',
        'Park Street', 'Behala', 'Dumdum', 'Howrah', 'Rajarhat', 'Alipore',
        'Kasba', 'Lake Town', 'Shyambazar'
    ]
}

# Dictionary containing localities as keys and their respective areas as values
locality_areas = {
    'Banashankari': ['Banashankari 1st Stage', 'Banashankari 2nd Stage', 'Banashankari 3rd Stage', 'Banashankari 4th Stage', 'Banashankari 5th Stage', 'Banashankari 6th Stage'],
    'Bannerghatta Road': ['Arekere', 'Hulimavu', 'Kalena Agrahara', 'Bilekahalli', 'J P Nagar', 'Bannerghatta'],
    'Basavanagudi': ['Gandhi Bazaar', 'Bull Temple Road', 'DVG Road', 'Ramkrishna Ashram', 'Srinivasanagar', 'Hanumanthnagar'],
    'Bellandur': ['Green Glen Layout', 'Outer Ring Road', 'Sarjapur Road', 'Devarabeesanahalli', 'Ibblur'],
    'Benson Town': ['Benson Cross Road', 'Miller’s Road', 'Jayamahal', 'Pillanna Garden', 'Pulkeshi Nagar'],
    'BTM Layout': ['BTM Layout 1st Stage', 'BTM Layout 2nd Stage', 'BTM Layout 3rd Stage', 'BTM Layout 4th Stage'],
    'Chandapura': ['Chandapura Anekal Road', 'Hebbagodi', 'Chandapura Circle', 'Attibele Road', 'Bommasandra'],
    'Cooke Town': ['Wheelers Road', 'Davis Road', 'Frazer Town', 'Richards Town'],
    'Devanahalli': ['Nandi Hills', 'Devanahalli Town', 'Vijayapura', 'Airport Road'],
    'Electronic City': ['Electronic City Phase 1', 'Electronic City Phase 2', 'Neeladri Nagar', 'Dodda Thogur'],
    'Frazer Town': ['Mosque Road', 'Coles Road', 'St. John’s Church Road', 'Promenade Road'],
    'HSR Layout': ['HSR Layout Sector 1', 'HSR Layout Sector 2', 'HSR Layout Sector 3', 'HSR Layout Sector 4', 'HSR Layout Sector 5', 'HSR Layout Sector 6', 'HSR Layout Sector 7'],
    'Indiranagar': ['100 Feet Road', 'CMH Road', 'Indiranagar 1st Stage', 'Indiranagar 2nd Stage', 'Defence Colony'],
    'Jayanagar': ['Jayanagar 1st Block', 'Jayanagar 2nd Block', 'Jayanagar 3rd Block', 'Jayanagar 4th Block', 'Jayanagar 5th Block', 'Jayanagar 6th Block', 'Jayanagar 7th Block', 'Jayanagar 8th Block', 'Jayanagar 9th Block'],
    'Koramangala': ['Koramangala 1st Block', 'Koramangala 2nd Block', 'Koramangala 3rd Block', 'Koramangala 4th Block', 'Koramangala 5th Block', 'Koramangala 6th Block', 'Koramangala 7th Block', 'Koramangala 8th Block'],
    'Malleshwaram': ['Malleswaram 1st Cross', 'Malleswaram 2nd Cross', 'Malleswaram 3rd Cross', 'Malleswaram 4th Cross', 'Malleswaram 5th Cross', 'Malleswaram 6th Cross', 'Malleswaram 7th Cross', 'Malleswaram 8th Cross', 'Malleswaram 9th Cross', 'Malleswaram 10th Cross'],
    'Marathahalli': ['Marathahalli Bridge', 'Kundalahalli Gate', 'Munnekolala', 'AECS Layout', 'Brookefield'],
    'Nagarbhavi': ['Nagarbhavi 1st Stage', 'Nagarbhavi 2nd Stage', 'BDA Layout', 'Vijayanagar'],
    'Rajajinagar': ['Rajajinagar 1st Block', 'Rajajinagar 2nd Block', 'Rajajinagar 3rd Block', 'Rajajinagar 4th Block', 'Rajajinagar 5th Block', 'Rajajinagar 6th Block'],
    'Sadashivanagar': ['Palace Orchards', 'RMV Extension', 'Sankey Road', 'Nandidurga Road'],
    'Sarjapur Road': ['Doddakannelli', 'Kaikondrahalli', 'Kasavanahalli', 'Wipro Corporate Office', 'Carmelaram'],
    'Ulsoor': ['Cambridge Layout', 'Murphy Town', 'Jogupalya', 'Cox Town'],
    'Whitefield': ['ITPL', 'Varthur', 'Kadugodi', 'Hope Farm Junction', 'Nallurhalli'],
    'Yelahanka': ['Yelahanka New Town', 'Yelahanka Old Town', 'Attur Layout', 'Vidyaranyapura', 'Kogilu']
}

location_data = {
    'Bengaluru': {
        'localities': {
            'Banashankari': {
                'areas': {
                    'Banashankari 1st Stage': {
                        'streets': ['1st Main', '2nd Main', '3rd Cross'],
                        'societies': ['Prestige Acropolis', 'Raheja Residency'],
                        'buildings': ['Building A', 'Building B'],
                    },
                    'Banashankari 2nd Stage': {
                        'streets': ['1st Cross', '2nd Cross'],
                        'societies': ['Greenwood Residency', 'Concorde Garden'],
                        'buildings': ['Building C', 'Building D'],
                    },
                    'Banashankari 3rd Stage': {

                    },

                }
            },
            # Add more localities and their corresponding data
        }
    },
}
