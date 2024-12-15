from sorting_logic.datastructures.binary_tree import ArbolBinarioBusqueda
from sorting_logic.algorithms.mergesort import merge_sort

# Usa tuplas para almacenar valores internos, el recorrido si se almacena en listas
class BSTBasedSurvey():
    def __init__(self):
        self.arbol_participantes = ArbolBinarioBusqueda()
        self.arbol_temas_preguntas = ArbolBinarioBusqueda()
        #self.arbol_preguntas = ArbolBinarioBusqueda()

    def ejecutar_proceso(self, contenido, con_archivo=False, participantes_raw=None, temas_preguntas_raw=None):

        self.cargar_datos(contenido, con_archivo, participantes_raw, temas_preguntas_raw)

        return self.generar_resultados()


    def cargar_datos(self, contenido, con_archivo, participantes_raw, temas_preguntas_raw):

        if con_archivo:
            with open(contenido, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()

            secciones = contenido.split("\n\n")

            # Cargar participantes
            participantes_raw = secciones[0].split("\n")
            self.arbol_participantes = self.cargar_participantes(participantes_raw)

            # Cargar preguntas y temas
            self.arbol_temas_preguntas = self.cargar_preguntas_temas(secciones[1:])

        else:
            self.arbol_participantes = self.cargar_participantes(participantes_raw)
            self.arbol_temas_preguntas = self.cargar_preguntas_temas(temas_preguntas_raw)
        

    def cargar_participantes(self, participantes_raw):
        """Carga los participantes en un árbol binario de búsqueda."""
        bst_participantes = ArbolBinarioBusqueda()
        for idx, p in enumerate(participantes_raw, start=1):
            try:
                # Dividir la línea en nombre y detalles
                partes = p.split(", Experticia:")

                nombre = partes[0].strip()
                detalles = partes[1].split(", Opinión:")
                
                # Extraer valores de experticia y opinión
                experticia = int(detalles[0].strip())
                opinion = int(detalles[1].strip())
                
                # Insertar en el árbol usando la clave (experticia, idx, opinión)
                bst_participantes.insertar((experticia, idx, opinion), nombre)
            except ValueError:
                print(f"Error al procesar la línea: {p}. Formato incorrecto.")
        
        return bst_participantes
        
    def cargar_preguntas_temas(self, secciones):
        """Carga las preguntas y temas en un árbol binario de búsqueda basado en tuplas."""
        
        bst_temas_preguntas = ArbolBinarioBusqueda()
        tema_id = 0
        
        for tema_raw in secciones:
            tema_id += 1
            preguntas_raw = tema_raw.split("\n")
            preguntas_raw.pop(0)
            numero_preguntas_tema = len(preguntas_raw)
            
            print(preguntas_raw)

            if numero_preguntas_tema == 0:
                print(f"Advertencia: El tema {tema_id} no tiene preguntas.")
                continue
            
            # Inicializar acumuladores
            acumulador_opiniones = 0
            acumulador_experticia = 0
            
            # Crear árbol para almacenar preguntas del tema
            bst_preguntas_tema = ArbolBinarioBusqueda()
            
            for pregunta_id, pregunta in enumerate(preguntas_raw, start=1):
                try:
                    # Parsear IDs de encuestados
                    ids_encuestados = tuple(eval((pregunta.strip())))

                    # Ordenar IDs y obtener datos de participantes
                    ids_ordenados = self.merge_sort_ids(ids_encuestados, self.arbol_participantes)
                    datos_participantes = [self.arbol_participantes.buscar_clave_general(id, 1) for id in ids_ordenados]
                    
                    # Calcular promedios
                    suma_opiniones = sum(dato[2] for dato in datos_participantes)
                    suma_experticia = sum(dato[0] for dato in datos_participantes)
                    promedio_opiniones = round(suma_opiniones / len(ids_ordenados), 2)
                    promedio_experticia = round(suma_experticia / len(ids_ordenados), 2)
                    
                    # Actualizar acumuladores
                    acumulador_opiniones += promedio_opiniones
                    acumulador_experticia += promedio_experticia
                    
                    # Insertar pregunta en el árbol
                    clave_pregunta = (promedio_opiniones, promedio_experticia, len(ids_ordenados), pregunta_id)
                    bst_preguntas_tema.insertar(clave_pregunta, ids_ordenados)
                
                except Exception as e:
                    print(f"Error al procesar la pregunta '{pregunta}' en el tema {tema_id}: {e}")
            
            # Calcular promedios globales del tema
            promedio_opiniones_tema = round(acumulador_opiniones / numero_preguntas_tema, 2)
            promedio_experticia_tema = round(acumulador_experticia / numero_preguntas_tema, 2)
            
            # Insertar tema en el árbol
            clave_tema = (promedio_opiniones_tema, promedio_experticia_tema, numero_preguntas_tema, tema_id)
            bst_temas_preguntas.insertar(clave_tema, bst_preguntas_tema)

            print("-----------------------------------------------------------------------------")
            print(bst_preguntas_tema.recorrido_en_orden(descendente=True))
            print("-----------------------------------------------------------------------------")
        
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

        # Título de los resultados
        salida.append("Resultados de la encuesta")
        salida.append("")

        # Ordenar temas y preguntas
        temas_ordenados = self.obtener_temas_ordenados()

        # Construcción de la sección de temas y preguntas
        for tema_id, promedio_opinion_tema, promedio_experticia_tema, preguntas_ordenadas in temas_ordenados:
            salida.append(f"[{promedio_opinion_tema}] Tema {tema_id}:")
            for promedio_opinion_pregunta, promedio_experticia_pregunta, num_encuestados, id_pregunta, ids_encuestados in preguntas_ordenadas:
                salida.append(f"  [{promedio_opinion_pregunta}] Pregunta {tema_id}.{id_pregunta}: {ids_encuestados}")
            salida.append("")

        # Construcción de la sección de encuestados
        salida.append("Lista de encuestados:")
        encuestados_ordenados = self.arbol_participantes.recorrido_en_orden(descendente=True)
        for _, (clave, nombre) in enumerate(encuestados_ordenados, start=1):
            experticia, idp, opinion = clave
            salida.append(f" ({idp}, Nombre:'{nombre}', Experticia:{experticia}, Opinión:{opinion})")
        salida.append("")

        # Resultados adicionales
        salida.append("Resultados:")
        salida.extend(self.generar_resultados_adicionales(temas_ordenados, encuestados_ordenados))

        return "\n".join(salida)

    # Métodos auxiliares

    def obtener_temas_ordenados(self):
        """Obtiene los temas con preguntas ordenadas."""
        temas_en_orden = self.arbol_temas_preguntas.recorrido_en_orden(descendente=True)
        temas_ordenados = []
        for clave_tema, bst_preguntas_tema in temas_en_orden:
            promedio_opinion_tema, promedio_experticia_tema, _, tema_id = clave_tema
            preguntas_ordenadas = [
                (clave_pregunta[0], clave_pregunta[1], clave_pregunta[2], clave_pregunta[3], datos_pregunta)
                for clave_pregunta, datos_pregunta in bst_preguntas_tema.recorrido_en_orden(descendente=True)
            ]
            print("TEMAS", preguntas_ordenadas)
            temas_ordenados.append((tema_id, promedio_opinion_tema, promedio_experticia_tema, preguntas_ordenadas))
        return temas_ordenados

    def generar_resultados_adicionales(self, temas_ordenados, encuestados_ordenados):
        """Genera la sección de resultados adicionales."""
        resultados = []

        print("DE TEMES", temas_ordenados)
        # Preguntas con mayor y menor promedio de opinión y experticia
        preguntas = [
            (promedio_opinion_pregunta, promedio_experticia_pregunta ,tema_id, id_pregunta)
            for tema_id, _, _, preguntas_ordenadas in temas_ordenados
            for promedio_opinion_pregunta, promedio_experticia_pregunta, _, id_pregunta, _ in preguntas_ordenadas
        ]

        print("DE QUESTIONS", preguntas)

        pregunta_mayor_opinion = max(preguntas, key=lambda x: x[0])
        pregunta_menor_opinion = min(preguntas, key=lambda x: x[0])
        pregunta_mayor_experticia = max(preguntas, key=lambda x: x[1])
        pregunta_menor_experticia = min(preguntas, key=lambda x: x[1])

        print(pregunta_mayor_opinion)
        print(pregunta_menor_opinion)
        print(pregunta_mayor_experticia)
        print(pregunta_menor_experticia)

        resultados.append(f" Pregunta con mayor promedio de opinión: [{pregunta_mayor_opinion[0]}] Pregunta {pregunta_mayor_opinion[2]}.{pregunta_mayor_opinion[3]}")
        resultados.append(f" Pregunta con menor promedio de opinión: [{pregunta_menor_opinion[0]}] Pregunta {pregunta_menor_opinion[2]}.{pregunta_menor_opinion[3]}")
        resultados.append(f" Pregunta con mayor promedio de experticia: [{pregunta_mayor_experticia[1]}] Pregunta {pregunta_mayor_experticia[2]}.{pregunta_mayor_experticia[3]}")
        resultados.append(f" Pregunta con menor promedio de experticia: [{pregunta_menor_experticia[1]}] Pregunta {pregunta_menor_experticia[2]}.{pregunta_menor_experticia[3]}")

        # Encuestado con mayor y menor opinión/experticia
        formato_encuestado = lambda clave, nombre: f"({clave[1]}, Nombre:'{nombre}', Experticia:{clave[0]}, Opinión:{clave[2]})"
        encuestado_mayor_opinion = max(encuestados_ordenados, key=lambda x: x[0][2])
        encuestado_menor_opinion = min(encuestados_ordenados, key=lambda x: x[0][2])
        encuestado_mayor_experticia = max(encuestados_ordenados, key=lambda x: x[0][0])
        encuestado_menor_experticia = min(encuestados_ordenados, key=lambda x: x[0][0])

        resultados.append(f" Encuestado con mayor opinión: {formato_encuestado(encuestado_mayor_opinion[0], encuestado_mayor_opinion[1])}")
        resultados.append(f" Encuestado con menor opinión: {formato_encuestado(encuestado_menor_opinion[0], encuestado_menor_opinion[1])}")
        resultados.append(f" Encuestado con mayor experticia: {formato_encuestado(encuestado_mayor_experticia[0], encuestado_mayor_experticia[1])}")
        resultados.append(f" Encuestado con menor experticia: {formato_encuestado(encuestado_menor_experticia[0], encuestado_menor_experticia[1])}")

        # Promedios generales
        promedio_experticia_encuestados = round(sum(x[0][0] for x in encuestados_ordenados) / len(encuestados_ordenados), 2)
        promedio_opinion_encuestados = round(sum(x[0][2] for x in encuestados_ordenados) / len(encuestados_ordenados), 2)

        resultados.append(f" Promedio de experticia de los encuestados: {promedio_experticia_encuestados}")
        resultados.append(f" Promedio de opinión de los encuestados: {promedio_opinion_encuestados}")

        return resultados

        

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
