def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    users_not_allowed = usuarios_no_permitidos
    if nombre in users_not_allowed:
        return False
    else:
        return True


def serializar_mensaje(mensaje: str) -> bytearray:
    mensaje_codificado = mensaje.encode('utf-8', 'big')
    return bytearray(mensaje_codificado)


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
    chunk_one = bytearray()
    chunk_two = bytearray()
    chunk_three = bytearray()
    actual_index = 0
    index_direction = 'up'
    for index, byte in enumerate(mensaje):
        byte = byte.to_bytes(1, byteorder='big')

        if actual_index == 0:
            if index_direction == 'up':
                chunk_one.extend(byte)
                actual_index += 1
            elif index_direction == 'down':
                chunk_one.extend(byte)
                index_direction = 'up'

        elif actual_index == 1:
            if index_direction == 'up':
                chunk_two.extend(byte)
                actual_index += 1
            elif index_direction == 'down':
                chunk_two.extend(byte)
                actual_index -= 1

        elif actual_index == 2:
            if index_direction == 'up':
                chunk_three.extend(byte)
                index_direction = 'down'
            elif index_direction == 'down':
                chunk_three.extend(byte)
                actual_index -= 1

    first_byte_A = chunk_one[0]
    last_byte_B = chunk_two[-1]
    first_byte_C = chunk_three[0]
    ACBsum = first_byte_A+last_byte_B+first_byte_C

    if int(ACBsum) % 2 == 0:
        return [chunk_one, chunk_two, chunk_three]
    else:
        return [chunk_one, chunk_two, chunk_three]


def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    separar_result = separar_mensaje(mensaje)
    one, two, three = separar_result[0], separar_result[1], separar_result[2]
    first_byte_one = one[0]
    last_byte_two = two[-1]
    first_byte_three = three[0]
    total_sum = first_byte_one+last_byte_two+first_byte_three
    byte_1 = bytearray(b'\x01')
    byte_0 = bytearray(b'\x00')
    if total_sum % 2 == 0:
        response = bytearray()
        response.extend(byte_1)
        response.extend(one)
        response.extend(three)
        response.extend(two)
        return response
    else:
        response = bytearray()
        response.extend(byte_0)
        response.extend(two)
        response.extend(one)
        response.extend(three)
        return response


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    mensaje_tomado = mensaje
    largo_mensaje_bytes = len(mensaje_tomado).to_bytes(4, 'big')
    num_of_block = 1
    list_to_send = list()
    list_to_send.append(bytearray(largo_mensaje_bytes))

    while len(mensaje_tomado) > 36:
        list_to_send.append(bytearray(num_of_block.to_bytes(4, 'big')))
        list_to_send.append(mensaje_tomado[0:36])
        mensaje_tomado = mensaje_tomado[36:]
        num_of_block += 1
    if len(mensaje_tomado) <= 36:
        list_to_send.append(bytearray(num_of_block.to_bytes(4, 'big')))
        list_to_send.append(
            mensaje_tomado + bytearray(b'\x00'*(36-len(mensaje_tomado))))

    return list_to_send
