from classes.abstrac.algorithm import Algorithm
from classes.baseFunctions import baseFunctions as bf
import numpy as np
import pandas as pd

class Greedy(Algorithm):
    """
    
    """

    def __init__():
        pass

    def movement_operator(actual_state, actual_solution, neighbours_limit, n_slots):
        """
        Operador de movimiento para el algoritmo greedy
        
        Parametros
        
        Return
        
        """
        
        n = len(actual_solution) # Guardamos el tamanio de la solucion para hacer los bucles
        neighbours_list = np.array([]) # Lista de vecinos encontrados
        neighbours_n = 0 # Numero de vecinos encontrados
        
        # Recorremos todos los posibles vecinos (movimiento de n_slots entre todas las combinaciones de estaciones posibles)
        for i in range(1, n):
            for j in range(i, n): 
                # Buscamos todos los vecinos posibles que no superen nuestro limite de exploracion
                if neighbours_n < neighbours_limit:
                    # Ahora comprobamos si cambio de n_slots entra las estaciones 'i' y 'j' es posible realizar (la capacidad de una estacion no puede ser negativa)
                    if actual_solution[i] >= n_slots and (actual_solution[i]-n_slots) >= actual_state[i]:
                        neighbours_n += 1 # Aumentamos el numero de vecinos encontrados
                        
                        new_neighbour = actual_solution.copy() # Creamos una copia de la solucion actual para poder crear la vecina
                        new_neighbour[i] -= n_slots # Le quitamos n_slots a la estacion 'i'
                        new_neighbour[j] += n_slots # Le aniadimos los n_slots quitados de 'i' a 'j'
                        
                        if len(neighbours_list) == 0:
                            neighbours_list = np.array([new_neighbour])
                        else:
                            neighbours_list = np.append(neighbours_list, np.array([new_neighbour]), axis=0) # Aniadimos una nueva fila(axis=0) a la lista de vecinos. axis=0 para que la nueva solucion se aniada como fila
                            
        # Devolvemos el mejor vecino
        return neighbours_list

    def run(seed, max_slots, n_slots, neighbours_limit, deltas_df, index_df, kms_df):
        """
        Ejecuta el algoritmo Greedy para el problema de la practica 1
        
        Parametros
        
        Return
        
        """
        index_m = index_df.to_numpy() # index matrix
        kms_m = kms_df.to_numpy() # kms matrix

        init_state = deltas_df.iloc[0].to_numpy() # Estado inicial
        init_solution = bf.generate_initial_solution(init_state, max_slots, seed) # Generamos la solucion inicial
        move_list = bf.movements_to_list(deltas_df) # Creamos la lista de movimientos

        actual_solution = init_solution.copy()
        init_tmks = bf.evaluate(move_list, init_state, init_solution, index_m, kms_m) # Evaluamos nuestra solucion
        kms_m = kms_df.to_numpy() # kms matrix
        best_tkms = init_tkms

        print('Greedy init_solution: {} - {} kms'.format(init_solution, best_tkms))
        neigbours_list = movement_operator(init_state, actual_solution, neighbours_limit, n_slots) # Lista de vecinos de la solucion inicial
        for neighbour in neigbours_list:
            new_tkms = bf.evaluate(move_list, init_state, neighbour, index_m, kms_m) # Evaluamos el vecino
            if best_tkms > new_tkms:
                best_solution = neighbour.copy()
                best_tkms = new_tkms
                print('New Greedy best_solution: {} - {} kms '.format(best_solution, best_tkms))

        bf.show_variation(init_solution, init_tkms, best_solution, best_tkms)

        return np.array([best_solution, best_tkms])