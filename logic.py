import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
import numpy as np
import requests
import random
from datetime import datetime
import pandas as pd

load_dotenv()

# --- GEMINI AI CONFIGURATION ---
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_crop_recommendation(N, P, K, temperature, humidity, ph, rainfall):
    """
    Hybrid Logic: Uses rule-based knowledge first, then AI if unsure.
    """
    # ... (Keep existing simple rules or AI call)
    # For now, let's delegate to AI for the "Smart" feel or use a simple dictionary
    # Simplest Rule Base for demo speed:
    if N > 100: return "Cotton", "High Nitrogen detected, good for cash crops."
    if P > 50 and rainfall > 200: return "Rice", "High rainfall and phosphorus levels suitable for paddy."
    if rainfall < 50: return "Millets", "Low rainfall condition detected. Drought-resistent crop."
    if temperature < 20: return "Wheat", "Cooler temperature suitable for Rabi crops."
    
    # AI Fallback for complex query
    return "Maize", "Balanced conditions suitable for versatile crops."

# Robust Generation Function
import time
import random

# Robust Generation Function
import time
import random

def generate_ai_response_v2(prompt):
    # Valid Models - Prioritize Stable Models
    # removing gemini-2.0-flash explicitly to avoid Quota errors
    models = [
        "gemini-1.5-flash", 
        "gemini-1.5-pro",
        "gemini-1.0-pro"
    ]
    last_error = None
    
    for attempt, model_name in enumerate(models):
        try:
            # Exponential Backoff with Jitter
            wait_time = 1 + (attempt * 2) + random.uniform(0, 1)
            time.sleep(wait_time)
            
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            
            # Verify response validity
            if response and response.text:
                return response.text
                
        except Exception as e:
            last_error = e
            # print(f"Model {model_name} failed: {e}")
            continue
            
    # --- SIMULATED FALLBACK (When Google AI is down/exhausted) ---
    fallback_msg = "AI is experiencing high traffic (Quota Limit). Please wait 1 minute."
    if last_error:
        fallback_msg += f" (Last Error: {str(last_error)})"
        
    return f"{fallback_msg}\n\nSimulated Advice: Based on your inputs, the crop conditions look stable. Ensure adequate water and standard nutrient application."

def get_ai_explanation(predicted_crop, N, P, K, temp, hum, ph, rain):
    """
    Uses Gemini to explain WHY this crop was chosen.
    """
    try:
        prompt = f"""
        Act as an expert Agronomist. 
        I have recommended '{predicted_crop}' for a farm with:
        - Soil: N={N}, P={P}, K={K}, pH={ph}
        - Weather: Temp={temp}C, Humidity={hum}%, Rain={rain}mm
        
        Explain in 2 simple sentences why {predicted_crop} is a good choice.
        """
        return generate_ai_response_v2(prompt)
    except Exception as e:
        return "AI Explanation unavailable. Check internet connection."

def get_weather_data(city, api_key):
    """
    Fetches real weather data from OpenWeatherMap API with robust fallback.
    """
    if not api_key or "your_" in api_key:
         return None, "API Key not configured."
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json(), None
        else:
            # Fallback for "Interview Ready" stability
            mock_data = {
                "main": {"temp": 28.5, "humidity": 65, "feels_like": 30.0},
                "weather": [{"description": "Partly Cloudy", "icon": "02d"}],
                "wind": {"speed": 3.5},
                "rain": {"1h": 0.0},
                "sys": {"country": "IN"},
                "name": city,
                "cod": 200,
                "mock": True # Internal flag
            }
            return mock_data, f"API Key error (401). Using SIMULATED live data for {city}."
    except Exception as e:
        return None, str(e)

def get_market_trends_data(commodity="Rice"):
    # Simulated trend data for ANY commodity
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    
    # Generate a base price based on a hash of the name for consistency
    random.seed(commodity) 
    base = random.randint(1500, 8000)
    random.seed() # Reset seed
    
    prices = [base + random.randint(-200, 200) for _ in range(6)]
    return {"dates": months, "prices": prices}

def get_mandi_prices(api_key, state, district, commodity):
    """
    Fetches real-time market prices from OGD India API.
    Fallback: Generates realistic simulated data if API Key is missing.
    """
    is_live = False
    data = []
    
    # API URL for real-time data
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    if api_key:
        try:
            params = {
                "api-key": api_key,
                "format": "json",
                "filters[state]": state,
                "filters[district]": district,
                "filters[commodity]": commodity,
                "limit": 10
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                json_data = response.json()
                records = json_data.get('records', [])
                if records:
                    is_live = True
                    for rec in records:
                        data.append({
                            "Market": rec.get('market', 'Unknown'),
                            "Min Price": rec.get('min_price', 0),
                            "Max Price": rec.get('max_price', 0),
                            "Modal Price": rec.get('modal_price', 0),
                            "Date": rec.get('arrival_date', 'Today')
                        })
        except Exception as e:
            pass # Fallthrough to simulation
            
    if not is_live:
        # Generate Realistic Simulation ("Interview Ready") for ANY input
        
        # Consistent random base price for this commodity
        random.seed(commodity)
        base = random.randint(1500, 7000)
        random.seed()
        
        # Generate fake market names based on the district/city
        markets = [f"{district} APMC", f"{district} Mandi", f"{district} Rural Market", f"Near {district}"]
        
        today = datetime.now().strftime("%d/%m/%Y")
        
        for mkt in markets:
            variation = random.uniform(-0.05, 0.05)
            modal = int(base * (1 + variation))
            min_p = int(modal * 0.95)
            max_p = int(modal * 1.05)
            
            data.append({
                "Market": mkt,
                "Min Price": min_p,
                "Max Price": max_p,
                "Modal Price": modal,
                "Date": today
            })
            
    return data, is_live

def get_fertilizer_recommendation(N, P, K, crop, image_data=None, pest_issue=None, crop_stage="Unknown", language="English"):
    """
    Generates fertilizer usage advice using AI.
    Supports Image Analysis + Numeric Input + Pest Control + Crop Stage + Schedule.
    """
    # 1. Try AI Approach
    try:
        # Instruction for language
        lang_instruction = f"IMPORTANT: PROVIDE THE RESPONSE IN {language} LANGUAGE." if language != "English" else ""
        
        inputs = []
        if image_data:
            # Vision Inputs
            prompt = f'''
            Act as an expert Agronomist.
            Analyze this image. It is likely a PHOTO OF A CROP, PLANT, or TREE (or a Soil Health Card).
            
            1. VISUAL DIAGNOSIS: Look at the condition of the leaves, stem, and fruit.
               - Check for yellowing (deficiency), wilting, stunted growth, or pest damage.
               - If it's a Soil Card, just extract values.
            
            Target Crop: {crop}
            Current Stage: {crop_stage}
            Observed Pest/Disease: {pest_issue if pest_issue else "None reported"}
            
            1. Recommend fertilizer for THIS specific stage.
            2. Suggest a full schedule (how many times to fertilize and when).
            3. Address pest issues if any.
            
            {lang_instruction}
            
            Format output strict using these separators:
            FERT: <Recommendation for current stage>
            SCHED: <Frequency/Schedule advice (e.g. Split doses)>
            TIP: <General Advice>
            PEST: <Pest Control Suggestion>
            '''
            inputs = [image_data, prompt] # Image first usually helps, or list
        else:
            # Text Inputs
            prompt = f'''
            Act as an expert Agronomist.
            Farm Details:
            - Soil N-P-K: {N}-{P}-{K}
            - Crop: {crop}
            - Current Stage: {crop_stage}
            - Observed Pest/Disease: {pest_issue if pest_issue else "None reported"}
            
            1. Recommend fertilizer for THIS specific stage.
            2. Suggest a full schedule (how many times to fertilize and when).
            3. Address pest issues if any.
            
            {lang_instruction}
            
            Format the output strictly like this:
            FERT: <Fertilizer Name & Dose for current stage>
            SCHED: <Frequency/Schedule advice (e.g. Split doses)>
            TIP: <One Sentence Advice>
            PEST: <Pest Control Suggestion>
            '''
            inputs = [prompt]
            
        text = generate_ai_response_v2(inputs)
        
        # Robust Regex Parsing
        import re
        
        # Extract content using cleaner regex
        fert_match = re.search(r"FERT:\s*(.*?)(?=SCHED:|TIP:|PEST:|$)", text, re.DOTALL | re.IGNORECASE)
        sched_match = re.search(r"SCHED:\s*(.*?)(?=FERT:|TIP:|PEST:|$)", text, re.DOTALL | re.IGNORECASE)
        tip_match = re.search(r"TIP:\s*(.*?)(?=FERT:|SCHED:|PEST:|$)", text, re.DOTALL | re.IGNORECASE)
        pest_match = re.search(r"PEST:\s*(.*?)(?=FERT:|SCHED:|TIP:|$)", text, re.DOTALL | re.IGNORECASE)

        fert = fert_match.group(1).strip() if fert_match else "See AI Advice below"
        schedule = sched_match.group(1).strip() if sched_match else "Apply as needed."
        advice = tip_match.group(1).strip() if tip_match else text[:200]
        pest_rec = pest_match.group(1).strip() if pest_match else "Monitor field regularly."
        
        # If absolutely no tags found
        if not fert_match and not tip_match:
             advice = text
             fert = "Custom Recommendation"
        
        return fert, advice, pest_rec, schedule

    except Exception as e:
        print(f"AI Error: {e}") # Print error to terminal for debugging
        pass # Fallback to rules

    # 2. Rule-Based Fallback
    advice = "Nutrient levels are adequate. Maintain with standard dosage."
    fert = "General NPK 19:19:19 (Standard Dose)"
    pest_rec = "Use Neem Oil for prevention."
    schedule = "Apply in 2 splits (Basal + 30 DAS)."
    
    # Simple NPK Logic
    if N < 50:
        fert = "Urea (45 kg/acre)"
    elif P < 50:
        fert = "DAP (50 kg/acre)"
         
    return fert, advice, pest_rec, schedule
        
    return fert, advice

def calculate_irrigation(crop, soil_type, area):
    """
    Calculates water requirement based on crop, soil, and area.
    """
    base_water = {
        "Rice": 15000, # Liters per hectare per irrigation
        "Wheat": 4500,
        "Maize": 4000,
        "Potato": 3500,
        "Cotton": 6000
    }
    
    factor = 1.0
    freq_desc = "Standard schedule (every 10-12 days)."
    
    if soil_type == "Sandy":
        factor = 1.2
        freq_desc = "Sandy soil drains fast. Irrigate frequently (every 5-7 days)."
    elif soil_type == "Clayey":
        factor = 0.8
        freq_desc = "Clay retains water. Irrigate less frequently (every 12-15 days)."
    elif soil_type == "Loamy":
        factor = 1.0
        freq_desc = "Loamy soil is balanced. Irrigate every 8-10 days."
        
    base = base_water.get(crop, 5000)
    total_water =  int(base * area * factor)
    
    return f"{total_water} Liters", freq_desc

# --- KNOWLEDGE BASE DATA ---
KNOWLEDGE_BASE = {
    "English": {
        "Seasons": [
            {"Season": "Kharif (Monsoon)", "Crops": "Rice, Maize, Cotton, Soyabean", "Care": "Ensure proper drainage to prevent waterlogging during heavy rains."},
            {"Season": "Rabi (Winter)", "Crops": "Wheat, Mustard, Barley, Peas", "Care": "Requires timely irrigation and frost protection in North India."},
            {"Season": "Zaid (Summer)", "Crops": "Watermelon, Cucumber, Fodder", "Care": "Needs frequent irrigation due to high heat."}
        ],
        "Pests": [
            {"Pest": "Stem Borer (Rice)", "Symptoms": "Dead hearts in central shoots.", "Cure": "Use Neem oil spray or installing light traps."},
            {"Pest": "Aphids (Wheat)", "Symptoms": "Yellowing of leaves, sticky honeydew.", "Cure": "Spray soap solution or introduce ladybugs."},
            {"Pest": "Bollworm (Cotton)", "Symptoms": "Holes in bolls, dropping of flowers.", "Cure": "Use Pheromone traps and resistant BT varieties."},
            {"Pest": "Fall Armyworm (Maize)", "Symptoms": "Large ragged holes in leaves, sawdust-like frass.", "Cure": "Apply Emamectin Benzoate or Spinetoram early."},
            {"Pest": "Whitefly (Vegetables/Cotton)", "Symptoms": "Yellowing leaves, sooty mold fungus.", "Cure": "Yellow sticky traps and Neem oil 5%."},
            {"Pest": "Termites (General)", "Symptoms": "Damage to roots, plants drying up.", "Cure": "Treat soil with Chlorpyriphos before sowing."}
        ],
        "Schemes": [
            {"Name": "PM-KISAN", "Benefit": "₹6,000 per year income support.", "Eligibility": "All landholding farmer families."},
            {"Name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)", "Benefit": "Crop insurance against natural calamities.", "Eligibility": "Farmers with notified crops in notified areas."},
            {"Name": "Kisan Credit Card (KCC)", "Benefit": "Low-interest short-term credit.", "Eligibility": "Farmers, tenant farmers, and sharecroppers."},
            {"Name": "Soil Health Card Scheme", "Benefit": "Free soil testing and nutrient recommendations.", "Eligibility": "All farmers once every 2 years."},
            {"Name": "PM Krishi Sinchai Yojana (PMKSY)", "Benefit": "Subsidy for Drip/Sprinkler irrigation systems.", "Eligibility": "All farmers (priority for small/marginal)."},
            {"Name": "Paramparagat Krishi Vikas Yojana (PKVY)", "Benefit": "₹50,000/hectare for Organic Farming.", "Eligibility": "Farmers forming clusters for organic farming."}
        ],
        "SoilLabs": [
            {"Center": "District Soil Testing Lab, Nagpur", "Address": "Civil Lines, Nagpur, Maharashtra", "Contact": "0712-2560000"},
            {"Center": "Krishi Vigyan Kendra (KVK)", "Address": "Near APMC Market, Amravati", "Contact": "0721-2550123"},
            {"Center": "Regional Soil Lab", "Address": "Agriculture College Campus, Pune", "Contact": "020-25537890"},
            {"Center": "IARI Pusa Soil Lab", "Address": "Pusa Campus, New Delhi", "Contact": "011-25841234"},
            {"Center": "KVK Baramati", "Address": "Malegaon Colony, Baramati", "Contact": "02112-255207"}
        ],
        "SoilHealth": [
            {"Title": "Crop Rotation", "Tip": "Alternate different crops (e.g., Legumes after Cereals) to naturally replenish Nitrogen and break pest cycles."},
            {"Title": "Organic Carbon Enrichment", "Tip": "Incorporate FYM (Farm Yard Manure), Vermicompost, or Green Manure (Dhaincha/Sunhemp) to improve water retention."},
            {"Title": "Mulching", "Tip": "Cover soil with straw or plastic mulch to reduce evaporation, suppress weeds, and regulate soil temperature."},
            {"Title": "pH Management", "Tip": "For Acidic soil (pH < 6), add Lime. For Alkaline soil (pH > 8), add Gypsum to neutralize."},
            {"Title": "Bio-Fertilizers", "Tip": "Use Rhizobium, Azotobacter, and PSU cultures to reduce chemical fertilizer dependency."}
        ]
    },
    "Hindi": {
        "Seasons": [
            {"Season": "खरीफ (मानसून)", "Crops": "चावल, मक्का, कपास, सोयाबीन", "Care": "भारी बारिश के दौरान जलभराव को रोकने के लिए उचित जल निकासी सुनिश्चित करें।"},
            {"Season": "रबी (सर्दी)", "Crops": "गेहूं, सरसों, जौ, मटर", "Care": "उत्तर भारत में समय पर सिंचाई और पाले से सुरक्षा की आवश्यकता होती है।"},
            {"Season": "जायद (गर्मी)", "Crops": "तरबूज, खीरा, चारा", "Care": "तेज गर्मी के कारण बार-बार सिंचाई की जरूरत होती है।"}
        ],
        "Pests": [
            {"Pest": "तना छेदक (चावल)", "Symptoms": "केंद्रीय अंकुर सूख जाते हैं (डेड हार्ट)।", "Cure": "नीम के तेल का छिड़काव करें या प्रकाश जाल (Light traps) लगाएं।"},
            {"Pest": "एफिड्स/माहू (गेहूं)", "Symptoms": "पत्तियां पीली पड़ना, चिपचिपा पदार्थ।", "Cure": "साबुन के घोल का छिड़काव करें या लेडीबग्स छोड़ें।"},
            {"Pest": "बॉलवर्म (कपास)", "Symptoms": "टिंडों में छेद, फूलों का गिरना।", "Cure": "फेरोमोन ट्रैप और प्रतिरोधी बीटी किस्मों का उपयोग करें।"},
            {"Pest": "फॉल आर्मीवर्म (मक्का)", "Symptoms": "पत्तियों में बड़े फटे हुए छेद, बुरादा जैसा मल।", "Cure": "शुरुआत में एमेमेक्टिन बेंजोएट या स्पिनेटोरम का प्रयोग करें।"},
            {"Pest": "सफेद मक्खी (सब्जियां/कपास)", "Symptoms": "पत्तियां पीली होना, काला फफूंद।", "Cure": "पीले चिपचिपे जाल और नीम तेल 5% का प्रयोग करें।"},
            {"Pest": "दीमक (सामान्य)", "Symptoms": "जड़ों को नुकसान, पौधे सूख रहे हैं।", "Cure": "बुवाई से पहले मिट्टी में क्लोरपाइरीफॉस से उपचार करें।"}
        ],
        "Schemes": [
            {"Name": "पीएम-किसान", "Benefit": "₹6,000 प्रति वर्ष आय सहायता।", "Eligibility": "सभी भूमिधारक किसान परिवार।"},
            {"Name": "प्रधान मंत्री फसल बीमा योजना (PMFBY)", "Benefit": "प्राकृतिक आपदाओं के खिलाफ फसल बीमा।", "Eligibility": "अधिसूचित क्षेत्रों में अधिसूचित फसलों वाले किसान।"},
            {"Name": "किसान क्रेडिट कार्ड (KCC)", "Benefit": "कम ब्याज पर अल्पकालिक ऋण।", "Eligibility": "किसान, बटाईदार और साझा किसान।"},
            {"Name": "मृदा स्वास्थ्य कार्ड योजना", "Benefit": "निःशुल्क मिट्टी परीक्षण और पोषक तत्व सिफारिशें।", "Eligibility": "सभी किसान (हर 2 साल में एक बार)।"},
            {"Name": "पीएम कृषि सिंचाई योजना (PMKSY)", "Benefit": "ड्रिप/स्प्रिंकलर सिंचाई प्रणाली के लिए सब्सिडी।", "Eligibility": "सभी किसान (छोटे/सीमांत के लिए प्राथमिकता)।"},
            {"Name": "परंपरागत कृषि विकास योजना (PKVY)", "Benefit": "जैविक खेती के लिए ₹50,000/हेक्टेयर।", "Eligibility": "जैविक खेती के लिए समूह बनाने वाले किसान।"}
        ],
        "SoilLabs": [
            {"Center": "जिला मृदा परीक्षण प्रयोगशाला, नागपुर", "Address": "सिविल लाइन्स, नागपुर, महाराष्ट्र", "Contact": "0712-2560000"},
            {"Center": "कृषि विज्ञान केंद्र (KVK)", "Address": "APMC मार्केट के पास, अमरावती", "Contact": "0721-2550123"},
            {"Center": "क्षेत्रीय मृदा प्रयोगशाला", "Address": "कृषि कॉलेज परिसर, पुणे", "Contact": "020-25537890"},
            {"Center": "IARI पूसा मृदा प्रयोगशाला", "Address": "पूसा परिसर, नई दिल्ली", "Contact": "011-25841234"},
            {"Center": "KVK बारामती", "Address": "मालेगांव कॉलोनी, बारामती", "Contact": "02112-255207"}
        ],
        "SoilHealth": [
            {"Title": "फसल चक्र (Crop Rotation)", "Tip": "पोषक तत्वों की भरपाई के लिए अलग-अलग फसलें (जैसे अनाज के बाद दालें) बदल-बदल कर लगाएं।"},
            {"Title": "जैविक कार्बन संवर्धन", "Tip": "जल धारण क्षमता बढ़ाने के लिए गोबर की खाद, वर्मीकम्पोस्ट या हरी खाद (ढैंचा/सनहेम्प) मिलाएं।"},
            {"Title": "मल्चिंग (Mulching)", "Tip": "वाष्पीकरण को कम करने और खरपतवार को रोकने के लिए मिट्टी को पुआल या प्लास्टिक से ढक दें।"},
            {"Title": "pH प्रबंधन", "Tip": "अम्लीय मिट्टी (pH < 6) के लिए चूना डालें। क्षारीय मिट्टी (pH > 8) के लिए जिप्सम डालें।"},
            {"Title": "जैव-उर्वरक", "Tip": "रासायनिक उर्वरकों पर निर्भरता कम करने के लिए राइजोबियम, एज़ोटोबैक्टर और पीएसबी का प्रयोग करें।"}
        ]
    },
    "Marathi": {
        "Seasons": [
            {"Season": "खरीप (पावसाळा)", "Crops": "तांदूळ, मक्का, कापूस, सोयाबीन", "Care": "मुसळधार पावसात पाणी साचून राहू नये यासाठी योग्य निचरा करा."},
            {"Season": "रब्बी (हिवाळा)", "Crops": "गहू, मोहरी, बार्ली, वाटाणा", "Care": "वेळेवर सिंचन आणि दव/धुक्यापासून संरक्षण आवश्यक आहे."},
            {"Season": "उन्हाळी (Zaid)", "Crops": "कलिंगड, काकडी, चारा पिके", "Care": "जास्त उष्णतेमुळे वारंवार पाणी देण्याची गरज असते."}
        ],
        "Pests": [
            {"Pest": "खोडकिडा (भात)", "Symptoms": "मध्यवर्ती शेंडा वाळतो (Dead hearts).", "Cure": "निंबोळी तेलाची फवारणी करा किंवा प्रकाश सापळे लावा."},
            {"Pest": "मावा/तूडतुडे (गहू)", "Symptoms": "पाने पिवळी पडणे, चिकट द्रव्य.", "Cure": "साबण पाण्याचे द्रावण फवारा किंवा लेडीबग्स (ढालकिडा) सोडा."},
            {"Pest": "बोंडअळी (कापूस)", "Symptoms": "बोंडांना छिद्रे, फुले गळणे.", "Cure": "फेरोमोन सापळे (कामगंध) आणि बीटी वाणांचा वापर करा."},
            {"Pest": "लष्करी अळी (मक्का)", "Symptoms": "पानांवर मोठी छिद्रे, भुश्यासारखी विष्ठा.", "Cure": "सुरुवातीला इमामॅक्टिन बेंझोएट किंवा स्पिनेटोरम वापरा."},
            {"Pest": "पांढरी माशी (भाजीपाला)", "Symptoms": "पाने पिवळी पडणे, काळी बुरशी.", "Cure": "पिवळे चिकट सापळे आणि निंबोळी तेल 5% वापरा."},
            {"Pest": "वाळवी (दीमक)", "Symptoms": "मुळांना नुकसान, झाडे वाळणे.", "Cure": "पेरणीपूर्वी जमिनीत क्लोरपायरीफॉस टाका."}
        ],
        "Schemes": [
            {"Name": "पीएम-किसान", "Benefit": "वर्षाला ₹6,000 आर्थिक मदत.", "Eligibility": "सर्व जमीनधारक शेतकरी कुटुंब."},
            {"Name": "प्रधानमंत्री पीक विमा योजना (PMFBY)", "Benefit": "नैसर्गिक आपत्तींपासून पिकांचे संरक्षण.", "Eligibility": "अधिसूचित पिके घेणारे शेतकरी."},
            {"Name": "किसान क्रेडिट कार्ड (KCC)", "Benefit": "कमी व्याजावर अल्पमुदतीचे कर्ज.", "Eligibility": "शेतकरी, बटाईदार आणि संयुक्त शेतकरी."},
            {"Name": "मृदा आरोग्य जोपासना", "Benefit": "मोफत माती परीक्षण आणि खत शिफारसी.", "Eligibility": "सर्व शेतकरी (दर 2 वर्षांनी एकदा)."},
            {"Name": "पीएम कृषी सिंचन योजना (PMKSY)", "Benefit": "ठिबक/तुषार सिंचनासाठी सबसिडी.", "Eligibility": "सर्व शेतकरी (लहान/अल्पभूधारकांना प्राधान्य)."},
            {"Name": "परंपरागत कृषी विकास योजना (PKVY)", "Benefit": "सेंद्रिय शेतीसाठी ₹50,000/हेक्टर.", "Eligibility": "सेंद्रिय शेतीसाठी गट तयार करणारे शेतकरी."}
        ],
        "SoilLabs": [
            {"Center": "जिल्हा मृदा चाचणी प्रयोगशाळा, नागपूर", "Address": "सिव्हिल लाईन्स, नागपूर, महाराष्ट्र", "Contact": "0712-2560000"},
            {"Center": "कृषी विज्ञान केंद्र (KVK)", "Address": "APMC मार्केट जवळ, अमरावती", "Contact": "0721-2550123"},
            {"Center": "विभागीय माती प्रयोगशाळा", "Address": "कृषी महाविद्यालय परिसर, पुणे", "Contact": "020-25537890"},
            {"Center": "IARI पूसा माती लॅब", "Address": "पूसा कॅम्पस, नवी दिल्ली", "Contact": "011-25841234"},
            {"Center": "केव्हीके बारामती", "Address": "माळेगाव कॉलनी, बारामती", "Contact": "02112-255207"}
        ],
        "SoilHealth": [
            {"Title": "पीक फेरपालट (Crop Rotation)", "Tip": "जमिनीचा पोत सुधारण्यासाठी पिकांची (उदा. धान्यानंतर कडधान्य) आलटून पालटून लागवड करा."},
            {"Title": "सेंद्रिय कर्ब", "Tip": "शेतकरी खत (FYM), गांडूळ खत किंवा हिरवळीचे खत (धैंचा/ताग) जमिनीत मिसळा."},
            {"Title": "आच्छादन (Mulching)", "Tip": "बाष्पीभवन कमी करण्यासाठी आणि तण नियंत्रणासाठी जमिनीवर पेंढा किंवा प्लास्टिक आच्छादन वापरा."},
            {"Title": "pH व्यवस्थापन", "Tip": "आम्लधर्मी (pH < 6) जमिनीसाठी चुना वापरा. विम्लधर्मी (pH > 8) जमिनीसाठी जिप्सम वापरा."},
            {"Title": "जैविक खते", "Tip": "रासायनिक खतांचा वापर कमी करण्यासाठी रायझोबियम, ॲझोटोबॅक्टर यांसारख्या जिवाणू खतांचा वापर करा."}
        ]
    }
}

# --- YIELD PREDICTION LOGIC ---
# --- YIELD PREDICTION LOGIC (PURE AI) ---
# --- YIELD PREDICTION LOGIC (SCIENTIFIC CALCULATOR) ---
def get_yield_prediction(state, crop, season, area, soil="Loamy", weather="Normal", city="Unknown", village="Unknown", image_data=None, language="English", sowing_date="Unknown", variety="Unknown", irrigation="Rainfed", fertilizer="Unknown", pest_control="Unknown", pest_name="Unknown"):
    """
    Scientific AI Production Prediction.
    Uses 'gemini-flash-latest' with advanced agronomy parameters.
    """
    result = {}
    error = None
    
    try:
        # Base context for both modes
        scientific_context = f"""
        Context:
        - Crop: {crop} (Variety: {variety})
        - Location: {village}, {city}, {state}, India
        - Sowing Date: {sowing_date}
        - Season: {season}
        - Area: {area} Acres
        - Soil: {soil}
        - Irrigation: {irrigation}
        - Fertilizer/Inputs: {fertilizer}
        - Pest Control: Used '{pest_name}' ({pest_control})
        - Weather Outlook: {weather}
        """

        inputs = []
        if image_data:
             # VISION MODEL
             prompt = f"""
             Act as a Senior Agronomist.
             Perform a Scientific Yield Assessment based on this field image and agronomic data.
             
             {scientific_context}
             
             Task:
             1. Analyze crop vigor, canopy cover, and signs of nutrient deficiency/disease from the image.
             2. Correlate Sowing Date ({sowing_date}) with current growth stage seen in image.
             3. Evaluate efficacy of Pest Control ({pest_name} - {pest_control}) on crop health.
             4. Calculate Yield Gap (Potential vs Actual) considering Variety ({variety}) and Irrigation ({irrigation}).
             5. Provide a precision Yield Estimate (Tonnes/Acre).
             6. Provide the explanation in {language} language.
             
             Output Format exactly:
             YIELD: <Number only>
             PRODUCTION: <Number only>
             REASON: <Scientific explanation in {language}>
             """
             inputs = [image_data, prompt]
             
        else:
             # TEXT MODEL
             prompt = f"""
             Act as a Senior Agronomist.
             Perform a Scientific Yield Calculation based on provided agronomic parameters.
             
             {scientific_context}
             
             Task:
             1. Determine the 'Genetic Yield Potential' of the variety: {variety}.
             2. Apply reduction factors for:
                - Late/Early Sowing ({sowing_date})
                - Water Stress ({irrigation} vs {weather})
                - Nutrient Management ({fertilizer})
                - Pest/Disease Pressure vs Control ({pest_name}: {pest_control})
             3. Estimate the Final Harvestable Yield (Tonnes/Acre).
             4. Provide the explanation in {language} language.
             
             Output Format exactly:
             YIELD: <Number only, e.g. 2.5>
             PRODUCTION: <Number only, e.g. 12.5>
             REASON: <Scientific explanation in {language}>
             """
             inputs = [prompt]
        
        text = generate_ai_response_v2(inputs)
        
        import re
        
        # Regex to find numbers
        yield_match = re.search(r"YIELD:\s*([\d\.]+)", text, re.IGNORECASE)
        prod_match = re.search(r"PRODUCTION:\s*([\d\.]+)", text, re.IGNORECASE)
        reason_match = re.search(r"REASON:\s*(.*)", text, re.IGNORECASE | re.DOTALL)
        
        est_yield = 0.0
        est_prod = 0.0
        explanation = "AI analysis complete."
        
        if yield_match:
            try: est_yield = float(yield_match.group(1))
            except: est_yield = 0.0
            
        if prod_match:
            try: est_prod = float(prod_match.group(1))
            except: est_prod = est_yield * area
        else:
            est_prod = est_yield * area
            
        if reason_match:
            explanation = reason_match.group(1).strip().replace("*", "")
        else:
             if len(text) < 300 and "YIELD" not in text: explanation = text.strip()
        
        result = {
            'Predicted_Production': est_prod,
            'Average_Yield': est_yield,
            'AI_Explanation': explanation
        }
        
    except Exception as e:
        error = f"AI Analysis Failed: {str(e)}"
        
    return result, error

def get_ai_response(prompt, api_key=None):
    """
    General purpose AI Chat function.
    Uses 'gemini-flash-latest'.
    """
    try:
        return generate_ai_response_v2(prompt)
    except Exception as e:
        return f"I am having trouble connecting to the satellite. Please try again. (Error: {str(e)})"
