def scale_recipe(name, servings, *ingredients, unit="g", **options):

    print(f"\nRecipe: {name}")
    print(f"Servings: {servings}")
    print("Shopping List:")

    if servings < 1:
        print(f"Error - servings must be at least 1 : {name}")
        return 0

    result = {}

    for ingredient, amount in ingredients:
        scaled_amount = amount * servings
        result[ingredient] = scaled_amount
        print(f"- {ingredient}: {scaled_amount} {unit}")

    if options:
        print("Cooking Notes:")
        for key, value in options.items():
            print(f"  {key}: {value}")

    return result

print("Demo.... ")

# Simple recipe
print(scale_recipe("chocolate cake",4,("All purpose", 100),("Milk", 200),("Sugar", 20),("coco powder", 20)))

# Different unit
print(scale_recipe("Lemonade", 3,("Water", 250),("Lemon Juice", 50),unit="ml"))

# Several options
print(scale_recipe("Biryani",2,("Rice", 300),("Masala", 150),("Ghee", 100),("Onions", 100),time="60min",Style="Dum"))

# Invalid servings
print(scale_recipe("dessert",0,("Flour", 200),("Sugar", 100)))
