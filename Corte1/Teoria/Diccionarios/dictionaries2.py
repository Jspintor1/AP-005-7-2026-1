# --- Obtener una clave ---
building_heights = {"Burj Khalifa": 828, "Shanghai Tower": 632, "Abraj Al Bait": 601, "Ping An": 599, "Lotte World Tower": 554.5, "One World Trade": 541.3}

# Se accede al valor usando el nombre de la clave entre corchetes
print(building_heights["Burj Khalifa"]) # Imprime 828
print(building_heights["Ping An"]) # Imprime 599

zodiac_elements = {"water": ["Cancer", "Scorpio", "Pisces"], "fire": ["Aries", "Leo", "Sagittarius"], "earth": ["Taurus", "Virgo", "Capricorn"], "air":["Gemini", "Libra", "Aquarius"]}
print(zodiac_elements["earth"])
print(zodiac_elements["fire"])

# --- Obtener una clave inválida ---
# print(building_heights["Landmark 81"]) # Esto arrojaría un error (KeyError) porque la clave no existe

# Forma segura 1: Comprobar si la clave existe con "in"
key_to_check = "Landmark 81"
if key_to_check in building_heights:
  print(building_heights["Landmark 81"])

zodiac_elements["energy"] = "Not a Zodiac element"
if "energy" in zodiac_elements:
  print(zodiac_elements["energy"])

# --- Obtener una clave de forma segura con .get() ---
# .get() devuelve el valor si existe, o None (u otro valor por defecto) si no existe, evitando errores
building_heights.get("Shanghai Tower") # Devuelve 632
building_heights.get("My House") # Devuelve None

user_ids = {"teraCoder": 100019, "pythonGuy": 182921, "samTheJavaMaam": 123112, "lyleLoop": 102931, "keysmithKeith": 129384}

# Validando si .get() devuelve None para asignar un valor por defecto
if user_ids.get("teraCoder") == None:
   tc_id = 1000
else: 
   tc_id = user_ids.get("teraCoder")
print(tc_id)

if user_ids.get("superStackSmash") == None:
     stack_id = 100000
print(stack_id)

# --- Eliminar una clave ---
# .pop() elimina la clave y devuelve su valor. El segundo argumento es el valor por defecto si no la encuentra.
raffle = {223842: "Teddy Bear", 872921: "Concert Tickets", 320291: "Gift Basket", 412123: "Necklace", 298787: "Pasta Maker"}
print(raffle.pop(320291, "No Prize")) # Elimina 320291 y devuelve "Gift Basket"
print(raffle)

print(raffle.pop(100000, "No Prize")) # No existe, así que devuelve "No Prize"
print(raffle)

print(raffle.pop(872921, "No Prize")) # Elimina 872921 y devuelve "Concert Tickets"
print(raffle)

# Usando .pop() en cálculos
available_items = {"health potion": 10, "cake of the cure": 5, "green elixir": 20, "strength sandwich": 25, "stamina grains": 15, "power stew": 30}
health_points = 20

health_points += available_items.pop("stamina grains", 0) # Suma 15 y lo elimina
health_points += available_items.pop("power stew", 0)     # Suma 30 y lo elimina
health_points += available_items.pop("mystic bread", 0)   # No existe, suma 0

print(available_items)
print(health_points)

# --- Obtener Todas las Claves ---
test_scores = {"Grace":[80, 72, 90], "Jeffrey":[88, 68, 81], "Sylvia":[80, 82, 84], "Pedro":[98, 96, 95], "Martin":[78, 80, 78], "Dina":[64, 60, 75]}

# Imprime todas las claves en forma de lista
print(list(test_scores))

# Itera sobre las claves usando .keys()
for student in test_scores.keys():
 print(student)

user_ids = {"teraCoder": 100019, "pythonGuy": 182921, "samTheJavaMaam": 123112, "lyleLoop": 102931, "keysmithKeith": 129384}
num_exercises = {"functions": 10, "syntax": 13, "control flow": 15, "loops": 22, "lists": 19, "classes": 18, "dictionaries": 18}

users = user_ids.keys()
lessons = num_exercises.keys()

print(users)
print(lessons)

# --- Obtener Todos los Valores ---
# Itera solo sobre los valores del diccionario usando .values()
for score_list in test_scores.values():
 print(score_list)

total_exercises = 0
for exercises in num_exercises.values():
  total_exercises += exercises # Suma todos los valores
print(total_exercises)

# --- Obtener Todos los Items (Clave y Valor simultáneamente) ---
biggest_brands = {"Apple": 184, "Google": 141.7, "Microsoft": 80, "Coca-Cola": 69.7, "Amazon": 64.8}

# .items() permite desempaquetar la clave y el valor en variables separadas dentro del bucle
for company, value in biggest_brands.items():
 print(company + " has a value of " + str(value) + " billion dollars. ")

pct_women_in_occupation = {"CEO": 28, "Engineering Manager": 9, "Pharmacist": 58, "Physician": 40, "Lawyer": 37, "Aerospace Engineer": 9}

for occupation, percentage in pct_women_in_occupation.items():
  print("Women make up " + str(percentage) + " percent of " + occupation + "s.")