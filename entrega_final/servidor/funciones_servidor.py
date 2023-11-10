def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    users_not_allowed = usuarios_no_permitidos
    if nombre in users_not_allowed:
        return False
    else:
        return True


def serializar_mensaje(mensaje: str) -> bytearray:
    mensaje_codificado = mensaje.encode('utf-8', 'big')
    return bytearray(mensaje_codificado)

def deserializar_mensaje(mensaje: bytearray) -> str:
    mensaje_codificado = mensaje.decode('utf-8','big')
    return mensaje_codificado


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
    
def recuperar_orden(chunks: tuple, orden: str) -> bytearray:
    mensaje_ordenado = bytearray()
    mensaje = chunks[0]+chunks[1]+chunks[2]
    try:
        if orden == 'ACB':
            chunk_A = chunks[0]
            chunk_C = chunks[2]
            chunk_B = chunks[1]
            mensaje = chunk_A+chunk_C+chunk_B
            actual_index = 0
            index_direction = 'up'
            for index, byte in enumerate(mensaje):
                byte = byte.to_bytes(1, byteorder='big')
                if actual_index == 0:
                    if index_direction == 'up':
                        byte = chunk_A.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        actual_index += 1
                    elif index_direction == 'down':
                        byte = chunk_A.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        index_direction = 'up'

                elif actual_index == 1:
                    if index_direction == 'up':
                        byte = chunk_C.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        actual_index += 1
                    elif index_direction == 'down':
                        byte = chunk_C.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        actual_index -= 1

                elif actual_index == 2:
                    if index_direction == 'up':
                        byte = chunk_B.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        index_direction = 'down'
                    elif index_direction == 'down':
                        byte = chunk_B.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        actual_index -= 1
        elif orden == 'BAC':
            chunk_B = chunks[1]
            chunk_A = chunks[0]
            chunk_C = chunks[2]
            actual_index = 0
            
            index_direction = 'up'
            for index, byte in enumerate(mensaje):
                byte = byte.to_bytes(1, byteorder='big')
                if actual_index == 0:
                    if index_direction == 'up':
                        byte = chunk_B.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        actual_index += 1
                    elif index_direction == 'down':
                        byte = chunk_B.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        index_direction = 'up'

                elif actual_index == 1:
                    if index_direction == 'up':
                        byte = chunk_A.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        actual_index += 1
                    elif index_direction == 'down':
                        byte = chunk_A.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        actual_index -= 1

                elif actual_index == 2:
                    if index_direction == 'up':
                        byte = chunk_C.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        index_direction = 'down'
                    elif index_direction == 'down':
                        byte = chunk_C.pop(0).to_bytes(1, byteorder='big')
                        mensaje_ordenado.extend(byte)
                        actual_index -= 1 
    except Exception as err:
        print('Error en recuperar orden, error tipo Exception: ',err)
        return mensaje_ordenado
    return mensaje_ordenado

def encriptar_mensaje(mensaje: bytearray) -> list[bytearray]:
    separar_result = separar_mensaje(mensaje)
    one, two, three = separar_result[0], separar_result[1], separar_result[2]
    first_byte_one = one[0]
    last_byte_two = two[-1]
    first_byte_three = three[0]
    total_sum = first_byte_one+last_byte_two+first_byte_three
    byte_1 = bytearray(b'\x01')
    byte_0 = bytearray(b'\x00')
    list_to_send = list()
    if total_sum % 2 == 0:
        response = bytearray()
        response.extend(byte_1)
        list_to_send.append(byte_1)
        response.extend(one)
        list_to_send.append(one)
        response.extend(three)
        list_to_send.append(three)
        response.extend(two)
        list_to_send.append(two)
        return list_to_send, response
    else:
        response = bytearray()
        response.extend(byte_0)
        list_to_send.append(byte_0)
        response.extend(two)
        list_to_send.append(two)
        response.extend(one)
        list_to_send.append(one)
        response.extend(three)
        list_to_send.append(three)
        return list_to_send, response

def desencriptar_mensaje(mensaje: list[bytearray], chunks: tuple) -> bytearray:
    mensaje_inicio = mensaje.pop(0)
    longitud = len(mensaje)
    tercio = longitud // 3
    if mensaje_inicio == 0: # Si el primer byte es 0, entonces el mensaje esta en orden nBAC, con n = 0
        orden = 'BAC'
    elif mensaje_inicio == 1: # Si el primer byte es 1, entonces el mensaje esta en orden nACB, con n = 1
        orden = 'ACB'
    if orden == 'BAC':
        mensaje = (chunks[0],chunks[1],chunks[2])
    elif orden == 'ACB':
        mensaje = (chunks[0],chunks[1],chunks[2])
        
    mensaje_ordenado = recuperar_orden(mensaje, orden)
    return mensaje_ordenado



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

def decodificar_mensaje(lista_codificada: list[bytearray]) -> bytearray:
    mensaje_decodificado = bytearray()
    largo_mensaje = int.from_bytes(mensaje_codificado[0])
    num_of_block = int.from_bytes(mensaje_codificado[1])
    list_to_recive = list()
    # list_to_recive.append(bytearray(largo_mensaje))
    if len(lista_codificada) > 3:
        lista_codificada.pop(0)
        while len(lista_codificada) > 3:
            actual_num_of_block = lista_codificada.pop(0)
            actual_mensaje_part = lista_codificada.pop(0)
            list_to_recive.append(actual_mensaje_part)
            lista_codificada.pop(0) #Elimina el mensaje actual
            lista_codificada.pop(0) #Elimina el numero de bloque actual o bytes de relleno
    else:
        list_to_recive.append(lista_codificada[2])
    for elem in list_to_recive:
        mensaje_decodificado += elem
    print(len(mensaje_decodificado))
    if len(mensaje_decodificado) < 36:
        mensaje_decodificado += bytearray(b'\x00'*(36-len(mensaje_decodificado)))
    return mensaje_decodificado, largo_mensaje

strr = 'aHOLA me llamo joseee j'
print(len(strr))
mensaje_serializado = serializar_mensaje(strr)
print('seriali', mensaje_serializado)
mensaje_encripado = encriptar_mensaje(mensaje_serializado)
mensaje_codificado = codificar_mensaje(mensaje_encripado[1])

print('msj encripado  ',mensaje_encripado[0][0],mensaje_encripado[0][1],mensaje_encripado[0][2],mensaje_encripado[0][3])
print('-------------------')
mensaje_recibido_del_server,largo_mensaje = decodificar_mensaje(mensaje_codificado)
mensaje_recibido_del_server = mensaje_recibido_del_server[0:largo_mensaje]
print('aa',mensaje_codificado[2])
print('',mensaje_recibido_del_server)
chunks = (mensaje_encripado[0][1],mensaje_encripado[0][2],mensaje_encripado[0][3])
mensaje_desencriptado = desencriptar_mensaje(mensaje_recibido_del_server, chunks)
print('msj desencripado',mensaje_desencriptado)

print('msj deserializadoOO',deserializar_mensaje(mensaje_desencriptado))