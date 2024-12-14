class NodoEncuestado:
    def __init__(self, valor_opinion, id, nivel_experticia, nombre):
        self.valor_opinion = valor_opinion
        self.id = id
        self.nivel_experticia = nivel_experticia
        self.nombre = nombre
        self.siguiente = None
        self.anterior = None

class ListaEncuestados:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar(self, valor_opinion, id, nivel_experticia, nombre):
        nuevo_nodo = NodoEncuestado(valor_opinion, id, nivel_experticia, nombre)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo


    def merge_sort(self, criterio="experticia"):
        if self.cabeza is None or self.cabeza.siguiente is None:
            return self
        
        # Divide las listas en dos mitades
        mitad = self.get_mitad()
        izquierda = ListaEncuestados()
        derecha = ListaEncuestados()
        izquierda.cabeza = self.cabeza
        derecha.cabeza = mitad

        # Actualiza las referencias para separar las listas
        if mitad.anterior:
            mitad.anterior.siguiente = None
            mitad.anterior = None

        # Ordena las mitades recursivamente
        izquierda = izquierda.merge_sort(criterio)
        derecha = derecha.merge_sort(criterio)

        # Combina las dos mitades ordenadas
        return self.merge(izquierda, derecha, criterio)

    def merge(self, izquierda, derecha, criterio):
        resultado = ListaEncuestados()
        actual_izquierda = izquierda.cabeza
        actual_derecha = derecha.cabeza

        while actual_izquierda and actual_derecha:
            # Decisión sobre el criterio de ordenación
            if criterio == "experticia":
                if (actual_izquierda.nivel_experticia > actual_derecha.nivel_experticia or
                    (actual_izquierda.nivel_experticia == actual_derecha.nivel_experticia and
                     actual_izquierda.id > actual_derecha.id)):
                    resultado.insertar_nodo_directo(actual_izquierda)
                    actual_izquierda = actual_izquierda.siguiente
                else:
                    resultado.insertar_nodo_directo(actual_derecha)
                    actual_derecha = actual_derecha.siguiente
            elif criterio == "opinion":
                if (actual_izquierda.valor_opinion > actual_derecha.valor_opinion or
                    (actual_izquierda.valor_opinion == actual_derecha.valor_opinion and
                     actual_izquierda.nivel_experticia > actual_derecha.nivel_experticia)):
                    resultado.insertar_nodo_directo(actual_izquierda)
                    actual_izquierda = actual_izquierda.siguiente
                else:
                    resultado.insertar_nodo_directo(actual_derecha)
                    actual_derecha = actual_derecha.siguiente

        # Agrega los nodos restantes
        while actual_izquierda:
            resultado.insertar_nodo_directo(actual_izquierda)
            actual_izquierda = actual_izquierda.siguiente

        while actual_derecha:
            resultado.insertar_nodo_directo(actual_derecha)
            actual_derecha = actual_derecha.siguiente

        return resultado

    def insertar_nodo_directo(self, nodo):
        nuevo_nodo = NodoEncuestado(nodo.valor_opinion, nodo.id, nodo.nivel_experticia, nodo.nombre)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo

    def get_mitad(self):
        lento = self.cabeza
        rapido = self.cabeza

        while rapido and rapido.siguiente and rapido.siguiente.siguiente:
            lento = lento.siguiente
            rapido = rapido.siguiente.siguiente


        # 'lento' ahora está en el medio, lo dividimos en dos listas
        mitad = lento.siguiente
        lento.siguiente = None  # Termina la primera mitad

        return mitad

    # Método para imprimir la lista de izquierda a derecha como generador
    def imprimir_descendentemente_gen(self):
        actual = self.cabeza
        while actual:
            yield f" ({actual.id}, Nombre: '{actual.nombre}', Experticia: {actual.nivel_experticia}, Opinión: {actual.valor_opinion})"
            actual = actual.siguiente
        yield " "  # Indica el final de la lista

    # Método para imprimir la lista de derecha a izquierda
    def imprimir_derecha_a_izquierda(self):
        actual = self.cola
        while actual:
            print(f" ({actual.id}, Nombre: '{actual.nombre}', Experticia: {actual.nivel_experticia}, Opinión: {actual.valor_opinion})")
            actual = actual.anterior
        print("None")  # Indica el final de la lista
    

    def imprimir_izquierda_a_derecha(self):
        actual = self.cabeza
        while actual:
            print( f" ({actual.id}, Nombre: '{actual.nombre}', Experticia: {actual.nivel_experticia}, Opinión: {actual.valor_opinion})")
            actual = actual.siguiente
        print("None")  # Indica el final de la lista

    def calcular_promedio_opinion(self):
        if not self.cabeza:
            return 0
        total_opinion = 0
        cantidad = 0
        actual = self.cabeza
        while actual:
            total_opinion += actual.valor_opinion
            cantidad += 1
            actual = actual.siguiente
        return total_opinion / cantidad if cantidad > 0 else 0

    def calcular_promedio_experticia(self):
        if not self.cabeza:
            return 0
        total_experticia = 0
        cantidad = 0
        actual = self.cabeza
        while actual:
            total_experticia += actual.nivel_experticia
            cantidad += 1
            actual = actual.siguiente
        return total_experticia / cantidad if cantidad > 0 else 0


    def contar_encuestados(self):
        cantidad = 0
        actual = self.cabeza
        while actual:
            cantidad += 1
            actual = actual.siguiente
        return cantidad

  
    # Método para buscar un encuestado por su id
    def buscar_por_id(self, id):
        actual = self.cabeza
        while actual:
            if actual.id == id:
                return actual  # Retorna el nodo que coincide con el id
            actual = actual.siguiente
        return None  # Si no se encuentra el id, retorna None
    
    # Método para iterar sobre todos los temas y devolverlos
    def iterar_encuestados(self):
        actual = self.cabeza
        while actual:
            yield actual  # "yield" permite que iteres sobre los temas sin imprimirlos directamente
            actual = actual.siguiente


    # Método flexible para obtener el participante extremo según un criterio
    def obtener_extremo(self, criterio, mayor=True):
        participante_extremo = None
        # Inicializamos el valor de mayor_valor dependiendo de si buscamos el mayor o el menor
        if mayor:
            mayor_valor = float('-inf')  # Buscamos el valor máximo
        else:
            mayor_valor = float('inf')  # Buscamos el valor mínimo

        current_encuestado = self.cabeza
        while current_encuestado:
            if criterio == 'opinion':  # Comparamos con el criterio de valor de opinión
                if (mayor and current_encuestado.valor_opinion > mayor_valor) or \
                   (not mayor and current_encuestado.valor_opinion < mayor_valor):
                    mayor_valor = current_encuestado.valor_opinion
                    participante_extremo = current_encuestado
            elif criterio == 'experticia':  # Comparamos con el criterio de nivel de experticia
                if (mayor and current_encuestado.nivel_experticia > mayor_valor) or \
                   (not mayor and current_encuestado.nivel_experticia < mayor_valor):
                    mayor_valor = current_encuestado.nivel_experticia
                    participante_extremo = current_encuestado
            current_encuestado = current_encuestado.siguiente

        return participante_extremo


if __name__ == '__main__':
 

    lista = ListaEncuestados()

    lista.insertar(6, 1, 1, "Sofía García")
    lista.insertar(10, 2, 7, "Alejandro Torres")
    lista.insertar(0, 3, 9, "Valentina Rodríguez")
    lista.insertar(1, 4, 10, "Juan López")
    lista.insertar(0, 5, 7, "Martina Martínez")
    lista.insertar(9, 6, 8, "Sebastián Pérez")
    lista.insertar(7, 7, 2, "Camila Fernández")
    lista.insertar(7, 8, 4, "Mateo González")
    lista.insertar(5, 9, 7, "Isabella Díaz")
    lista.insertar(9, 10, 2, "Daniel Ruiz")
    lista.insertar(7, 11, 1, "Luciana Sánchez")
    lista.insertar(8, 12, 6, "Lucas Vásquez")

    resultado = lista.merge_sort()
    #lista.imprimir_izquierda_a_derecha()
    #resultado.imprimir_izquierda_a_derecha()

    promedio_opinion = resultado.calcular_promedio_opinion()
    promedio_experticia = resultado.calcular_promedio_experticia()
    numero_encuestados = resultado.contar_encuestados()
    encuestado_5 = resultado.buscar_por_id(5)
    encuestado_mayor_opinion = resultado.obtener_extremo('opinion', True)
    encuestado_menor_opinion = resultado.obtener_extremo('opinion', False)
    encuestado_mayor_experticia = resultado.obtener_extremo('experticia', True)
    encuestado_menor_experticia = resultado.obtener_extremo('experticia', False)

    print(f"Promedio de opinion {promedio_opinion}")
    print(f"Promedio de opinion {promedio_experticia}")
    print(f"Número de encuestados {numero_encuestados}")
    print(f"El encuestadito 5 nombre {encuestado_5.nombre}")
    print(f"El encuestado con mayor opinion {encuestado_mayor_opinion.nombre}")
    print(f"El encuestado con menor opinion {encuestado_menor_opinion.nombre}")
    print(f"El encuestado con mayor experticia {encuestado_mayor_experticia.nombre}")
    print(f"El encuestado con menor experticia {encuestado_menor_experticia.nombre}")
    
    salida = []

    salida.extend(resultado.imprimir_descendentemente_gen())
 
    print("\n".join(salida))

