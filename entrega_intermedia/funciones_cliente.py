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


def riesgo_mortal(laberinto: list[list]) -> bool:
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


def validar_direccion(laberinto: list[list], tecla: str) -> bool:
    wall_positions = []
    row_counter, col_counter = 0, 0
    rabbit_position = (0, 0)
    for row in laberinto:
        for col in row:
            if col == 'P':
                wall_positions.append((row_counter, col_counter))
            elif col == 'C':
                rabbit_position = (row_counter, col_counter)
            col_counter += 1
        col_counter = 0
        row_counter += 1
    row_counter = 0
    for wall in wall_positions:
        if tecla.lower() == 'w':
            if wall[1] == rabbit_position[1] and rabbit_position[0] == wall[0] + 1:
                return False
        elif tecla.lower() == 'a':
            if wall[0] == rabbit_position[0] and wall[1] == rabbit_position[1] - 1:
                return False
        elif tecla.lower() == 's':
            if wall[1] == rabbit_position[1] and rabbit_position[0] == wall[0] - 1:
                return False
        elif tecla.lower() == 'd':
            if wall[0] == rabbit_position[0] and wall[1] == rabbit_position[1] + 1:
                return False
    return True
