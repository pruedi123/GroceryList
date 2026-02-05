#!/usr/bin/env python3
"""Simple Grocery Shopping List Application - Streamlit Version"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

# Detect if running on Streamlit Cloud (apps run from /mount/src/)
IS_CLOUD = str(Path(__file__).parent).startswith("/mount/src")

# File for persisting item preferences (local only)
PREFS_FILE = Path(__file__).parent / "item_preferences.json"
CUSTOM_BRANDS_FILE = Path(__file__).parent / "custom_brands.json"
HIDDEN_ITEMS_FILE = Path(__file__).parent / "hidden_items.json"
CUSTOM_ITEMS_FILE = Path(__file__).parent / "custom_items.json"


def load_preferences():
    """Load item preferences from file (local only)."""
    if IS_CLOUD:
        return {}
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_preferences(data):
    """Save item preferences to file (local only)."""
    if IS_CLOUD:
        return
    try:
        with open(PREFS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        pass


def load_custom_brands():
    """Load custom brands from file (local only)."""
    if IS_CLOUD:
        return {}
    if CUSTOM_BRANDS_FILE.exists():
        try:
            with open(CUSTOM_BRANDS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_custom_brands(data):
    """Save custom brands to file (local only)."""
    if IS_CLOUD:
        return
    try:
        with open(CUSTOM_BRANDS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        pass


def load_hidden_items():
    """Load hidden/deleted items from file (local only)."""
    if IS_CLOUD:
        return set()
    if HIDDEN_ITEMS_FILE.exists():
        try:
            with open(HIDDEN_ITEMS_FILE, "r") as f:
                return set(json.load(f))
        except (json.JSONDecodeError, IOError):
            return set()
    return set()


def save_hidden_items(data):
    """Save hidden/deleted items to file (local only)."""
    if IS_CLOUD:
        return
    try:
        with open(HIDDEN_ITEMS_FILE, "w") as f:
            json.dump(list(data), f, indent=2)
    except IOError:
        pass


def load_custom_items():
    """Load custom items from file (local only). Format: {category: {item: unit}}"""
    if IS_CLOUD:
        return {}
    if CUSTOM_ITEMS_FILE.exists():
        try:
            with open(CUSTOM_ITEMS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_custom_items(data):
    """Save custom items to file (local only)."""
    if IS_CLOUD:
        return
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


def get_brands_for_item(item, custom_brands_dict, preferences_dict=None):
    """Get all brands for an item (predefined + custom from same group + saved preference)."""
    if item not in ITEM_BRANDS:
        return []

    brands = list(ITEM_BRANDS[item])  # Start with predefined

    # Add custom brands from the same group
    group = get_brand_group(item)
    if group and group in custom_brands_dict:
        for custom_brand in custom_brands_dict[group]:
            if custom_brand not in brands:
                brands.append(custom_brand)

    # Add saved preference brand if it's not already in the list
    if preferences_dict and item in preferences_dict:
        saved_brand = preferences_dict[item].get("brand")
        if saved_brand and saved_brand not in brands:
            brands.append(saved_brand)

    return brands

# Master list of items organized by category with default units
# Format: {"item_name": "default_unit"}
MASTER_LIST = {
    "Produce - Fruits": {
        "Apples": "lb",
        "Avocados": "each",
        "Bananas": "bunch",
        "Blackberries": "pint",
        "Blueberries": "pint",
        "Cantaloupe": "each",
        "Cherries": "lb",
        "Grapefruit": "each",
        "Grapes": "lb",
        "Honeydew": "each",
        "Kiwi": "each",
        "Lemons": "each",
        "Limes": "each",
        "Mango": "each",
        "Oranges": "lb",
        "Peaches": "lb",
        "Pears": "lb",
        "Pineapple": "each",
        "Plums": "lb",
        "Raspberries": "pint",
        "Strawberries": "lb",
        "Watermelon": "each",
    },
    "Produce - Vegetables": {
        "Acorn Squash": "each",
        "Arugula": "bag",
        "Asparagus": "bunch",
        "Beets": "lb",
        "Bell Peppers (Green)": "each",
        "Bell Peppers (Red)": "each",
        "Bell Peppers (Yellow)": "each",
        "Broccoli": "lb",
        "Brussels Sprouts": "lb",
        "Butternut Squash": "each",
        "Cabbage (Green)": "head",
        "Cabbage (Red)": "head",
        "Carrots": "lb",
        "Cauliflower": "head",
        "Celery": "bunch",
        "Cherry Tomatoes": "pint",
        "Corn on the Cob": "each",
        "Cucumbers": "each",
        "Eggplant": "each",
        "Garlic": "head",
        "Grape Tomatoes": "pint",
        "Green Beans": "lb",
        "Jalapeños": "each",
        "Kale": "bunch",
        "Lettuce (Iceberg)": "head",
        "Lettuce (Romaine)": "head",
        "Mixed Greens": "bag",
        "Mushrooms (Cremini)": "oz",
        "Mushrooms (Portobello)": "each",
        "Mushrooms (White)": "oz",
        "Onions (Red)": "each",
        "Onions (White)": "each",
        "Onions (Yellow)": "each",
        "Parsnips": "lb",
        "Potatoes (Red)": "lb",
        "Potatoes (Russet)": "lb",
        "Potatoes (Yukon Gold)": "lb",
        "Radishes": "bunch",
        "Serrano Peppers": "each",
        "Snap Peas": "lb",
        "Spaghetti Squash": "each",
        "Spinach": "bag",
        "Sweet Potatoes": "lb",
        "Tomatoes": "lb",
        "Turnips": "lb",
        "Yellow Squash": "each",
        "Zucchini": "each",
    },
    "Produce - Herbs": {
        "Basil (Fresh)": "bunch",
        "Chives": "bunch",
        "Cilantro": "bunch",
        "Dill": "bunch",
        "Ginger Root": "each",
        "Green Onions/Scallions": "bunch",
        "Mint": "bunch",
        "Parsley (Curly)": "bunch",
        "Parsley (Flat)": "bunch",
        "Rosemary": "bunch",
        "Sage": "bunch",
        "Thyme": "bunch",
    },
    "Dairy": {
        "2% Milk": "half gal",
        "American Cheese": "lb",
        "Blue Cheese": "oz",
        "Brie": "each",
        "Butter (Salted)": "lb",
        "Butter (Unsalted)": "lb",
        "Cheddar Cheese": "lb",
        "Cottage Cheese": "oz",
        "Cream Cheese": "oz",
        "Eggs (Large)": "dozen",
        "Feta Cheese": "oz",
        "Goat Cheese": "oz",
        "Half & Half": "pint",
        "Heavy Cream": "pint",
        "Mozzarella Cheese": "lb",
        "Parmesan Cheese": "lb",
        "Pepper Jack Cheese": "lb",
        "Provolone Cheese": "lb",
        "Ricotta Cheese": "oz",
        "Shredded Mexican Blend": "bag",
        "Skim Milk": "half gal",
        "Sour Cream": "oz",
        "Swiss Cheese": "lb",
        "Whole Milk": "half gal",
        "Yogurt (Greek)": "oz",
        "Yogurt (Plain)": "oz",
    },
    "Dairy Alternatives": {
        "Almond Milk": "carton",
        "Coconut Milk (Carton)": "carton",
        "Oat Milk": "carton",
        "Soy Milk": "carton",
        "Vegan Butter": "each",
        "Vegan Cheese": "each",
    },
    "Meat - Beef": {
        "Brisket": "lb",
        "Chuck Roast": "lb",
        "Filet Mignon": "lb",
        "Flank Steak": "lb",
        "Ground Beef (80/20)": "lb",
        "Ground Beef (90/10)": "lb",
        "NY Strip Steak": "lb",
        "Pastrami Slices": "lb",
        "Ribeye Steak": "lb",
        "Short Ribs": "lb",
        "Sirloin Steak": "lb",
        "Skirt Steak": "lb",
        "Stew Meat": "lb",
    },
    "Meat - Pork": {
        "Baby Back Ribs": "lb",
        "Bacon": "pack",
        "Bratwurst": "pack",
        "Breakfast Sausage": "pack",
        "Ground Pork": "lb",
        "Ham (Sliced)": "lb",
        "Ham (Whole)": "lb",
        "Hot Dogs": "pack",
        "Italian Sausage": "lb",
        "Pepperoni": "pack",
        "Pork Chops (Bone-In)": "lb",
        "Pork Chops (Boneless)": "lb",
        "Pork Loin Roast": "lb",
        "Pork Shoulder": "lb",
        "Pork Tenderloin": "lb",
        "Prosciutto": "oz",
        "Salami": "oz",
        "Spare Ribs": "lb",
    },
    "Meat - Poultry": {
        "Chicken Breast (Bone-In)": "lb",
        "Chicken Breast (Boneless)": "lb",
        "Chicken Drumsticks": "lb",
        "Chicken Thighs (Bone-In)": "lb",
        "Chicken Thighs (Boneless)": "lb",
        "Chicken Wings": "lb",
        "Ground Chicken": "lb",
        "Ground Turkey": "lb",
        "Rotisserie Chicken": "each",
        "Turkey (Deli Sliced)": "lb",
        "Turkey Breast": "lb",
        "Whole Chicken": "each",
    },
    "Seafood": {
        "Crab Meat": "lb",
        "Salmon Fillet": "lb",
        "Sea Bass": "lb",
        "Shrimp (Cooked)": "lb",
        "Shrimp (Raw)": "lb",
    },
    "Canned Goods": {
        "Artichoke Hearts": "can",
        "Baked Beans": "can",
        "Beef Broth": "carton",
        "Black Beans": "can",
        "Chicken Broth": "carton",
        "Chipotle in Adobo": "can",
        "Coconut Milk (Canned)": "can",
        "Corn (Canned)": "can",
        "Crushed Tomatoes": "can",
        "Diced Tomatoes": "can",
        "Evaporated Milk": "can",
        "Green Beans (Canned)": "can",
        "Green Chiles": "can",
        "Jalapeños (Pickled)": "jar",
        "Kidney Beans": "can",
        "Mixed Vegetables": "can",
        "Olives (Black)": "can",
        "Olives (Green)": "jar",
        "Peas (Canned)": "can",
        "Pinto Beans": "can",
        "Pumpkin Puree": "can",
        "Refried Beans": "can",
        "Roasted Red Peppers": "jar",
        "Sweetened Condensed Milk": "can",
        "Tomato Paste": "can",
        "Tomato Sauce": "can",
        "Tuna (Canned)": "can",
        "Vegetable Broth": "carton",
    },
    "Grains & Pasta": {
        "Angel Hair": "box",
        "Arborio Rice": "lb",
        "Barley": "lb",
        "Basmati Rice": "lb",
        "Brown Rice": "lb",
        "Bulgur": "lb",
        "Couscous": "box",
        "Egg Noodles": "bag",
        "Farfalle (Bow Tie)": "box",
        "Farro": "lb",
        "Fettuccine": "box",
        "Fusilli": "box",
        "Jasmine Rice": "lb",
        "Lasagna Noodles": "box",
        "Linguine": "box",
        "Macaroni": "box",
        "Oats (Instant)": "box",
        "Oats (Rolled)": "container",
        "Oats (Steel Cut)": "container",
        "Orzo": "box",
        "Penne": "box",
        "Quinoa": "lb",
        "Ramen Noodles": "pack",
        "Ravioli": "pack",
        "Rice Noodles": "pack",
        "Rigatoni": "box",
        "Soba Noodles": "pack",
        "Spaghetti": "box",
        "Tortellini": "pack",
        "Udon Noodles": "pack",
        "White Rice (Long Grain)": "lb",
        "Wild Rice": "lb",
    },
    "Bread & Bakery": {
        "Bagels": "pack",
        "Breadcrumbs": "container",
        "Ciabatta": "each",
        "Corn Tortillas": "pack",
        "Croissants": "pack",
        "Croutons": "bag",
        "English Muffins": "pack",
        "Flour Tortillas": "pack",
        "French Bread": "loaf",
        "Hamburger Buns": "pack",
        "Hot Dog Buns": "pack",
        "Italian Bread": "loaf",
        "Multigrain Bread": "loaf",
        "Naan": "pack",
        "Panko Breadcrumbs": "container",
        "Pita Bread": "pack",
        "Rye Bread": "loaf",
        "Sourdough Bread": "loaf",
        "Wheat Bread": "loaf",
        "White Bread": "loaf",
    },
    "Baking": {
        "Active Dry Yeast": "pack",
        "Agave Nectar": "bottle",
        "All-Purpose Flour": "lb",
        "Almond Extract": "bottle",
        "Almond Flour": "lb",
        "Baking Chocolate": "bar",
        "Baking Powder": "can",
        "Baking Soda": "box",
        "Bread Flour": "lb",
        "Brown Sugar": "lb",
        "Cake Flour": "lb",
        "Chocolate Chips": "bag",
        "Cocoa Powder": "container",
        "Coconut Flour": "lb",
        "Corn Syrup": "bottle",
        "Cornmeal": "lb",
        "Cornstarch": "box",
        "Cream of Tartar": "container",
        "Granulated Sugar": "lb",
        "Honey": "bottle",
        "Instant Yeast": "pack",
        "Maple Syrup": "bottle",
        "Molasses": "bottle",
        "Powdered Sugar": "lb",
        "Shortening": "can",
        "Vanilla Extract": "bottle",
        "Whole Wheat Flour": "lb",
    },
    "Oils & Vinegars": {
        "Apple Cider Vinegar": "bottle",
        "Avocado Oil": "bottle",
        "Balsamic Vinegar": "bottle",
        "Canola Oil": "bottle",
        "Coconut Oil": "jar",
        "Cooking Spray": "can",
        "Olive Oil (Extra Virgin)": "bottle",
        "Olive Oil (Light)": "bottle",
        "Peanut Oil": "bottle",
        "Red Wine Vinegar": "bottle",
        "Rice Vinegar": "bottle",
        "Sesame Oil": "bottle",
        "Vegetable Oil": "bottle",
        "White Vinegar": "bottle",
    },
    "Spices & Seasonings": {
        "Allspice": "container",
        "Basil (Dried)": "container",
        "Bay Leaves": "container",
        "Black Pepper": "container",
        "Caraway Seeds": "container",
        "Cardamom": "container",
        "Cayenne Pepper": "container",
        "Celery Salt": "container",
        "Celery Seed": "container",
        "Chili Powder": "container",
        "Cinnamon (Ground)": "container",
        "Cinnamon Sticks": "container",
        "Cloves": "container",
        "Coriander": "container",
        "Cumin": "container",
        "Curry Powder": "container",
        "Dill (Dried)": "container",
        "Fennel Seeds": "container",
        "Garam Masala": "container",
        "Garlic Powder": "container",
        "Ginger (Ground)": "container",
        "Herbs de Provence": "container",
        "Italian Seasoning": "container",
        "Mustard (Dry)": "container",
        "Mustard Seeds": "container",
        "Nutmeg": "container",
        "Onion Powder": "container",
        "Oregano (Dried)": "container",
        "Paprika": "container",
        "Poppy Seeds": "container",
        "Ranch Seasoning": "pack",
        "Red Pepper Flakes": "container",
        "Rosemary (Dried)": "container",
        "Saffron": "container",
        "Salt (Kosher)": "box",
        "Salt (Sea)": "container",
        "Salt (Table)": "container",
        "Sesame Seeds": "container",
        "Smoked Paprika": "container",
        "Taco Seasoning": "pack",
        "Thyme (Dried)": "container",
        "Turmeric": "container",
        "White Pepper": "container",
    },
    "Condiments": {
        "Alfredo Sauce": "jar",
        "BBQ Sauce": "bottle",
        "Blue Cheese Dressing": "bottle",
        "Caesar Dressing": "bottle",
        "Capers": "jar",
        "Fish Sauce": "bottle",
        "Guacamole": "container",
        "Hoisin Sauce": "bottle",
        "Hot Sauce": "bottle",
        "Hummus": "container",
        "Italian Dressing": "bottle",
        "Ketchup": "bottle",
        "Kimchi": "jar",
        "Marinara Sauce": "jar",
        "Mayonnaise": "jar",
        "Mustard (Dijon)": "jar",
        "Mustard (Spicy Brown)": "bottle",
        "Mustard (Yellow)": "bottle",
        "Oyster Sauce": "bottle",
        "Pesto": "jar",
        "Pickles (Bread & Butter)": "jar",
        "Pickles (Dill)": "jar",
        "Pico de Gallo": "container",
        "Ranch Dressing": "bottle",
        "Relish": "jar",
        "Salsa": "jar",
        "Sauerkraut": "jar",
        "Soy Sauce": "bottle",
        "Sriracha": "bottle",
        "Sun-Dried Tomatoes": "jar",
        "Tahini": "jar",
        "Teriyaki Sauce": "bottle",
        "Thousand Island": "bottle",
        "Vinaigrette": "bottle",
        "Worcestershire Sauce": "bottle",
    },
    "Nuts & Seeds": {
        "Almond Butter": "jar",
        "Almonds": "bag",
        "Brazil Nuts": "bag",
        "Cashews": "bag",
        "Chia Seeds": "bag",
        "Flax Seeds": "bag",
        "Hazelnuts": "bag",
        "Hemp Seeds": "bag",
        "Macadamia Nuts": "bag",
        "Peanut Butter": "jar",
        "Peanuts": "bag",
        "Pecans": "bag",
        "Pine Nuts": "bag",
        "Pistachios": "bag",
        "Pumpkin Seeds": "bag",
        "Sunflower Seeds": "bag",
        "Walnuts": "bag",
    },
    "Dried Fruits": {
        "Dates": "container",
        "Dried Apricots": "bag",
        "Dried Cranberries": "bag",
        "Dried Figs": "bag",
        "Dried Mango": "bag",
        "Dried Pineapple": "bag",
        "Prunes": "bag",
        "Raisins": "box",
        "Trail Mix": "bag",
    },
    "Frozen - Vegetables": {
        "Frozen Broccoli": "bag",
        "Frozen Cauliflower Rice": "bag",
        "Frozen Corn": "bag",
        "Frozen Edamame": "bag",
        "Frozen Green Beans": "bag",
        "Frozen Mixed Vegetables": "bag",
        "Frozen Peas": "bag",
        "Frozen Spinach": "bag",
        "Frozen Stir Fry Mix": "bag",
    },
    "Frozen - Fruits": {
        "Frozen Bananas": "bag",
        "Frozen Blueberries": "bag",
        "Frozen Mango": "bag",
        "Frozen Mixed Berries": "bag",
        "Frozen Peaches": "bag",
        "Frozen Pineapple": "bag",
        "Frozen Raspberries": "bag",
        "Frozen Strawberries": "bag",
    },
    "Frozen - Meats": {
        "Frozen Burgers": "box",
        "Frozen Chicken Breasts": "bag",
        "Frozen Chicken Wings": "bag",
        "Frozen Ground Beef": "lb",
        "Frozen Meatballs": "bag",
    },
    "Frozen - Seafood": {
        "Frozen Fish Sticks": "box",
        "Frozen Salmon": "lb",
        "Frozen Shrimp": "bag",
        "Frozen Tilapia": "bag",
    },
    "Frozen - Prepared": {
        "Frozen Burritos": "pack",
        "Frozen Dinner Entrees": "each",
        "Frozen French Fries": "bag",
        "Frozen Hash Browns": "bag",
        "Frozen Pancakes": "box",
        "Frozen Pizza": "each",
        "Frozen Pot Pies": "each",
        "Frozen Tater Tots": "bag",
        "Frozen Waffles": "box",
    },
    "Frozen - Desserts": {
        "Frozen Phyllo Dough": "box",
        "Frozen Pie Crusts": "pack",
        "Frozen Puff Pastry": "box",
        "Frozen Yogurt": "pint",
        "Ice Cream": "pint",
        "Ice Cream Bars": "box",
    },
    "Beverages": {
        "Apple Juice": "bottle",
        "Bottled Water": "pack",
        "Club Soda": "bottle",
        "Coconut Water": "carton",
        "Cranberry Juice": "bottle",
        "Energy Drinks": "pack",
        "Fresca": "pack",
        "Grape Juice": "bottle",
        "Iced Tea": "bottle",
        "Lemonade": "carton",
        "Orange Juice": "carton",
        "Soda (Cola)": "cans",
        "Soda (Ginger Ale)": "pack",
        "Soda (Lemon-Lime)": "pack",
        "Sparkling Water": "pack",
        "Sports Drinks": "pack",
        "Tonic Water": "bottle",
    },
    "Coffee & Tea": {
        "Black Tea": "box",
        "Chai Tea": "box",
        "Chamomile Tea": "box",
        "Coffee (Ground)": "bag",
        "Coffee (Instant)": "jar",
        "Coffee (K-Cups)": "box",
        "Coffee (Whole Bean)": "bag",
        "Decaf Coffee": "bag",
        "Earl Grey Tea": "box",
        "Espresso": "bag",
        "Green Tea": "box",
        "Herbal Tea": "box",
        "Matcha Powder": "container",
        "Peppermint Tea": "box",
    },
    "Snacks": {
        "Beef Jerky": "bag",
        "Cheese Puffs": "bag",
        "Crackers (Cheese)": "box",
        "Crackers (Graham)": "box",
        "Crackers (Saltine)": "box",
        "Crackers (Wheat)": "box",
        "Fruit Snacks": "box",
        "Granola Bars": "box",
        "Popcorn": "bag",
        "Potato Chips": "bag",
        "Pretzels": "bag",
        "Protein Bars": "box",
        "Rice Cakes": "bag",
        "Tortilla Chips": "bag",
        "Veggie Straws": "bag",
    },
    "Breakfast": {
        "Breakfast Bars": "box",
        "Cereal (Cold)": "box",
        "Granola": "bag",
        "Muesli": "bag",
        "Muffin Mix": "box",
        "Pancake Mix": "box",
        "Pop-Tarts": "box",
        "Waffle Mix": "box",
    },
    "Baby & Infant": {
        "Baby Cereal": "box",
        "Baby Food (Jars)": "jar",
        "Baby Food (Pouches)": "each",
        "Baby Formula": "can",
        "Teething Biscuits": "box",
    },
    "Pet Food": {
        "Cat Food (Dry)": "bag",
        "Cat Food (Wet)": "can",
        "Cat Treats": "bag",
        "Dog Food (Dry)": "bag",
        "Dog Food (Wet)": "can",
        "Dog Treats": "bag",
    },
    "Household - Paper": {
        "Aluminum Foil": "roll",
        "Facial Tissues": "box",
        "Napkins": "pack",
        "Paper Cups": "pack",
        "Paper Plates": "pack",
        "Paper Towels": "pack",
        "Parchment Paper": "roll",
        "Plastic Wrap": "roll",
        "Toilet Paper": "pack",
        "Trash Bags (Kitchen)": "box",
        "Trash Bags (Large)": "box",
        "Wax Paper": "roll",
        "Zip-Lock Bags (Gallon)": "box",
        "Zip-Lock Bags (Quart)": "box",
        "Zip-Lock Bags (Sandwich)": "box",
    },
    "Household - Cleaning": {
        "All-Purpose Cleaner": "bottle",
        "Bleach": "bottle",
        "Broom": "each",
        "Dish Soap": "bottle",
        "Dishwasher Detergent": "bottle",
        "Disinfecting Wipes": "container",
        "Dryer Sheets": "box",
        "Fabric Softener": "bottle",
        "Glass Cleaner": "bottle",
        "Laundry Detergent": "bottle",
        "Mop": "each",
        "Scrub Brushes": "each",
        "Sponges": "pack",
    },
    "Personal Care": {
        "Bar Soap": "pack",
        "Body Wash": "bottle",
        "Conditioner": "bottle",
        "Cotton Balls": "bag",
        "Cotton Swabs": "box",
        "Dental Floss": "each",
        "Deodorant": "each",
        "Hand Sanitizer": "bottle",
        "Hand Soap": "bottle",
        "Lip Balm": "each",
        "Lotion": "bottle",
        "Mouthwash": "bottle",
        "Razors": "pack",
        "Shampoo": "bottle",
        "Shaving Cream": "can",
        "Sunscreen": "bottle",
        "Toothbrush": "each",
        "Toothpaste": "each",
    },
    "Health": {
        "Allergy Medicine": "box",
        "Antacid": "bottle",
        "Bandages": "box",
        "Cold Medicine": "bottle",
        "Cough Drops": "bag",
        "First Aid Kit": "each",
        "Fish Oil": "bottle",
        "Melatonin": "bottle",
        "Multivitamins": "bottle",
        "Pain Reliever (Acetaminophen)": "bottle",
        "Pain Reliever (Ibuprofen)": "bottle",
        "Probiotics": "bottle",
        "Vitamin C": "bottle",
        "Vitamin D": "bottle",
    },
    "International": {
        "Coconut Cream": "can",
        "Curry Paste": "jar",
        "Enchilada Sauce": "can",
        "Miso Paste": "container",
        "Mole Sauce": "jar",
        "Seaweed/Nori": "pack",
        "Taco Shells": "box",
        "Tempeh": "pack",
        "Tofu": "pack",
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
    "carton", "bottle", "cans", "jar", "container",  # containers
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

# Initialize session state - load from files if they exist (local), otherwise clean slate
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
if "confirm_reset" not in st.session_state:
    st.session_state.confirm_reset = False

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
            all_brands = get_brands_for_item(item, st.session_state.custom_brands, st.session_state.item_preferences)
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
    # Header with edit mode toggle and reset button
    col_header, col_edit, col_reset = st.columns([4, 1, 1])
    with col_header:
        st.subheader("Add Items to Shopping List")
    with col_edit:
        edit_mode = st.toggle("Edit", value=st.session_state.edit_mode, key="edit_toggle")
        if edit_mode != st.session_state.edit_mode:
            st.session_state.edit_mode = edit_mode
            st.rerun()
    with col_reset:
        if st.button("Clear Cart", help="Clear all items from shopping list"):
            st.session_state.grocery_list = []
            st.toast("Shopping list cleared")
            st.rerun()

    if st.session_state.edit_mode:
        st.caption("Edit mode: Add or remove items from your master list")
    else:
        st.caption("Click + to add items. Your saved brand preferences will be used automatically.")

    # Search box
    search_query = st.text_input("🔍 Search items", key="search_items", placeholder="Type to search...").strip().lower()

    # Get items currently in shopping list
    items_in_cart = {e["item"] for e in st.session_state.grocery_list}

    for category, base_items in MASTER_LIST.items():
        # Merge base items with custom items for this category
        items = dict(base_items)
        if category in st.session_state.custom_items:
            items.update(st.session_state.custom_items[category])

        # Filter out hidden items
        visible_items = {k: v for k, v in items.items() if k not in st.session_state.hidden_items}

        # Apply search filter
        if search_query:
            visible_items = {k: v for k, v in visible_items.items() if search_query in k.lower()}

        # Skip empty categories when searching
        if search_query and not visible_items:
            continue

        # Count items in cart (only visible ones)
        cart_count = len([i for i in visible_items if i in items_in_cart])
        is_open = st.session_state.open_category == category or bool(search_query)

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
                                st.session_state.open_category = category  # Keep expander open
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
                            if st.button("🗑", key=f"del_{category}_{item}", help=f"Remove {item}"):
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
                                st.session_state.open_category = category  # Keep expander open
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
                                if st.button(f"+ {display_text}", key=f"add_{category}_{item}", use_container_width=True):
                                    # Add to shopping list with saved preferences
                                    entry = {
                                        "item": item,
                                        "qty": 1,
                                        "unit": saved_unit,
                                        "brand": saved_brand
                                    }
                                    st.session_state.grocery_list.append(entry)
                                    st.session_state.open_category = category  # Keep expander open
                                    st.toast(f"Added {item}" + (f" ({saved_brand})" if saved_brand else ""))
                                    st.rerun()

                        with col_gear:
                            # Show gear icon for all items (set brand/unit preferences)
                            if st.button("⚙", key=f"config_{category}_{item}", help="Set preferences"):
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
            found = False
            for category, cat_items in MASTER_LIST.items():
                if item in cat_items:
                    if category not in items_by_category:
                        items_by_category[category] = []
                    items_by_category[category].append(item)
                    found = True
                    break
            if not found:
                # Check custom items
                for category, cat_items in st.session_state.custom_items.items():
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
                    else:
                        # Use general UNITS list for items without custom options
                        unit_options = UNITS
                        current_unit = prefs.get("unit", get_default_unit(item))
                        unit_idx = unit_options.index(current_unit) if current_unit in unit_options else 0

                    old_unit = current_unit
                    new_unit = st.selectbox(
                        "Unit", unit_options, index=unit_idx,
                        key=f"pref_unit_{item}", label_visibility="collapsed"
                    )
                    if new_unit != old_unit:
                        st.session_state.item_preferences[item]["unit"] = new_unit
                        save_preferences(st.session_state.item_preferences)

                with c3:
                    # Brand display/edit
                    current_brand = prefs.get("brand", "")
                    if item in ITEM_BRANDS:
                        all_brands = get_brands_for_item(item, st.session_state.custom_brands, st.session_state.item_preferences)
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
                            found_cat = False
                            for cat, cat_items in MASTER_LIST.items():
                                if item in cat_items:
                                    st.session_state.open_category = cat
                                    found_cat = True
                                    break
                            if not found_cat:
                                for cat, cat_items in st.session_state.custom_items.items():
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

    # Export/Import preferences
    st.divider()
    with st.expander("Backup & Restore Preferences", expanded=False):
        st.caption("Export your preferences to a file, or import them on another browser/device.")

        # Export
        all_data = {
            "preferences": st.session_state.item_preferences,
            "custom_brands": st.session_state.custom_brands,
            "hidden_items": list(st.session_state.hidden_items),
            "custom_items": st.session_state.custom_items,
        }
        st.download_button(
            "📤 Export Preferences",
            json.dumps(all_data, indent=2),
            file_name=f"grocery_preferences_{datetime.now(ZoneInfo('America/Chicago')).strftime('%b%d_%-I-%M%p')}.json",
            mime="application/json",
            use_container_width=True,
        )

        # Import
        uploaded = st.file_uploader(
            "📥 Import Preferences",
            type=["json"],
            key="import_prefs",
        )
        if uploaded is not None and "import_applied" not in st.session_state:
            try:
                imported = json.loads(uploaded.getvalue())
                if "preferences" in imported:
                    st.session_state.item_preferences = imported["preferences"]
                    save_preferences(imported["preferences"])
                if "custom_brands" in imported:
                    st.session_state.custom_brands = imported["custom_brands"]
                    save_custom_brands(imported["custom_brands"])
                if "hidden_items" in imported:
                    st.session_state.hidden_items = set(imported["hidden_items"])
                    save_hidden_items(st.session_state.hidden_items)
                if "custom_items" in imported:
                    st.session_state.custom_items = imported["custom_items"]
                    save_custom_items(imported["custom_items"])
                st.session_state.import_applied = True
                st.toast("Preferences imported successfully!")
                st.rerun()
            except (json.JSONDecodeError, KeyError):
                st.error("Invalid file. Please upload a valid preferences backup.")
        elif "import_applied" in st.session_state:
            st.success("Preferences loaded!")
            if st.button("Clear upload", use_container_width=True):
                del st.session_state.import_applied
                st.rerun()

    def apply_scan_import(raw_json):
        """Merge scanned product JSON into existing preferences and custom items."""
        scanned = json.loads(raw_json)
        added = []
        if "preferences" in scanned:
            for item, prefs in scanned["preferences"].items():
                if isinstance(prefs, dict) and "unit" in prefs and "brand" in prefs:
                    st.session_state.item_preferences[item] = prefs
                    added.append(item)
            save_preferences(st.session_state.item_preferences)
        if "custom_brands" in scanned:
            for group, brands in scanned["custom_brands"].items():
                existing = st.session_state.custom_brands.get(group, [])
                merged = list(dict.fromkeys(existing + brands))
                st.session_state.custom_brands[group] = merged
            save_custom_brands(st.session_state.custom_brands)
        if "custom_items" in scanned:
            master_items = {item for cat in MASTER_LIST.values() for item in cat}
            for category, items in scanned["custom_items"].items():
                if category not in st.session_state.custom_items:
                    st.session_state.custom_items[category] = {}
                for item_name, unit in items.items():
                    if item_name not in master_items:
                        st.session_state.custom_items[category][item_name] = unit
            save_custom_items(st.session_state.custom_items)
        st.toast(f"Added: {', '.join(added)}" if added else "Scan imported!")

    with st.expander("Add from Scan", expanded=False):
        st.caption("Add products from a Grocery Scanner. Paste JSON or upload a file.")
        paste_tab, file_tab = st.tabs(["Paste JSON", "Upload File"])
        with paste_tab:
            scan_text = st.text_area(
                "Paste JSON here",
                height=150,
                key="scan_paste",
                placeholder='{\n  "preferences": { ... },\n  "custom_items": { ... }\n}',
            )
            if st.button("Import", key="scan_paste_btn", use_container_width=True):
                if scan_text.strip():
                    try:
                        apply_scan_import(scan_text)
                        st.rerun()
                    except (json.JSONDecodeError, KeyError):
                        st.error("Invalid JSON. Please paste valid scan data.")
                else:
                    st.warning("Paste JSON above first.")
        with file_tab:
            scan_file = st.file_uploader(
                "Upload scan JSON",
                type=["json"],
                key="import_scan_file",
            )
            if st.button("Import File", key="scan_file_btn", use_container_width=True):
                if scan_file is not None:
                    try:
                        apply_scan_import(scan_file.getvalue())
                        st.rerun()
                    except (json.JSONDecodeError, KeyError):
                        st.error("Invalid file. Please upload a valid scan JSON.")
                else:
                    st.warning("Upload a JSON file first.")

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
            def get_item_category(item_name):
                """Find the category for an item."""
                for cat, items in MASTER_LIST.items():
                    if item_name in items:
                        return cat
                # Check custom items
                for cat, items in st.session_state.custom_items.items():
                    if item_name in items:
                        return cat
                return "Other"

            # Group items by category
            items_by_category = {}
            for e in st.session_state.grocery_list:
                cat = get_item_category(e['item'])
                if cat not in items_by_category:
                    items_by_category[cat] = []
                items_by_category[cat].append(e)

            # Build HTML export

            html_lines = []
            html_lines.append("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grocery List</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 12px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #2e7d32;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
            margin: 0;
        }
        .date {
            font-size: 14px;
            color: #666;
            margin-top: 6px;
        }
        .category {
            font-size: 16px;
            font-weight: bold;
            color: #1565c0;
            margin-top: 16px;
            margin-bottom: 8px;
            padding-bottom: 5px;
            border-bottom: 1px solid #1565c0;
        }
        .item {
            font-size: 15px;
            padding: 10px 8px;
            border-bottom: 1px solid #eee;
            display: block;
        }
        .item:has(input:checked) {
            opacity: 0.4;
            text-decoration: line-through;
        }
        input[type="checkbox"] {
            width: 26px;
            height: 26px;
            margin-right: 10px;
            vertical-align: middle;
        }
        .item-name {
            vertical-align: middle;
        }
        .footer {
            text-align: center;
            margin-top: 25px;
            padding-top: 12px;
            border-top: 2px solid #2e7d32;
            font-size: 14px;
            color: #666;
        }
        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; padding: 20px; }
            .item:hover { background-color: transparent; }
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            const countSpan = document.getElementById('item-count');
            const totalItems = checkboxes.length;

            function updateCount() {
                const checked = document.querySelectorAll('input[type="checkbox"]:checked').length;
                const remaining = totalItems - checked;
                countSpan.textContent = remaining + ' item' + (remaining !== 1 ? 's' : '') + ' remaining';
            }

            checkboxes.forEach(function(cb) {
                cb.addEventListener('change', updateCount);
            });
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">🛒 Grocery List</div>
            <div class="date">""" + datetime.now(ZoneInfo('America/Chicago')).strftime('%B %d, %Y') + """</div>
        </div>
""")

            # Sort categories to match MASTER_LIST order
            category_order = list(MASTER_LIST.keys()) + ["Other"]
            sorted_categories = sorted(items_by_category.keys(),
                key=lambda x: category_order.index(x) if x in category_order else 999)

            item_count = 0
            for cat in sorted_categories:
                items = items_by_category[cat]
                # Simplify category name
                display_cat = cat.replace("Produce - ", "").replace("Pantry - ", "").replace("Meat & Seafood - ", "")
                html_lines.append(f'        <div class="category">{display_cat}</div>')

                for e in items:
                    qty = int(e['qty']) if e['qty'] == int(e['qty']) else e['qty']
                    brand_text = f" ({e['brand']})" if e.get('brand') else ""
                    html_lines.append(f'''        <label class="item">
            <input type="checkbox"><span class="item-name">{e['item']}{brand_text} - {qty} {e['unit']}</span>
        </label>''')
                    item_count += 1

            total_items = len(st.session_state.grocery_list)
            html_lines.append(f"""
        <div class="footer">
            <span id="item-count">{total_items} item{'s' if total_items != 1 else ''} remaining</span>
        </div>
    </div>
</body>
</html>""")

            html_text = "\n".join(html_lines)
            st.download_button(
                "📥 Export List",
                html_text,
                file_name=f"grocery_list_{datetime.now(ZoneInfo('America/Chicago')).strftime('%b%d_%-I-%M%p')}.html",
                mime="text/html",
                use_container_width=True
            )
