################# LISTAS ####################
# Se declaran con corchetes y permiten almacenar múltiples elementos
my_lista = ['Rojo', 'Azul', 'Amarillo', 'Naranja', 'Violeta', 'Verde']

print(my_lista)
print(type(my_lista)) # Muestra que el tipo es 'list'
print(my_lista[2])    # Accede al tercer elemento (índice 2, "Amarillo")

print("my_lista size: ", len(my_lista)) # len() devuelve la cantidad de elementos
print(my_lista[0:2]) # Slicing: Obtiene los elementos desde el índice 0 hasta el 1 (el 2 no se incluye)
print(my_lista[:2])  # Es equivalente a lo anterior

my_lista.append('Blanco') # Agrega 'Blanco' al final de la lista
print(my_lista)

my_lista.insert(3, 'Negro') # Inserta 'Negro' en la posición (índice) 3, empujando el resto a la derecha
print(my_lista)

my_lista.extend(['Marron', 'Gris']) # .extend() concatena los elementos de otra lista al final
print(my_lista)

print(my_lista.index('Azul')) # Busca 'Azul' y devuelve en qué índice se encuentra

my_lista.remove('Marron') # Busca el elemento 'Marron' y lo elimina de la lista
print(my_lista)

my_lista.insert(8, 'Marron')
print(my_lista)

print(my_lista.pop()) # Elimina y devuelve el ÚLTIMO elemento de la lista por defecto
size = len(my_lista)
print("size = ", size)

my_lista_3 = my_lista*3 # Multiplicar una lista repite sus elementos esa cantidad de veces
print("my_lista_3: ", my_lista_3)

print("Sort:")
print()
# El método .sort() ordena la lista alfabéticamente in-place (modifica la lista original)
# Nota: sort() devuelve None, por lo que 'my_listaSort' guardará 'None'
my_listaSort = my_lista.sort() 
print(my_listaSort) # Esto imprimirá None

my_NumList = [10, 9, 8, 7, 6 , 5 , 4, 3, 2, 1]
print("Ordering my_NumList: ")
my_NumList.sort() # Ordena los números de menor a mayor
print(my_NumList)

# Ordenando lista de mayor a menor pasando el argumento reverse=True
my_NumList.sort(reverse = True)
print("De menor a mayor: ", my_NumList)


################# TUPLAS ####################
# Son similares a las listas, pero inmutables (no se pueden modificar, agregar ni borrar elementos)

print("###########################")
print("############ TUPLAS #########")

# tuple() convierte una lista en una tupla (se usan paréntesis en lugar de corchetes)
my_tupla = tuple(my_lista)
print()
print("my_tuple: ", my_tupla)

# El acceso por índice funciona igual que en las listas
print(my_tupla[0])
print(my_tupla[2])

# Evaluar si un elemento está contenido en la tupla usando 'in' (Devuelve True o False)
print('Rojo' in my_tupla)
# .count() devuelve cuántas veces aparece el elemento en la tupla
print(my_tupla.count('Rojo'))

# Tupla con un solo elemento (NOTA: en Python, para que sea tupla de un elemento debe llevar coma, ej. ('Blanco',). 
# Aquí solo se está creando un string entre paréntesis)
my_tupla_unitaria = ('Blanco')
print(my_tupla_unitaria)

# Empaquetado de tupla: se pueden crear tuplas sin usar paréntesis, solo separando por comas
my_tupla = 'Gaspar', 5, 8, 1999
print(my_tupla)

# Desempaquetado de tupla: se asignan los valores de la tupla a múltiples variables en una sola línea
nombre, dia, mes, año = my_tupla
print(nombre)
print(dia)
print(mes)
print(año)

print("Nombre: ", nombre, " - Dia:", dia, " - Mes: ", mes, "- Año: ", año)

# list() permite convertir una tupla de vuelta a una lista mutable
my_lista2 = list(my_tupla)
print(my_lista2)
