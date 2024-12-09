

# Esta clase representa una ejecución ya hecha
class Execution:
    def __init__(self, nombre):
        self.nombre = nombre
        self.id_ejecucion = None
        self.fecha_ejecucion = None
        self.tamano_entrada = None
        self.tiempos_de_ejecucion = {}  # Guardar tiempos separados por algoritmo
        self.algoritmos_usados = None
        self.content = {}  # Diccionario para almacenar la salida por algoritmo
        self.chart = None

    def agregar_salida(self, algoritmo, salida):
        """Agrega la salida de un algoritmo específico."""
        self.content[algoritmo] = salida

    def cargar_datos_ejecucion(self, id_ejecucion, fecha_ejecucion, algoritmos_usados):
        """Carga los datos de la ejecución."""
        self.id_ejecucion = id_ejecucion
        self.fecha_ejecucion = fecha_ejecucion
        self.algoritmos_usados = algoritmos_usados

    def calcular_tamano_entrada(self):
        secciones = self.content.split("\n\n")
        participantes_raw = secciones[0].split("\n")
        temas_preguntas_raw = secciones[1:]

        """Calcula el tamaño de la entrada basada en participantes, preguntas y temas."""
        num_participantes = len(participantes_raw)
        print(num_participantes)

        num_temas = 0
        num_preguntas = 0

        for temas_raw in temas_preguntas_raw:
            preguntas_raw = temas_raw.split("\n")
            if preguntas_raw and any(p.strip() for p in preguntas_raw):  # Validar sección no vacía
                num_temas += 1

            for pregunta in preguntas_raw:
                pregunta = pregunta.strip()
                if pregunta:  # Verificar que no sea una línea vacía
                    print("pregunta", pregunta)
                    num_preguntas += 1

        self.tamano_entrada = {
            "participantes": num_participantes,
            "preguntas": num_preguntas,
            "temas": num_temas,
            "total": num_participantes + num_preguntas + num_temas
        }

        return participantes_raw, temas_preguntas_raw