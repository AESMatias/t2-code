from parametros import VELOCIDAD_CONEJO, PUNTAJE_INF, PUNTAJE_LOBO,DURACION_NIVEL_INICIAL, CANTIDAD_VIDAS, PONDERADOR_LABERINTO_1, PONDERADOR_LABERINTO_2, PONDERADOR_LABERINTO_3, ANCHO_LABERINTO, DURACION_NIVEL_INICIAL, VELOCIDAD_ZANAHORIA, VELOCIDAD_LOBO
from cliente.backend.movements import Carrot_Motion
from cliente.backend.funciones_cliente import validar_direccion, validate_enemy_colision, has_reached_end
import os
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap, QCursor
from frontend.Components.buttons import Enter_Button
import sys
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from Styles.styles import button_style,fama_style
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path_derrota = QUrl.fromLocalFile(os.path.join(
    project_root, 'assets', 'sonidos', 'derrota.wav'))
path_victoria = QUrl.fromLocalFile(os.path.join(
    project_root,'assets', 'sonidos', 'victoria.wav'))


class Frame_Game(QWidget):
    signal_infinite_cheat = QtCore.pyqtSignal(str)
    signal_cheat_delete = QtCore.pyqtSignal(str)
    signal_pause_game = QtCore.pyqtSignal(str)
    level_up = QtCore.pyqtSignal(str,int,int)
    signal_user_valid = QtCore.pyqtSignal(str,str,int)
    signal_pickup_item = QtCore.pyqtSignal(tuple)
    signal_has_lost = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tablero_items = []
        self.timer_duracion = QTimer(self)
        self.tiempo_restante = DURACION_NIVEL_INICIAL
        self.items_inventario = []
        self.enemies_deleted = False
        self.is_game_paused = False
        self.duracion_nivel = DURACION_NIVEL_INICIAL
        self.login_button = Enter_Button(
            name='exitButton', text='Salir', username='usernameeeee')
        self.setStyleSheet("background-color: rgba(140, 0, 150, 255);")
        self.pause_button = Enter_Button(
            name='pauseButton', text='Salir', username='usernameeeee')
        self.setStyleSheet("background-color: rgba(140, 0, 150, 255);")
        self.setWindowIcon(
            QIcon(os.path.join('assets', 'sprites', 'icon.png')))
        self.last_keys_pressed = [0, 0, 0]
        self.nivel = 1
        self.puntaje_nivel = 0 # luego se actualiza con el puntaje del nivel y se usa correctamente.
        self.lobos_eliminados = 0
        self.movement_is_allowed = True
        self.vidas = CANTIDAD_VIDAS
        self.level_time = DURACION_NIVEL_INICIAL
        self.velocidad_conejo_ms = int(1000/VELOCIDAD_CONEJO)
        self.velocidad_zanahoria = int(1000/VELOCIDAD_ZANAHORIA)
        self.conejopixmap = QPixmap(os.path.join(
            project_root, 'assets', 'sprites', 'conejo.png')).scaled(
            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.piso_pixmap = QPixmap(os.path.join(
            project_root,'assets', 'sprites', 'bloque_fondo.jpeg'))
        # self.init_gui()
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        # Monitor dimensions
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        self.labels = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_rabbit)
        self.last_key_pressed = None
        self.counter_sprints = 1
        self.Carrot_Motion2 = Carrot_Motion(self)
        # This allows to play the victory sound
        self.victory = QMediaPlayer(self)
        self.victory.setAudioOutput(QAudioOutput(self))
        self.victory.setSource(path_victoria)
        # This allows to play the defeat sound
        self.defeat = QMediaPlayer(self)
        self.defeat.setAudioOutput(QAudioOutput(self))
        self.defeat.setSource(path_derrota)

    def pause_game(self) -> None:
        if self.is_game_paused == False:
            self.timer_duracion.stop()
            self.is_game_paused = True
            self.movement_is_allowed = False
            if self.enemies_deleted == False:
                self.timer.stop()
                self.Carrot_Motion2.timer.stop()
                self.Carrot_Motion2.timer_wolf.stop()
                for wolve_timer in self.Carrot_Motion2.wolves_timers:
                    wolve_timer.stop()
        else:
            self.timer_duracion.start(1000)
            self.is_game_paused = False
            self.movement_is_allowed = True
            self.timer.start(self.velocidad_conejo_ms)
            if self.enemies_deleted == False:
                self.Carrot_Motion2.timer.start(self.velocidad_zanahoria)
                self.Carrot_Motion2.timer_wolf.start(
                    self.Carrot_Motion2.wolf_velocity)
                for wolve_timer in self.Carrot_Motion2.wolves_timers:
                    wolve_timer.start()

    def ES_USUARIO_VALIDO(self, username) -> bool:
        return True
    
    def receive_username(self, sender) -> None:
        self.username = sender
        self.stats_label.setText(
            f'Bienvenido/a {self.username}\nTe quedan {self.vidas} vidas')
        if self.ES_USUARIO_VALIDO(self.username) == True:
            self.signal_user_valid.emit(f'{self.username}', 'localhost', self.port)
            
    def pickup_item(self, rabbit_position) -> None:
        for idx_row, row in enumerate(self.tablero_items):
            for idx_col, col in enumerate(row):
                if col == 'BM' and self.tablero_grande[idx_row][idx_col] == 'C' or \
                    col == 'BC' and self.tablero_grande[idx_row][idx_col] == 'C':
                    self.tablero_items[idx_row][idx_col] = '-'
                    self.tablero_grande[idx_row][idx_col] = 'C'
                    self.labels[idx_row][idx_col].setPixmap(
                        self.piso_pixmap)
                    self.items_inventario.append(col)
        if len(self.items_inventario) >0:
            self.stats_label.setText(
            f'Bienvenido/a {self.username}\nTe quedan {self.vidas} vidas\nTienes \
                {len(self.items_inventario)} items en tu inventario\
                    \n{self.items_inventario}')

    def play_victory_sound(self) -> None:
        self.victory.play()

    def play_defeat_sound(self) -> None:
        self.defeat.play()
    def archivo_txt(self) -> None:
        if self.lobos_eliminados>0:
            self.puntaje = ( (self.tiempo_restante)*self.vidas)/ (self.lobos_eliminados)*PUNTAJE_LOBO
            round(self.puntaje,2)
        else:
            self.puntaje = 0
        try:
            archivo_puntaje_ruta = os.path.join(project_root,'puntajes.txt')
            with open(archivo_puntaje_ruta, 'a') as file:
                file.write(f'{self.username} | {self.nivel-1} | {self.puntaje}\n')
        except FileNotFoundError:
            print('No se ha encontrado el archivo', FileNotFoundError)
        
    def infinite_cheat(self) -> None:
        self.vidas = float('inf')
        self.timer_duracion.stop()
        if self.vidas == float('inf'):
            self.stats_label.setText(
                f'Bienvenido/a {self.username}\nTienes vidas infinitas')
        self.puntaje_nivel = PUNTAJE_INF
            
    def has_lost(self) -> None:
        self.play_defeat_sound()
        self.timer.stop()
        self.movement_is_allowed = False
        self.stats_label.setText(
                                f'Bienvenido/a {self.username}\nTe quedan {self.vidas} vidas\nHas perdido el juego')
        
    def timer_duracion_func(self) -> None:
        if self.tiempo_restante == 0:
            self.signal_has_lost.emit()
            self.timer_duracion.stop()
        self.stats_counter_label.setText('Tiempo restante: '+str(self.tiempo_restante))
        self.tiempo_restante -= 1
        
    def move_rabbit(self):
        key = self.last_key_pressed
        if self.counter_sprints == 4:
            self.counter_sprints = 1
        if key not in ['A', 'S', 'D', 'W']:
            pass
        elif key in ['A', 'S', 'D', 'W']:
            self.is_valid_movement, rabbit_position = validar_direccion(
                self.tablero_grande, key, self.entrada)
            self.has_colisionated_an_enemy, rabbit_position = validate_enemy_colision(
                self.tablero_grande, key)
            self.has_reached_end, rabbit_position = has_reached_end(
                self.tablero_grande, key, self.salida)
            if self.has_reached_end == True:
                self.is_valid_movement = False
                self.stats_label.setText(
                    f'Bienvenido/a {self.username}\nTe quedan {self.vidas} vidas')
                if self.nivel == 3:  # Then, the user has won the game
                    self.play_victory_sound()
                    self.timer.stop()
                    self.movement_is_allowed = False
                    self.stats_label.setText(
                        f'Bienvenido/a {self.username}\nTe quedan {self.vidas} vidas\nHas ganado el juego')

                if self.nivel < 4:
                    self.nivel += 1
                    for row in self.tablero_grande:
                        if 'C' in row:
                            # Cambia el conejo por piso
                            row[row.index('C')] = '-'
                            self.timer.disconnect()
                            self.timer.stop()
                            self.movement_is_allowed = False
                            
                            self.archivo_txt()
                    self.timer.stop()
                    self.timer.deleteLater()
                    self.Carrot_Motion2.timer.stop()
                    self.Carrot_Motion2.timer.deleteLater()
                    self.Carrot_Motion2.timer_wolf.stop()
                    self.Carrot_Motion2.timer_wolf.deleteLater()
                    self.Carrot_Motion2.delete_mobs()
                    self.Carrot_Motion2.deleteLater()
                    self.another_gui(self.nivel)
                    self.level_up.emit(self.name,self.nivel,self.puntaje)
            elif self.has_colisionated_an_enemy == True:
                self.timer.stop
                self.last_key_pressed = None  # Esto asegura que la ultima tecla presionada
                # No se cuente, por lo que el conejo no se mueve al volver al inicio
                self.vidas -= 1
                self.is_valid_movement = False
                for idx, label_list in enumerate(self.labels):
                    if idx == self.rabbit_position[0]:
                        for i in range(len(label_list)):
                            if i == self.rabbit_position[1]:
                                self.last_pixmap = label_list[self.rabbit_position[1]].pixmap(
                                )
                                self.piso_pixmap = QPixmap(os.path.join(project_root,'assets', 'sprites', 'bloque_fondo.jpeg')).scaled(
                                    100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                                self.conejo_pixmap = QPixmap(os.path.join(project_root,'assets', 'sprites', 'conejo.png')).scaled(
                                    100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                                self.combined_pixmap = QPixmap(
                                    self.piso_pixmap.size())
                                with QPainter(self.combined_pixmap) as painter:
                                    painter.drawPixmap(
                                        0, 0, self.piso_pixmap)
                                    painter.drawPixmap(
                                        0, 0, self.conejo_pixmap)

                                self.labels[idx][i].setPixmap(
                                    self.piso_pixmap)
                                self.tablero_grande[idx][i] = '-'
                                self.tablero_grande[self.entrada[0]
                                                    ][self.entrada[1]] = 'C'
                                self.rabbit_position = (
                                    self.entrada[0], self.entrada[1])
                                self.labels[self.entrada[0]][self.entrada[1]].setPixmap(
                                    self.combined_pixmap)
                                if self.vidas == 0:
                                    self.signal_has_lost.emit()
                                elif self.vidas == float('inf'):
                                    self.stats_label.setText(
                                        f'Bienvenido/a {self.username}\nTienes vidas infinitas')
                                else:
                                    self.stats_label.setText(
                                        f'Bienvenido/a {self.username}\nTe quedan {self.vidas} vidas')
            if self.movement_is_allowed == True:
                
                if key == 'D':
                    mov_y = 0
                    mov_x = +1
                    self.conejopixmap = QPixmap(os.path.join(
                        project_root,'assets', 'sprites', f'conejo_derecha_{self.counter_sprints}.png'))
                elif key == 'A':
                    mov_y = 0
                    mov_x = -1
                    self.conejopixmap = QPixmap(os.path.join(
                        project_root, 'assets', 'sprites', f'conejo_izquierda_{self.counter_sprints}.png'))
                elif key == 'W':
                    mov_y = -1
                    mov_x = 0
                    self.conejopixmap = QPixmap(os.path.join(
                        project_root, 'assets', 'sprites', f'conejo_arriba_{self.counter_sprints}.png'))
                elif key == 'S':
                    mov_y = +1
                    mov_x = 0
                    self.conejopixmap = QPixmap(os.path.join(
                        project_root,'assets', 'sprites', f'conejo_abajo_{self.counter_sprints}.png'))
                    
                self.conejopixmap = self.conejopixmap.scaled(
                    100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                self.counter_sprints += 1
                
                if self.is_valid_movement == True:
                    next_pos = self.tablero_items[self.rabbit_position[0]+mov_y][self.rabbit_position[1]+mov_x]
                    if next_pos == 'BM':
                        self.tablero_items[self.rabbit_position[0]+mov_y
                                            ][self.rabbit_position[1]+mov_x] = 'BM'
                    self.tablero_grande[self.rabbit_position[0]+mov_y
                                        ][self.rabbit_position[1]+mov_x] = 'C'
                    self.rabbit_position = self.rabbit_position[0] + \
                        mov_y, self.rabbit_position[1]+mov_x
                    for idx, label_list in enumerate(self.labels):
                        if idx == self.rabbit_position[0]:
                            for i in range(len(label_list)):
                                if i == self.rabbit_position[1]:
                                    self.last_pixmap = label_list[self.rabbit_position[1]].pixmap(
                                    )
                                    manzana_conejo_pixmap = QPixmap(self.piso_pixmap.size())
                                    with QPainter(manzana_conejo_pixmap) as painter:
                                        painter.drawPixmap(0, 0, self.manzana_pixmap)
                                        painter.drawPixmap(0, 0, self.combined_pixmap)
                                    
                                    if self.last_pixmap != os.path.join(
                                            project_root,'assets', 'sprites', 'conejo.png'):
                                        self.combined_pixmap = QPixmap(
                                            self.piso_pixmap.size())
                                        with QPainter(self.combined_pixmap) as painter:
                                            painter.drawPixmap(
                                                0, 0, self.piso_pixmap)
                                            painter.drawPixmap(
                                                0, 0, self.conejopixmap)
                                        label_list[self.rabbit_position[1]].setPixmap(
                                            self.combined_pixmap)
                                        self.labels[idx-mov_y][i-mov_x].setPixmap(
                                            self.last_pixmap)
                                        self.labels[idx-mov_y][i-mov_x].setPixmap(
                                            self.piso_pixmap)
                                        self.tablero_grande[idx -
                                                            mov_y][i-mov_x] = '-'
                                        self.last_row = idx-mov_y
                                        self.last_col = i-mov_x
                                    if next_pos == 'BM':
                                        self.labels[self.rabbit_position[0]][self.rabbit_position[1]]\
                        .setPixmap(self.manzana_pixmap)

                                        self.labels[idx][i].setPixmap(manzana_conejo_pixmap)
                else:
                    if self.last_key_pressed == 'D':
                        self.conejo_pixmap = QPixmap(os.path.join(
                            project_root, 'assets', 'sprites', 'conejo_derecha_1.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    elif self.last_key_pressed == 'A':
                        self.conejo_pixmap = QPixmap(os.path.join(
                            project_root, 'assets', 'sprites', 'conejo_izquierda_1.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    elif self.last_key_pressed == 'W':
                        self.conejo_pixmap = QPixmap(os.path.join(
                            project_root, 'assets', 'sprites', 'conejo_arriba_1.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    elif self.last_key_pressed == 'S':
                        self.conejo_pixmap = QPixmap(os.path.join(
                            project_root, 'assets', 'sprites', 'conejo_abajo_1.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                    self.tablero_grande[self.rabbit_position[0]
                                        ][self.rabbit_position[1]] = 'C'
                    self.rabbit_position = self.rabbit_position[0], self.rabbit_position[1]
                    for idx, label_list in enumerate(self.labels):
                        if idx == self.rabbit_position[0]:
                            for i in range(len(label_list)):
                                if i == self.rabbit_position[1]:
                                    self.last_pixmap = label_list[self.rabbit_position[1]].pixmap(
                                    )
                                    self.combined_pixmap_conejoD = QPixmap(
                                        self.piso_pixmap.size())

                                    self.piso_pixmap = QPixmap(os.path.join(
                                        project_root,'assets', 'sprites', 'bloque_fondo.jpeg')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                                    with QPainter(self.combined_pixmap_conejoD) as painter:
                                        painter.drawPixmap(
                                            0, 0, self.piso_pixmap)
                                        painter.drawPixmap(
                                            0, 0, self.conejo_pixmap)

                                    label_list[self.rabbit_position[1]].setPixmap(
                                        self.combined_pixmap_conejoD)
                                    self.labels[idx][i].setPixmap(
                                        self.combined_pixmap_conejoD)

                                    self.tablero_grande[idx][i] = 'C'

    def keyPressEvent(self, event) -> None:
        if self.movement_is_allowed == True:
            if event.key() == Qt.Key.Key_D:
                self.last_key_pressed = 'D'
                self.move_rabbit()
                self.timer.start(self.velocidad_conejo_ms)
                self.last_keys_pressed.append(self.last_key_pressed)

            elif event.key() == Qt.Key.Key_A:
                self.last_key_pressed = 'A'
                self.move_rabbit()
                self.timer.start(self.velocidad_conejo_ms)
                self.last_keys_pressed.append(self.last_key_pressed)
                
            elif event.key() == Qt.Key.Key_W:
                self.last_key_pressed = 'W'
                self.move_rabbit()
                self.timer.start(self.velocidad_conejo_ms)
                self.last_keys_pressed.append(self.last_key_pressed)

            elif event.key() == Qt.Key.Key_S:
                self.last_key_pressed = 'S'
                self.move_rabbit()
                self.timer.start(self.velocidad_conejo_ms)
                self.last_keys_pressed.append(self.last_key_pressed)
                
        # Checks if the cheat code or paused is pressed
        if event.key() == Qt.Key.Key_K:
            self.last_keys_pressed.append('K')
        elif event.key() == Qt.Key.Key_I:
            self.last_keys_pressed.append('I')
        elif event.key() == Qt.Key.Key_G:
            self.last_keys_pressed.append('G')
            self.signal_pickup_item.emit(self.rabbit_position)
        elif event.key() == Qt.Key.Key_L:
            self.last_keys_pressed.append('L')
        elif event.key() == Qt.Key.Key_N:
            self.last_keys_pressed.append(
                'N')
        elif event.key() == Qt.Key.Key_F:
            self.last_keys_pressed.append('F')
        if event.key() == Qt.Key.Key_P:
            self.last_key_pressed = 'P'
            self.last_keys_pressed.append(self.last_key_pressed)
            self.signal_pause_game.emit('pause')
        if self.last_keys_pressed[-1] == 'L':
            if self.last_keys_pressed[-2] == 'I':
                if self.last_keys_pressed[-3] == 'K':
                    self.signal_cheat_delete.emit('Activated')
                    self.enemies_deleted = True
        if self.last_keys_pressed[-1] == 'F':
            if self.last_keys_pressed[-2] == 'N':
                if self.last_keys_pressed[-3] == 'I':
                    self.signal_infinite_cheat.emit('Activated')
        
    def another_gui(self, nivel) -> None:  # Esto renueva el tablero y los pixmap al pasar de nivel
        self.Carrot_Motion2 = Carrot_Motion(self)
        self.setWindowIcon(
            QIcon(os.path.join('frontend','assets', 'sprites', 'icon.png')))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_rabbit)
        self.tablero_grande = []  # Limpia el tablero para renovarlo con el sig level
        # Window Geometry
        self.setFocus()
        self.nivel = nivel
        self.setGeometry(100, 200, 1280, 720)
        # Login
        self.login_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_button.setText('Salir')
        self.pause_button.setText('Pausar')
        self.pause_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        ruta_al_archivo = os.path.join(
            project_root,  'assets', 'laberintos', f'tablero_{self.nivel}.txt')
        if ruta_al_archivo.endswith('_1.txt'):
            self.nivel = 1
            self.wolf_velocity = int(VELOCIDAD_LOBO/PONDERADOR_LABERINTO_1)
        if ruta_al_archivo.endswith('_2.txt'):
            self.nivel = 2
            self.duracion_nivel = int(DURACION_NIVEL_INICIAL*PONDERADOR_LABERINTO_2)
            self.tiempo_restante = int(self.duracion_nivel)
            self.wolf_velocity = int(VELOCIDAD_LOBO/PONDERADOR_LABERINTO_2)
            self.timer_duracion.start(1000)
            # self.wolf_velocity = int(self.wolf_velocity/PONDERADOR_LABERINTO_2)
        if ruta_al_archivo.endswith('_3.txt'):
            self.nivel = 3
            duracion_nivel_2 = (self.duracion_nivel)
            self.duracion_nivel = int(duracion_nivel_2*PONDERADOR_LABERINTO_3)
            self.tiempo_restante = int(self.duracion_nivel)
            self.wolf_velocity = int(VELOCIDAD_LOBO/PONDERADOR_LABERINTO_3)
            self.timer_duracion.start(1000)
            # self.wolf_velocity = int(self.wolf_velocity/PONDERADOR_LABERINTO_3)
        self.tablero = []
        if self.nivel<4: #If the user has not won the game, then the game continues
            try:
                with open(ruta_al_archivo, "r") as archivo:
                    contenido = archivo.read()
                    self.tablero = contenido
            except FileNotFoundError:
                print("El archivo no se encontró en la ubicación especificada.")
            except Exception as e:
                print(f"Ocurrió un error al abrir el archivo: {e}")
            self.tablero.replace('\n', '')
            tablero_splitted = self.tablero.split(',')

            temporal_array = []
            temporal_array2 = []
            idxx = 0
            for _ in tablero_splitted:
                while len(tablero_splitted) > 0:
                    if idxx <= ANCHO_LABERINTO-1:
                        first_item = tablero_splitted.pop(0)
                        if first_item.__contains__('\n'):
                            first_item = first_item.replace('\n', '')
                        temporal_array.append(first_item)
                        idxx += 1
                    else:
                        self.tablero_grande.append(temporal_array)
                        self.tablero_items.append(temporal_array2)
                        temporal_array = []
                        temporal_array2 = []
                        idxx = 0
            for idx_row, row in enumerate(self.tablero_grande):
                for idx_col, col in enumerate(row):
                    label = self.labels[idx_row][idx_col]
                    if col == 'P':
                        label.setText('P')
                        label.setPixmap(QPixmap(os.path.join(
                            project_root,'assets', 'sprites', 'bloque_pared.jpeg')))
                    elif col == 'E':
                        label.setText('E')
                        label.setPixmap(self.piso_pixmap)
                        self.entrada = (idx_row, idx_col)
                    elif col == 'S':
                        label.setText('S')
                        label.setPixmap(self.piso_pixmap)
                        self.salida = (idx_row, idx_col)
                    elif col == '-':
                        label.setText('-')
                        label.setPixmap(self.piso_pixmap)

                    elif col == 'C':
                        label.setText('C')
                        label.setPixmap(self.conejopixmap)
                        painter = QPainter(self.combined_pixmap)
                        painter.drawPixmap(0, 0, self.piso_pixmap)
                        painter.drawPixmap(0, 0, self.conejopixmap)
                        label.setPixmap(self.combined_pixmap)
                        self.rabbit_position = (idx_row, idx_col)

                    elif col == 'LV':
                        label.setText('LV')
                        piso_pixmap = self.piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        v_wolf_pixmap = QPixmap(os.path.join(
                            project_root,'assets', 'sprites', 'lobo_vertical_abajo_1.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        combined_pixmap = QPixmap(piso_pixmap.size())
                        with QPainter(combined_pixmap) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, v_wolf_pixmap)
                        label.setPixmap(combined_pixmap)
                    elif col == 'LH':
                        label.setText('LH')
                        piso_pixmap = self.piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        h_wolf_pixmap = QPixmap(os.path.join(
                            project_root, 'assets', 'sprites', 'lobo_horizontal_derecha_1.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        combined_pixmap = QPixmap(piso_pixmap.size())
                        with QPainter(combined_pixmap) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, h_wolf_pixmap)
                        label.setPixmap(combined_pixmap)
                    elif col == 'BM':
                        label.setText('BM')
                        piso_pixmap = self.piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        apple_pixmap = QPixmap(os.path.join(
                            project_root, 'assets', 'sprites', 'manzana.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        combined_pixmap = QPixmap(piso_pixmap.size())
                        with QPainter(combined_pixmap) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, apple_pixmap)
                        label.setPixmap(combined_pixmap)
                        self.manzana_pixmap = combined_pixmap
                        self.tablero_grande[idx_row][idx_col] = 'BM'
                        self.tablero_items[idx_row][idx_col] = 'BM'
                    elif col == 'BC':
                        label.setText('BC')
                        piso_pixmap = self.piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        freeze_bomb_pixmap = QPixmap(os.path.join(
                            project_root, 'assets', 'sprites', 'congelacion.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        combined_pixmap = QPixmap(piso_pixmap.size())
                        with QPainter(combined_pixmap) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, freeze_bomb_pixmap)
                        label.setPixmap(combined_pixmap)
                        self.tablero_grande[idx_row][idx_col] = 'BC'
                    elif col == 'CU':
                        label.setText('CU')
                        piso_pixmap = self.piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        canyon_pixmap = QPixmap(os.path.join(
                            project_root,'assets', 'sprites', 'canon_arriba.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        combined_pixmap = QPixmap(piso_pixmap.size())
                        with QPainter(combined_pixmap) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(7, 0, canyon_pixmap)
                        label.setPixmap(combined_pixmap)
                        self.tablero_grande[idx_row][idx_col] = 'CU'

                    elif col == 'CD':
                        label.setText('CD')
                        piso_pixmap = self.piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        canyon_pixmap = QPixmap(os.path.join(
                            project_root, 'assets', 'sprites', 'canon_abajo.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                        combined_pixmap = QPixmap(piso_pixmap.size())
                        with QPainter(combined_pixmap) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(7, 0, canyon_pixmap)
                        label.setPixmap(combined_pixmap)
                        self.tablero_grande[idx_row][idx_col] = 'CD'

                    elif col == 'CL':
                        piso_pixmap = self.piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        canyon_pixmap = QPixmap(os.path.join(
                            project_root,'assets', 'sprites', 'canon_izquierda.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                        combined_pixmap = QPixmap(piso_pixmap.size())
                        with QPainter(combined_pixmap) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 7, canyon_pixmap)
                        label.setPixmap(combined_pixmap)
                        self.tablero_grande[idx_row][idx_col] = 'CL'
                    elif col == 'CR':
                        piso_pixmap = self.piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        canyon_pixmap = QPixmap(os.path.join(
                            project_root, 'assets', 'sprites', 'canon_derecha.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                        combined_pixmap = QPixmap(piso_pixmap.size())
                        with QPainter(combined_pixmap) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 7, canyon_pixmap)
                        label.setPixmap(combined_pixmap)
                        self.tablero_grande[idx_row][idx_col] = 'CR'
            self.movement_is_allowed = True
            #Conectamos nuevamente las senales para no perder el bindeo a la referencia al nuevo objeto
            self.Carrot_Motion2.start_carrot_motion(
                self.velocidad_zanahoria, self.wolf_velocity, self.tablero_grande, self.labels)
            self.signal_cheat_delete.connect(self.Carrot_Motion2.delete_mobs)
            self.signal_cheat_delete.connect(
                self.Carrot_Motion2.timer_wolf.stop)


    def init_gui(self) -> None:
        # Window Geometry
        self.setFocus()
        self.setGeometry(100, 200, 1280, 720)
        self.setWindowTitle(
            f'DCConejoChico - Game - Nivel {self.nivel}')
        self.setWindowIcon(
            QIcon(os.path.join('frontend','assets', 'sprites', 'icon.png')))
        # Login
        self.login_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_button.setStyleSheet(button_style)
        self.login_button.setText('Salir')
        # Pause
        self.pause_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pause_button.setStyleSheet(button_style)
        self.pause_button.setText('Pausar')
        # Information label
        self.stats_label = QLabel(
            f'Te quedan {self.vidas} vidas', self)
        self.stats_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet(fama_style)
        self.stats_label.setFixedWidth(500)
        # Tiempo restante label
        self.stats_counter_label = QLabel(
            f'Tiempo restante: {self.level_time}', self)
        self.stats_counter_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.stats_counter_label.setStyleSheet(fama_style)
        self.stats_counter_label.setFixedWidth(500)

        ruta_al_archivo = os.path.join(project_root, 'assets', 'laberintos', f'tablero_{self.nivel}.txt')
        if ruta_al_archivo.endswith('_1.txt'):
            self.nivel = 1
            self.wolf_velocity = int(VELOCIDAD_LOBO/PONDERADOR_LABERINTO_1)
        if ruta_al_archivo.endswith('_2.txt'):
            self.nivel = 2
            self.wolf_velocity = int(VELOCIDAD_LOBO/PONDERADOR_LABERINTO_2)
            # self.wolf_velocity = int(self.wolf_velocity/PONDERADOR_LABERINTO_2)
        if ruta_al_archivo.endswith('_3.txt'):
            self.nivel = 3
            self.wolf_velocity = int(VELOCIDAD_LOBO/PONDERADOR_LABERINTO_3)
            # self.wolf_velocity = int(self.wolf_velocity/PONDERADOR_LABERINTO_3)
        self.tablero = []
        try:
            with open(ruta_al_archivo, "r") as archivo:
                contenido = archivo.read()
                self.tablero = contenido
        except FileNotFoundError:
            print("El archivo no se encontró en la ubicación especificada:",ruta_al_archivo)
        except Exception as e:
            print(f"Ocurrió un error al abrir el archivo: {e}")

        self.tablero.replace('\n', '')
        tablero_splitted = self.tablero.split(',')

        self.tablero_grande = []
        temporal_array = []
        temporal_array_items = []
        idxx = 0
        for _ in tablero_splitted:
            while len(tablero_splitted) > 0:
                if idxx <= ANCHO_LABERINTO-1:
                    first_item = tablero_splitted.pop(0)
                    if first_item.__contains__('\n'):
                        first_item = first_item.replace('\n', '')
                    temporal_array.append(first_item)
                    temporal_array_items.append(first_item)
                    idxx += 1
                else:
                    self.tablero_items.append(temporal_array_items)
                    self.tablero_grande.append(temporal_array)
                    temporal_array = []
                    temporal_array_items = []
                    idxx = 0
        self.timer_duracion.timeout.connect(self.timer_duracion_func)
        self.timer_duracion.start(1000)
        self.principal_layout = QHBoxLayout()
        self.principal_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout = QVBoxLayout()  # Usamos un QVBoxLayout para apilar las filas
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(0)
        for idx_row, row in enumerate(self.tablero_grande):
            self.layout.setSpacing(0)
            row_widget = QWidget()  # Creamos un widget para cada fila
            row_widget.setContentsMargins(0, 0, 0, 0)
            # Usamos un QHBoxLayout para organizar las casillas en la fila
            row_layout = QHBoxLayout()
            row_layout.setSpacing(0)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row_layout.setContentsMargins(0, 0, 0, 0)
            for idx_col, col in enumerate(row):
                label = QLabel()
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFixedWidth(50)
                label.setFixedHeight(50)
                label.setScaledContents(True)
                label.setContentsMargins(0, 0, 0, 0)
                label.setStyleSheet("padding: 0px;")
                label.setStyleSheet("margin: 0px;")
                if col == 'P':
                    label.setPixmap(QPixmap(os.path.join(
                        project_root, 'assets', 'sprites', 'bloque_pared.jpeg')))
                elif col == 'E':
                    label.setText('E')
                    label.setPixmap(self.piso_pixmap)
                    self.entrada = (idx_row, idx_col)
                elif col == 'S':
                    label.setText('S')
                    label.setPixmap(self.piso_pixmap)
                    self.salida = (idx_row, idx_col)
                elif col == '-':
                    label.setText('-')
                    label.setPixmap(self.piso_pixmap)

                elif col == 'C':
                    label.setText('C')

                    self.combined_pixmap = QPixmap(self.piso_pixmap.size())
                    painter = QPainter(self.combined_pixmap)
                    painter.drawPixmap(0, 0, self.piso_pixmap)
                    painter.drawPixmap(0, 0, self.conejopixmap)
                    label.setPixmap(self.combined_pixmap)
                    self.rabbit_position = (idx_row, idx_col)

                elif col == 'LV':
                    label.setText('LV')
                    piso_pixmap = self.piso_pixmap.scaled(
                        100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    v_wolf_pixmap = QPixmap(os.path.join(
                        project_root,'assets', 'sprites', 'lobo_vertical_abajo_1.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    combined_pixmap = QPixmap(piso_pixmap.size())
                    with QPainter(combined_pixmap) as painter:
                        painter.drawPixmap(0, 0, piso_pixmap)
                        painter.drawPixmap(0, 0, v_wolf_pixmap)
                    label.setPixmap(combined_pixmap)
                elif col == 'LH':
                    label.setText('LH')
                    piso_pixmap = self.piso_pixmap.scaled(
                        100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    h_wolf_pixmap = QPixmap(os.path.join(
                        project_root, 'assets', 'sprites', 'lobo_horizontal_derecha_1.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    combined_pixmap = QPixmap(piso_pixmap.size())
                    with QPainter(combined_pixmap) as painter:
                        painter.drawPixmap(0, 0, piso_pixmap)
                        painter.drawPixmap(0, 0, h_wolf_pixmap)
                    label.setPixmap(combined_pixmap)
                elif col == 'BM':
                    label.setText('BM')
                    piso_pixmap = self.piso_pixmap.scaled(
                        100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    apple_pixmap = QPixmap(os.path.join(
                        project_root, 'assets', 'sprites', 'manzana.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    combined_pixmap = QPixmap(piso_pixmap.size())
                    with QPainter(combined_pixmap) as painter:
                        painter.drawPixmap(0, 0, piso_pixmap)
                        painter.drawPixmap(0, 0, apple_pixmap)
                    label.setPixmap(combined_pixmap)
                    self.tablero_grande[idx_row][idx_col] = 'BM'
                    self.manzana_pixmap = combined_pixmap
                    self.tablero_items[idx_row][idx_col] = 'BM'
                elif col == 'BC':
                    label.setText('BC')
                    piso_pixmap = self.piso_pixmap.scaled(
                        100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    freeze_bomb_pixmap = QPixmap(os.path.join(
                        project_root,'assets', 'sprites', 'congelacion.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    combined_pixmap = QPixmap(piso_pixmap.size())
                    with QPainter(combined_pixmap) as painter:
                        painter.drawPixmap(0, 0, piso_pixmap)
                        painter.drawPixmap(0, 0, freeze_bomb_pixmap)
                    label.setPixmap(combined_pixmap)
                elif col == 'CU':
                    label.setText('CU')
                    piso_pixmap = self.piso_pixmap.scaled(
                        100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    canyon_pixmap = QPixmap(os.path.join(
                        project_root, 'assets', 'sprites', 'canon_arriba.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    combined_pixmap = QPixmap(piso_pixmap.size())
                    with QPainter(combined_pixmap) as painter:
                        painter.drawPixmap(0, 0, piso_pixmap)
                        painter.drawPixmap(7, 0, canyon_pixmap)
                    label.setPixmap(combined_pixmap)
                    self.tablero_grande[idx_row][idx_col] = 'CU'
                elif col == 'CD':
                    label.setText('CD')
                    piso_pixmap = self.piso_pixmap.scaled(
                        100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    canyon_pixmap = QPixmap(os.path.join(
                        project_root,'assets', 'sprites', 'canon_abajo.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                    combined_pixmap = QPixmap(piso_pixmap.size())
                    with QPainter(combined_pixmap) as painter:
                        painter.drawPixmap(0, 0, piso_pixmap)
                        painter.drawPixmap(7, 0, canyon_pixmap)
                    label.setPixmap(combined_pixmap)

                elif col == 'CL':
                    piso_pixmap = self.piso_pixmap.scaled(
                        100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    canyon_pixmap = QPixmap(os.path.join(
                        project_root,'assets', 'sprites', 'canon_izquierda.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                    combined_pixmap = QPixmap(piso_pixmap.size())
                    with QPainter(combined_pixmap) as painter:
                        painter.drawPixmap(0, 0, piso_pixmap)
                        painter.drawPixmap(0, 7, canyon_pixmap)
                    label.setPixmap(combined_pixmap)
                elif col == 'CR':
                    piso_pixmap = self.piso_pixmap.scaled(
                        100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    canyon_pixmap = QPixmap(os.path.join(
                        project_root, 'assets', 'sprites', 'canon_derecha.png')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                    combined_pixmap = QPixmap(piso_pixmap.size())
                    with QPainter(combined_pixmap) as painter:
                        painter.drawPixmap(0, 0, piso_pixmap)
                        painter.drawPixmap(0, 7, canyon_pixmap)
                    label.setPixmap(combined_pixmap)
                    self.tablero_grande[idx_row][idx_col] = 'CR'

                row_layout.addWidget(label)

            row_widget.setLayout(row_layout)
            self.layout.addWidget(row_widget)

        # horizontal stats layout
        self.horizontal_stats_layout = QHBoxLayout()
        self.horizontal_stats_layout.addWidget(self.stats_label)
        self.horizontal_stats_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # horizontal tiempo restante layout
        self.horizontal_stats_layout = QHBoxLayout()
        self.horizontal_stats_layout.addWidget(self.stats_counter_label)
        self.horizontal_stats_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # vertical layout
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vertical_layout.addWidget(self.login_button)
        self.vertical_layout.addWidget(self.pause_button)
        self.vertical_layout.addWidget(self.stats_label)
        self.vertical_layout.addWidget(self.stats_counter_label)
        #
        self.principal_layout.addStretch(2)
        self.principal_layout.addLayout(self.vertical_layout)
        self.principal_layout.addStretch(2)
        self.principal_layout.addLayout(self.layout)
        self.principal_layout.addStretch(2)
        self.setLayout(self.principal_layout)

        self.resize(800, 800)
        for i in range(self.layout.count()):
            temporal_array = []
            for idx in range(ANCHO_LABERINTO):
                actual_label = self.layout.itemAt(
                    i).widget().layout().itemAt(idx).widget()
                temporal_array.append(actual_label)
            self.labels.append(temporal_array)

        self.Carrot_Motion2.start_carrot_motion(
            self.velocidad_zanahoria, self.wolf_velocity, self.tablero_grande, self.labels)
        self.movement_is_allowed = True
        self.show()
        self.setFocus()
