import numpy as np

class baseFunctions:
    """
    Clase que almacena el conjunto de operaciones necesarias para realizar la practica 1
    """
    
    def __init__(self):
        pass
    
    @staticmethod
    def movements_to_list(deltas_df):
        """
        Devuelve array con todos los movimientos realizados en las estaciones. Cada posicion del array esta compuesto por el id de la estacion y la cantidad de bicis retiradas/aniadidas en cada movimiento

        Parametros
            deltas_df : DataFrame
                Pandas DataFrame a convertir
        Return
            Numpy ndarray
        """
        move_list = np.array([]) # Inicializamos el array
        rows = len(deltas_df.index) # Mediciones totales realizadas
        columns = len(deltas_df.columns) # Numero de estaciones

        # Recorreremos todas las mediciones e iremos transformando todas ellas que sean distintas de 0
        for i in range(0, rows):
            if i != 0:
                row = deltas_df.iloc[i] # Seleccionamos una medicion
                selec = row[row != 0] # Seleccionamos que estaciones han sufrido algun cambio
                for j in range(0, len(selec)):
                    lst = np.array([[int(selec.index[j]), selec[j]]]) # Obtenemos un array con el index y el numero de bicis retiradas/aniadidas
                    # En la setencia anterior, el primer corchete sirve para crear el array. Mientras que el segundo para crear una tupla tal que: [estacion, movements]
                    if len(move_list) == 0:
                        move_list = lst # Asignamos la primera tupla como 
                    else:
                        move_list = np.append(move_list, lst, axis=0) # Aniadimos una nueva fila(axis=0) a move_list

        return move_list
    
    @staticmethod
    def find_nearest_station_index(index_m, station, actual_state, capacity, search, search_type):
        """
        Devuelve la posicion (index-columna) de la estacion mas cercana con respecto al parametro station en la variable index_m

        Parametros
            index_m : Numpy ndarray
                Almacena las estaciones mas cercanas a cada estacion ordenadas de mas cercanas a mas lejanas. La fila indica la estacion de refencia, mientras que la columna como de cerca esta la estacion
            station : int
                Estacion desde la que buscar su estacion vecina mas proxima
            actual_state : Numpy ndarray
                Array con el estado actual de bicicletas en cada estacion
            capacity : Numpy ndarray
                Contiene la capacidad maxima de bicicletas que puede almacenar una estacion
            search : int
                Numero de bicicletas o slots a buscar
            search_type : str
                Cadena de caracteres que nos indica el tipo de elemento a buscar: 'bicycles' o 'slots'

        Return
            Devuelve un int
        """
        # Valor que almacena la posicion (columna) de la estacion mas cercana con respecto al parametro station
        row_selec = index_m[station] # Seleccionamos el array de estaciones cercanas de la estacion station

        # Comprobamos que tipo de busqueda estamos realizando, 'bicycles' o 'slots'
        if search_type == 'bicycles':
            # Recorremos el array seleccionado y comprobamos cual es la estacion mas cercana con bicicletas suficientes
            for j in range(1, len(row_selec)):
                # Seleccionamos con row_selec la estacion mas cercana a station, despues comprobamos la capacidad disponibles. Y por ultimo comprobamos si es suficiente
                if search <= actual_state[row_selec[j]]:
                    return j # Devolvemos el index

        elif search_type == 'slots':
            # Recorremos el array seleccionado y comprobamos cual es la estacion mas cercana con slots suficientes
            for j in range(1, len(row_selec)):
                # Seleccionamos con row_selec la estacion mas cercana a station, despues comprobamos la capacidad disponibles. Y por ultimo comprobamos si es suficiente
                free_slots = capacity[row_selec[j]] - actual_state[row_selec[j]] # Calculamos el numero de slots disponibles restandole a la capacidad total el numero de bicicletas actuales
                if search <= free_slots:
                    return j # Devolvemos el index
        else:
            raise Exception("La variable search_type no contiene un tipo valido") # La palabra 'raise' nos permite lanzar una excepcion. Es igual que la palabra 'throw' en otros lenguajes


    @staticmethod
    def evaluate(move_list, init_state, capacity, index_m, kms_m):
        '''
        La funcion estipula el numero de kilometros recorrido por los usuarios al no encontrar una bicicleta en su estación de preferencia y tener que desplazarse a la estaion mas cercana con bicicletas disponibles, o la distancia recorrida en caso de no haber sitio para dejar la bicicleta en la estación deseada y tener que desplazarse a la estacion mas cercana con capacidad. La distancia realizada a pie es 3 veces mayor que la recorrida en bicicleta

        Parametros
            move_list : Numpy ndarray
                lista con todos los movimientos realizados. Cada elemento de la lista debe tener la siguiente estructura: [index, desplazamientos]
            init_state : Numpy ndarray
                Contiene el numero de biciclestas alojadas en cada estacion al comienzo de la evaluacion
            capacity : Numpy ndarray
                Contiene la capacidad maxima de bicicletas que puede almacenar una estacion
            index_m : Numpy ndarray
                Almacena las estaciones mas cercanas a cada estacion ordenadas de mas cercanas a mas lejanas. La fila indica la estacion de refencia, mientras que la columna como de cerca esta la estacion
            kms_m : Numpy ndarray
                Almacena la distancia que hay desde una estacion a otra. La disposicion de la informacion se basa en la variable index_m. Es decir, el valor de cada celda de esta matriz corresponde a la posicion homologa en index_m
        Returns
            El numero total de kilometros recorridos por los usuarios
        '''
        tkms = 0 # Kilometros totales
        travel_kms = 0 # Kilometros recorridos por un usuario
        actual_state = init_state.copy() # Variable en la que iremos modificando el numero de biciclestas que se encuentran en cada estacion
        walk_multiplier = 3 # La distancia recorrida andando costara 3 veces mas que la recorrida en bici (valor calculado en kms_m es la distancia en bici)

        for move in move_list:
            station = move[0] # Guardamos la estacion 
            n_bicycle = actual_state[station] + move[1]  # Al numero de bicis de la estacion es cuestion, se le suma el numero de bicis desplazadas (este valor puede ser positivo o negativo) 

            # Tenemos que comprobar que el numero de desplazamientos es posible. Es decir, en caso de que se hayan retirado biciletas, que hubiese suficientes para suplir la demanda.
            # Y caso de que se quisiera dejar bicicletas, que existan suficientes slots/espaciones disponibles en la estacion
            if n_bicycle >= 0 and n_bicycle <= capacity[station]: 
                actual_state[station] = n_bicycle # Como el numero obtenido es posible, actualizamos el estado actual de la estacion
            else:
                # En caso de que no existan bicicletas suficientes para suplir la demanda en la estacion
                if n_bicycle < 0:
                    actual_state[station] = 0 # La estacion ahora tiene 0 bicicletas
                    search = abs(n_bicycle) # abs() nos devuelve el valor absoluto. Obtenemos el valor de bicicletas que necesitamos buscar
                    nearest_station_index = find_nearest_station_index(index_m, station, actual_state, capacity, search, 'bicycles') # Obtenemos la estacion mas cercana con capacidad suficiente de bicicletas

                    # Calculamos los kms recorridos para llegar a la estacion mas cercana
                    travel_kms = kms_m[station][nearest_station_index] * search * walk_multiplier # Kms hacia la estacion * numero de bicicletas a buscar * multiplicador por andar

                    # Actualizamos el estado de la estacion mas cercana
                    nearest_station = index_m[station][nearest_station_index] # Estacion mas cercana a la nuestra
                    actual_state[nearest_station] -= search # Le restamos el numero de bicicletas necesario

                # En caso de que no existan slots suficientes para suplir la demanda en la estacion
                elif n_bicycle > capacity[station]:
                    actual_state[station] = capacity[station] # Ahora la estacion esta llena
                    search = n_bicycle - capacity[station] # Obtenemos el numero de slots a buscar
                    nearest_station_index = self.find_nearest_station_index(index_m, station, actual_state, capacity, search, 'slots') # Obtenemos la estacion mas cercana con capacidad suficiente de slots

                    # Calculamos los kms recorridos para llegar a la estacion mas cercana
                    travel_kms = kms_m[station][nearest_station_index] * search # Kms hacia la estacion * numero de slots a buscar

                    # Actualizamos el estado de la estacion mas cercana
                    nearest_station = index_m[station][nearest_station_index] # Estacion mas cercana a la nuestra
                    actual_state[nearest_station] += search # Le sumamos el numero de bicicletas dejas en los slots libres

                tkms += travel_kms # Sumamos los kilometros recorridos al total

        return tkms

    @staticmethod
    def show_variation(init_solution, init_tkms, new_solution, new_tkms):
        """
        Muestra por pantalla la diferencia de slots existentes entre dos soluciones

        Parametros
            init_solution : Numpy ndarray
                Solucion inicial a comparar
            new_solution : Numpy ndarray
                Solucion a comparar con respecto a init_solution
        """

        columns = np.arange(0,len(init_solution))
        variation = abs(init_solution - new_solution)

        # Para representarlo carrectamente la variacion crearemos un string con los espacios correspondientes
        string = '['
        space = ' '
        for i in range(0,len(init_solution)):
            if variation[i] < 10:
                string += space + str(variation[i])
            else:
                string += str(variation[i])

            if i != len(init_solution)-1:
                string += space

        string += ']'

        print('----------------------COMPARACION DE SOLUCIONES-----------------------')
        print('    Estacion    : {}'.format(columns))
        print('----------------------------------------------------------------------')
        print('Solucion inicial: {} - {} km'.format(init_solution, init_tkms))
        print(' Solucion final : {} - {} km'.format(new_solution, new_tkms))
        print('----------------------------------------------------------------------')
        print('    Variacion   : ' + string)
        print('----------------------------------------------------------------------')
        
        
    @staticmethod
    def generate_initial_solution(init_state, max_slots, seed):
        '''
        Crea una solucion a partir del estado inicial de las estaciones medidas y el numero de slots disponibles

        Parametros
            init_state : Numpy ndarray
                Estado inicial de las estaciones
            max_slots : int
                Numero maximo de slots disponibles a repartir
            seed : int
                Semilla con la que generar numeros aleatorios

        Return
            Devuelve un array con el numero de slots disponibles en cada estacion (capacity)
        '''
        np.random.seed(seed) # Inicializamos la semilla
        init_solution = init_state.copy() # Nuestro punto de partida para crear nuestra solucion sera el estado inicial de las estaciones
        taken_slots = init_solution.sum() # Numero de slots ocupados inicialmente

        while taken_slots < max_slots:
            selec = np.random.randint(0,len(init_state)) # Seleccionamos una estacion de forma aleatoria
            init_solution[selec] += 1 # Aumentamos el numero de slots disponibles en 1
            taken_slots += 1 # Aumentamos el numero de slots disponibles

        return init_solution
    