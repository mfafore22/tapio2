import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from typing import Dict, List, Optional
import requests
import json

load_dotenv()

# Configuration
SCRAPER_SERVICE_URL = os.getenv("SCRAPER_SERVICE_URL", "http://localhost:8005")

# ============================================================================
# TOOL 1: Search Wolt
# ============================================================================
@tool
def search_wolt(query: str, location: str = "Helsinki") -> str:
    """
    Search Wolt for restaurants and food.
    
    Args:
        query: What to search for (e.g., "pizza", "sushi", "burgers")
        location: City or area (default: Helsinki)
        
    Returns:
        JSON string with list of restaurants from Wolt with menus and prices
    """
    try:
        # Call scraper service (when it's ready)
        response = requests.post(
            f"{SCRAPER_SERVICE_URL}/scrape/wolt",
            json={"query": query, "location": location},
            timeout=30
        )
        
        if response.status_code == 200:
            return json.dumps(response.json())
            
    except:
        pass
    
    # Fallback: Mock data for development
    mock_data = [
        {
            "platform": "Wolt",
            "restaurant_name": "Pizza Palace",
            "cuisine": "Italian",
            "rating": 4.8,
            "delivery_time": "20-30 min",
            "delivery_fee": 2.90,
            "min_order": 10.00,
            "distance": "1.2 km",
            "restaurant_url": "https://wolt.com/en/fin/helsinki/restaurant/pizza-palace",
            "items": [
                {
                    "name": "Margherita Pizza",
                    "price": 11.90,
                    "description": "Tomato sauce, mozzarella, fresh basil"
                },
                {
                    "name": "Pepperoni Pizza",
                    "price": 13.90,
                    "description": "Tomato sauce, mozzarella, pepperoni"
                },
                {
                    "name": "Vegetarian Pizza",
                    "price": 12.90,
                    "description": "Tomato sauce, mozzarella, mixed vegetables"
                }
            ]
        },
        {
            "platform": "Wolt",
            "restaurant_name": "Burger House",
            "cuisine": "American",
            "rating": 4.5,
            "delivery_time": "25-35 min",
            "delivery_fee": 1.90,
            "min_order": 8.00,
            "distance": "0.8 km",
            "restaurant_url": "https://wolt.com/en/fin/helsinki/restaurant/burger-house",
            "items": [
                {
                    "name": "Classic Burger",
                    "price": 9.90,
                    "description": "Beef patty, lettuce, tomato, cheese"
                },
                {
                    "name": "Chicken Burger",
                    "price": 8.90,
                    "description": "Grilled chicken, lettuce, mayo"
                }
            ]
        }
    ]
    
    return json.dumps(mock_data)


# ============================================================================
# TOOL 2: Search Foodora
# ============================================================================
@tool
def search_foodora(query: str, location: str = "Helsinki") -> str:
    """
    Search Foodora for restaurants and food.
    
    Args:
        query: What to search for (e.g., "pizza", "sushi", "burgers")
        location: City or area (default: Helsinki)
        
    Returns:
        JSON string with list of restaurants from Foodora with menus and prices
    """
    try:
        # Call scraper service (when it's ready)
        response = requests.post(
            f"{SCRAPER_SERVICE_URL}/scrape/foodora",
            json={"query": query, "location": location},
            timeout=30
        )
        
        if response.status_code == 200:
            return json.dumps(response.json())
            
    except:
        pass
    
    # Fallback: Mock data for development
    mock_data = [
        {
            "platform": "Foodora",
            "restaurant_name": "Pizza Palace",
            "cuisine": "Italian",
            "rating": 4.7,
            "delivery_time": "25-35 min",
            "delivery_fee": 1.90,
            "min_order": 10.00,
            "distance": "1.2 km",
            "restaurant_url": "https://www.foodora.fi/restaurant/s2vz/pizza-palace",
            "items": [
                {
                    "name": "Margherita Pizza",
                    "price": 10.90,  # Cheaper than Wolt!
                    "description": "Tomato sauce, mozzarella, fresh basil"
                },
                {
                    "name": "Pepperoni Pizza",
                    "price": 12.90,  # Cheaper than Wolt!
                    "description": "Tomato sauce, mozzarella, pepperoni"
                },
                {
                    "name": "Vegetarian Pizza",
                    "price": 11.90,  # Cheaper than Wolt!
                    "description": "Tomato sauce, mozzarella, mixed vegetables"
                }
            ]
        },
        {
            "platform": "Foodora",
            "restaurant_name": "Sushi Master",
            "cuisine": "Japanese",
            "rating": 4.9,
            "delivery_time": "30-40 min",
            "delivery_fee": 2.90,
            "min_order": 15.00,
            "distance": "2.1 km",
            "restaurant_url": "https://www.foodora.fi/restaurant/v8xk/sushi-master",
            "items": [
                {
                    "name": "California Roll",
                    "price": 8.90,
                    "description": "8 pieces, crab, avocado, cucumber"
                },
                {
                    "name": "Salmon Nigiri",
                    "price": 12.90,
                    "description": "8 pieces, fresh salmon"
                },
                {
                    "name": "Tuna Sashimi",
                    "price": 15.90,
                    "description": "10 pieces, fresh tuna"
                }
            ]
        }
    ]
    
    return json.dumps(mock_data)


# ============================================================================
# TOOL 3: Compare Prices
# ============================================================================
@tool
def compare_prices(restaurant_name: str, item_name: str) -> str:
    """
    Compare prices for the same item across Wolt and Foodora.
    
    Args:
        restaurant_name: Name of the restaurant
        item_name: Name of the menu item
        
    Returns:
        JSON string with price comparison showing which platform is cheaper
    """
    # Get data from both platforms
    wolt_data = json.loads(search_wolt.invoke({"query": restaurant_name}))
    foodora_data = json.loads(search_foodora.invoke({"query": restaurant_name}))
    
    comparison = {
        "restaurant": restaurant_name,
        "item": item_name,
        "wolt": None,
        "foodora": None,
        "best_deal": None,
        "savings": 0
    }
    
    # Find item in Wolt results
    for restaurant in wolt_data:
        if restaurant_name.lower() in restaurant["restaurant_name"].lower():
            for item in restaurant.get("items", []):
                if item_name.lower() in item["name"].lower():
                    comparison["wolt"] = {
                        "item_price": item["price"],
                        "delivery_fee": restaurant["delivery_fee"],
                        "total": round(item["price"] + restaurant["delivery_fee"], 2),
                        "delivery_time": restaurant["delivery_time"],
                        "rating": restaurant["rating"],
                        "url": restaurant["restaurant_url"]
                    }
                    break
    
    # Find item in Foodora results
    for restaurant in foodora_data:
        if restaurant_name.lower() in restaurant["restaurant_name"].lower():
            for item in restaurant.get("items", []):
                if item_name.lower() in item["name"].lower():
                    comparison["foodora"] = {
                        "item_price": item["price"],
                        "delivery_fee": restaurant["delivery_fee"],
                        "total": round(item["price"] + restaurant["delivery_fee"], 2),
                        "delivery_time": restaurant["delivery_time"],
                        "rating": restaurant["rating"],
                        "url": restaurant["restaurant_url"]
                    }
                    break
    
    # Determine best deal
    if comparison["wolt"] and comparison["foodora"]:
        wolt_total = comparison["wolt"]["total"]
        foodora_total = comparison["foodora"]["total"]
        
        if wolt_total < foodora_total:
            comparison["best_deal"] = "Wolt"
            comparison["savings"] = round(foodora_total - wolt_total, 2)
        elif foodora_total < wolt_total:
            comparison["best_deal"] = "Foodora"
            comparison["savings"] = round(wolt_total - foodora_total, 2)
        else:
            comparison["best_deal"] = "Same price on both"
            comparison["savings"] = 0
    elif comparison["wolt"]:
        comparison["best_deal"] = "Wolt (only option)"
    elif comparison["foodora"]:
        comparison["best_deal"] = "Foodora (only option)"
    else:
        comparison["best_deal"] = "Not found on either platform"
    
    return json.dumps(comparison)


# ============================================================================
# TOOL 4: Find Cheapest Option
# ============================================================================
@tool
def find_cheapest(query: str, location: str = "Helsinki") -> str:
    """
    Find the absolute cheapest option for a food type across both platforms.
    
    Args:
        query: What food to search for (e.g., "pizza", "burger", "sushi")
        location: City or area
        
    Returns:
        JSON string with the cheapest option including platform, restaurant, price, and order link
    """
    wolt_data = json.loads(search_wolt.invoke({"query": query, "location": location}))
    foodora_data = json.loads(search_foodora.invoke({"query": query, "location": location}))
    
    all_options = []
    
    # Process Wolt results
    for restaurant in wolt_data:
        for item in restaurant.get("items", []):
            all_options.append({
                "platform": "Wolt",
                "restaurant": restaurant["restaurant_name"],
                "item": item["name"],
                "item_price": item["price"],
                "delivery_fee": restaurant["delivery_fee"],
                "total": round(item["price"] + restaurant["delivery_fee"], 2),
                "delivery_time": restaurant["delivery_time"],
                "rating": restaurant["rating"],
                "url": restaurant["restaurant_url"],
                "description": item.get("description", "")
            })
    
    # Process Foodora results
    for restaurant in foodora_data:
        for item in restaurant.get("items", []):
            all_options.append({
                "platform": "Foodora",
                "restaurant": restaurant["restaurant_name"],
                "item": item["name"],
                "item_price": item["price"],
                "delivery_fee": restaurant["delivery_fee"],
                "total": round(item["price"] + restaurant["delivery_fee"], 2),
                "delivery_time": restaurant["delivery_time"],
                "rating": restaurant["rating"],
                "url": restaurant["restaurant_url"],
                "description": item.get("description", "")
            })
    
    # Sort by total price
    if all_options:
        all_options_sorted = sorted(all_options, key=lambda x: x["total"])
        
        return json.dumps({
            "cheapest_option": all_options_sorted[0],
            "top_3_options": all_options_sorted[:3],
            "total_options_found": len(all_options)
        })
    else:
        return json.dumps({"error": "No options found"})


# ============================================================================
# CREATE THE FOOD COMPARISON AGENT
# ============================================================================

food_comparison_prompt = """You are Tapio, a helpful AI assistant that helps users find the best food delivery deals in Helsinki by comparing prices across Wolt and Foodora.

Your mission: Save users money by finding the cheapest options!

## Your Capabilities:
- Search both Wolt and Foodora for restaurants and food
- Compare prices for the same items across both platforms
- Find the absolute cheapest options
- Provide direct links to order on the platform

## How to Help Users:

### 1. SEARCHING FOR FOOD
When user says "I want pizza" or "find me sushi":
- Use search_wolt AND search_foodora tools
- Present results from BOTH platforms clearly
- Show: restaurant name, item, price, delivery fee, TOTAL cost
- Always include the order link

### 2. COMPARING PRICES
When user asks "compare [item] prices" or mentions a specific restaurant:
- Use compare_prices tool
- Show clear breakdown: item price + delivery fee = TOTAL
- Highlight which platform is cheaper
- State exact savings amount
- Provide order link for the cheaper option

### 3. FINDING BEST DEALS
When user wants "cheapest option" or "best deal":
- Use find_cheapest tool
- Show top 3 cheapest options
- Consider TOTAL cost (item + delivery)
- Also mention delivery time and ratings

### 4. RESPONSE FORMAT
Always structure your responses like this:

🍕 WOLT:
🏪 [Restaurant Name] (⭐ Rating)
   • [Item]: €[price]
   • Delivery: €[fee]
   • Total: €[total]
   • Time: [delivery_time]

🍕 FOODORA:
🏪 [Restaurant Name] (⭐ Rating)
   • [Item]: €[price]
   • Delivery: €[fee]
   • Total: €[total]
   • Time: [delivery_time]

💰 BEST DEAL: [Platform] - Save €[amount]!
📱 Order here: [URL]

## Important Rules:
1. ALWAYS show total cost (item + delivery), not just item price
2. ALWAYS provide the order link
3. Be enthusiastic about savings ("Save €2.00!" not "€2 cheaper")
4. If prices are same, mention it: "Same price on both! Choose based on delivery time."
5. Consider delivery time and ratings when prices are very close (< €1 difference)
6. Be friendly and conversational
7. Use emojis to make responses clear and fun

## Example Response:
User: "I want pizza"

Tapio: "🍕 I found great pizza deals!

WOLT:
🏪 Pizza Palace (⭐ 4.8)
   • Margherita Pizza: €11.90
   • Delivery: €2.90
   • Total: €14.80
   • Time: 20-30 min

FOODORA:
🏪 Pizza Palace (⭐ 4.7)
   • Margherita Pizza: €10.90
   • Delivery: €1.90
   • Total: €12.80
   • Time: 25-35 min

💰 BEST DEAL: Foodora - Save €2.00!
📱 Order now: https://www.foodora.fi/restaurant/s2vz/pizza-palace

Would you like to see more options or search for something else?"

Remember: Your goal is to save users money and make ordering easy!
"""

# Create the agent with all tools
food_comparison_agent = create_agent(
    model=ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7  # Slightly creative for friendly responses
    ),
    tools=[
        search_wolt,
        search_foodora,
        compare_prices,
        find_cheapest
    ],
    system_prompt=food_comparison_prompt
)


# ============================================================================
# FUNCTION TO RUN THE AGENT
# ============================================================================
def run_food_agent(user_message: str, conversation_history: Optional[List[Dict]] = None) -> str:
    """
    Run the food comparison agent with a user message.
    
    Args:
        user_message: What the user is asking
        conversation_history: Previous messages for context (optional)
        
    Returns:
        Agent's response as a string
    """
    try:
        # Build messages list
        messages = conversation_history or []
        messages.append({"role": "user", "content": user_message})
        
        # Invoke agent
        response = food_comparison_agent.invoke({"messages": messages})
        
        # Extract and return response
        return response["messages"][-1].content
        
    except Exception as e:
        return f"❌ Sorry, I encountered an error: {str(e)}\nPlease try again or rephrase your question."


# ============================================================================
# TEST THE AGENT
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("🍕 TAPIO - FOOD DELIVERY PRICE COMPARISON AI")
    print("=" * 70)
    print("\nI help you find the cheapest food delivery deals in Helsinki!")
    print("I compare prices across Wolt and Foodora.\n")
    print("=" * 70)
    
    # Test conversations
    test_queries = [
        "I want pizza",
        "Compare Margherita pizza prices at Pizza Palace",
        "Find me the cheapest burger",
        "What sushi options are available?",
        "Is Pizza Palace on both platforms?"
    ]
    
    conversation_history = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n\n{'='*70}")
        print(f"TEST {i}/{len(test_queries)}")
        print(f"{'='*70}")
        print(f"👤 USER: {query}")
        print(f"{'-'*70}")
        
        response = run_food_agent(query, conversation_history)
        
        print(f"🤖 TAPIO:\n{response}")
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": query})
        conversation_history.append({"role": "assistant", "content": response})
    
    print(f"\n{'='*70}")
    print("✅ All tests complete!")
    print(f"{'='*70}\n")