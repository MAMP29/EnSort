class Nodo:
    def __init__(self, clave, datos):
        self.clave = clave  # La clave será el criterio principal de ordenamiento
        self.datos = datos  # Almacena los datos asociados (puede ser encuestados, preguntas, etc.)
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    
    def insertar(self, clave, datos):
        if self.raiz is None:
            self.raiz = Nodo(clave, datos)
        else:
           self._insertar_recursivo(self.raiz, clave, datos)

    def _insertar_recursivo(self, nodo, clave, datos):
        if clave < nodo.clave:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(clave, datos)
            else:
                self._insertar_recursivo(nodo.izquierda, clave, datos)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(clave, datos)
            else:
                self._insertar_recursivo(nodo.derecha, clave, datos)

    # Método general de recorrido que acepta un parámetro de orden, cuenta como un recorrido inorden
    def recorrido_en_orden(self, descendente=False):
        resultado = []
        self._recorrido_en_orden_recursivo(self.raiz, resultado, descendente)
        return resultado
    
    # Método recursivo que realiza el recorrido en orden
    def _recorrido_en_orden_recursivo(self, nodo, resultado, descendente):
        if nodo is not None:
            if descendente:
                # Recorrido en orden descendente: primero derecho, luego el nodo, luego izquierdo
                self._recorrido_en_orden_recursivo(nodo.derecha, resultado, descendente)
                resultado.append((nodo.clave, nodo.datos))
                self._recorrido_en_orden_recursivo(nodo.izquierda, resultado, descendente)
            else:
                # Recorrido en orden ascendente: primero izquierdo, luego el nodo, luego derecho
                self._recorrido_en_orden_recursivo(nodo.izquierda, resultado, descendente)
                resultado.append((nodo.clave, nodo.datos))
                self._recorrido_en_orden_recursivo(nodo.derecha, resultado, descendente)

    def buscar(self, clave):
        return self._buscar_recursivo(self.raiz, clave)
    
    def _buscar_recursivo(self, nodo, clave):
        if nodo is None:
            return None
        if clave == nodo.clave:
            return nodo.datos
        elif clave < nodo.clave:
            return self._buscar_recursivo(nodo.izquierda, clave)
        else:
            return self._buscar_recursivo(nodo.derecha, clave)
        
        
    # Busca en todas las ramas la clave que tenga el valor en la posición 'indice' igual a 'valor', el motivo de buscar en todas las ramas es porque si
    # se necesita algo como la ID, podría no encontrarla considerando que la experticia es la clave principal
    def buscar_clave_general(self, valor, indice):
        return self.buscar_clave_general_recursivo(self.raiz, valor, indice)

    def buscar_clave_general_recursivo(self, nodo, valor, indice):
        if nodo is None:
            return None
        
        # Comparar el valor en la posición 'indice' de la clave
        if valor == nodo.clave[indice]:
            return nodo.clave
        
        # Recursión para los subárboles
        resultado_izq = None
        resultado_der = None
        
        if nodo.izquierda:
            resultado_izq = self.buscar_clave_general_recursivo(nodo.izquierda, valor, indice)
        
        if nodo.derecha:
            resultado_der = self.buscar_clave_general_recursivo(nodo.derecha, valor, indice)
        
        return resultado_izq or resultado_der


if __name__ == "__main__":
    # Crear un árbol binario de búsqueda
    arbol = ArbolBinarioBusqueda()

    '''
    # Insertar nodos
    arbol.insertar((50, 1), "Dato 50")
    arbol.insertar((30, 3), "Dato 30")
    arbol.insertar((70, 7), "Dato 70")
    arbol.insertar((20, 2), "Dato 20")
    arbol.insertar((40, 4),"Dato 40")
    arbol.insertar((60, 6), "Dato 60")
    arbol.insertar((80, 8), "Dato 80")
    '''
    arbol.insertar((80, 8, 100), "Dato 80")
    arbol.insertar((70, 7, 200), "Dato 70")
    arbol.insertar((90, 9, 300), "Dato 90")

    # Realizar un recorrido en orden
    resultado = arbol.recorrido_en_orden()
    print("------------------------------------------------------")
    print(resultado)
    print("------------------------------------------------------")
    # Imprimir el resultado del recorrido
    print("Recorrido en orden del árbol:")
    for clave, datos in resultado:
        print(f"Clave: {clave}, Datos: {datos}")

    print("------------------------------------------------------")

    #id_busqueda = arbol.buscar_por_valor_en_clave(8, 1)
    id_busqueda = arbol.buscar_clave_general(8, 1)

    print(id_busqueda)
