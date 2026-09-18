from random import randint

def generar_ejercicio_triangulo():
    base = randint(5, 20)
    altura = randint(4, 15)
    area = (base * altura) / 2
    
    ejercicio = f"Un triángulo tiene una base de {base} cm y una altura de {altura} cm.\nCalcula su área."
    respuesta = f"Respuesta: El área es {area} cm²"
    
    return ejercicio, respuesta

# Generamos 5 ejercicios distintos
for i in range(5):
    ej, res = generar_ejercicio_triangulo()
    print(f"Ejercicio {i+1}:")
    print(ej)
    print(res)
    print("-" * 40)