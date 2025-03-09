
import json
import sqlite3
import pandas as pd
import os


conn = sqlite3.connect('nutrition.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS food_nutrition (
    id INTEGER PRIMARY KEY,
    food_name TEXT,
    category TEXT,
    serving_size TEXT,
    calories REAL,
    protein REAL,
    fat REAL,
    carbohydrate REAL
)
''')
conn.commit()


food_categories = [
    {"category": "apple_pie", "search_term": "apple pie"},
    {"category": "pizza", "search_term": "pizza"},
    {"category": "hamburger", "search_term": "hamburger"},
    {"category": "chicken_curry", "search_term": "chicken curry"},
    {"category": "sushi", "search_term": "sushi"},
]

food_nutrition_mapping = {}

df_cols = pd.read_sql("SELECT * FROM food_nutrition LIMIT 1", conn)
columns = df_cols.columns.tolist()

print(f"Database columns: {columns}")


food_name_col = next((col for col in columns if col.lower() in 
                      ['food_name', 'name', 'description', 'item']), columns[0])


nutrient_cols = [col for col in columns if col.lower() not in 
                ['id', 'food_id', food_name_col.lower(), 'category', 'serving_size']]

print(f"Using '{food_name_col}' as the food name column")
print(f"Identified {len(nutrient_cols)} potential nutrient columns")

for item in food_categories:
    category = item["category"]
    search_term = item["search_term"]

    query = f"""
    SELECT * FROM food_nutrition 
    WHERE "{food_name_col}" LIKE ? 
    LIMIT 1
    """
    
    df_result = pd.read_sql_query(query, conn, params=('%' + search_term + '%',))
    
    if not df_result.empty:
        row = df_result.iloc[0]
        
       
        nutrients = []
        for nutrient_col in nutrient_cols:
            if pd.notna(row[nutrient_col]):
                nutrients.append({
                    "nutrient_name": nutrient_col,
                    "amount": float(row[nutrient_col]),
                    "unit": "g" 
                    if "carb" in nutrient_col.lower() 
                    or 
                    "protein" in nutrient_col.lower() 
                    or 
                    "fat" in nutrient_col.lower() 
                    else "kcal" 
                    if "calorie" in nutrient_col.lower() else ""
                })
        
 
        food_nutrition_mapping[category] = {
            "food_name": row[food_name_col],
            "nutrition": nutrients
        }
        
        print(f"Mapped '{category}' to '{row[food_name_col]}' with {len(nutrients)} nutrients")
    else:
        print(f"No match found for {category} ({search_term})")


with open('../food_nutrition_mapping.json', 'w') as f:
    json.dump(food_nutrition_mapping, f, indent=4)

print(f"\nCreated mapping for {len(food_nutrition_mapping)} food categories")
print(f"Mapping saved to '../food_nutrition_mapping.json'")
conn.close()