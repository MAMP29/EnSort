from datastructures.binary_tree import ArbolBinarioBusqueda

# Usa sets, tuplas y diccionarios, además de listas
class BSTBasedSurvey():
    def __init__(self):
        self.arbol_participantes = ArbolBinarioBusqueda()
        self.arbol_temas_preguntas = ArbolBinarioBusqueda()

    def cargar_datos(self, archivo):

        with open(archivo, 'r') as f:
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
                participante = {
                    "nombre": nombre.strip(),
                    "experticia": experticia,
                    "opinion": opinion
                }
                
                # Insertar en el árbol, usando una clave compuesta
                bst_participantes.insertar(idx, participante)
            except ValueError:
                print(f"Error al procesar la línea: {p}. Formato incorrecto.")
        
        return bst_participantes
        
    def cargar_preguntas_temas(self, secciones):
        """Carga las preguntas y temas en un árbol binario de búsqueda"""
        bst_temas_preguntas = ArbolBinarioBusqueda()
        tema_id = 0

        for tema_raw in secciones:
            tema_id += 1
            preguntas_raw = tema_raw.split("\n")
            preguntas_raw.pop(0)
            numero_preguntas_tema = len(preguntas_raw)

            preguntas_opiniones_promedio_acumm = 0
            preguntas_experticia_promedio_acumm = 0
            preguntas_tema = {}

            for pregunta_id, pregunta in enumerate(preguntas_raw, start=1):
                try:
                    ids_encuestados = tuple(eval(pregunta.strip()))  # Convertir "{1, 2}"
                    suma_opiniones = sum(self.arbol_participantes.buscar(id)["opinion"] for id in ids_encuestados)
                    suma_experticia = sum(self.arbol_participantes.buscar(id)["experticia"] for id in ids_encuestados)

                    promedio_opiniones = round(suma_opiniones / len(ids_encuestados), 2)
                    promedio_experticia = round(suma_experticia / len(ids_encuestados), 2)

                    preguntas_opiniones_promedio_acumm += promedio_opiniones
                    preguntas_experticia_promedio_acumm += promedio_experticia

                    # Almacenar solo información relevante para la pregunta
                    elementos_pregunta = {
                        "ids_encuestados": ids_encuestados,
                        "promedio_opinion_pregunta": promedio_opiniones,
                        "promedio_experticia_pregunta": promedio_experticia,
                    }
                    preguntas_tema[f"{tema_id}.{pregunta_id}"] = elementos_pregunta
                except Exception as e:
                    print(f"Error al procesar la pregunta: {pregunta}. {e}")

            # Al finalizar el tema, calcular los promedios globales
            promedio_opiniones_tema = round(preguntas_opiniones_promedio_acumm / numero_preguntas_tema, 2)
            promedio_experticia_tema = round(preguntas_experticia_promedio_acumm / numero_preguntas_tema, 2)

            # Crear un nodo para el tema que contiene sus promedios y preguntas
            nodo_tema = {
                "promedio_tema_opinion": promedio_opiniones_tema,
                "promedio_tema_experticia": promedio_experticia_tema,
                "preguntas": preguntas_tema,
            }

            bst_temas_preguntas.insertar(tema_id, nodo_tema)

        return bst_temas_preguntas



    def generar_salida(self):
        salida = []

        temas = self.arbol_temas_preguntas.recorrido_en_orden()
        participantes = self.arbol_participantes.recorrido_en_orden(descendente=True)

        for tema in temas:
            print(tema)
            print()
            t = tema[1]
            salida.append(f"[{t['promedio_tema_opinion']:.2f}] Tema {tema[0]}:")

            for clave, pregunta in t["preguntas"].items():  # Aquí usamos .items() para obtener clave y valor
                print(pregunta)
                # Ahora puedes usar la clave dentro de la cadena
                salida.append(f"  [{pregunta['promedio_opinion_pregunta']:.2f}] Pregunta {clave}: {pregunta['ids_encuestados']}")

        return "\n".join(salida)
        
        
        #print(temas)
        '''
        # Listar participantes ordenados
        salida.append("Participantes ordenados (por experticia, luego opinión):")
        participantes_ordenados = self.arbol_participantes.recorrido_en_orden()
        print("----------------------------------------------------")
        #print(participantes_ordenados[1][1])
        for idx, participante in enumerate(participantes_ordenados, start=1):

            print(participante)
            p = participante[1]
            salida.append(f"({idx}, Nombre: {p['nombre']}, Experticia: {p['experticia']}, Opinión: {p['opinion']})")
        salida.append("")  # Línea en blanco

        # Detallar temas y preguntas
        temas = self.arbol_temas_preguntas.recorrido_en_orden()
        print("----------------------------------------------------")
        print(temas)
        for tema_idx, tema in enumerate(temas, start=1):
            tema_clave = tema[0]  # La clave del tema, por ejemplo, 'Tema 1'
            tema_datos = tema[1]  # Los datos del tema (diccionario)

            # Promedios del tema
            promedio_opinion_tema = tema_datos['promedio_opinion']
            promedio_experticia_tema = tema_datos['promedio_experticia']

            salida.append(f"[{promedio_opinion_tema:.2f}] {tema_clave}:")
            
            # Procesar preguntas dentro del tema
            for pregunta in tema_datos['preguntas']:
                pregunta_clave = pregunta['clave']
                ids_encuestados = ", ".join(map(str, sorted(pregunta['ids_encuestados'])))
                promedio_opinion_pregunta = pregunta['promedio_opinion']
                promedio_experticia_pregunta = pregunta['promedio_experticia']

                salida.append(
                    f"   [{promedio_opinion_pregunta:.2f}] {pregunta_clave}: ({ids_encuestados})"
                )
            salida.append("")  # Línea en blanco entre temas

        # Resultados adicionales
        salida.append("Resultados:")

        # Pregunta con mayor y menor promedio de opinión
        pregunta_mayor_opinion = max(
            [(tema[0], pregunta) for tema in temas for pregunta in tema[1]['preguntas']],
            key=lambda x: x[1]['promedio_opinion']
        )
        pregunta_menor_opinion = min(
            [(tema[0], pregunta) for tema in temas for pregunta in tema[1]['preguntas']],
            key=lambda x: x[1]['promedio_opinion']
        )

        salida.append(
            f"  Pregunta con mayor promedio de opinión: [{pregunta_mayor_opinion[1]['promedio_opinion']:.2f}] "
            f"Pregunta: {pregunta_mayor_opinion[1]['clave']}"
        )
        salida.append(
            f"  Pregunta con menor promedio de opinión: [{pregunta_menor_opinion[1]['promedio_opinion']:.2f}] "
            f"Pregunta: {pregunta_menor_opinion[1]['clave']}"
        )

        # Pregunta con mayor y menor promedio de experticia
        pregunta_mayor_experticia = max(
            [(tema[0], pregunta) for tema in temas for pregunta in tema[1]['preguntas']],
            key=lambda x: x[1]['promedio_experticia']
        )
        pregunta_menor_experticia = min(
            [(tema[0], pregunta) for tema in temas for pregunta in tema[1]['preguntas']],
            key=lambda x: x[1]['promedio_experticia']
        )

        salida.append(
            f"  Pregunta con mayor promedio de experticia: [{pregunta_mayor_experticia[1]['promedio_experticia']:.2f}] "
            f"Pregunta: {pregunta_mayor_experticia[1]['clave']}"
        )
        salida.append(
            f"  Pregunta con menor promedio de experticia: [{pregunta_menor_experticia[1]['promedio_experticia']:.2f}] "
            f"Pregunta: {pregunta_menor_experticia[1]['clave']}"
        )

        # Encuestado con mayor y menor opinión
        encuestado_mayor_opinion = max(participantes_ordenados, key=lambda x: x[0][1])
        encuestado_menor_opinion = min(participantes_ordenados, key=lambda x: x[0][1])

        salida.append(
            f"  Encuestado con mayor opinión: ({encuestado_mayor_opinion[0][2]}, "
            f"Nombre:'{encuestado_mayor_opinion[1]['nombre']}', "
            f"Experticia:{encuestado_mayor_opinion[1]['experticia']}, "
            f"Opinión:{encuestado_mayor_opinion[1]['opinion']})"
        )
        salida.append(
            f"  Encuestado con menor opinión: ({encuestado_menor_opinion[0][2]}, "
            f"Nombre:'{encuestado_menor_opinion[1]['nombre']}', "
            f"Experticia:{encuestado_menor_opinion[1]['experticia']}, "
            f"Opinión:{encuestado_menor_opinion[1]['opinion']})"
        )

        # Encuestado con mayor y menor experticia
        encuestado_mayor_experticia = max(participantes_ordenados, key=lambda x: x[0][0])
        encuestado_menor_experticia = min(participantes_ordenados, key=lambda x: x[0][0])

        salida.append(
            f"  Encuestado con mayor experticia: ({encuestado_mayor_experticia[0][2]}, "
            f"Nombre:'{encuestado_mayor_experticia[1]['nombre']}', "
            f"Experticia:{encuestado_mayor_experticia[1]['experticia']}, "
            f"Opinión:{encuestado_mayor_experticia[1]['opinion']})"
        )
        salida.append(
            f"  Encuestado con menor experticia: ({encuestado_menor_experticia[0][2]}, "
            f"Nombre:'{encuestado_menor_experticia[1]['nombre']}', "
            f"Experticia:{encuestado_menor_experticia[1]['experticia']}, "
            f"Opinión:{encuestado_menor_experticia[1]['opinion']})"
        )

        # Promedios generales de opinión y experticia
        promedio_experticia = sum(x[0][0] for x in participantes_ordenados) / len(participantes_ordenados)
        promedio_opinion = sum(x[0][1] for x in participantes_ordenados) / len(participantes_ordenados)

        salida.append(f"  Promedio de experticia de los encuestados: {promedio_experticia:.2f}")
        salida.append(f"  Promedio de opinión de los encuestados: {promedio_opinion:.2f}")

        return "\n".join(salida)
        '''


        '''
        # Calcular el promedio de opiniones y experticia de las preguntas
            for pregunta in preguntas:
                ids = pregunta["ids_encuestados"]
                participantes = [
                    self.arbol_participantes.buscar(i) for i in ids
                ]
                participantes_validos = [
                    p for p in participantes if p is not None
                ]

                if participantes_validos:
                    promedio_opinion = sum(p["opinion"] for p in participantes_validos) / len(participantes_validos)
                    promedio_experticia = sum(p["experticia"] for p in participantes_validos) / len(participantes_validos)
                else:
                    promedio_opinion = promedio_experticia = 0

                pregunta["promedio_opinion"] = promedio_opinion
                pregunta["promedio_experticia"] = promedio_experticia
            
            # Calcular el promedio del tema
            promedio_opinion_tema = sum(p["promedio_opinion"] for p in preguntas) / len(preguntas)
            promedio_experticia_tema = sum(p["promedio_experticia"] for p in preguntas) / len(preguntas)
            
            # Insertar en el árbol de temas
            tema_data = {
                "promedio_opinion": promedio_opinion_tema,
                "promedio_experticia": promedio_experticia_tema,
                "preguntas": preguntas
            }
            bst_temas_preguntas.insertar(tema_clave, tema_data)
        
        return bst_temas_preguntas
    '''



if __name__ == "__main__":
    algo_arbol = BSTBasedSurvey()
    archivo_prueba = "testsfiles/entrada_prueba_1.txt"
    
    algo_arbol.cargar_datos(archivo_prueba)
    #print("----------------------------------------------------")
    resultado_participantes = algo_arbol.arbol_participantes.recorrido_en_orden()
    #print(resultado_participantes)

    print("----------------------------------------------------")
    resultado_temas = algo_arbol.arbol_temas_preguntas.recorrido_en_orden()
    #print(resultado_temas)

    resultado = algo_arbol.generar_salida()

    print("----------------------------------------------------")
    print(resultado)

