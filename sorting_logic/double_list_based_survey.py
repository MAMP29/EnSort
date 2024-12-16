from sorting_logic.datastructures.doublyl_linked_list.ls_encuestados import ListaEncuestados
from sorting_logic.datastructures.doublyl_linked_list.ls_preguntas import ListaPreguntas
from sorting_logic.datastructures.doublyl_linked_list.ls_temas import ListaTemas

#from datastructures.doublyl_linked_list.ls_encuestados import ListaEncuestados
#from datastructures.doublyl_linked_list.ls_preguntas import ListaPreguntas
#from datastructures.doublyl_linked_list.ls_temas import ListaTemas

class DoubleListBasedSurvey:
    def __init__(self):
        self.participantes = ListaEncuestados()
        self.preguntas = ListaPreguntas()
        self.temas = ListaTemas()

    def ejecutar_proceso(self, contenido, con_archivo=False, participantes_raw=None, temas_preguntas_raw=None):

        self.cargar_datos(contenido, con_archivo, participantes_raw, temas_preguntas_raw)

        self.participantes, self.temas = self.ordenar_encuestados_temas_preguntas()

        return self.generar_resultados()

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

            self.temas = self.cargar_temas_preguntas(secciones[1:], self.participantes)
        
        else:
            #print("lOS TEMAS RAW QUE ME LLEGAN: \n", temas_preguntas_raw)
            self.participantes = self.cargar_participantes(participantes_raw)
            self.temas = self.cargar_temas_preguntas(temas_preguntas_raw, self.participantes)

    
    def cargar_participantes(self, participantes_raw):
        participantes = ListaEncuestados()

        for idx, p in enumerate(participantes_raw, start=1):
            try:
                # Dividir la línea en nombre y detalles
                nombre, detalles = p.split(", Experticia:")
                opinion = int(detalles.split("Opinión:")[1].strip())
                experticia = int(detalles.split(", Opinión:")[0].strip())
            
                participantes.insertar(opinion, idx, experticia, nombre)

            except (ValueError, IndexError) as e:
                print(f"Error al procesar el participante: {p}. Detalle: {e}")

        return participantes
            
    def cargar_temas_preguntas(self, temas_preguntas_raw, participantes):
        # Crear listas para preguntas y temas
        temas = ListaTemas()

        for idx, tp in enumerate(temas_preguntas_raw, start=1):
            # Dividir la línea en tema y pregunta
            preguntas_raw = tp.strip().split("\n")
            tema_actual = ListaPreguntas()

            for idx_preguntas, p in enumerate(preguntas_raw, start=1):
                try:
                    # Dividir la pregunta en texto y respuesta
                    ids_encuestados = [int(id.strip()) for id in p.strip("{} ").split(",")]
                    pregunta_actual = ListaEncuestados()

                    for id_encuestado in ids_encuestados:
                        # Buscar el participante en la lista de participantes
                        nodo_participante = participantes.buscar_por_id(id_encuestado)
                        if nodo_participante:
                            pregunta_actual.insertar(
                                nodo_participante.valor_opinion,
                                nodo_participante.id,
                                nodo_participante.nivel_experticia,
                                nodo_participante.nombre
                            )

                    #pregunta_actual.imprimir_derecha_a_izquierda()

                    #Añadir la pregunta procesada al tema
                    tema_actual.insertar(idx_preguntas, pregunta_actual)

                except ValueError as e:
                    print(f"Error al procesar la pregunta: {p}. Detalle: {e}")

            # Añadir el tema procesado a la listas de temas

            #tema_actual.imprimir_izquierda_a_derecha()          
            temas.insertar(idx, tema_actual)
        #temas.imprimir_temas()
        return temas

    def ordenar_encuestados_temas_preguntas(self):
        resultado_encuestados = self.participantes.merge_sort()
        resultado_temas = self.temas.merge_sort()
        resultado_temas.ordenar_todos_las_preguntas()


        print("Resultados temas")
        resultado_temas.imprimir_temas()

        return resultado_encuestados, resultado_temas
        #resultado.imprimir_izquierda_a_derecha()

    def generar_resultados(self):
    
        salida = []

        salida.append("Resultado de la encuesta:")
        salida.append("")

        # Temas
        for tema_idx, tema in enumerate(self.temas.iterar_temas(), start=1):
            promedio_opinion_tema = tema.calcular_promedio_opinion_total()
            salida.append(f"[{promedio_opinion_tema:.2f}] Tema {tema.id_tema}:")


            for pregunta_idx, pregunta in enumerate(tema.preguntas.iterar_preguntas(), start=1):
                promedio_opinion_pregunta = pregunta.calcular_promedio_opinion()

                # Obtener IDs de encuestados
                ids_encuestados = [str(encuestado.id) for encuestado in pregunta.encuestados.iterar_encuestados()]

                salida.append(f" [{promedio_opinion_pregunta:.2f}] Pregunta {tema.id_tema}.{pregunta.id_pregunta}: ({', '.join(ids_encuestados)})")
            
            salida.append("")

        # Lista de encuestados global
        salida.append("\nLista encuestados:")
        salida.extend(self.participantes.imprimir_descendentemente_gen())

        # Resultados adicionales
        salida.append("\nResultados:")

        # Preguntas con mayor y menor promedio de opinión y experticia
        mayor_opinion_pregunta, id_tema, id_pregunta = self.temas.obtener_extremo(criterio="opinion", mayor=True)
        salida.append(f"  Pregunta con mayor promedio de opinion: [{mayor_opinion_pregunta:.2f}] Pregunta: {id_tema}.{id_pregunta}")

        menor_opinion_pregunta, id_tema, id_pregunta = self.temas.obtener_extremo(criterio="opinion", mayor=False)
        salida.append(f"  Pregunta con menor promedio de opinion: [{menor_opinion_pregunta:.2f}] Pregunta: {id_tema}.{id_pregunta}")

        mayor_experticia_pregunta, id_tema, id_pregunta = self.temas.obtener_extremo(criterio="experticia", mayor=True)
        salida.append(f"  Pregunta con mayor promedio de experticia: [{mayor_experticia_pregunta:.2f}] Pregunta: {id_tema}.{id_pregunta}")

        menor_experticia_pregunta, id_tema, id_pregunta = self.temas.obtener_extremo(criterio="experticia", mayor=False)
        salida.append(f"  Pregunta con menor promedio de experticia: [{menor_experticia_pregunta:.2f}] Pregunta: {id_tema}.{id_pregunta}")

        # Encuestados con mayor y menor opinión y experticia
        mayor_opinion_encuestado = self.participantes.obtener_extremo(criterio="opinion", mayor=True)
        menor_opinion_encuestado = self.participantes.obtener_extremo(criterio="opinion", mayor=False)
        mayor_experticia_encuestado = self.participantes.obtener_extremo(criterio="experticia", mayor=True)
        menor_experticia_encuestado = self.participantes.obtener_extremo(criterio="experticia", mayor=False)

        salida.append(f"  Encuestado con mayor opinion: ({mayor_opinion_encuestado.id}, Nombre:'{mayor_opinion_encuestado.nombre}', Experticia:{mayor_opinion_encuestado.nivel_experticia}, Opinión:{mayor_opinion_encuestado.valor_opinion})")
        salida.append(f"  Encuestado con menor opinion: ({menor_opinion_encuestado.id}, Nombre:'{menor_opinion_encuestado.nombre}', Experticia:{menor_opinion_encuestado.nivel_experticia}, Opinión:{menor_opinion_encuestado.valor_opinion})")
        salida.append(f"  Encuestado con mayor experticia: ({mayor_experticia_encuestado.id}, Nombre:'{mayor_experticia_encuestado.nombre}', Experticia:{mayor_experticia_encuestado.nivel_experticia}, Opinión:{mayor_experticia_encuestado.valor_opinion})")
        salida.append(f"  Encuestado con menor experticia: ({menor_experticia_encuestado.id}, Nombre:'{menor_experticia_encuestado.nombre}', Experticia:{menor_experticia_encuestado.nivel_experticia}, Opinión:{menor_experticia_encuestado.valor_opinion})")

        # Promedios generales
        promedio_experticia = self.participantes.calcular_promedio_experticia()
        promedio_opinion = self.participantes.calcular_promedio_opinion()

        salida.append(f"  Promedio de experticia de los encuestados: {promedio_experticia:.2f}")
        salida.append(f"  Promedio de opinion de los encuestados: {promedio_opinion:.2f}")

        return "\n".join(salida)


if __name__ == '__main__':
    algo_lista = DoubleListBasedSurvey()
    archivo_prueba = "testsfiles/entrada_prueba_1.txt"
    #participantes, temas = algo_lista.cargar_datos(archivo_prueba)

    # Ordenar preguntas y temas
    #temas_ordenados = algo_lista.procesar_y_ordenar(temas, criterio_orden="opinion")

    # Generar salida
    salida = algo_lista.ejecutar_proceso(archivo_prueba, con_archivo=True)

    print(salida)

    print("-------------------------------------")