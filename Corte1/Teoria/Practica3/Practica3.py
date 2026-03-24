while True:

   a = input("Porfavor ingrese un valor: ")
   aInt = int(a)
   mod = aInt%2

   if (aInt < 0):
            print("el numero no es valido")
   else:
      if(mod == 0):
         print("El numero es par")
      if (mod != 0): 
         print("El numero es impar")
      
      i= input("¿desea continuar? 0 para no y 1 para si: ")

      iInt = int(i)

      if (iInt == 0):
          break
      if (iInt == 1):
          print("continuando...")


      
