def merge_sort(lista, claves, orden='asc'):
    if len(lista) <= 1:
        return lista
    mid = len(lista) // 2
    left = merge_sort(lista[:mid], claves, orden)
    right = merge_sort(lista[mid:], claves, orden)
    
    return merge(left, right, claves, orden)

def merge(left, right, claves, orden):
    result = []
    i = j = 0
    
    # Determinar la dirección de la comparación
    comparador = (lambda a, b: a < b) if orden == 'asc' else (lambda a, b: a > b)
    
    # Comparar y combinar las dos listas en orden
    while i < len(left) and j < len(right):
        # Para cada clave en claves, comparar
        for clave in claves:
            if comparador(left[i][clave], right[j][clave]):
                result.append(left[i])
                i += 1
                break
            elif comparador(right[j][clave], left[i][clave]):
                result.append(right[j])
                j += 1
                break
        else:  # Si son iguales en todas las claves, elegir el primero
            result.append(left[i])
            i += 1

    # Añadir lo que queda en cada lista
    result.extend(left[i:])
    result.extend(right[j:])
    return result