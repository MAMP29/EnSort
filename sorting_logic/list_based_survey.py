from sorting_logic.algorithms.mergesort import merge_sort

# Implementación basada en listas-diccionarios, como es una estructura propia de python no tiene una implementación directa en datastructures
class ListBasedSurvey:
    def __init__(self):
        self.participantes = []
        self.temas_preguntas = []

    def ejecutar_proceso(self, contenido, con_archivo=False, participantes_raw=None, temas_preguntas_raw=None):
        
        self.cargar_datos(contenido, con_archivo, participantes_raw, temas_preguntas_raw)

        self.temas_preguntas = self.procesar_y_ordenar(self.temas_preguntas)

        return self.generar_salida(self.participantes, self.temas_preguntas)
        

    def cargar_datos(self, contenido, con_archivo, participantes_raw, temas_preguntas_raw):
        # Leer el archivo y separar secciones
        if con_archivo:
            with open(contenido, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
        
            # Separar secciones por doble salto de línea
            secciones = contenido.split("\n\n")

            # Procesar la lista de participantes
            participantes_raw = secciones[0].split("\n")

            self.participantes = self.cargar_participantes(participantes_raw)
            
            # Procesar preguntas y temas

            self.temas_preguntas = self.cargar_temas_preguntas(secciones[1:], self.participantes)
        
        else:
            self.participantes = self.cargar_participantes(participantes_raw)
            self.temas_preguntas = self.cargar_temas_preguntas(temas_preguntas_raw, self.participantes)

    def cargar_participantes(self, participantes_raw):
        participantes = []
        id_counter = 1  # Contador de IDs únicos

        for p in participantes_raw:
            try:
                # Parsear los datos del participante
                nombre, detalles = p.split(", Experticia:")
                opinion = int(detalles.split("Opinión:")[1].strip())
                experticia = int(detalles.split(", Opinión:")[0].strip())

                # Agregar el participante a la lista
                participantes.append({
                    "id": id_counter,
                    "nombre": nombre.strip(),
                    "experticia": experticia,
                    "opinion": opinion
                })
                id_counter += 1
            except (ValueError, IndexError) as e:
                print(f"Error al procesar el participante: {p}. Detalle: {e}")

        return participantes

    def cargar_temas_preguntas(self, temas_preguntas_raw, participantes):
        participantes_index = {p["id"]: p for p in participantes}  # Índice para búsquedas rápidas
        temas = []

        for i, preguntas_raw in enumerate(temas_preguntas_raw, start=1):
            preguntas_tema = []
            preguntas_ids = preguntas_raw.strip().split("\n")
            for j, ids in enumerate(preguntas_ids, start=1):
                ids = [int(id_) for id_ in ids.strip("{}").split(", ")]
                preguntas_tema.append({
                    "id": f"{i}.{j}",
                    "encuestados": [participantes_index[id_] for id_ in ids if id_ in participantes_index]
                })
            temas.append({
                "tema_id": i,
                "preguntas": preguntas_tema
            })

        return temas

    def calcular_promedios(self, preguntas, criterio):
        """Calcula el promedio de un criterio (opinion o experticia) para cada pregunta."""
        for pregunta in preguntas:
            total = sum(e[criterio] for e in pregunta["encuestados"])
            cantidad = len(pregunta["encuestados"])
            pregunta["promedio"] = total / cantidad if cantidad > 0 else 0    

    def ordenar_encuestados_por_pregunta(self, preguntas):
        """
        Ordena los encuestados dentro de cada pregunta en orden descendente por opinión,
        y en caso de empate, por nivel de experticia.
        """
        for pregunta in preguntas:
            pregunta["encuestados"] = merge_sort(
                pregunta["encuestados"],
                claves=["opinion", "experticia"],
                orden="desc"
            )   
        
    def procesar_y_ordenar(self, temas, criterio_orden="opinion"):

        for tema in temas:
            # Ordenar encuestados por pregunta
            self.ordenar_encuestados_por_pregunta(tema["preguntas"])
            
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

        salida.append("Resultados de la encuesta:")
        salida.append("")
        
        # Procesar temas
        for tema in temas:
            salida.append(f"[{tema['promedio']:.2f}] Tema {tema['tema_id']}:")
            
            for pregunta in tema["preguntas"]:
                ids = ", ".join(str(e["id"]) for e in pregunta["encuestados"])
                salida.append(f"  [{pregunta['promedio']:.2f}] Pregunta {pregunta['id']}: ({ids})")
            
            salida.append("")  # Línea en blanco entre temas

        # Lista de participantes ordenada
        participantes = merge_sort(participantes, claves=["experticia", "id"], orden="desc")
        salida.append("Lista de encuestados:")
        for p in participantes:
            salida.append(
                f" ({p['id']}, Nombre:'{p['nombre']}', Experticia:{p['experticia']}, Opinión:{p['opinion']})"
            )
        
        # Cálculo de promedios generales de encuestados
        num_participantes = len(participantes)
        if num_participantes > 0:
            promedio_opinion = sum(p["opinion"] for p in participantes) / num_participantes
            promedio_experticia = sum(p["experticia"] for p in participantes) / num_participantes
        else:
            promedio_opinion = promedio_experticia = 0

        # Calcular resultados extremos
        try:
            max_opinion_participante = max(participantes, key=lambda p: p["opinion"])
            min_opinion_participante = min(participantes, key=lambda p: p["opinion"])
            max_experticia_participante = max(participantes, key=lambda p: p["experticia"])
            min_experticia_participante = min(participantes, key=lambda p: p["experticia"])
        except ValueError:
            max_opinion_participante = min_opinion_participante = {}
            max_experticia_participante = min_experticia_participante = {}

        todas_preguntas = [p for tema in temas for p in tema["preguntas"]]
        if todas_preguntas:
            max_opinion_pregunta = max(todas_preguntas, key=lambda p: p["promedio"])
            min_opinion_pregunta = min(todas_preguntas, key=lambda p: p["promedio"])
            max_experticia_pregunta = max(
                todas_preguntas, key=lambda p: sum(e["experticia"] for e in p["encuestados"]) / len(p["encuestados"])
            )
            min_experticia_pregunta = min(
                todas_preguntas, key=lambda p: sum(e["experticia"] for e in p["encuestados"]) / len(p["encuestados"])
            )
        else:
            max_opinion_pregunta = min_opinion_pregunta = {}
            max_experticia_pregunta = min_experticia_pregunta = {}

        # Generación de resultados
        salida.append("\nResultados:")
        if todas_preguntas:
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
        else:
            salida.append("  No se encontraron preguntas con datos válidos.")

        if participantes:
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
        else:
            salida.append("  No se encontraron encuestados con datos válidos.")
            
        return "\n".join(salida)

    

if __name__ == '__main__':
    algo_lista = ListBasedSurvey()
    archivo_prueba = "testsfiles/entrada_prueba_3.txt"
    #participantes, temas = algo_lista.cargar_datos(archivo_prueba)

    # Ordenar preguntas y temas
    #temas_ordenados = algo_lista.procesar_y_ordenar(temas, criterio_orden="opinion")

    # Generar salida
    salida = algo_lista.ejecutar_proceso(archivo_prueba, con_archivo=True)

    print(salida)

    print("-------------------------------------")