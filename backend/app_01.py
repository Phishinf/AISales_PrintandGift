from flask import Flask, request, jsonify, session
import json
import os
import requests
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO
import uuid

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

conversations = {}

app.secret_key = "printngift_secret_key"  # for session management

# Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key")
PRODUCTS_JSON = "products.json"

# Load data from JSON files
def load_json(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            # Check if the file contains an object with a 'products' key
            if isinstance(json_data, dict) and 'products' in json_data:
                data = json_data['products']
            # Or if it's a direct array of products
            elif isinstance(json_data, list):
                data = json_data
            else:
                print(f"Unexpected JSON structure in {file_path}")
        print(f"Loaded {len(data)} items from {file_path}")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
    return data

# Load data on startup
products = load_json(PRODUCTS_JSON)

@app.route('/process-text', methods=['POST'])
def process_text():
    """Process text requests from the chatbot"""
    # Get request data
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    user_message = data['message']
    print(f"Received message: {user_message}")
    
    # Get or create a conversation ID
    conversation_id = data.get('conversation_id')
    
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
    
    # Get or initialize conversation history
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    # Add the user message to history
    conversations[conversation_id].append({"role": "user", "content": user_message})
    
    # Get relevant products
    relevant_products = search_products(user_message, 5)
    
    # Format product context based on our specific JSON structure
    product_context = [
        {
            "name": p.get("name", ""),
            "original_price": p.get("original_price", ""),
            "sale_price": p.get("sale_price", ""),
            "description": p.get("description", "")[:200] + "..." if p.get("description") else "",
            "category": p.get("category", ""),
            "material": p.get("material", ""),
            "dimensions": p.get("dimensions", ""),
            "color": p.get("color", ""),
            "brand": p.get("brand", "")
        }
        for p in relevant_products
    ]
    
    # Call LLM with conversation history
    response = call_openai_api_with_history(conversations[conversation_id], product_context)
    
    # Add assistant response to history
    conversations[conversation_id].append({"role": "assistant", "content": response})
    
    # Return response with conversation ID
    return jsonify({
        "response": response,
        "products": relevant_products[:3],
        "conversation_id": conversation_id
    })

@app.route('/process-image', methods=['POST'])
def process_image():
    """Process image uploads from the chatbot"""
    # Check if an image was uploaded
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    # Get the image
    image_file = request.files['image']
    
    try:
        # Open the image using PIL
        img = Image.open(image_file)
        
        # Convert to RGB if needed (in case of RGBA, etc.)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        max_size = 1024
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size))
        
        # Convert to base64 for OpenAI API
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Call OpenAI Vision API if available
        if OPENAI_API_KEY and OPENAI_API_KEY != "your-api-key":
            try:
                # Call Vision API
                description = call_vision_api(img_str)
            except Exception as e:
                print(f"Error calling Vision API: {e}")
                description = "I can see your image! Let me suggest some relevant gift options from our collection."
        else:
            description = "I can see your image! Let me suggest some relevant gift options from our collection."
        
        # Get diverse product categories
        gift_categories = ["electronics", "bags", "drinkware", "clothing", "premium", "home appliances"]
        
        # Get sample products from various categories
        suggested_products = []
        for category in gift_categories:
            # Look for products that might match the category
            category_products = [p for p in products if p.get("category", "").lower().find(category.lower()) != -1 or 
                               p.get("name", "").lower().find(category.lower()) != -1]
            if category_products and len(category_products) > 0:
                suggested_products.append(category_products[0])  # Add first product from category
                if len(suggested_products) >= 3:
                    break
        
        # If we still need more products, add random ones
        while len(suggested_products) < 3 and products:
            import random
            random_product = random.choice(products)
            if random_product not in suggested_products:
                suggested_products.append(random_product)
        
        return jsonify({
            "response": description,
            "products": suggested_products
        })
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({
            "response": "I couldn't process this image. Please try another or describe what you're looking for.",
            "products": products[:3] if products else []
        })

import threading
import time

def cleanup_old_conversations():
    """Remove conversations that are older than 30 minutes"""
    while True:
        time.sleep(1800)  # Run every 30 minutes
        current_time = time.time()
        to_remove = []
        
        for conv_id, messages in conversations.items():
            if not messages:
                continue
                
            # Check if conversation has been inactive for more than 30 minutes
            if 'timestamp' in conversations[conv_id]:
                last_activity = conversations[conv_id]['timestamp']
                if current_time - last_activity > 1800:  # 30 minutes
                    to_remove.append(conv_id)
        
        # Remove old conversations
        for conv_id in to_remove:
            del conversations[conv_id]
        
        print(f"Cleaned up {len(to_remove)} inactive conversations")

def call_openai_api_with_history(conversation_history, product_context):
    """Call the OpenAI API with conversation history"""
    # Build system prompt for corporate gifts retailer
    system_prompt = """
    🎁 PRINTNGIFT.com Corporate Gifts Specialist – System Prompt

    You are an expert corporate gifts consultant for PRINTNGIFT.com, Singapore's premier provider of customized corporate gifts, promotional items, and premium business gifts. Your mission is to help businesses and individuals find the perfect gifts for any occasion while building lasting relationships.

    Your expertise covers diverse product categories:
    - Electronics & Tech Accessories
    - Small Home Electrical Appliances  
    - Premium Collections & Luxury Items
    - Corporate Clothing & Apparel
    - Bags & Pouches (briefcases, laptop bags, tote bags)
    - Drinkware & Food Containers (mugs, tumblers, lunch boxes)
    - Festive & Seasonal Gifts
    - Promotional Items & Branded Merchandise

    The product data structure includes:
        - name: Product name
        - original_price: Original price in SGD
        - sale_price: Discounted price if available
        - description: Detailed product description
        - category: Product category
        - material: Construction material
        - dimensions: Size specifications
        - color: Available colors
        - brand: Manufacturer/brand name

    🎯 Your Primary Objectives:
    1. Understand the customer's gifting purpose and context
    2. Recommend appropriate products based on occasion, budget, and recipient
    3. Provide expert guidance on corporate gift etiquette and trends
    4. Suggest customization options for branding and personalization
    5. Build trust through knowledgeable, professional service

    💼 Corporate Gift Scenarios & Expertise:

    **Client Appreciation & Relationship Building:**
    - Executive gifts for key clients and partners
    - Year-end appreciation gifts
    - Thank you gifts for successful projects
    - Welcome gifts for new clients

    **Employee Recognition & Motivation:**
    - Achievement awards and milestone gifts
    - Employee appreciation gifts
    - Welcome packages for new hires
    - Team building and company event gifts
    - Long service recognition items

    **Business Events & Conferences:**
    - Conference giveaways and swag bags
    - Trade show promotional items
    - Seminar and workshop gifts
    - Networking event door prizes

    **Seasonal & Festive Occasions:**
    - Chinese New Year corporate gifts
    - Christmas and holiday presents
    - Mid-Autumn Festival gifts
    - Deepavali and Hari Raya gifts

    **Personal Occasions:**
    - Birthday and anniversary gifts
    - Wedding and baby shower presents
    - Graduation and achievement celebrations
    - Housewarming and farewell gifts

    🧠 Key Information to Gather:
    - 🎯 Purpose: What's the occasion or reason for gifting?
    - 👥 Recipient: Who are you gifting to? (clients, employees, partners, friends)
    - 🏢 Context: Corporate event, personal occasion, or relationship building?
    - 💰 Budget: What's your budget range per item or total?
    - 📊 Quantity: How many items do you need?
    - ⏰ Timeline: When do you need the gifts?
    - 🎨 Customization: Do you want branding, logos, or personalization?
    - 🚚 Delivery: Where should the gifts be delivered?

    💡 Expert Recommendations by Category:

    **Electronics & Tech:**
    - Power banks for busy professionals
    - Wireless chargers for modern offices
    - Bluetooth speakers for entertainment
    - USB drives for data storage

    **Premium Collections:**
    - Executive pen sets for VIP clients
    - Luxury notebooks for professionals
    - High-end desk accessories
    - Premium gift sets

    **Bags & Pouches:**
    - Laptop bags for business professionals
    - Tote bags for conferences and events
    - Travel organizers for frequent travelers
    - Document holders for meetings

    **Drinkware:**
    - Branded mugs for office use
    - Insulated tumblers for on-the-go
    - Glass bottles for health-conscious recipients
    - Coffee sets for coffee lovers

    **Clothing:**
    - Polo shirts for corporate uniforms
    - Jackets for outdoor events
    - Caps and hats for casual branding
    - Scarves for elegant corporate gifts

    🎨 Customization & Branding Options:
    - Logo embossing and engraving
    - Screen printing and embroidery
    - Color customization to match brand colors
    - Packaging and presentation options
    - Gift wrapping services

    📋 Common FAQs & Responses:

    **Q: What's the minimum order quantity?**
    A: Our minimum order varies by product, typically starting from 50 pieces for promotional items and 10 pieces for premium gifts. Some luxury items can be ordered individually.

    **Q: How long does customization take?**
    A: Standard customization takes 7-14 business days. Rush orders can be accommodated with additional charges, typically 3-5 days.

    **Q: Do you provide samples?**
    A: Yes! We offer product samples for orders above certain quantities. Sample fees may apply but are often waived for confirmed orders.

    **Q: What's included in your service?**
    A: We provide end-to-end service including product sourcing, customization, quality control, packaging, and delivery. We also offer design consultation for logos and branding.

    **Q: Do you handle international shipping?**
    A: Yes, we ship internationally. Shipping costs and delivery times vary by destination. We'll provide detailed shipping information based on your location.

    🎯 Sales Approach:
    - Listen actively to understand the customer's needs
    - Ask thoughtful questions to clarify requirements
    - Provide multiple options at different price points
    - Explain the value and impact of each recommendation
    - Offer package deals and volume discounts
    - Suggest complementary items and accessories
    - Provide clear next steps and follow-up process

    💼 Professional Tone Guidelines:
    - Be warm, approachable, and professional
    - Show genuine interest in helping solve their gifting challenges
    - Demonstrate expertise without being overwhelming
    - Use positive, confident language
    - Be responsive to cultural considerations in Singapore's diverse market
    - Acknowledge both corporate and personal gifting needs

    🎁 Value Propositions to Highlight:
    - Quality products from trusted suppliers
    - Competitive pricing with volume discounts
    - Fast turnaround times for urgent orders
    - Professional customization services
    - Excellent customer service and support
    - Experience in serving Singapore's corporate market
    - Understanding of local gifting culture and preferences

    Your ultimate goal is to make gift-giving effortless and impactful for your customers, whether they're building business relationships or celebrating personal milestones. Every interaction should leave customers feeling confident in their choice and excited about the positive impact their gifts will have.
    """
    
    # Add product context
    if product_context:
        system_prompt += "\n\n🛍️ Available Products:\n"
        for i, product in enumerate(product_context, 1):
            price_info = product['sale_price'] if product['sale_price'] else product['original_price']
            details = []
            if product['category']:
                details.append(f"Category: {product['category']}")
            if product['material']:
                details.append(f"Material: {product['material']}")
            if product['brand']:
                details.append(f"Brand: {product['brand']}")
            details_str = " | ".join(details) if details else ""
            
            system_prompt += f"{i}. {product['name']} - {price_info}\n"
            if details_str:
                system_prompt += f"   Details: {details_str}\n"
            if product['description']:
                system_prompt += f"   Description: {product['description']}\n"
    
    # Create messages array with system prompt and conversation history
    messages = [{"role": "system", "content": system_prompt}]
    
    # Only include the last several messages to prevent context limit issues
    max_history = 10  # Adjust based on your needs
    recent_history = conversation_history[-max_history:] if len(conversation_history) > max_history else conversation_history
    
    # Add conversation history
    messages.extend(recent_history)
    
    # Call OpenAI API
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o",
            "messages": messages,
            "max_tokens": 600
        }
    )
    
    result = response.json()
    if 'choices' in result and len(result['choices']) > 0:
        return result['choices'][0]['message']['content']
    else:
        print(f"Unexpected OpenAI response: {result}")
        return fallback_response(conversation_history[-1]["content"], product_context)

def call_vision_api(image_base64):
    """Call the OpenAI Vision API for image analysis"""
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4-vision-preview",  # Vision model
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Analyze this image and suggest what type of corporate gift or promotional item would be suitable based on what you see. Consider the context, setting, or items visible in the image."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
    )
    
    result = response.json()
    if 'choices' in result and len(result['choices']) > 0:
        return result['choices'][0]['message']['content']
    else:
        print(f"Unexpected OpenAI Vision response: {result}")
        return "Based on your images, I can suggest some relevant gift options from our collection. Let me show you some suitable corporate gifts!"

def fallback_response(message, product_context):
    """Generate a fallback response without calling the OpenAI API"""
    message_lower = message.lower()
    
    # Check for common gift occasion queries
    if any(word in message_lower for word in ["client", "customer", "appreciation"]):
        return "For client appreciation gifts, I recommend our premium collections - executive pen sets, branded notebooks, or high-quality drinkware. These create lasting impressions while showing your professionalism. What's your budget range and how many clients are you gifting to?"
    
    elif any(word in message_lower for word in ["employee", "staff", "team", "recognition"]):
        return "Employee recognition gifts are so important for morale! Popular choices include branded apparel, tech accessories like power banks, or practical items like insulated tumblers. Are you celebrating a specific achievement or looking for general appreciation gifts?"
    
    elif any(word in message_lower for word in ["conference", "event", "seminar", "workshop"]):
        return "For corporate events, consider practical giveaways that attendees will actually use - branded bags, notebooks, pens, or tech accessories. The key is choosing items that align with your brand and provide ongoing value. How many attendees are you expecting?"
    
    elif any(word in message_lower for word in ["chinese new year", "cny", "festive", "holiday"]):
        return "Chinese New Year corporate gifts are perfect for strengthening business relationships! Traditional favorites include premium tea sets, elegant food containers, or luxury gift hampers. Red and gold packaging adds the perfect festive touch. Who are you planning to gift to?"
    
    elif any(word in message_lower for word in ["wedding", "birthday", "anniversary", "celebration"]):
        return "For personal celebrations, I'd suggest our premium collections - elegant home appliances, luxury drinkware, or personalized items. The key is choosing something meaningful that reflects your relationship with the recipient. What's the occasion and your relationship to the recipient?"
    
    elif any(word in message_lower for word in ["budget", "price", "cost", "how much"]):
        if product_context:
            product = product_context[0]
            price = product['sale_price'] if product['sale_price'] else product['original_price']
            return f"The {product['name']} is priced at {price}. We offer volume discounts for bulk orders, and our team can work with various budget ranges. What quantity are you considering and what's your target budget per item?"
        else:
            return "Our gifts range from affordable promotional items (starting around $10) to luxury executive gifts ($200+). We work with all budgets and offer volume discounts. What's your budget range and how many items do you need?"
    
    elif any(word in message_lower for word in ["customization", "branding", "logo", "personalize"]):
        return "We offer comprehensive customization services! This includes logo embossing, screen printing, embroidery, and color matching to your brand. Customization typically takes 7-14 business days, with rush options available. Do you have specific branding requirements or a logo you'd like to incorporate?"
    
    elif any(word in message_lower for word in ["delivery", "shipping", "when", "timeline"]):
        return "We offer flexible delivery options throughout Singapore and internationally. Standard orders take 5-7 business days, while customized items need 7-14 days. Rush orders can be accommodated with additional charges. When do you need your gifts delivered?"
    
    elif any(word in message_lower for word in ["electronics", "tech", "gadget", "power bank", "speaker"]):
        return "Our electronics and tech accessories are very popular for corporate gifts! Power banks, wireless chargers, and Bluetooth speakers are practical choices that recipients use daily. These items offer great branding opportunities and lasting value. What type of tech gift interests you?"
    
    elif any(word in message_lower for word in ["bag", "briefcase", "laptop", "tote"]):
        return "Bags and pouches make excellent corporate gifts as they're practical and provide great brand visibility. We have executive briefcases, laptop bags, conference totes, and travel organizers. They're perfect for professionals and can be customized with your logo. What style are you looking for?"
    
    elif any(word in message_lower for word in ["mug", "tumbler", "bottle", "drinkware", "coffee"]):
        return "Drinkware is one of our most popular categories! Branded mugs, insulated tumblers, and glass bottles are used daily, providing excellent brand exposure. They're perfect for office environments and make practical, appreciated gifts. Do you prefer ceramic, stainless steel, or glass materials?"
    
    elif any(word in message_lower for word in ["clothing", "shirt", "polo", "jacket", "apparel"]):
        return "Corporate clothing creates team unity and brand visibility! Our selection includes polo shirts, jackets, caps, and scarves. These are great for employee uniforms, event staff, or corporate gifts. Quality fabrics and professional embroidery make them suitable for business environments. What type of apparel interests you?"
    
    elif any(word in message_lower for word in ["minimum", "quantity", "order", "how many"]):
        return "Minimum order quantities vary by product - typically 50 pieces for promotional items and 10 pieces for premium gifts. Some luxury items can be ordered individually. Volume discounts apply for larger orders. How many items are you considering?"
    
    elif any(word in message_lower for word in ["sample", "demo", "try", "see"]):
        return "We definitely provide samples! For orders above certain quantities, we offer product samples so you can evaluate quality before committing. Sample fees may apply but are often waived for confirmed orders. This ensures you're completely satisfied with your choice."
    
    # Default response
    return "Welcome to PrintnGift! We're Singapore's leading corporate gifts specialist, offering everything from tech accessories to premium collections. Whether you're looking to appreciate clients, recognize employees, or celebrate special occasions, we have the perfect gifts. What type of gifting occasion can I help you with today?"

def search_products(query, limit=5):
    """Enhanced search for corporate gifts products"""
    query_terms = query.lower().split()
    scored_products = []
    
    # Define category mappings for better search results
    category_keywords = {
        "electronics": ["power bank", "speaker", "charger", "tech", "gadget", "electronics", "usb", "wireless"],
        "bags": ["bag", "briefcase", "laptop", "tote", "pouch", "backpack", "organizer", "travel"],
        "drinkware": ["mug", "tumbler", "bottle", "cup", "coffee", "tea", "water", "drink", "thermos"],
        "clothing": ["shirt", "polo", "jacket", "cap", "hat", "apparel", "clothing", "uniform"],
        "premium": ["executive", "luxury", "premium", "high-end", "elegant", "sophisticated"],
        "home": ["home", "kitchen", "appliance", "household", "domestic"],
        "festive": ["festive", "holiday", "seasonal", "christmas", "chinese new year", "celebration"]
    }
    
    # Occasion-based keywords
    occasion_keywords = {
        "corporate": ["client", "business", "corporate", "professional", "executive", "office"],
        "employee": ["employee", "staff", "team", "recognition", "appreciation", "achievement"],
        "event": ["conference", "seminar", "event", "meeting", "workshop", "trade show"],
        "personal": ["birthday", "wedding", "anniversary", "graduation", "farewell", "personal"]
    }
    
    for product in products:
        score = 0
        
        # Ensure we're handling both string and None values safely
        name = product.get('name', '') or ''
        description = product.get('description', '') or ''
        category = product.get('category', '') or ''
        
        product_text = f"{name} {description} {category}".lower()
        
        # Basic keyword matching
        for term in query_terms:
            if term in product_text:
                score += 1
        
        # Category-specific bonus scoring
        for category_name, keywords in category_keywords.items():
            for keyword in keywords:
                if any(keyword in term for term in query_terms):
                    for product_keyword in keywords:
                        if product_keyword in product_text:
                            score += 3  # Higher score for category matches
                            break
        
        # Occasion-specific bonus scoring
        for occasion_name, keywords in occasion_keywords.items():
            for keyword in keywords:
                if any(keyword in term for term in query_terms):
                    # All products are suitable for corporate occasions, but some are more specific
                    score += 1
        
        # Exact name matches get highest priority
        if any(term in name.lower() for term in query_terms):
            score += 5
        
        if score > 0:
            scored_products.append((score, product))
    
    # Sort by score and return top matches
    scored_products.sort(reverse=True, key=lambda x: x[0])
    return [product for score, product in scored_products[:limit]]

if __name__ == '__main__':
    print(f"Starting PrintnGift Corporate Gifts Service...")
    print(f"OpenAI API Key configured: {'Yes' if OPENAI_API_KEY and OPENAI_API_KEY != 'your-api-key' else 'No'}")
    print(f"Loaded {len(products)} products")
    print(f"Product categories available:")
    
    # Show available categories
    categories = set()
    for product in products:
        if product.get('category'):
            categories.add(product.get('category'))
    
    for category in sorted(categories):
        count = len([p for p in products if p.get('category') == category])
        print(f"  - {category}: {count} products")
    
    print(f"\nAPI endpoints:")
    print(f"  - POST /process-text (for text messages)")
    print(f"  - POST /process-images (for images uploads)")
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5100))
    
    # Start the cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_old_conversations, daemon=True)
    cleanup_thread.start()
    
    app.run(host=host, port=port, debug=True)