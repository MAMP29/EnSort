

# Implementación basada en listas-diccionarios
class ListBasedSurvey:
    def __init__(self):
        self.questions = []

    def cargar_datos(self, archivo):
        # Leer el archivo y separar secciones
        with open(archivo, 'r') as f:
            contenido = f.read().strip()
        
        # Separar secciones por doble salto de línea
        secciones = contenido.split("\n\n")
        
        # Procesar la lista de participantes
        participantes_raw = secciones[0].split("\n")
        participantes = []
        for p in participantes_raw:
            nombre, detalles = p.split(", Experticia:")
            print(nombre)
            print(detalles)
            opinion = int(detalles.split("Opinión:")[1].strip())
            print(opinion)
            experticia = int(detalles.split(", Opinión:")[0].strip())
            print(experticia)
            participantes.append({
                "id": len(participantes) + 1,
                "nombre": nombre.strip(),
                "experticia": experticia,
                "opinion": opinion
            })
        
        # Procesar preguntas y temas
        preguntas = []
        for i, preguntas_raw in enumerate(secciones[1:], start=1):
            preguntas_tema = []
            preguntas_ids = preguntas_raw.strip().split("\n")
            for j, ids in enumerate(preguntas_ids, start=1):
                ids = [int(id_) for id_ in ids.strip("{}").split(", ")]
                preguntas_tema.append({
                    "id": f"{i}.{j}",
                    "encuestados": [p for p in participantes if p["id"] in ids]
                })
            preguntas.append({
                "tema_id": i,
                "preguntas": preguntas_tema
            })
        
        return participantes, preguntas
    
    def ordenar_encuestados(self, encuestados):
        # Ordenar encuestados por opinión (descendente), en caso de empate por id (descendente)
        return merge_sort(encuestados, ["experticia", "id"], orden='desc')

def merge_sort(lista, claves, orden='asc'):
    if len(lista) <= 1:
        return lista
    mid = len(lista) // 2
    left = merge_sort(lista[:mid], claves, orden)
    right = merge_sort(lista[mid:], claves, orden)
    
    return merge(left, right, claves, orden)

def merge(left, right, claves, orden):
    result = []
    i = j = 0
    
    # Determinar la dirección de la comparación
    comparador = (lambda a, b: a < b) if orden == 'asc' else (lambda a, b: a > b)
    
    # Comparar y combinar las dos listas en orden
    while i < len(left) and j < len(right):
        # Para cada clave en claves, comparar
        for clave in claves:
            if comparador(left[i][clave], right[j][clave]):
                result.append(left[i])
                i += 1
                break
            elif comparador(right[j][clave], left[i][clave]):
                result.append(right[j])
                j += 1
                break
        else:  # Si son iguales en todas las claves, elegir el primero
            result.append(left[i])
            i += 1

    # Añadir lo que queda en cada lista
    result.extend(left[i:])
    result.extend(right[j:])
    return result

    

if __name__ == '__main__':
    algo_lista = ListBasedSurvey()
    archivo_prueba = "testsfiles/entrada_prueba_1.txt"
    participantes, temas = algo_lista.cargar_datos(archivo_prueba)

    print(algo_lista.ordenar_encuestados(participantes))


    '''
    print(participantes)

    print("-----------------------------------------------------------------")

    print(temas)

    print("-----------------------------------------------------------------")

    # Imprimir los datos cargados
    print("Participantes:")
    for p in participantes:
        print(p)

    print("\nTemas y Preguntas:")
    for tema in temas:
        print(f"Tema {tema['tema_id']}:")
        for pregunta in tema["preguntas"]:
            print(f"  Pregunta {pregunta['id']}: {[(e['id'], e['nombre']) for e in pregunta['encuestados']]}")'''