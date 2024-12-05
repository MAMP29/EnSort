from algorithms.mergesort import merge_sort

# Implementación basada en listas-diccionarios, como es una estructura propia de python no tiene una implementación directa en datastructures
class ListBasedSurvey:
    def __init__(self):
        self.participantes = []
        self.temas_preguntas = []

    def cargar_datos(self, archivo):
        # Leer el archivo y separar secciones
        with open(archivo, 'r') as f:
            contenido = f.read().strip()
        
        # Separar secciones por doble salto de línea
        secciones = contenido.split("\n\n")
        print(secciones)
        # Procesar la lista de participantes
        participantes_raw = secciones[0].split("\n")
        print("-----------------------------------------------")
        print(participantes_raw)
        participantes = []
        for p in participantes_raw:
            nombre, detalles = p.split(", Experticia:")
            #print(nombre)
            #print(detalles)
            opinion = int(detalles.split("Opinión:")[1].strip())
            #print(opinion)
            experticia = int(detalles.split(", Opinión:")[0].strip())
            #print(experticia)
            participantes.append({
                "id": len(participantes) + 1,
                "nombre": nombre.strip(),
                "experticia": experticia,
                "opinion": opinion
            })
        
        print("-------------------------------------------")
        print(secciones[1:])
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
        
        self.participantes = participantes
        self.preguntas = preguntas
        return participantes, preguntas
    
    def calcular_promedios(self, preguntas, criterio):
        """Calcula el promedio de un criterio (opinion o experticia) para cada pregunta."""
        for pregunta in preguntas:
            total = sum(e[criterio] for e in pregunta["encuestados"])
            cantidad = len(pregunta["encuestados"])
            pregunta["promedio"] = total / cantidad if cantidad > 0 else 0    
    
    def procesar_y_ordenar(self, temas, criterio_orden="opinion"):
        """
        Ordena las preguntas dentro de cada tema por el criterio definido.
        Calcula los promedios de cada pregunta y el promedio del tema.
        """
        for tema in temas:
            # Calcular promedios por pregunta
            self.calcular_promedios(tema["preguntas"], criterio_orden)
            
            # Ordenar preguntas por el promedio calculado
            tema["preguntas"] = merge_sort(tema["preguntas"], claves=["promedio"], orden="desc")
            
            # Calcular promedio del tema
            total = sum(p["promedio"] for p in tema["preguntas"])
            cantidad = len(tema["preguntas"])
            tema["promedio"] = total / cantidad if cantidad > 0 else 0

        # Ordenar temas por el promedio calculado
        temas = merge_sort(temas, claves=["promedio"], orden="desc")
        return temas
        
    def generar_salida(self, participantes, temas):
        """Genera el formato de salida requerido."""
        salida = []
        
        # Procesar temas
        for tema in temas:
            salida.append(f"[{tema['promedio']:.2f}] Tema {tema['tema_id']}:")
            
            for pregunta in tema["preguntas"]:
                ids = ", ".join(str(e["id"]) for e in pregunta["encuestados"])
                salida.append(f"  [{pregunta['promedio']:.2f}] Pregunta {pregunta['id']}: ({ids})")
            
            salida.append("")  # Línea en blanco entre temas

        # Lista de participantes ordenada
        participantes = merge_sort(participantes, claves=["experticia", "opinion"], orden="desc")
        salida.append("Lista de encuestados:")
        for p in participantes:
            salida.append(
                f" ({p['id']}, Nombre:'{p['nombre']}', Experticia:{p['experticia']}, Opinión:{p['opinion']})"
            )
        
        # Cálculo de promedios generales de encuestados
        total_opinion = sum(p["opinion"] for p in participantes)
        total_experticia = sum(p["experticia"] for p in participantes)
        num_participantes = len(participantes)
        promedio_opinion = total_opinion / num_participantes if num_participantes > 0 else 0
        promedio_experticia = total_experticia / num_participantes if num_participantes > 0 else 0
        
        # Calcular resultados extremos
        max_opinion_participante = max(participantes, key=lambda p: p["opinion"])
        min_opinion_participante = min(participantes, key=lambda p: p["opinion"])
        max_experticia_participante = max(participantes, key=lambda p: p["experticia"])
        min_experticia_participante = min(participantes, key=lambda p: p["experticia"])

        todas_preguntas = [p for tema in temas for p in tema["preguntas"]]
        max_opinion_pregunta = max(todas_preguntas, key=lambda p: p["promedio"])
        min_opinion_pregunta = min(todas_preguntas, key=lambda p: p["promedio"])
        
        max_experticia_pregunta = max(
            todas_preguntas, key=lambda p: sum(e["experticia"] for e in p["encuestados"]) / len(p["encuestados"])
        )
        min_experticia_pregunta = min(
            todas_preguntas, key=lambda p: sum(e["experticia"] for e in p["encuestados"]) / len(p["encuestados"])
        )

        # Generación de resultados
        salida.append("\nResultados:")
        salida.append(
            f"  Pregunta con mayor promedio de opinion: [{max_opinion_pregunta['promedio']:.2f}] "
            f"Pregunta: {max_opinion_pregunta['id']}"
        )
        salida.append(
            f"  Pregunta con menor promedio de opinion: [{min_opinion_pregunta['promedio']:.2f}] "
            f"Pregunta: {min_opinion_pregunta['id']}"
        )
        salida.append(
            f"  Pregunta con mayor promedio de experticia: [{sum(e['experticia'] for e in max_experticia_pregunta['encuestados']) / len(max_experticia_pregunta['encuestados']):.2f}] "
            f"Pregunta: {max_experticia_pregunta['id']}"
        )
        salida.append(
            f"  Pregunta con menor promedio de experticia: [{sum(e['experticia'] for e in min_experticia_pregunta['encuestados']) / len(min_experticia_pregunta['encuestados']):.2f}] "
            f"Pregunta: {min_experticia_pregunta['id']}"
        )
        salida.append(
            f"  Encuestado con mayor opinion: ({max_opinion_participante['id']}, "
            f"Nombre:'{max_opinion_participante['nombre']}', "
            f"Experticia:{max_opinion_participante['experticia']}, "
            f"Opinión:{max_opinion_participante['opinion']})"
        )
        salida.append(
            f"  Encuestado con menor opinion: ({min_opinion_participante['id']}, "
            f"Nombre:'{min_opinion_participante['nombre']}', "
            f"Experticia:{min_opinion_participante['experticia']}, "
            f"Opinión:{min_opinion_participante['opinion']})"
        )
        salida.append(
            f"  Encuestado con mayor experticia: ({max_experticia_participante['id']}, "
            f"Nombre:'{max_experticia_participante['nombre']}', "
            f"Experticia:{max_experticia_participante['experticia']}, "
            f"Opinión:{max_experticia_participante['opinion']})"
        )
        salida.append(
            f"  Encuestado con menor experticia: ({min_experticia_participante['id']}, "
            f"Nombre:'{min_experticia_participante['nombre']}', "
            f"Experticia:{min_experticia_participante['experticia']}, "
            f"Opinión:{min_experticia_participante['opinion']})"
        )
        salida.append(
            f"  Promedio de experticia de los encuestados: {promedio_experticia:.2f}"
        )
        salida.append(
            f"  Promedio de opinion de los encuestados: {promedio_opinion:.2f}" 
        )
        
        return "\n".join(salida)
    

if __name__ == '__main__':
    algo_lista = ListBasedSurvey()
    archivo_prueba = "testsfiles/entrada_prueba_1.txt"
    participantes, temas = algo_lista.cargar_datos(archivo_prueba)

    # Ordenar preguntas y temas
    temas_ordenados = algo_lista.procesar_y_ordenar(temas, criterio_orden="opinion")

    # Generar salida
    salida = algo_lista.generar_salida(participantes, temas_ordenados)

    print("-------------------------------------")