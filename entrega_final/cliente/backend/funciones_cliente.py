def validacion_formato(nombre: str) -> bool:
    if nombre.isalnum() and len(nombre) <= 16 and len(nombre) >= 3:
        if nombre.lower() == nombre:
            return False
        num_of_digits = 0
        for char in nombre:
            if char.isdigit():
                num_of_digits += 1
        if num_of_digits > 0:
            return True
        else:
            return False
    else:
        return False


def riesgo_mortal(laberinto: list[list], key: str) -> bool:
    rabbit_position = (0, 0)
    lv_positions = []
    lh_positions = []
    cr_positions = []
    cl_positions = []
    cu_positions = []
    cd_positions = []
    wall_positions = []
    row_position, char_position = 0, 0
    dangerous_list = []
    for row in laberinto:
        char_position = 0
        for char in row:
            if char == "C":
                rabbit_position = (row_position, char_position)
            if char == 'LV':
                lv_positions.append((row_position, char_position))
            if char == 'LH':
                lh_positions.append((row_position, char_position))
            if char == 'CR':
                cr_positions.append((row_position, char_position))
            if char == 'CL':
                cl_positions.append((row_position, char_position))
            if char == 'CU':
                cu_positions.append((row_position, char_position))
            if char == 'CD':
                cd_positions.append((row_position, char_position))
            if char == 'P':
                wall_positions.append((row_position, char_position))
            char_position += 1
        row_position += 1
    try:
        for lv in lv_positions:
            if lv[1] == rabbit_position[1]:
                for wall in wall_positions:
                    if wall[1] == lv[1]:
                        if (rabbit_position[0] > wall[0] > lv[0]) or \
                                (rabbit_position[0] < wall[0] < lv[0]):
                            dangerous_list.append(False)
                            dangerous_list.append('lv_false')
                if 'lv_false' not in dangerous_list:
                    dangerous_list.append(True)

        for lh in lh_positions:
            if lh[0] == rabbit_position[0]:
                for wall in wall_positions:
                    if wall[0] == lh[0] and (rabbit_position[1] > wall[1] > lh[1]) or \
                            wall[0] == lh[0] and (rabbit_position[1] < wall[1] < lh[1]):
                        dangerous_list.append(False)
                        dangerous_list.append('lh_false')
                        pass
                if 'lh_false' not in dangerous_list:
                    dangerous_list.append(True)

        for cr in cr_positions:
            if cr[0] == rabbit_position[0]:
                if cr[1] < rabbit_position[1]:
                    for wall in wall_positions:
                        if wall[0] == cr[0]:
                            if (rabbit_position[1] > wall[1] > cr[1]):
                                dangerous_list.append(False)
                                dangerous_list.append('cr_false')
                                pass
                    if 'cr_false' not in dangerous_list:
                        dangerous_list.append(True)

        for cl in cl_positions:
            if cl[0] == rabbit_position[0]:
                if cl[1] > rabbit_position[1]:
                    for wall in wall_positions:
                        if wall[0] == cl[0]:
                            if (rabbit_position[1] < wall[1] < cl[1]):
                                dangerous_list.append(False)
                                dangerous_list.append('cl_false')
                                pass
                    if 'cl_false' not in dangerous_list:
                        dangerous_list.append(True)

        for cu in cu_positions:
            if cu[1] == rabbit_position[1]:
                if rabbit_position[0] < cu[0]:
                    for wall in wall_positions:
                        if wall[1] == cu[1]:
                            if (rabbit_position[0] < wall[0] < cu[0]):
                                dangerous_list.append(False)
                                dangerous_list.append('cu_false')
                                pass
                    if 'cu_false' not in dangerous_list:
                        dangerous_list.append(True)

        for cd in cd_positions:
            if cd[1] == rabbit_position[1]:
                if rabbit_position[0] > cd[0]:
                    for wall in wall_positions:
                        if wall[1] == cd[1]:
                            if (rabbit_position[0] > wall[0] > cd[0]):
                                dangerous_list.append(False)
                                dangerous_list.append('cd_false')
                                pass
                    if 'cd_false' not in dangerous_list:
                        dangerous_list.append(True)
    except IndexError as e:
        print('IndexError', e)
        print('\n'*8)
    finally:
        for item in dangerous_list:
            if item == True:
                return True
        return False


def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    if item in inventario:
        inventario.remove(item)
        return True, inventario
    else:
        return False, inventario


def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int) -> float:
    if PUNTAJE_LOBO == 0 or cantidad_lobos == 0:
        return float(0)
    else:
        puntaje_nivel = tiempo * vidas/(cantidad_lobos * PUNTAJE_LOBO)
        return round(float(puntaje_nivel), 2)


def validar_direccion(laberinto: list[list], tecla: str, entrada: tuple) -> bool:
    wall_positions = []
    row_counter, col_counter = 0, 0
    rabbit_position = (0, 0)
    entrada = entrada
    for row in laberinto:
        for col in row:
            if col == 'P':
                wall_positions.append((row_counter, col_counter))
            elif col == 'C':
                rabbit_position = (row_counter, col_counter)
            elif col == 'E':
                entrada = (row_counter, col_counter)
            elif col.startswith('can'):
                carrot_position = (row_counter, col_counter)
            col_counter += 1
        col_counter = 0
        row_counter += 1
    row_counter = 0
    # Si el conejo esta en la entrada, solo puede moverse hacia abajo o la derecha
    # Si hay una muralla, no puede moverse en esa direccion
    for wall in wall_positions:
        if tecla.lower() == 'w':
            # Si esta en la entrada, y quiere retroceder un indice
            if rabbit_position[0] == entrada[0] and rabbit_position[1] == entrada[1]:
                return False, rabbit_position
            # Si intenta ir hacia la entrada
            if rabbit_position[0]-1 == entrada[0] and rabbit_position[1] == entrada[1]:
                return False, rabbit_position
            if wall[1] == rabbit_position[1] and rabbit_position[0] == wall[0] + 1:
                return False, rabbit_position
        elif tecla.lower() == 'a':
            # Si esta en la entrada, y quiere retroceder un indice
            if rabbit_position[1] == entrada[1] and rabbit_position[0] == entrada[0]:
                return False, rabbit_position
            # Si intenta ir hacia la entrada
            if rabbit_position[1]-1 == entrada[1] and rabbit_position[0] == entrada[0]:
                return False, rabbit_position
            if wall[0] == rabbit_position[0] and wall[1] == rabbit_position[1] - 1:
                return False, rabbit_position
        elif tecla.lower() == 's':
            if wall[1] == rabbit_position[1] and rabbit_position[0] == wall[0] - 1:
                return False, rabbit_position
        elif tecla.lower() == 'd':
            if wall[0] == rabbit_position[0] and wall[1] == rabbit_position[1] + 1:
                return False, rabbit_position
    return (True, rabbit_position)


def validate_enemy_colision(laberinto: list[list], direction: str) -> bool:
    enemy_positions = []
    row_counter, col_counter = 0, 0
    for row in laberinto:
        for col in row:
            if col.startswith('carrot'):
                enemy_positions.append((row_counter, col_counter))
            elif 'wolf' in col:
                enemy_positions.append((row_counter, col_counter))
            elif col == 'C':
                rabbit_position = (row_counter, col_counter)
            col_counter += 1
        col_counter = 0
        row_counter += 1
    row_counter = 0

    for enemy in enemy_positions:
        if enemy[1] == rabbit_position[1] and enemy[0] == rabbit_position[0] + 1\
                or enemy[1] == rabbit_position[1] and enemy[0] == rabbit_position[0]-1:
            return True, rabbit_position
        elif enemy[0] == rabbit_position[0] and rabbit_position[1] == enemy[1] + 1\
                or enemy[0] == rabbit_position[0] and rabbit_position[1] == enemy[1] - 1:
            return True, rabbit_position
    return False, rabbit_position


def has_reached_end(laberinto: list[list], direction: str, end_position: tuple) -> bool:
    row_counter, col_counter = 0, 0
    for row in laberinto:
        for col in row:
            if col == 'C':
                rabbit_position = ((row_counter, col_counter))
            col_counter += 1
        col_counter = 0
        row_counter += 1
    row_counter = 0

    for casilla in laberinto:
        if end_position[1] == rabbit_position[1] and end_position[0] == rabbit_position[0]:
            return True, rabbit_position
    return False, rabbit_position


def validar_direccion_carrot(laberinto: list[list], object_name: str) -> bool:
    if object_name == 'carrot_down':
        tecla = 's'
    elif object_name == 'carrot_up':
        tecla = 'w'
    elif object_name == 'carrot_right':
        tecla = 'd'
    elif object_name == 'carrot_left':
        tecla = 'a'
    wall_positions = []
    row_counter, col_counter = 0, 0
    object_position = (0, 0)
    for row in laberinto:
        for col in row:
            if col == 'P':
                wall_positions.append((row_counter, col_counter))
            elif col == 'carrot_right':
                object_position_r = (row_counter, col_counter)
            elif col == 'carrot_up':
                object_position_u = (row_counter, col_counter)
            elif col == 'carrot_down':
                object_position_d = (row_counter, col_counter)
            elif col == 'carrot_left':
                object_position_l = (row_counter, col_counter)
            col_counter += 1
        col_counter = 0
        row_counter += 1
    row_counter = 0

    for wall in wall_positions:
        if tecla.lower() == 'w':
            if wall[1] == object_position_u[1] and object_position_u[0] == wall[0] + 1:
                return False, object_position_u
        elif tecla.lower() == 'a':
            if wall[0] == object_position_l[0] and wall[1] == object_position_l[1] - 1:
                return False, object_position
        elif tecla.lower() == 's':
            if wall[1] == object_position_d[1] and object_position_d[0] == wall[0] - 1:
                return False, object_position_d
        elif tecla.lower() == 'd':
            if wall[0] == object_position_r[0] and wall[1] == object_position_r[1] + 1:
                return False, object_position_r
    return (True, 'nada', 'nada')


def validar_direccion_wolf(laberinto: list[list], object_name: str,object_position:tuple,carrot_positions:list) -> bool:
    if object_name == 'vertical_wolf_down':
        tecla = 's'
    if object_name == 'vertical_wolf_up':
        tecla = 'w'
    if object_name == 'horizontal_wolf_right':
        tecla = 'd'
    if object_name == 'horizontal_wolf_left':
        tecla = 'a'
    wall_positions = []
    row_counter, col_counter = 0, 0
    for row in laberinto:
        for col in row:
            if col == 'P':
                wall_positions.append((row_counter, col_counter))
            elif col == 'horizontal_wolf_right':
                object_position_r = (row_counter, col_counter)
            elif col == 'horizontal_wolf_left':
                object_position_l = (row_counter, col_counter)
            elif col == 'vertical_wolf_down':
                object_position_d = (row_counter, col_counter)
            elif col == 'vertical_wolf_up':
                object_position_u = (row_counter, col_counter)
            col_counter += 1
        col_counter = 0
        row_counter += 1
    row_counter = 0
    numbers_to_counter = [-5,-4,-3,-2,-1,0,1,+2,+3,+4,+5]
    for wall in wall_positions:

        if tecla.lower() == 'w':
            if wall[1] == object_position[1] and object_position[0] == wall[0] + 1\
                    or str(object_position[0]-1).startswith('carrot'):
                if str(object_position[0]-1).startswith('carrot'):
                    return False, object_position, 'nada'
                else:
                    return False, object_position, 'carrot'
                
        if tecla.lower() == 'd':
            if wall[0] == object_position[0] and object_position[1] == wall[1] - 1\
                    or str(object_position[1]+1).startswith('carrot'):
                if str(object_position[1]+1).startswith('carrot'):
                    return False, object_position, 'nada'
                else:
                    return False, object_position, 'carrot'

        if tecla.lower() == 's':
                if object_position[0]+1 == wall[0] and wall[1] == object_position[1]:
                    return False, object_position, 'nada'
                for carrot in carrot_positions:
                    if object_position[0]+1 == carrot[0]:
                        return False, object_position, 'nada'
                
        if tecla.lower() == 'a':
            if wall[0] == object_position[0] and object_position[1] == wall[1] + 1\
                    or str(object_position[1]-1).startswith('carrot'):
                if str(object_position[1]-1).startswith('carrot'):
                    return False, object_position, 'nada'
                else:
                    return False, object_position, 'carrot'
    return (True, 'nada', 'nada')
