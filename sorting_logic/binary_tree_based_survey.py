from sorting_logic.datastructures.binary_tree import ArbolBinarioBusqueda
from sorting_logic.algorithms.mergesort import merge_sort

# Usa tuplas para almacenar valores internos, el recorrido si se almacena en listas
class BSTBasedSurvey():
    def __init__(self):
        self.arbol_participantes = ArbolBinarioBusqueda()
        self.arbol_temas_preguntas = ArbolBinarioBusqueda()
        #self.arbol_preguntas = ArbolBinarioBusqueda()

    def ejecutar_proceso(self, contenido, con_archivo=False):

        self.cargar_datos(contenido, con_archivo)

        return self.generar_resultados()


    def cargar_datos(self, contenido, con_archivo):

        if con_archivo:
            with open(contenido, 'r') as f:
                contenido = f.read().strip()

        secciones = contenido.split("\n\n")

         # Cargar participantes
        participantes_raw = secciones[0].split("\n")
        self.arbol_participantes = self.cargar_participantes(participantes_raw)

        # Cargar preguntas y temas
        self.arbol_temas_preguntas = self.cargar_preguntas_temas(secciones[1:])

    def cargar_participantes(self, participantes_raw):
        """Carga los participantes en un árbol binario de búsqueda."""
        bst_participantes = ArbolBinarioBusqueda()
        for idx, p in enumerate(participantes_raw, start=1):
            try:
                # Parsear los datos del participante
                nombre, detalles = p.split(", Experticia:")
                opinion = int(detalles.split("Opinión:")[1].strip())
                experticia = int(detalles.split(", Opinión:")[0].strip())
                
                # Crear el diccionario del participante
                participante = nombre.strip()
                
                
                # Insertar en el árbol, usando una clave como tupla, esta ordenada por experticia, en caso de empate se considera el id
                bst_participantes.insertar((experticia, idx, opinion), participante)
            except ValueError:
                print(f"Error al procesar la línea: {p}. Formato incorrecto.")
        
        return bst_participantes
        
    def cargar_preguntas_temas(self, secciones):
        """Carga las preguntas y temas en un árbol binario de búsqueda basado en tuplas"""
        
        bst_temas_preguntas = ArbolBinarioBusqueda()
        tema_id = 0
        
        for tema_raw in secciones:
            tema_id += 1
            preguntas_raw = tema_raw.split("\n")
            preguntas_raw.pop(0)
            numero_preguntas_tema = len(preguntas_raw)
            
            preguntas_opiniones_promedio_acumm = 0
            preguntas_experticia_promedio_acumm = 0
            
            bst_preguntas_tema = ArbolBinarioBusqueda()
            
            for pregunta_id, pregunta in enumerate(preguntas_raw, start=1):
                try:
                    ids_encuestados = tuple(eval(pregunta.strip()))
                    ids_ordenados = self.merge_sort_ids(ids_encuestados, self.arbol_participantes)
                    
                    suma_opiniones = sum(self.arbol_participantes.buscar_clave_general(id, 1)[2] for id in ids_ordenados)
                    suma_experticia = sum(self.arbol_participantes.buscar_clave_general(id, 1)[0] for id in ids_ordenados)
                    
                    promedio_opiniones = round(suma_opiniones / len(ids_ordenados), 2)
                    promedio_experticia = round(suma_experticia / len(ids_ordenados), 2)
                    
                    preguntas_opiniones_promedio_acumm += promedio_opiniones
                    preguntas_experticia_promedio_acumm += promedio_experticia
                    
                    # Clave de pregunta: (promedio_experticia, num_encuestados, promedio_opinión)
                    clave_pregunta = (promedio_experticia, len(ids_ordenados), promedio_opiniones)
                    
                    # Dato de pregunta: tupla de IDs de encuestados
                    dato_pregunta = ids_ordenados
                    
                    bst_preguntas_tema.insertar(clave_pregunta, dato_pregunta)
                    
                except Exception as e:
                    print(f"Error al procesar la pregunta: {pregunta}. {e}")
            
            # Calcular promedios globales del tema
            promedio_opiniones_tema = round(preguntas_opiniones_promedio_acumm / numero_preguntas_tema, 2)
            promedio_experticia_tema = round(preguntas_experticia_promedio_acumm / numero_preguntas_tema, 2)
            
            # Clave de tema: (opinión_tema, experticia_tema, num_preguntas, tema_id)
            clave_tema = (promedio_opiniones_tema, promedio_experticia_tema, numero_preguntas_tema, tema_id)

            
            # Dato de tema: árbol de preguntas
            bst_temas_preguntas.insertar(clave_tema, bst_preguntas_tema)



        print("-------------------------------ÚLTIMO ARBOL DE PREGUNTAS-------------------------")
        print(bst_preguntas_tema.recorrido_en_orden()) # EL primero es la clave, el segundo la lista de encuestados
        print("--------------------------------------------------------------------------")
        return bst_temas_preguntas

            
    def merge_sort_ids(self, ids_encuestados, arbol):
        # Convertir los IDs a una lista de diccionarios con la información del árbol
        datos = []
        for id in ids_encuestados:
            clave = arbol.buscar_clave_general(id, 1)
            if clave:
                datos.append({
                    'id': id,
                    'opinion': clave[2],
                    'experticia': clave[0]
                })
        
        # Definir las claves para ordenamiento
        claves = ['opinion', 'experticia']
        
        # Ordenar de forma descendente
        datos_ordenados = merge_sort(datos, claves, orden='desc')
        
        # Extraer los IDs ordenados
        return tuple([dato['id'] for dato in datos_ordenados])

    def generar_resultados(self):
            """Genera la salida de los resultados en el formato deseado."""
            salida = []

            # Recorrido de temas
            salida.append("Resultados de la encuesta")
            salida.append("")
            temas_en_orden = self.arbol_temas_preguntas.recorrido_en_orden(descendente=True)
            for idx, (clave_tema, bst_preguntas_tema) in enumerate(temas_en_orden, start=1):
                promedio_opinion_tema, promedio_experticia_tema, _, tema_id = clave_tema
                salida.append(f"[{promedio_opinion_tema}] Tema {tema_id}:")
                preguntas_en_orden = bst_preguntas_tema.recorrido_en_orden(descendente=True)
                for idx_pregunta, (clave_pregunta, ids_encuestados) in enumerate(preguntas_en_orden, start=1):
                    promedio_experticia_pregunta, num_encuestados, promedio_opinion_pregunta = clave_pregunta
                    salida.append(f"  [{promedio_opinion_pregunta}] Pregunta {tema_id}.{idx_pregunta}: {ids_encuestados}")

                salida.append("")  # Salto de línea entre temas

            # Lista de encuestados
            salida.append("Lista de encuestados:")
            participantes_en_orden = self.arbol_participantes.recorrido_en_orden(descendente=True)
            for idx, (clave_participante, nombre) in enumerate(participantes_en_orden, start=1):
                experticia, idp, opinion = clave_participante
                salida.append(f" ({idp}, Nombre:'{nombre}', Experticia:{experticia}, Opinión:{opinion})")
            salida.append("")

            # Resultados adicionales
            salida.append("Resultados:")

            # Pregunta con mayor y menor promedio de opinión/experticia
            preguntas = [
                (clave_pregunta, tema_id, idx_pregunta)
                for _, bst_preguntas_tema in temas_en_orden
                for idx_pregunta, (clave_pregunta, _) in enumerate(bst_preguntas_tema.recorrido_en_orden(), start=1)
            ]
            pregunta_mayor_opinion = max(preguntas, key=lambda x: x[0][2])
            pregunta_menor_opinion = min(preguntas, key=lambda x: x[0][2])
            pregunta_mayor_experticia = max(preguntas, key=lambda x: x[0][0])
            pregunta_menor_experticia = min(preguntas, key=lambda x: x[0][0])

            salida.append(f" Pregunta con mayor promedio de opinión: [{pregunta_mayor_opinion[0][2]}] Pregunta {pregunta_mayor_opinion[1]}.{pregunta_mayor_opinion[2]}")
            salida.append(f" Pregunta con menor promedio de opinión: [{pregunta_menor_opinion[0][2]}] Pregunta {pregunta_menor_opinion[1]}.{pregunta_menor_opinion[2]}")
            salida.append(f" Pregunta con mayor promedio de experticia: [{pregunta_mayor_experticia[0][0]}] Pregunta {pregunta_mayor_experticia[1]}.{pregunta_mayor_experticia[2]}")
            salida.append(f" Pregunta con menor promedio de experticia: [{pregunta_menor_experticia[0][0]}] Pregunta {pregunta_menor_experticia[1]}.{pregunta_menor_experticia[2]}")

            # Encuestado con mayor y menor opinión/experticia
            encuestado_mayor_opinion = max(participantes_en_orden, key=lambda x: x[0][2])
            encuestado_menor_opinion = min(participantes_en_orden, key=lambda x: x[0][2])
            encuestado_mayor_experticia = max(participantes_en_orden, key=lambda x: x[0][0])
            encuestado_menor_experticia = min(participantes_en_orden, key=lambda x: x[0][0])

            # Formatear encuestados en el formato solicitado con la ID real
            formato_encuestado = lambda clave, nombre: f"({clave[1]}, Nombre:'{nombre}', Experticia:{clave[0]}, Opinión:{clave[2]})"

            salida.append(f" Encuestado con mayor opinión: {formato_encuestado(encuestado_mayor_opinion[0], encuestado_mayor_opinion[1])}")
            salida.append(f" Encuestado con menor opinión: {formato_encuestado(encuestado_menor_opinion[0], encuestado_menor_opinion[1])}")
            salida.append(f" Encuestado con mayor experticia: {formato_encuestado(encuestado_mayor_experticia[0], encuestado_mayor_experticia[1])}")
            salida.append(f" Encuestado con menor experticia: {formato_encuestado(encuestado_menor_experticia[0], encuestado_menor_experticia[1])}")

            # Promedios generales
            promedio_experticia_encuestados = round(sum(x[0][0] for x in participantes_en_orden) / len(participantes_en_orden), 2)
            promedio_opinion_encuestados = round(sum(x[0][2] for x in participantes_en_orden) / len(participantes_en_orden), 2)

            salida.append(f" Promedio de experticia de los encuestados: {promedio_experticia_encuestados}")
            salida.append(f" Promedio de opinión de los encuestados: {promedio_opinion_encuestados}")

            return "\n".join(salida)
        

if __name__ == "__main__":
    algo_arbol = BSTBasedSurvey()
    archivo_prueba = "testsfiles/entrada_prueba_1.txt"
    
    '''
    algo_arbol.cargar_datos(archivo_prueba)
    #print("----------------------------------------------------")
    resultado_participantes = algo_arbol.arbol_participantes.recorrido_en_orden(descendente=True)
    print(resultado_participantes)

    print("----------------------------------------------------")
    resultado_temas = algo_arbol.arbol_temas_preguntas.recorrido_en_orden()
    print(resultado_temas)

    print("----------------------------------------------------")
    arbol_preguntas = algo_arbol.arbol_temas_preguntas.buscar_por_valor_en_clave(1, 3)
    print(arbol_preguntas.recorrido_en_orden())

    resultado = algo_arbol.generar_resultados()
    
    print("----------------------------------------------------")
    print(resultado)
    '''

    resultado_completo = algo_arbol.ejecutar_proceso(archivo_prueba, con_archivo=True)
    print(resultado_completo)
