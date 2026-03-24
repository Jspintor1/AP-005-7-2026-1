# Creación de diccionarios básicos usando pares "clave": valor
sensors =  {"living room": 21, "kitchen": 23, "bedroom": 20, "pantry": 22}
num_cameras = {"backyard": 6,  "garage": 2, "driveway": 1}

# Imprime los diccionarios en la consola
print(sensors)
print(num_cameras)

# Diccionario con claves y valores de tipo texto (string)
translations = {"mountain": "orod", "bread": "bass", "friend": "mellon", "horse": "roch" }
print(translations)

# Error verificado: Las listas no pueden ser claves de un diccionario porque son mutables. 
# (Este código daría error si se ejecuta tal cual)
# powers = {[1, 2, 4, 8, 16]: 2, [1, 3, 9, 27, 81]: 3}

# Un diccionario puede tener listas como valores
children = {"von Trapp": ["Johannes", "Rosmarie", "Eleonore"] , "Corleone": ["Sonny", "Fredo", "Michael"]}
print(children)

# Creación de un diccionario vacío
my_empty_dictionary = {}
print(my_empty_dictionary)

# Agregar un nuevo elemento a un diccionario existente
menu = {"oatmeal": 3, "avocado toast": 6, "carrot juice": 5, "blueberry muffin": 2}
print("Before: ", menu)
menu["cheesecake"] = 8 # Se agrega la clave "cheesecake" con el valor 8
print("After", menu)

# Si defines el mismo diccionario varias veces, la última asignación sobrescribe a las anteriores
animals_in_zoo = {"dinosaurs": 0}
animals_in_zoo = {"horses": 2} # Esta línea sobrescribe el diccionario anterior
print(animals_in_zoo)

# --- Agregar múltiples claves a la vez ---
sensors = {"living room": 21, "kitchen": 23, "bedroom": 20}
print("Before", sensors)

# El método .update() permite agregar varios pares clave-valor de una sola vez
sensors.update({"pantry": 22, "guest room": 25, "patio": 34})
print("After", sensors)

user_ids = {"teraCoder": 9018293, "proProgrammer": 119238}
print(user_ids)
user_ids.update({"theLooper": 138475, "stringQueen": 85739})
print(user_ids)

# --- Sobrescribir Valores ---
menu = {"oatmeal": 3, "avocado toast": 6, "carrot juice": 5, "blueberry muffin": 2}
print("Before: ", menu)
# Al asignar un nuevo valor a una clave existente, el valor anterior se reemplaza
menu["oatmeal"] = 5 
print("After", menu)

oscar_winners = {"Best Picture": "La La Land", "Best Actor": "Casey Affleck", "Best Actress": "Emma Stone", "Animated Feature": "Zootopia"}
print("Before", oscar_winners)
print()

# Actualizando con .update() y reasignación directa
oscar_winners.update({"Supporting Actress": "Viola Davis"})
print("After1", oscar_winners)
print()
oscar_winners["Best Picture"] = "Moonlight" # Reemplaza "La La Land" por "Moonlight"
print("After2", oscar_winners)

# --- Dict Comprehensions (Comprensiones de diccionarios) ---
names = ['Jenny', 'Alexus', 'Sam', 'Grace']
heights = [61, 70, 67, 64]

# zip() une las dos listas creando pares (tuplas). La comprensión {key:value for...} lo convierte en diccionario.
students = {key:value for key, value in zip(names, heights)}
print(students)

drinks = ["espresso", "chai", "decaf", "drip"]
caffeine = [64, 40, 0, 120]

# Paso a paso: primero zip, luego la comprensión
zipped_drinks = zip(drinks, caffeine)
print(zipped_drinks) # Esto imprime el objeto iterador, no el diccionario aún
drinks_to_caffeine = {key:value for key, value in zipped_drinks}
print(drinks_to_caffeine)

# Otro ejemplo de creación y actualización
songs = ["Like a Rolling Stone", "Satisfaction", "Imagine", "What's Going On", "Respect", "Good Vibrations"]
playcounts = [78, 29, 44, 21, 89, 5]
plays = {key:value for key, value in zip(songs, playcounts)}
print(plays)

plays.update({"Purple Haze": 1}) # Agrega un nuevo elemento
plays.update({"Respect": 94}) # Actualiza un elemento existente
print("After: ", plays)

# Diccionario anidado: un diccionario como valor de otro diccionario
library = {"The Best Songs": plays, "Sunday Feelings": {}}
print(library)