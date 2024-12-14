from sorting_logic.datastructures.doublyl_linked_list.ls_encuestados import ListaEncuestados
#from datastructures.doublyl_linked_list.ls_encuestados import ListaEncuestados

class NodoPregunta:
    def __init__(self, id_pregunta, lista_encuestados):
        self.id_pregunta = id_pregunta
        self.encuestados = lista_encuestados  # Lista de encuestados
        self.siguiente = None
        self.anterior = None

    # Método para imprimir la pregunta y sus encuestados
    def imprimir_pregunta(self):
        print(f"Pregunta ID: {self.id_pregunta}")
        print("  Encuestados:")
        self.encuestados.imprimir_izquierda_a_derecha()

    def calcular_promedio_opinion(self):
        return self.encuestados.calcular_promedio_opinion()

    def calcular_promedio_experticia(self):
        return self.encuestados.calcular_promedio_experticia()

    def contar_encuestados(self):
        return self.encuestados.contar_encuestados()
    '''
    # Método para calcular el promedio de opiniones de los encuestados de esta pregunta
    def calcular_promedio_opinion(self):
        if not self.encuestados.cabeza:
            return 0
        total_opinion = 0
        cantidad = 0
        current_encuestado = self.encuestados.cabeza
        while current_encuestado:
            total_opinion += current_encuestado.valor_opinion
            cantidad += 1
            current_encuestado = current_encuestado.siguiente
        return total_opinion / cantidad if cantidad > 0 else 0

    # Método para calcular el promedio de experticia de los encuestados de esta pregunta
    def calcular_promedio_experticia(self):
        if not self.encuestados.cabeza:
            return 0
        total_experticia = 0
        cantidad = 0
        current_encuestado = self.encuestados.cabeza
        while current_encuestado:
            total_experticia += current_encuestado.nivel_experticia
            cantidad += 1
            current_encuestado = current_encuestado.siguiente
        return total_experticia / cantidad if cantidad > 0 else 0
    
    # Método para contar los encuestados en todas las preguntas
    def contar_encuestados(self):
        cantidad = 0
        actual_pregunta = self.cabeza
        while actual_pregunta:
            cantidad += actual_pregunta.contar_encuestados()  # Llamada al método de NodoPregunta
            actual_pregunta = actual_pregunta.siguiente
        return cantidad
    '''

class ListaPreguntas:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar(self, id_pregunta, lista_encuestados):
        nuevo_nodo = NodoPregunta(id_pregunta, lista_encuestados)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo

    def merge_sort(self):
        if self.cabeza is None or self.cabeza.siguiente is None:
            return self

        # Divide la lista en dos mitades
        mitad = self.get_mitad()
        izquierda = ListaPreguntas()
        derecha = ListaPreguntas()
        izquierda.cabeza = self.cabeza
        derecha.cabeza = mitad

        # Actualiza las referencias para separar las listas
        if mitad.anterior:
            mitad.anterior.siguiente = None
            mitad.anterior = None

        # Ordena las mitades recursivamente
        izquierda = izquierda.merge_sort()
        derecha = derecha.merge_sort()

        # Combina las dos mitades ordenadas
        return self.merge(izquierda, derecha)

    def merge(self, izquierda, derecha):
        resultado = ListaPreguntas()
        actual_izquierda = izquierda.cabeza
        actual_derecha = derecha.cabeza

        while actual_izquierda and actual_derecha:
            # Calcula los promedios necesarios para comparar
            promedio_opinion_izq = actual_izquierda.calcular_promedio_opinion()
            promedio_experticia_izq = actual_izquierda.calcular_promedio_experticia()

            promedio_opinion_der = actual_derecha.calcular_promedio_opinion()
            promedio_experticia_der = actual_derecha.calcular_promedio_experticia()

            if (promedio_opinion_izq > promedio_opinion_der or
                (promedio_opinion_izq == promedio_opinion_der and promedio_experticia_izq > promedio_experticia_der) or
                (promedio_opinion_izq == promedio_opinion_der and promedio_experticia_izq == promedio_experticia_der and
                 actual_izquierda.contar_encuestados() > actual_derecha.contar_encuestados())):
                resultado.insertar_nodo_directo(actual_izquierda)
                actual_izquierda = actual_izquierda.siguiente
            else:
                resultado.insertar_nodo_directo(actual_derecha)
                actual_derecha = actual_derecha.siguiente

        while actual_izquierda:
            resultado.insertar_nodo_directo(actual_izquierda)
            actual_izquierda = actual_izquierda.siguiente

        while actual_derecha:
            resultado.insertar_nodo_directo(actual_derecha)
            actual_derecha = actual_derecha.siguiente

        return resultado

    def insertar_nodo_directo(self, nodo):
        nuevo_nodo = NodoPregunta(nodo.id_pregunta, nodo.encuestados)
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
    
    def imprimir_preguntas(self):
        actual = self.cabeza
        while actual:
            actual.imprimir_pregunta()
            actual = actual.siguiente

    '''def calcular_promedio_opinion(self):
        actual = self.cabeza
        return actual.encuestados.calcular_promedio_opinion()'''

    def calcular_promedio_opinion_total(self):
        if not self.cabeza:
            return 0
        total_opinion = 0
        cantidad = 0
        actual = self.cabeza
        while actual:
            total_opinion += actual.encuestados.calcular_promedio_opinion()
            cantidad += 1
            actual = actual.siguiente
        return total_opinion / cantidad if cantidad > 0 else 0

    '''def calcular_promedio_experticia(self):
        actual = self.cabeza
        return actual.encuestados.calcular_promedio_experticia()'''
    
    def calcular_promedio_experticia_total(self):
        if not self.cabeza:
            return 0
        total_opinion = 0
        cantidad = 0
        actual = self.cabeza
        while actual:
            total_opinion += actual.encuestados.calcular_promedio_experticia()
            cantidad += 1
            actual = actual.siguiente
        return total_opinion / cantidad if cantidad > 0 else 0
    

    def contar_encuestados_todos(self):
        cantidad = 0
        actual = self.cabeza
        while actual:
            cantidad += actual.encuestados.contar_encuestados()
            actual = actual.siguiente
        return cantidad
    
    def ordenar_encuestados_nodos(self):
        actual = self.cabeza
        while actual:
            if actual.encuestados:
                actual.encuestados = actual.encuestados.merge_sort(criterio="opinion")  # Asegúrate de devolver la lista ordenada
            actual = actual.siguiente
        return self


    '''   
    def contar_encuestados(self):
        actual = self.cabeza
        return actual.encuestados.contar_encuestados()
    '''

    # Método para iterar sobre todos los temas y devolverlos
    def iterar_preguntas(self):
        actual = self.cabeza
        while actual:
            yield actual  # "yield" permite que iteres sobre los temas sin imprimirlos directamente
            actual = actual.siguiente


    def obtener_pregunta_extrema(self, criterio, mayor=True):
        pregunta_extrema = None

        if mayor:
            mayor_valor = float('-inf')  # Buscamos el valor máximo
        else:
            mayor_valor = float('inf')  # Buscamos el valor mínimo

        current_pregunta = self.cabeza
        while current_pregunta:
            promedio_opinion = current_pregunta.calcular_promedio_opinion()
            promedio_experticia = current_pregunta.calcular_promedio_experticia()

            if criterio == 'opinion':
                if (mayor and promedio_opinion > mayor_valor) or \
                 (not mayor and promedio_opinion < mayor_valor):
                     mayor_valor = promedio_opinion
                     pregunta_extrema = current_pregunta
            elif criterio == 'experticia':
                 if (mayor and promedio_experticia> mayor_valor) or \
                 (not mayor and promedio_experticia < mayor_valor):
                    mayor_valor = promedio_experticia
                    pregunta_extrema = current_pregunta


            # Avanzar a la siguiente pregunta
            current_pregunta = current_pregunta.siguiente

        # Si no se encontró ninguna pregunta extrema, devolvemos None
        return pregunta_extrema if pregunta_extrema else None



if __name__ == '__main__':

    print("Que mazda")

    
    lista_de_encuestados_pregunta_1 = ListaEncuestados()
    lista_de_encuestados_pregunta_1.insertar(10, 2, 7, "Alejandro Torres")
    lista_de_encuestados_pregunta_1.insertar(9, 10, 2, "Daniel Ruiz")

    lista_de_encuestados_pregunta_2 = ListaEncuestados()
    lista_de_encuestados_pregunta_2.insertar(6, 1, 1, "Sofía García")
    lista_de_encuestados_pregunta_2.insertar(5, 9, 7, "Isabella Díaz")
    lista_de_encuestados_pregunta_2.insertar(8, 12, 6, "Lucas Vásquez")
    lista_de_encuestados_pregunta_2.insertar(9, 6, 8, "Sebastián Pérez")
    
    '''
    lista_de_encuestados_pregunta_1 = ListaEncuestados()
    lista_de_encuestados_pregunta_1.insertar(0, 3, 9, "Valentina Rodríguez")
    lista_de_encuestados_pregunta_1.insertar(1, 4, 10, "Juan López")
    lista_de_encuestados_pregunta_1.insertar(0, 5, 7, "Martina Martínez")

    lista_de_encuestados_pregunta_2 = ListaEncuestados()
    lista_de_encuestados_pregunta_2.insertar(7, 11, 1, "Luciana Sánchez")
    lista_de_encuestados_pregunta_2.insertar(7, 8, 4, "Mateo González")    
    lista_de_encuestados_pregunta_2.insertar(7, 7, 2, "Camila Fernández")
    '''
    #rest = lista_de_encuestados_pregunta_2.merge_sort(criterio="opinion")

    #rest.imprimir_izquierda_a_derecha()

    pregunta_1 = ListaPreguntas()

    pregunta_1.insertar(1, lista_de_encuestados_pregunta_1)
    pregunta_1.insertar(2, lista_de_encuestados_pregunta_2)

    #promedio_opinion_pregunta = pregunta_1.calcular_promedio_opinion()
    #encuestados_primera_pregunta = pregunta_1.contar_encuestados_todos()
    promedio_opinion_total_preguntas = pregunta_1.calcular_promedio_opinion_total()
    promedio_experticia_total_preguntas = pregunta_1.calcular_promedio_experticia_total()

    #print(f"Promedio de opinion de la primera pregunta {promedio_opinion_pregunta}")
    #print(f"Número de encuestados de la primera pregunta  {encuestados_primera_pregunta}")
    print(f"Promedio total opinion de las preguntas {promedio_opinion_total_preguntas}")
    print(f"Promedio total experticia de las preguntas {promedio_experticia_total_preguntas}")


    #pregunta_1.imprimir_preguntas()

    resultado = pregunta_1.merge_sort()
    
    resultado.ordenar_encuestados_nodos()

    print(resultado.obtener_pregunta_extrema(criterio='opinion',mayor=True).calcular_promedio_opinion())

    print(resultado.imprimir_preguntas())


    

