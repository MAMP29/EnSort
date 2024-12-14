from datastructures.doublyl_linked_list.ls_preguntas import ListaPreguntas
from datastructures.doublyl_linked_list.ls_encuestados import ListaEncuestados
#from ls_preguntas import ListaPreguntas
#from ls_encuestados import ListaEncuestados

class NodoTema:
    def __init__(self, id_tema, listaPreguntas):
        self.id_tema = id_tema
        self.preguntas = listaPreguntas  # Lista de preguntas
        self.siguiente = None
        self.anterior = None

        def calcular_promedio_opinion_total(self):
            return self.preguntas.calcular_promedio_opinion_total()

        def calcular_promedio_experticia_total(self):
            return self.preguntas.calcular_promedio_experticia_total()

        def contar_encuestados_total(self):
            return self.preguntas.contar_encuestados_todos()
        

    # Método para imprimir el tema y sus preguntas
    def imprimir_tema(self):
        print(f"Tema ID: {self.id_tema}")
        print("Preguntas:")
        self.preguntas.imprimir_preguntas()

    # Método para calcular el promedio total de opiniones en este tema
    def calcular_promedio_opinion_total(self):
        return self.preguntas.calcular_promedio_opinion_total()

    # Método para calcular el promedio total de experticia en este tema
    def calcular_promedio_experticia_total(self):
        return self.preguntas.calcular_promedio_experticia_total()

   # Método para contar los encuestados en todas las preguntas de este tema
    def contar_encuestados(self):
        return self.preguntas.contar_encuestados_todos()
    

class ListaTemas:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar(self, id_tema, listaPreguntas):
        nuevo_nodo = NodoTema(id_tema, listaPreguntas)
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
        izquierda = ListaTemas()
        derecha = ListaTemas()
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
        resultado = ListaTemas()
        actual_izquierda = izquierda.cabeza
        actual_derecha = derecha.cabeza

        while actual_izquierda and actual_derecha:
            # Calcula los promedios necesarios para comparar
            promedio_opinion_izq = actual_izquierda.calcular_promedio_opinion_total()
            promedio_experticia_izq = actual_izquierda.calcular_promedio_experticia_total()

            promedio_opinion_der = actual_derecha.calcular_promedio_opinion_total()
            promedio_experticia_der = actual_derecha.calcular_promedio_experticia_total()

            if (promedio_opinion_izq > promedio_opinion_der or
                (promedio_opinion_izq == promedio_opinion_der and promedio_experticia_izq > promedio_experticia_der) or
                (promedio_opinion_izq == promedio_opinion_der and promedio_experticia_izq == promedio_experticia_der and
                 actual_izquierda.contar_encuestados_total() > actual_derecha.contar_encuestados_total())):
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
        nuevo_nodo = NodoTema(nodo.id_tema, nodo.preguntas)
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
    
    def ordenar_todos_las_preguntas(self):
        actual = self.cabeza
        while actual:
            if actual.preguntas:
                actual.preguntas = actual.preguntas.merge_sort()
                actual.preguntas = actual.preguntas.ordenar_encuestados_nodos()  # Asegúrate de devolver la lista ordenada
            actual = actual.siguiente
        return self

    '''
    def calcular_promedio_opinion(self):
        if not self.cabeza:
            return 0
        total_opinion = 0
        cantidad = 0
        actual = self.cabeza
        while actual:
            total_opinion += actual.preguntas.calcular_promedio_opinion()
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
            total_experticia += actual.preguntas.calcular_promedio_experticia()
            cantidad += 1
            actual = actual.siguiente
        return total_experticia / cantidad if cantidad > 0 else 0

    def contar_encuestados(self):
        cantidad = 0
        actual = self.cabeza
        while actual:
            cantidad += actual.preguntas.contar_encuestados()
            actual = actual.siguiente
        return cantidad
    '''
    def obtener_extremo(self, criterio, mayor=True):
        actual = self.cabeza  # Empieza con el primer nodo (tema)
        extremo = None
        id_tema = None
        pregunta_extrema = None

        # Definimos el método para obtener el valor según el criterio
        def obtener_valor(pregunta, criterio):
            if criterio == 'opinion':
                return pregunta.calcular_promedio_opinion()
            elif criterio == 'experticia':
                return pregunta.calcular_promedio_experticia()
            else:
                return None

        while actual:
            # Obtenemos el extremo de la pregunta actual en el tema
            pregunta_actual = actual.preguntas.obtener_pregunta_extrema(criterio, mayor)
            
            valor = obtener_valor(pregunta_actual, criterio)

            # Si es la primera vez o el valor es mejor según el criterio, actualizamos el extremo
            if extremo is None:
                extremo = valor
                id_tema = actual.id_tema  # Guardamos el id del tema correspondiente
                pregunta_extrema = pregunta_actual 
            else:
                if mayor:
                    # Si el valor es mayor que el extremo actual, lo actualizamos
                    if valor > extremo:
                        extremo = valor
                        id_tema = actual.id_tema
                        pregunta_extrema = pregunta_actual
                else:
                    # Si el valor es menor que el extremo actual, lo actualizamos
                    if valor < extremo:
                        extremo = valor
                        id_tema = actual.id_tema
                        pregunta_extrema = pregunta_actual

            actual = actual.siguiente

        return extremo, id_tema, pregunta_extrema.id_pregunta
        
    # Método para iterar sobre todos los temas y devolverlos
    def iterar_temas(self):
        actual = self.cabeza
        while actual:
            yield actual  # "yield" permite que iteres sobre los temas sin imprimirlos directamente
            actual = actual.siguiente

    # Método para imprimir todos los temas
    def imprimir_temas(self):
        actual = self.cabeza
        while actual:
            actual.imprimir_tema()
            actual = actual.siguiente


if __name__ == '__main__':

    print("Que mazda")

    lista_de_encuestados_pregunta_1_tema_1 = ListaEncuestados()
    lista_de_encuestados_pregunta_1_tema_1.insertar(10, 2, 7, "Alejandro Torres")
    lista_de_encuestados_pregunta_1_tema_1.insertar(9, 10, 2, "Daniel Ruiz")

    lista_de_encuestados_pregunta_2_tema_1 = ListaEncuestados()
    lista_de_encuestados_pregunta_2_tema_1.insertar(6, 1, 1, "Sofía García")
    lista_de_encuestados_pregunta_2_tema_1.insertar(5, 9, 7, "Isabella Díaz")
    lista_de_encuestados_pregunta_2_tema_1.insertar(8, 12, 6, "Lucas Vásquez")
    lista_de_encuestados_pregunta_2_tema_1.insertar(9, 6, 8, "Sebastián Pérez")

    
    lista_de_encuestados_pregunta_1_tema_2 = ListaEncuestados()
    lista_de_encuestados_pregunta_1_tema_2.insertar(0, 3, 9, "Valentina Rodríguez")
    lista_de_encuestados_pregunta_1_tema_2.insertar(1, 4, 10, "Juan López")
    lista_de_encuestados_pregunta_1_tema_2.insertar(0, 5, 7, "Martina Martínez")

    lista_de_encuestados_pregunta_2_tema_2 = ListaEncuestados()
    lista_de_encuestados_pregunta_2_tema_2.insertar(7, 11, 1, "Luciana Sánchez")
    lista_de_encuestados_pregunta_2_tema_2.insertar(7, 8, 4, "Mateo González")    
    lista_de_encuestados_pregunta_2_tema_2.insertar(7, 7, 2, "Camila Fernández")

    preguntas_tema_1 = ListaPreguntas()

    preguntas_tema_1.insertar(1, lista_de_encuestados_pregunta_1_tema_1)
    preguntas_tema_1.insertar(2, lista_de_encuestados_pregunta_2_tema_1)

    preguntas_tema_2 = ListaPreguntas()

    preguntas_tema_2.insertar(1, lista_de_encuestados_pregunta_1_tema_2)
    preguntas_tema_2.insertar(2, lista_de_encuestados_pregunta_2_tema_2)

    temas = ListaTemas()

    temas.insertar(1, preguntas_tema_1)
    temas.insertar(2, preguntas_tema_2)

    #temas.imprimir_temas()

    resultado = temas.merge_sort()

    resultado.ordenar_todos_las_preguntas()

    resultado.imprimir_temas()

    print(resultado.obtener_extremo(criterio='opinion',mayor=True))

