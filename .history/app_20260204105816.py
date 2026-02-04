#!/usr/bin/env python3
"""Simple Grocery Shopping List Application - Streamlit Version"""

import streamlit as st
import json
from pathlib import Path

# File for persisting item preferences (brand/unit choices)
PREFS_FILE = Path(__file__).parent / "item_preferences.json"
CUSTOM_BRANDS_FILE = Path(__file__).parent / "custom_brands.json"
HIDDEN_ITEMS_FILE = Path(__file__).parent / "hidden_items.json"
CUSTOM_ITEMS_FILE = Path(__file__).parent / "custom_items.json"


def load_preferences():
    """Load item preferences from file."""
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_preferences(data):
    """Save item preferences to file."""
    try:
        with open(PREFS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        pass


def load_custom_brands():
    """Load custom brands from file."""
    if CUSTOM_BRANDS_FILE.exists():
        try:
            with open(CUSTOM_BRANDS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_custom_brands(data):
    """Save custom brands to file."""
    try:
        with open(CUSTOM_BRANDS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        pass


def load_hidden_items():
    """Load hidden/deleted items from file."""
    if HIDDEN_ITEMS_FILE.exists():
        try:
            with open(HIDDEN_ITEMS_FILE, "r") as f:
                return set(json.load(f))
        except (json.JSONDecodeError, IOError):
            return set()
    return set()


def save_hidden_items(data):
    """Save hidden/deleted items to file."""
    try:
        with open(HIDDEN_ITEMS_FILE, "w") as f:
            json.dump(list(data), f, indent=2)
    except IOError:
        pass


def load_custom_items():
    """Load custom items from file. Format: {category: {item: unit}}"""
    if CUSTOM_ITEMS_FILE.exists():
        try:
            with open(CUSTOM_ITEMS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_custom_items(data):
    """Save custom items to file."""
    try:
        with open(CUSTOM_ITEMS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        pass


# Brand groups - items that share custom brands
BRAND_GROUPS = {
    "cheese": [
        "Cheddar Cheese", "Swiss Cheese", "Mozzarella Cheese", "Parmesan Cheese",
        "Provolone Cheese", "American Cheese", "Pepper Jack Cheese", "Feta Cheese",
        "Blue Cheese", "Goat Cheese", "Ricotta Cheese", "Brie", "Shredded Mexican Blend",
        "Cottage Cheese"
    ],
    "milk": ["Whole Milk", "2% Milk", "Skim Milk"],
    "cream": ["Half & Half", "Heavy Cream"],
    "butter": ["Butter (Salted)", "Butter (Unsalted)"],
    "yogurt": ["Yogurt (Plain)", "Yogurt (Greek)"],
    "milk_alt": ["Almond Milk", "Oat Milk"],
    "canned_tomatoes": ["Diced Tomatoes", "Crushed Tomatoes", "Tomato Paste", "Tomato Sauce"],
    "canned_beans": ["Black Beans", "Kidney Beans", "Pinto Beans"],
    "broth": ["Chicken Broth", "Beef Broth", "Vegetable Broth"],
    "coffee": ["Coffee (Ground)", "Coffee (Whole Bean)"],
    "nut_butter": ["Peanut Butter", "Almond Butter"],
}


def get_brand_group(item):
    """Get the brand group for an item."""
    for group, items in BRAND_GROUPS.items():
        if item in items:
            return group
    return None


def get_brands_for_item(item, custom_brands_dict):
    """Get all brands for an item (predefined + custom from same group)."""
    if item not in ITEM_BRANDS:
        return []

    brands = list(ITEM_BRANDS[item])  # Start with predefined

    # Add custom brands from the same group
    group = get_brand_group(item)
    if group and group in custom_brands_dict:
        for custom_brand in custom_brands_dict[group]:
            if custom_brand not in brands:
                brands.append(custom_brand)

    return brands

# Master list of items organized by category with default units
# Format: {"item_name": "default_unit"}
MASTER_LIST = {
    "Produce - Fruits": {
        "Apples": "lb",
        "Bananas": "bunch",
        "Oranges": "lb",
        "Lemons": "each",
        "Limes": "each",
        "Grapes": "lb",
        "Strawberries": "lb",
        "Blueberries": "pint",
        "Raspberries": "pint",
        "Blackberries": "pint",
        "Watermelon": "each",
        "Cantaloupe": "each",
        "Honeydew": "each",
        "Pineapple": "each",
        "Mango": "each",
        "Avocados": "each",
        "Peaches": "lb",
        "Pears": "lb",
        "Plums": "lb",
        "Cherries": "lb",
        "Kiwi": "each",
        "Grapefruit": "each",
    },
    "Produce - Vegetables": {
        "Onions (Yellow)": "each",
        "Onions (Red)": "each",
        "Onions (White)": "each",
        "Garlic": "head",
        "Potatoes (Russet)": "lb",
        "Potatoes (Red)": "lb",
        "Potatoes (Yukon Gold)": "lb",
        "Sweet Potatoes": "lb",
        "Carrots": "lb",
        "Celery": "bunch",
        "Broccoli": "lb",
        "Cauliflower": "head",
        "Lettuce (Romaine)": "head",
        "Lettuce (Iceberg)": "head",
        "Spinach": "bag",
        "Kale": "bunch",
        "Mixed Greens": "bag",
        "Arugula": "bag",
        "Cabbage (Green)": "head",
        "Cabbage (Red)": "head",
        "Brussels Sprouts": "lb",
        "Asparagus": "bunch",
        "Green Beans": "lb",
        "Snap Peas": "lb",
        "Bell Peppers (Green)": "each",
        "Bell Peppers (Red)": "each",
        "Bell Peppers (Yellow)": "each",
        "Jalapeños": "each",
        "Serrano Peppers": "each",
        "Tomatoes": "lb",
        "Cherry Tomatoes": "pint",
        "Grape Tomatoes": "pint",
        "Cucumbers": "each",
        "Zucchini": "each",
        "Yellow Squash": "each",
        "Butternut Squash": "each",
        "Acorn Squash": "each",
        "Spaghetti Squash": "each",
        "Eggplant": "each",
        "Mushrooms (White)": "oz",
        "Mushrooms (Cremini)": "oz",
        "Mushrooms (Portobello)": "each",
        "Corn on the Cob": "each",
        "Radishes": "bunch",
        "Beets": "lb",
        "Turnips": "lb",
        "Parsnips": "lb",
    },
    "Produce - Herbs": {
        "Basil (Fresh)": "bunch",
        "Cilantro": "bunch",
        "Parsley (Flat)": "bunch",
        "Parsley (Curly)": "bunch",
        "Mint": "bunch",
        "Dill": "bunch",
        "Rosemary": "bunch",
        "Thyme": "bunch",
        "Sage": "bunch",
        "Chives": "bunch",
        "Green Onions/Scallions": "bunch",
        "Ginger Root": "each",
    },
    "Dairy": {
        "Whole Milk": "half gal",
        "2% Milk": "half gal",
        "Skim Milk": "half gal",
        "Half & Half": "pint",
        "Heavy Cream": "pint",
        "Butter (Salted)": "lb",
        "Butter (Unsalted)": "lb",
        "Eggs (Large)": "dozen",
        "Sour Cream": "oz",
        "Cream Cheese": "oz",
        "Cottage Cheese": "oz",
        "Ricotta Cheese": "oz",
        "Yogurt (Plain)": "oz",
        "Yogurt (Greek)": "oz",
        "Cheddar Cheese": "lb",
        "Mozzarella Cheese": "lb",
        "Parmesan Cheese": "lb",
        "Swiss Cheese": "lb",
        "Provolone Cheese": "lb",
        "American Cheese": "lb",
        "Pepper Jack Cheese": "lb",
        "Feta Cheese": "oz",
        "Blue Cheese": "oz",
        "Goat Cheese": "oz",
        "Brie": "each",
        "Shredded Mexican Blend": "bag",
    },
    "Dairy Alternatives": {
        "Almond Milk": "carton",
        "Oat Milk": "carton",
        "Soy Milk": "carton",
        "Coconut Milk (Carton)": "carton",
        "Vegan Butter": "each",
        "Vegan Cheese": "each",
    },
    "Meat - Beef": {
        "Ground Beef (80/20)": "lb",
        "Ground Beef (90/10)": "lb",
        "Ribeye Steak": "lb",
        "NY Strip Steak": "lb",
        "Sirloin Steak": "lb",
        "Filet Mignon": "lb",
        "Flank Steak": "lb",
        "Skirt Steak": "lb",
        "Chuck Roast": "lb",
        "Brisket": "lb",
        "Short Ribs": "lb",
        "Pastrami Slices": "lb",
        "Stew Meat": "lb",
    },
    "Meat - Pork": {
        "Ground Pork": "lb",
        "Pork Chops (Bone-In)": "lb",
        "Pork Chops (Boneless)": "lb",
        "Pork Tenderloin": "lb",
        "Pork Loin Roast": "lb",
        "Pork Shoulder": "lb",
        "Baby Back Ribs": "lb",
        "Spare Ribs": "lb",
        "Bacon": "pack",
        "Ham (Sliced)": "lb",
        "Ham (Whole)": "lb",
        "Italian Sausage": "lb",
        "Breakfast Sausage": "pack",
        "Bratwurst": "pack",
        "Hot Dogs": "pack",
        "Pepperoni": "pack",
        "Prosciutto": "oz",
        "Salami": "oz",
    },
    "Meat - Poultry": {
        "Chicken Breast (Boneless)": "lb",
        "Chicken Breast (Bone-In)": "lb",
        "Chicken Thighs (Boneless)": "lb",
        "Chicken Thighs (Bone-In)": "lb",
        "Chicken Wings": "lb",
        "Chicken Drumsticks": "lb",
        "Whole Chicken": "each",
        "Ground Chicken": "lb",
        "Ground Turkey": "lb",
        "Turkey Breast": "lb",
        "Turkey (Deli Sliced)": "lb",
        "Rotisserie Chicken": "each",
    },
    "Seafood": {
        "Salmon Fillet": "lb",
        "Sea Bass": "lb",
        "Shrimp (Raw)": "lb",
        "Shrimp (Cooked)": "lb",
        "Crab Meat": "lb",
    },
    "Canned Goods": {
        "Diced Tomatoes": "can",
        "Crushed Tomatoes": "can",
        "Tomato Paste": "can",
        "Tomato Sauce": "can",
        "Black Beans": "can",
        "Kidney Beans": "can",
        "Pinto Beans": "can",
        "Refried Beans": "can",
        "Baked Beans": "can",
        "Green Beans (Canned)": "can",
        "Corn (Canned)": "can",
        "Peas (Canned)": "can",
        "Mixed Vegetables": "can",
        "Tuna (Canned)": "can",
        "Chicken Broth": "carton",
        "Beef Broth": "carton",
        "Vegetable Broth": "carton",
        "Coconut Milk (Canned)": "can",
        "Evaporated Milk": "can",
        "Sweetened Condensed Milk": "can",
        "Olives (Black)": "can",
        "Olives (Green)": "jar",
        "Artichoke Hearts": "can",
        "Roasted Red Peppers": "jar",
        "Jalapeños (Pickled)": "jar",
        "Chipotle in Adobo": "can",
        "Green Chiles": "can",
        "Pumpkin Puree": "can",
    },
    "Grains & Pasta": {
        "White Rice (Long Grain)": "lb",
        "Brown Rice": "lb",
        "Jasmine Rice": "lb",
        "Basmati Rice": "lb",
        "Arborio Rice": "lb",
        "Wild Rice": "lb",
        "Quinoa": "lb",
        "Couscous": "box",
        "Bulgur": "lb",
        "Farro": "lb",
        "Barley": "lb",
        "Oats (Rolled)": "container",
        "Oats (Steel Cut)": "container",
        "Oats (Instant)": "box",
        "Spaghetti": "box",
        "Penne": "box",
        "Rigatoni": "box",
        "Farfalle (Bow Tie)": "box",
        "Fusilli": "box",
        "Linguine": "box",
        "Fettuccine": "box",
        "Angel Hair": "box",
        "Lasagna Noodles": "box",
        "Egg Noodles": "bag",
        "Orzo": "box",
        "Macaroni": "box",
        "Tortellini": "pack",
        "Ravioli": "pack",
        "Ramen Noodles": "pack",
        "Rice Noodles": "pack",
        "Udon Noodles": "pack",
        "Soba Noodles": "pack",
    },
    "Bread & Bakery": {
        "White Bread": "loaf",
        "Wheat Bread": "loaf",
        "Sourdough Bread": "loaf",
        "French Bread": "loaf",
        "Italian Bread": "loaf",
        "Ciabatta": "each",
        "Rye Bread": "loaf",
        "Multigrain Bread": "loaf",
        "English Muffins": "pack",
        "Bagels": "pack",
        "Croissants": "pack",
        "Hamburger Buns": "pack",
        "Hot Dog Buns": "pack",
        "Flour Tortillas": "pack",
        "Corn Tortillas": "pack",
        "Pita Bread": "pack",
        "Naan": "pack",
        "Breadcrumbs": "container",
        "Panko Breadcrumbs": "container",
        "Croutons": "bag",
    },
    "Baking": {
        "All-Purpose Flour": "lb",
        "Bread Flour": "lb",
        "Cake Flour": "lb",
        "Whole Wheat Flour": "lb",
        "Almond Flour": "lb",
        "Coconut Flour": "lb",
        "Cornmeal": "lb",
        "Cornstarch": "box",
        "Granulated Sugar": "lb",
        "Brown Sugar": "lb",
        "Powdered Sugar": "lb",
        "Honey": "bottle",
        "Maple Syrup": "bottle",
        "Agave Nectar": "bottle",
        "Molasses": "bottle",
        "Corn Syrup": "bottle",
        "Baking Soda": "box",
        "Baking Powder": "can",
        "Active Dry Yeast": "pack",
        "Instant Yeast": "pack",
        "Vanilla Extract": "bottle",
        "Almond Extract": "bottle",
        "Cocoa Powder": "container",
        "Chocolate Chips": "bag",
        "Baking Chocolate": "bar",
        "Cream of Tartar": "container",
        "Shortening": "can",
    },
    "Oils & Vinegars": {
        "Olive Oil (Extra Virgin)": "bottle",
        "Olive Oil (Light)": "bottle",
        "Vegetable Oil": "bottle",
        "Canola Oil": "bottle",
        "Coconut Oil": "jar",
        "Avocado Oil": "bottle",
        "Sesame Oil": "bottle",
        "Peanut Oil": "bottle",
        "Cooking Spray": "can",
        "White Vinegar": "bottle",
        "Apple Cider Vinegar": "bottle",
        "Balsamic Vinegar": "bottle",
        "Red Wine Vinegar": "bottle",
        "Rice Vinegar": "bottle",
    },
    "Spices & Seasonings": {
        "Salt (Table)": "container",
        "Salt (Kosher)": "box",
        "Salt (Sea)": "container",
        "Black Pepper": "container",
        "White Pepper": "container",
        "Cayenne Pepper": "container",
        "Red Pepper Flakes": "container",
        "Paprika": "container",
        "Smoked Paprika": "container",
        "Chili Powder": "container",
        "Cumin": "container",
        "Coriander": "container",
        "Turmeric": "container",
        "Curry Powder": "container",
        "Garam Masala": "container",
        "Cinnamon (Ground)": "container",
        "Cinnamon Sticks": "container",
        "Nutmeg": "container",
        "Allspice": "container",
        "Cloves": "container",
        "Ginger (Ground)": "container",
        "Garlic Powder": "container",
        "Onion Powder": "container",
        "Oregano (Dried)": "container",
        "Basil (Dried)": "container",
        "Thyme (Dried)": "container",
        "Rosemary (Dried)": "container",
        "Bay Leaves": "container",
        "Italian Seasoning": "container",
        "Herbs de Provence": "container",
        "Taco Seasoning": "pack",
        "Ranch Seasoning": "pack",
        "Mustard (Dry)": "container",
        "Mustard Seeds": "container",
        "Celery Salt": "container",
        "Celery Seed": "container",
        "Dill (Dried)": "container",
        "Caraway Seeds": "container",
        "Fennel Seeds": "container",
        "Poppy Seeds": "container",
        "Sesame Seeds": "container",
        "Cardamom": "container",
        "Saffron": "container",
    },
    "Condiments": {
        "Ketchup": "bottle",
        "Mustard (Yellow)": "bottle",
        "Mustard (Dijon)": "jar",
        "Mustard (Spicy Brown)": "bottle",
        "Mayonnaise": "jar",
        "Relish": "jar",
        "Hot Sauce": "bottle",
        "Sriracha": "bottle",
        "BBQ Sauce": "bottle",
        "Worcestershire Sauce": "bottle",
        "Soy Sauce": "bottle",
        "Teriyaki Sauce": "bottle",
        "Hoisin Sauce": "bottle",
        "Fish Sauce": "bottle",
        "Oyster Sauce": "bottle",
        "Tahini": "jar",
        "Hummus": "container",
        "Salsa": "jar",
        "Pico de Gallo": "container",
        "Guacamole": "container",
        "Ranch Dressing": "bottle",
        "Italian Dressing": "bottle",
        "Caesar Dressing": "bottle",
        "Blue Cheese Dressing": "bottle",
        "Thousand Island": "bottle",
        "Vinaigrette": "bottle",
        "Marinara Sauce": "jar",
        "Alfredo Sauce": "jar",
        "Pesto": "jar",
        "Capers": "jar",
        "Sun-Dried Tomatoes": "jar",
        "Pickles (Dill)": "jar",
        "Pickles (Bread & Butter)": "jar",
        "Sauerkraut": "jar",
        "Kimchi": "jar",
    },
    "Nuts & Seeds": {
        "Almonds": "bag",
        "Walnuts": "bag",
        "Pecans": "bag",
        "Cashews": "bag",
        "Peanuts": "bag",
        "Pistachios": "bag",
        "Macadamia Nuts": "bag",
        "Pine Nuts": "bag",
        "Hazelnuts": "bag",
        "Brazil Nuts": "bag",
        "Peanut Butter": "jar",
        "Almond Butter": "jar",
        "Sunflower Seeds": "bag",
        "Pumpkin Seeds": "bag",
        "Chia Seeds": "bag",
        "Flax Seeds": "bag",
        "Hemp Seeds": "bag",
    },
    "Dried Fruits": {
        "Raisins": "box",
        "Dried Cranberries": "bag",
        "Dried Apricots": "bag",
        "Dates": "container",
        "Prunes": "bag",
        "Dried Figs": "bag",
        "Dried Mango": "bag",
        "Dried Pineapple": "bag",
        "Trail Mix": "bag",
    },
    "Frozen - Vegetables": {
        "Frozen Peas": "bag",
        "Frozen Corn": "bag",
        "Frozen Green Beans": "bag",
        "Frozen Broccoli": "bag",
        "Frozen Spinach": "bag",
        "Frozen Mixed Vegetables": "bag",
        "Frozen Stir Fry Mix": "bag",
        "Frozen Cauliflower Rice": "bag",
        "Frozen Edamame": "bag",
    },
    "Frozen - Fruits": {
        "Frozen Strawberries": "bag",
        "Frozen Blueberries": "bag",
        "Frozen Raspberries": "bag",
        "Frozen Mixed Berries": "bag",
        "Frozen Mango": "bag",
        "Frozen Peaches": "bag",
        "Frozen Pineapple": "bag",
        "Frozen Bananas": "bag",
    },
    "Frozen - Meats": {
        "Frozen Chicken Breasts": "bag",
        "Frozen Chicken Wings": "bag",
        "Frozen Ground Beef": "lb",
        "Frozen Meatballs": "bag",
        "Frozen Burgers": "box",
    },
    "Frozen - Seafood": {
        "Frozen Shrimp": "bag",
        "Frozen Salmon": "lb",
        "Frozen Tilapia": "bag",
        "Frozen Fish Sticks": "box",
    },
    "Frozen - Prepared": {
        "Frozen Pizza": "each",
        "Frozen Waffles": "box",
        "Frozen Pancakes": "box",
        "Frozen French Fries": "bag",
        "Frozen Tater Tots": "bag",
        "Frozen Hash Browns": "bag",
        "Frozen Burritos": "pack",
        "Frozen Pot Pies": "each",
        "Frozen Dinner Entrees": "each",
    },
    "Frozen - Desserts": {
        "Ice Cream": "pint",
        "Frozen Yogurt": "pint",
        "Ice Cream Bars": "box",
        "Frozen Pie Crusts": "pack",
        "Frozen Puff Pastry": "box",
        "Frozen Phyllo Dough": "box",
    },
    "Beverages": {
        "Bottled Water": "pack",
        "Sparkling Water": "pack",
        "Orange Juice": "carton",
        "Apple Juice": "bottle",
        "Grape Juice": "bottle",
        "Cranberry Juice": "bottle",
        "Lemonade": "carton",
        "Iced Tea": "bottle",
        "Soda (Cola)": "pack",
        "Soda (Lemon-Lime)": "pack",
        "Fresca": "pack",
        "Soda (Ginger Ale)": "pack",
        "Tonic Water": "bottle",
        "Club Soda": "bottle",
        "Energy Drinks": "pack",
        "Sports Drinks": "pack",
        "Coconut Water": "carton",
    },
    "Coffee & Tea": {
        "Coffee (Ground)": "bag",
        "Coffee (Whole Bean)": "bag",
        "Coffee (Instant)": "jar",
        "Coffee (K-Cups)": "box",
        "Espresso": "bag",
        "Decaf Coffee": "bag",
        "Black Tea": "box",
        "Green Tea": "box",
        "Herbal Tea": "box",
        "Chamomile Tea": "box",
        "Peppermint Tea": "box",
        "Earl Grey Tea": "box",
        "Chai Tea": "box",
        "Matcha Powder": "container",
    },
    "Snacks": {
        "Potato Chips": "bag",
        "Tortilla Chips": "bag",
        "Pretzels": "bag",
        "Popcorn": "bag",
        "Crackers (Saltine)": "box",
        "Crackers (Graham)": "box",
        "Crackers (Cheese)": "box",
        "Crackers (Wheat)": "box",
        "Rice Cakes": "bag",
        "Granola Bars": "box",
        "Protein Bars": "box",
        "Fruit Snacks": "box",
        "Beef Jerky": "bag",
        "Cheese Puffs": "bag",
        "Veggie Straws": "bag",
    },
    "Breakfast": {
        "Cereal (Cold)": "box",
        "Granola": "bag",
        "Muesli": "bag",
        "Pancake Mix": "box",
        "Waffle Mix": "box",
        "Muffin Mix": "box",
        "Breakfast Bars": "box",
        "Pop-Tarts": "box",
    },
    "Baby & Infant": {
        "Baby Formula": "can",
        "Baby Cereal": "box",
        "Baby Food (Jars)": "jar",
        "Baby Food (Pouches)": "each",
        "Teething Biscuits": "box",
    },
    "Pet Food": {
        "Dog Food (Dry)": "bag",
        "Dog Food (Wet)": "can",
        "Dog Treats": "bag",
        "Cat Food (Dry)": "bag",
        "Cat Food (Wet)": "can",
        "Cat Treats": "bag",
    },
    "Household - Paper": {
        "Paper Towels": "pack",
        "Toilet Paper": "pack",
        "Facial Tissues": "box",
        "Napkins": "pack",
        "Paper Plates": "pack",
        "Paper Cups": "pack",
        "Plastic Wrap": "roll",
        "Aluminum Foil": "roll",
        "Parchment Paper": "roll",
        "Wax Paper": "roll",
        "Zip-Lock Bags (Gallon)": "box",
        "Zip-Lock Bags (Quart)": "box",
        "Zip-Lock Bags (Sandwich)": "box",
        "Trash Bags (Large)": "box",
        "Trash Bags (Kitchen)": "box",
    },
    "Household - Cleaning": {
        "Dish Soap": "bottle",
        "Dishwasher Detergent": "bottle",
        "Laundry Detergent": "bottle",
        "Fabric Softener": "bottle",
        "Dryer Sheets": "box",
        "Bleach": "bottle",
        "All-Purpose Cleaner": "bottle",
        "Glass Cleaner": "bottle",
        "Disinfecting Wipes": "container",
        "Sponges": "pack",
        "Scrub Brushes": "each",
        "Broom": "each",
        "Mop": "each",
    },
    "Personal Care": {
        "Shampoo": "bottle",
        "Conditioner": "bottle",
        "Body Wash": "bottle",
        "Bar Soap": "pack",
        "Hand Soap": "bottle",
        "Lotion": "bottle",
        "Deodorant": "each",
        "Toothpaste": "each",
        "Toothbrush": "each",
        "Mouthwash": "bottle",
        "Dental Floss": "each",
        "Razors": "pack",
        "Shaving Cream": "can",
        "Cotton Balls": "bag",
        "Cotton Swabs": "box",
        "Sunscreen": "bottle",
        "Lip Balm": "each",
        "Hand Sanitizer": "bottle",
    },
    "Health": {
        "Bandages": "box",
        "First Aid Kit": "each",
        "Pain Reliever (Ibuprofen)": "bottle",
        "Pain Reliever (Acetaminophen)": "bottle",
        "Antacid": "bottle",
        "Allergy Medicine": "box",
        "Cold Medicine": "bottle",
        "Cough Drops": "bag",
        "Multivitamins": "bottle",
        "Vitamin C": "bottle",
        "Vitamin D": "bottle",
        "Fish Oil": "bottle",
        "Probiotics": "bottle",
        "Melatonin": "bottle",
    },
    "International": {
        "Taco Shells": "box",
        "Enchilada Sauce": "can",
        "Mole Sauce": "jar",
        "Curry Paste": "jar",
        "Coconut Cream": "can",
        "Miso Paste": "container",
        "Tofu": "pack",
        "Tempeh": "pack",
        "Seaweed/Nori": "pack",
    },
}

# Common units for grocery items
UNITS = [
    "each",        # individual items
    "lb", "oz", "kg", "g",  # weight
    "gal", "half gal", "qt", "pint", "cup", "fl oz", "L", "mL",  # volume
    "tsp", "tbsp",  # small measures
    "dozen",  # eggs etc
    "pack", "box", "bag", "bundle", "roll",  # packages
    "carton", "bottle", "can", "jar", "container",  # containers
    "loaf", "bunch", "head", "clove",  # produce specific
]

# Items with custom unit options (item_name: [units list, default_index])
CUSTOM_UNITS = {
    # Milk
    "Whole Milk": (["quart", "half gallon", "gallon"], 1),
    "2% Milk": (["quart", "half gallon", "gallon"], 1),
    "Skim Milk": (["quart", "half gallon", "gallon"], 1),
    # Cream
    "Half & Half": (["pint", "quart"], 0),
    "Heavy Cream": (["half pint", "pint", "quart"], 1),
    # Butter
    "Butter (Salted)": (["stick", "lb"], 0),
    "Butter (Unsalted)": (["stick", "lb"], 0),
    # Eggs
    "Eggs (Large)": (["half dozen", "dozen", "18-count"], 1),
    # Container dairy
    "Sour Cream": (["8 oz", "16 oz"], 1),
    "Cream Cheese": (["8 oz", "tub"], 0),
    "Cottage Cheese": (["16 oz", "24 oz"], 0),
    "Ricotta Cheese": (["15 oz", "32 oz"], 0),
    "Yogurt (Plain)": (["5.3 oz", "32 oz"], 1),
    "Yogurt (Greek)": (["5.3 oz", "32 oz"], 0),
    # Block/Slice cheeses
    "Cheddar Cheese": (["slices", "block", "lb", "8 oz shredded"], 1),
    "Swiss Cheese": (["slices", "block", "lb"], 0),
    "Mozzarella Cheese": (["slices", "block", "lb", "8 oz shredded", "fresh ball"], 1),
    "Parmesan Cheese": (["wedge", "grated", "lb"], 0),
    "Provolone Cheese": (["slices", "block", "lb"], 0),
    "American Cheese": (["slices", "block", "lb"], 0),
    "Pepper Jack Cheese": (["slices", "block", "lb", "8 oz shredded"], 1),
    # Specialty cheese
    "Feta Cheese": (["4 oz crumbles", "8 oz block", "lb"], 0),
    "Blue Cheese": (["4 oz crumbles", "8 oz wedge", "lb"], 0),
    "Goat Cheese": (["4 oz log", "8 oz log", "crumbles"], 0),
    "Brie": (["small wheel", "wedge", "lb"], 0),
    # Shredded cheese
    "Shredded Mexican Blend": (["8 oz", "16 oz", "32 oz"], 1),
}

# Items with brand options (item_name: [brand options])
# Focused on items where brand matters - Central Illinois stores
ITEM_BRANDS = {
    # Dairy - Milk (Prairie Farms is regional)
    "Whole Milk": ["", "Prairie Farms", "Organic Valley", "Fairlife", "Kirkland"],
    "2% Milk": ["", "Prairie Farms", "Organic Valley", "Fairlife", "Kirkland"],
    "Skim Milk": ["", "Prairie Farms", "Organic Valley", "Fairlife"],
    "Half & Half": ["", "Prairie Farms", "Organic Valley", "Land O'Lakes"],
    "Heavy Cream": ["", "Prairie Farms", "Organic Valley", "Land O'Lakes"],
    # Dairy - Butter
    "Butter (Salted)": ["", "Kerrygold", "Land O'Lakes", "Kirkland", "Prairie Farms"],
    "Butter (Unsalted)": ["", "Kerrygold", "Land O'Lakes", "Kirkland", "Prairie Farms"],
    # Dairy - Eggs
    "Eggs (Large)": ["", "Kirkland", "Eggland's Best", "Vital Farms", "Store Brand"],
    # Dairy - Yogurt
    "Yogurt (Plain)": ["", "Fage", "Chobani", "Kirkland", "Stonyfield"],
    "Yogurt (Greek)": ["", "Fage", "Chobani", "Kirkland", "Stonyfield"],
    # Dairy - Cream Cheese, Sour Cream, Cottage Cheese
    "Cream Cheese": ["", "Philadelphia", "Prairie Farms", "Store Brand"],
    "Sour Cream": ["", "Daisy", "Prairie Farms", "Store Brand"],
    "Cottage Cheese": ["", "Prairie Farms", "Daisy", "Breakstone's", "Store Brand"],
    # Dairy - Cheese (consistent higher-end brands)
    "Cheddar Cheese": ["", "Tillamook", "Kerrygold", "Cabot", "Boar's Head", "Kirkland"],
    "Swiss Cheese": ["", "Boar's Head", "Tillamook", "Finlandia", "Kirkland"],
    "Mozzarella Cheese": ["", "BelGioioso", "Galbani", "Boar's Head", "Kirkland"],
    "Parmesan Cheese": ["", "Parmigiano-Reggiano", "BelGioioso", "Kirkland"],
    "Provolone Cheese": ["", "Boar's Head", "BelGioioso", "Tillamook", "Kirkland"],
    "American Cheese": ["", "Boar's Head", "Tillamook", "Land O'Lakes", "Kirkland"],
    "Pepper Jack Cheese": ["", "Tillamook", "Boar's Head", "Cabot", "Kirkland"],
    "Feta Cheese": ["", "Mt Vikos", "Athenos", "Kirkland", "BelGioioso"],
    "Blue Cheese": ["", "Rogue Creamery", "Maytag", "Point Reyes", "Kirkland"],
    "Goat Cheese": ["", "Montchevre", "Laura Chenel", "Kirkland"],
    "Ricotta Cheese": ["", "BelGioioso", "Galbani", "Calabro"],
    "Brie": ["", "President", "St. Andre", "Kirkland"],
    "Shredded Mexican Blend": ["", "Tillamook", "Kirkland", "Sargento"],
    # Dairy Alternatives
    "Almond Milk": ["", "Silk", "Kirkland", "Blue Diamond"],
    "Oat Milk": ["", "Oatly", "Chobani", "Kirkland", "Planet Oat"],
    # Canned Tomatoes (San Marzano is premium)
    "Diced Tomatoes": ["", "Muir Glen", "Cento", "Kirkland", "San Marzano"],
    "Crushed Tomatoes": ["", "Muir Glen", "Cento", "Kirkland", "San Marzano"],
    "Tomato Paste": ["", "Muir Glen", "Cento", "Amore"],
    "Tomato Sauce": ["", "Muir Glen", "Cento", "Kirkland"],
    # Canned Beans
    "Black Beans": ["", "Bush's", "Goya", "Kirkland", "Store Brand"],
    "Kidney Beans": ["", "Bush's", "Goya", "Store Brand"],
    "Pinto Beans": ["", "Bush's", "Goya", "Store Brand"],
    # Canned Goods
    "Tuna (Canned)": ["", "Wild Planet", "Kirkland", "Starkist", "Bumble Bee"],
    "Chicken Broth": ["", "Swanson", "Kirkland", "Pacific", "Store Brand"],
    "Beef Broth": ["", "Swanson", "Kirkland", "Pacific", "Store Brand"],
    "Vegetable Broth": ["", "Swanson", "Kirkland", "Pacific", "Store Brand"],
    # Condiments
    "Ketchup": ["", "Heinz", "Hunt's", "Store Brand"],
    "Mustard (Yellow)": ["", "French's", "Heinz"],
    "Mustard (Dijon)": ["", "Grey Poupon", "Maille"],
    "Mayonnaise": ["", "Hellmann's", "Duke's", "Kirkland"],
    "Hot Sauce": ["", "Tabasco", "Frank's RedHot", "Cholula", "Sriracha"],
    "Soy Sauce": ["", "Kikkoman", "San-J", "Kirkland"],
    "Marinara Sauce": ["", "Rao's", "La San Marzano", "Victoria", "Kirkland"],
    # Peanut Butter
    "Peanut Butter": ["", "Smucker's Natural", "Justin's", "Kirkland", "Jif"],
    "Almond Butter": ["", "Justin's", "MaraNatha", "Kirkland"],
    # Olive Oil
    "Olive Oil (Extra Virgin)": ["", "California Olive Ranch", "Kirkland", "Lucini", "Colavita"],
    # Bacon & Meat
    "Bacon": ["", "Nueske's", "Applegate", "Wright", "Kirkland"],
    # Coffee
    "Coffee (Ground)": ["", "Peet's", "Intelligentsia", "Starbucks", "Kirkland"],
    "Coffee (Whole Bean)": ["", "Intelligentsia", "Peet's", "Lavazza", "Kirkland"],
}

# Initialize session state
if "item_preferences" not in st.session_state:
    st.session_state.item_preferences = load_preferences()
if "custom_brands" not in st.session_state:
    st.session_state.custom_brands = load_custom_brands()
if "hidden_items" not in st.session_state:
    st.session_state.hidden_items = load_hidden_items()
if "custom_items" not in st.session_state:
    st.session_state.custom_items = load_custom_items()
if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = []
if "open_category" not in st.session_state:
    st.session_state.open_category = None
if "input_key_counter" not in st.session_state:
    st.session_state.input_key_counter = 0
if "config_item" not in st.session_state:
    st.session_state.config_item = None
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False


def get_default_unit(item_name):
    """Get the default unit for an item."""
    if item_name in CUSTOM_UNITS:
        units, default_idx = CUSTOM_UNITS[item_name]
        return units[default_idx]
    for category, items in MASTER_LIST.items():
        if item_name in items:
            return items[item_name]
    return "each"


def get_item_display(item, show_brand=True):
    """Get display text for an item, including saved brand if any."""
    prefs = st.session_state.item_preferences.get(item, {})
    brand = prefs.get("brand", "")
    if show_brand and brand:
        return f"{item} ({brand})"
    return item


st.title("🛒 Grocery Shopping List")

# Configuration dialog at TOP of page (if an item is being configured)
# This shows above all tabs so it works from any tab
if "config_item" in st.session_state and st.session_state.config_item:
    item = st.session_state.config_item
    st.subheader(f"Configure: {item}")

    prefs = st.session_state.item_preferences.get(item, {})

    col1, col2 = st.columns(2)

    with col1:
        # Unit selection
        if item in CUSTOM_UNITS:
            unit_options, default_idx = CUSTOM_UNITS[item]
            current_unit = prefs.get("unit", unit_options[default_idx])
            unit_idx = unit_options.index(current_unit) if current_unit in unit_options else default_idx
            new_unit = st.selectbox("Preferred Unit", unit_options, index=unit_idx, key="config_unit")
        else:
            new_unit = get_default_unit(item)
            st.write(f"Unit: {new_unit}")

    with col2:
        # Brand selection
        if item in ITEM_BRANDS:
            # Get brands including any custom ones from the same group
            all_brands = get_brands_for_item(item, st.session_state.custom_brands)
            brand_options = all_brands + ["Other..."]
            current_brand = prefs.get("brand", "")

            # Check if current brand is in options
            if current_brand and current_brand not in all_brands:
                brand_idx = len(brand_options) - 1  # Select "Other..."
                default_custom = current_brand
            else:
                brand_idx = brand_options.index(current_brand) if current_brand in brand_options else 0
                default_custom = ""

            selected_brand = st.selectbox(
                "Preferred Brand",
                brand_options,
                index=brand_idx,
                key="config_brand",
                format_func=lambda x: x if x else "No preference"
            )

            # Show text input if "Other..." selected
            if selected_brand == "Other...":
                new_brand = st.text_input("Enter brand name", value=default_custom, key="config_custom_brand")
            else:
                new_brand = selected_brand
        else:
            # No predefined brands - allow custom one-off brand entry
            current_brand = prefs.get("brand", "")
            new_brand = st.text_input(
                "Brand (optional)",
                value=current_brand,
                key="config_custom_brand",
                placeholder="Enter brand name..."
            )

    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("Save Preferences", type="primary", use_container_width=True):
            st.session_state.item_preferences[item] = {
                "unit": new_unit,
                "brand": new_brand
            }
            save_preferences(st.session_state.item_preferences)

            # If this is a custom brand (not in predefined list), save it to the group
            if new_brand and item in ITEM_BRANDS and new_brand not in ITEM_BRANDS[item]:
                group = get_brand_group(item)
                if group:
                    if group not in st.session_state.custom_brands:
                        st.session_state.custom_brands[group] = []
                    if new_brand not in st.session_state.custom_brands[group]:
                        st.session_state.custom_brands[group].append(new_brand)
                        save_custom_brands(st.session_state.custom_brands)

            st.session_state.config_item = None
            st.toast(f"Saved preferences for {item}")
            st.rerun()
    with col_cancel:
        if st.button("Cancel", use_container_width=True):
            st.session_state.config_item = None
            st.rerun()

    st.divider()

# Create tabs
tab1, tab2, tab3 = st.tabs(["📋 Master List", "⚙️ My Preferences", "🛒 Shopping List"])

# Tab 1: Master List - browse and add items to shopping list
with tab1:
    # Header with edit mode toggle
    col_header, col_edit = st.columns([4, 1])
    with col_header:
        st.subheader("Add Items to Shopping List")
    with col_edit:
        edit_mode = st.toggle("Edit", value=st.session_state.edit_mode, key="edit_toggle")
        if edit_mode != st.session_state.edit_mode:
            st.session_state.edit_mode = edit_mode
            st.rerun()

    if st.session_state.edit_mode:
        st.caption("Edit mode: Add or remove items from your master list")
    else:
        st.caption("Click + to add items. Your saved brand preferences will be used automatically.")

    # Get items currently in shopping list
    items_in_cart = {e["item"] for e in st.session_state.grocery_list}

    for category, base_items in MASTER_LIST.items():
        # Merge base items with custom items for this category
        items = dict(base_items)
        if category in st.session_state.custom_items:
            items.update(st.session_state.custom_items[category])

        # Filter out hidden items
        visible_items = {k: v for k, v in items.items() if k not in st.session_state.hidden_items}

        # Count items in cart (only visible ones)
        cart_count = len([i for i in visible_items if i in items_in_cart])
        is_open = st.session_state.open_category == category

        # Show cart count in expander if any items selected
        if cart_count > 0:
            expander_label = f"**{category}** ({cart_count} in cart)"
        else:
            expander_label = f"**{category}**"

        with st.expander(expander_label, expanded=is_open):
            # In edit mode, show add item form at top of category
            if st.session_state.edit_mode:
                with st.container():
                    add_cols = st.columns([3, 1.5, 1])
                    with add_cols[0]:
                        new_item_name = st.text_input(
                            "New item",
                            key=f"new_item_{category}",
                            placeholder="Add new item...",
                            label_visibility="collapsed"
                        )
                    with add_cols[1]:
                        new_item_unit = st.selectbox(
                            "Unit",
                            UNITS,
                            key=f"new_unit_{category}",
                            label_visibility="collapsed"
                        )
                    with add_cols[2]:
                        if st.button("Add", key=f"add_new_{category}", use_container_width=True):
                            if new_item_name.strip():
                                # Add to custom items
                                if category not in st.session_state.custom_items:
                                    st.session_state.custom_items[category] = {}
                                st.session_state.custom_items[category][new_item_name.strip()] = new_item_unit
                                save_custom_items(st.session_state.custom_items)
                                st.toast(f"Added {new_item_name.strip()} to {category}")
                                st.rerun()
                    st.write("")  # spacing

            cols = st.columns(2)
            for idx, (item, default_unit) in enumerate(visible_items.items()):
                prefs = st.session_state.item_preferences.get(item, {})
                saved_brand = prefs.get("brand", "")
                saved_unit = prefs.get("unit", get_default_unit(item))
                in_cart = item in items_in_cart
                is_custom = category in st.session_state.custom_items and item in st.session_state.custom_items[category]

                # Build display text
                if saved_brand:
                    display_text = f"{item} • {saved_brand}"
                elif item in CUSTOM_UNITS:
                    display_text = item
                else:
                    display_text = f"{item} ({default_unit})"

                with cols[idx % 2]:
                    if st.session_state.edit_mode:
                        # Edit mode: show delete button
                        col_name, col_del = st.columns([5, 1])
                        with col_name:
                            if is_custom:
                                st.write(f"📝 {item} ({default_unit})")
                            else:
                                st.write(f"{item} ({default_unit})")
                        with col_del:
                            if st.button("🗑", key=f"del_{item}", help=f"Remove {item}"):
                                if is_custom:
                                    # Remove from custom items entirely
                                    del st.session_state.custom_items[category][item]
                                    if not st.session_state.custom_items[category]:
                                        del st.session_state.custom_items[category]
                                    save_custom_items(st.session_state.custom_items)
                                else:
                                    # Hide built-in item
                                    st.session_state.hidden_items.add(item)
                                    save_hidden_items(st.session_state.hidden_items)
                                st.toast(f"Removed {item}")
                                st.rerun()
                    else:
                        # Normal mode: show add button and gear
                        col_btn, col_gear = st.columns([5, 1])
                        with col_btn:
                            if in_cart:
                                # Show as selected (green) - can still click to add more
                                st.success(f"✓ {display_text}")
                            else:
                                if st.button(f"+ {display_text}", key=f"add_{item}", use_container_width=True):
                                    # Add to shopping list with saved preferences
                                    entry = {
                                        "item": item,
                                        "qty": 1,
                                        "unit": saved_unit,
                                        "brand": saved_brand
                                    }
                                    st.session_state.grocery_list.append(entry)
                                    st.toast(f"Added {item}" + (f" ({saved_brand})" if saved_brand else ""))
                                    st.rerun()

                        with col_gear:
                            # Show gear icon for all items (set brand/unit preferences)
                            if st.button("⚙", key=f"config_{item}", help="Set preferences"):
                                st.session_state.open_category = category
                                st.session_state.config_item = item
                                st.rerun()

# Tab 2: My Preferences - view and edit saved preferences
with tab2:
    st.subheader("My Saved Preferences")
    st.caption("Your preferred brands and units for items")

    if not st.session_state.item_preferences:
        st.info("No preferences saved yet. Go to Master List and click ⚙ to configure items.")
    else:
        # Group by category
        items_by_category = {}
        for item in st.session_state.item_preferences:
            for category, cat_items in MASTER_LIST.items():
                if item in cat_items:
                    if category not in items_by_category:
                        items_by_category[category] = []
                    items_by_category[category].append(item)
                    break

        for category, items in items_by_category.items():
            st.write(f"**{category}**")
            for item in items:
                prefs = st.session_state.item_preferences[item]

                c1, c2, c3, c4 = st.columns([2, 1.2, 1.2, 0.5])

                with c1:
                    st.write(item)

                with c2:
                    # Unit dropdown
                    if item in CUSTOM_UNITS:
                        unit_options, default_idx = CUSTOM_UNITS[item]
                        current_unit = prefs.get("unit", unit_options[default_idx])
                        unit_idx = unit_options.index(current_unit) if current_unit in unit_options else default_idx
                        old_unit = current_unit
                        new_unit = st.selectbox(
                            "Unit", unit_options, index=unit_idx,
                            key=f"pref_unit_{item}", label_visibility="collapsed"
                        )
                        if new_unit != old_unit:
                            st.session_state.item_preferences[item]["unit"] = new_unit
                            save_preferences(st.session_state.item_preferences)
                    else:
                        st.write(prefs.get("unit", get_default_unit(item)))

                with c3:
                    # Brand display/edit
                    current_brand = prefs.get("brand", "")
                    if item in ITEM_BRANDS:
                        all_brands = get_brands_for_item(item, st.session_state.custom_brands)
                        # If current brand is in predefined list, show dropdown
                        if not current_brand or current_brand in all_brands:
                            brand_options = all_brands
                            brand_idx = brand_options.index(current_brand) if current_brand in brand_options else 0
                            selected_brand = st.selectbox(
                                "Brand", brand_options, index=brand_idx,
                                key=f"pref_brand_{item}", label_visibility="collapsed",
                                format_func=lambda x: x if x else "No preference"
                            )
                            # Save on change
                            if selected_brand != current_brand:
                                st.session_state.item_preferences[item]["brand"] = selected_brand
                                save_preferences(st.session_state.item_preferences)
                                st.rerun()
                        else:
                            # Custom brand - show as text (edit via gear button)
                            st.write(current_brand)
                    else:
                        # No predefined brands - show current brand as text
                        st.write(current_brand if current_brand else "-")

                with c4:
                    # Edit and delete buttons
                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        if st.button("✏️", key=f"edit_pref_{item}", help="Edit preferences"):
                            # Find the category for this item
                            for cat, cat_items in MASTER_LIST.items():
                                if item in cat_items:
                                    st.session_state.open_category = cat
                                    break
                            st.session_state.config_item = item
                            # Switch to Master List tab (tab index 0)
                            st.rerun()
                    with col_del:
                        if st.button("🗑", key=f"del_pref_{item}", help="Remove preference"):
                            del st.session_state.item_preferences[item]
                            save_preferences(st.session_state.item_preferences)
                            st.rerun()

            st.write("")  # spacing

    # Section to manage custom brands
    st.divider()
    with st.expander("Manage Custom Brands", expanded=False):
        if not st.session_state.custom_brands:
            st.info("No custom brands added yet. Use 'Other...' when setting preferences to add custom brands.")
        else:
            # Display custom brands by group with delete buttons
            group_display_names = {
                "cheese": "Cheese",
                "milk": "Milk",
                "cream": "Cream",
                "butter": "Butter",
                "yogurt": "Yogurt",
                "milk_alt": "Milk Alternatives",
                "canned_tomatoes": "Canned Tomatoes",
                "canned_beans": "Canned Beans",
                "broth": "Broth",
                "coffee": "Coffee",
                "nut_butter": "Nut Butter",
            }
            for group, brands in st.session_state.custom_brands.items():
                if brands:  # Only show groups that have custom brands
                    group_name = group_display_names.get(group, group.title())
                    st.write(f"**{group_name}**")
                    for brand in brands:
                        col_brand, col_del = st.columns([4, 1])
                        with col_brand:
                            st.write(brand)
                        with col_del:
                            if st.button("🗑", key=f"del_brand_{group}_{brand}", help=f"Delete {brand}"):
                                st.session_state.custom_brands[group].remove(brand)
                                # Clean up empty groups
                                if not st.session_state.custom_brands[group]:
                                    del st.session_state.custom_brands[group]
                                save_custom_brands(st.session_state.custom_brands)
                                st.toast(f"Deleted {brand} from {group_name}")
                                st.rerun()

    # Section to restore hidden items
    with st.expander("Restore Hidden Items", expanded=False):
        if not st.session_state.hidden_items:
            st.info("No hidden items. Use Edit mode in Master List to hide items you don't need.")
        else:
            st.caption("These items were removed from your master list. Click to restore them.")
            for item in sorted(st.session_state.hidden_items):
                col_item, col_restore = st.columns([4, 1])
                with col_item:
                    st.write(item)
                with col_restore:
                    if st.button("↩", key=f"restore_{item}", help=f"Restore {item}"):
                        st.session_state.hidden_items.remove(item)
                        save_hidden_items(st.session_state.hidden_items)
                        st.toast(f"Restored {item}")
                        st.rerun()

# Tab 3: Shopping List - this trip's items
with tab3:
    st.subheader("Current Shopping List")

    # Add custom item
    with st.expander("Add custom item", expanded=False):
        key_suffix = st.session_state.input_key_counter
        cols = st.columns([2, 1, 1.5, 1])
        with cols[0]:
            new_item = st.text_input("Item", key=f"new_item_{key_suffix}", label_visibility="collapsed", placeholder="Item name...")
        with cols[1]:
            new_qty = st.number_input("Qty", min_value=1, value=1, step=1, key=f"new_qty_{key_suffix}", label_visibility="collapsed")
        with cols[2]:
            new_unit = st.selectbox("Unit", UNITS, key=f"new_unit_{key_suffix}", label_visibility="collapsed")
        with cols[3]:
            if st.button("Add", use_container_width=True):
                if new_item.strip():
                    st.session_state.grocery_list.append({
                        "item": new_item.strip(),
                        "qty": new_qty,
                        "unit": new_unit,
                        "brand": ""
                    })
                    st.session_state.input_key_counter += 1
                    st.rerun()

    if not st.session_state.grocery_list:
        st.info("Your shopping list is empty. Go to Master List to add items.")
    else:
        st.write(f"**{len(st.session_state.grocery_list)} items:**")

        for i, entry in enumerate(st.session_state.grocery_list):
            cols = st.columns([0.5, 3.5, 1])

            qty_str = int(entry["qty"]) if entry["qty"] == int(entry["qty"]) else entry["qty"]
            brand_suffix = f" - {entry['brand']}" if entry.get("brand") else ""
            display = f"{qty_str} {entry['unit']} {entry['item']}{brand_suffix}"

            with cols[0]:
                # Quantity adjuster
                if st.button("−", key=f"dec_shop_{i}"):
                    if st.session_state.grocery_list[i]["qty"] > 1:
                        st.session_state.grocery_list[i]["qty"] -= 1
                        st.rerun()

            with cols[1]:
                st.write(f"☐ {display}")

            with cols[2]:
                col_inc, col_del = st.columns(2)
                with col_inc:
                    if st.button("＋", key=f"inc_shop_{i}"):
                        st.session_state.grocery_list[i]["qty"] += 1
                        st.rerun()
                with col_del:
                    if st.button("✕", key=f"remove_{i}", help="Remove"):
                        st.session_state.grocery_list.pop(i)
                        st.rerun()

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear List", type="secondary", use_container_width=True):
                st.session_state.grocery_list.clear()
                st.session_state.input_key_counter += 1
                st.rerun()
        with col2:
            def format_export_line(e):
                qty = int(e['qty']) if e['qty'] == int(e['qty']) else e['qty']
                brand = f" - {e['brand']}" if e.get('brand') else ""
                return f"{qty} {e['unit']} {e['item']}{brand}"
            list_text = "\n".join([format_export_line(e) for e in st.session_state.grocery_list])
            st.download_button(
                "📥 Export List",
                list_text,
                file_name="grocery_list.txt",
                mime="text/plain",
                use_container_width=True
            )
