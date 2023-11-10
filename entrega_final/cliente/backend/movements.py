from cliente.backend.funciones_cliente import validar_direccion_carrot, validar_direccion_wolf
import os
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap
import sys
from PyQt6.QtCore import QMutex, QMutexLocker
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
carpeta_superior = os.path.join(project_root, "..")
sys.path.append(carpeta_superior)

class Wolf(QWidget):
    id_counter = 0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.counter_mov_wolf_down = 0
        Wolf.id_counter += 1
        self.id = Wolf.id_counter


class Carrot_Motion(QWidget):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.timer = QTimer()
        self.carrot_positions = []
        self.counter_mov_carrot_down = 0
        self.counter_mov_carrot_up = 0
        self.counter_mov_carrot_right = 0
        self.counter_mov_carrot_left = 0
        self.counter_mov_wolf_down = 0
        self.counter_mov_wolf_up = 0
        self.timer = QTimer()
        self.timer_wolf = QTimer()
        self.my_lock = QMutex()
        self.wolves_array = [] #Contains tuples (row,col,wolf_class,wolf_id)
        self.wolf_id_counter = 0
        self.wolves_timers = []


    def vertical_wolf_mov(self, wolf_tuple: tuple):
        # Inicia moviendose hacia abajo por default
        wolf_direction = wolf_tuple[2].direction
        wolf_position = (wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down,wolf_tuple[1])
        try:
            if validar_direccion_wolf(self.tablero_grande, wolf_direction,wolf_position,self.carrot_positions)[0] == False and wolf_direction == 'vertical_wolf_down':
                self.labels[wolf_tuple[0] + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[wolf_tuple[0] +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = '-'
                wolf_tuple[2].counter_mov_wolf_down -= 1
                if wolf_tuple[2].counter_mov_wolf_down%2 == 0:
                    self.labels[wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]
                                                                                ].setPixmap(self.combined_pixmap_LVU)
                else:
                                        self.labels[wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]
                                                                                ].setPixmap(self.combined_pixmap_LVU2)

                self.tablero_grande[wolf_tuple[0] +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = 'vertical_wolf_up'
                wolf_tuple[2].direction = 'vertical_wolf_up'
            elif validar_direccion_wolf(self.tablero_grande, wolf_direction,wolf_position,self.carrot_positions)[0] == False and wolf_direction == 'vertical_wolf_up':
                
                self.labels[wolf_tuple[0] + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[wolf_tuple[0] +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = '-'
                wolf_tuple[2].counter_mov_wolf_down += 1
                if wolf_tuple[2].counter_mov_wolf_down%2 == 1:
                    self.labels[wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]
                                                                                ].setPixmap(self.combined_pixmap_LVD)
                else:
                    self.labels[wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]
                                                                                ].setPixmap(self.combined_pixmap_LVD2)

                self.tablero_grande[wolf_tuple[0] +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = 'vertical_wolf_down'
                wolf_tuple[2].direction = 'vertical_wolf_down'

            else:
                if wolf_direction == 'vertical_wolf_down':
                    self.labels[wolf_tuple[0] + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(
                        self.piso_pixmap)
                    self.tablero_grande[wolf_tuple[0] +
                                        wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = '-'
                    if wolf_tuple[2].counter_mov_wolf_down%2 == 1:
                        self.labels[wolf_tuple[0] + 1 +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(self.combined_pixmap_LVD)
                    else:
                        self.labels[wolf_tuple[0] + 1 + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(self.combined_pixmap_LVD2)
                    self.tablero_grande[wolf_tuple[0] + 1 +
                                        wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = 'vertical_wolf_down'
                    wolf_tuple[2].counter_mov_wolf_down += 1
                elif wolf_direction == 'vertical_wolf_up':
                    self.labels[wolf_tuple[0] + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(
                        self.piso_pixmap)
                    self.tablero_grande[wolf_tuple[0] +
                                        wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = '-'
                    if wolf_tuple[2].counter_mov_wolf_down%2 == 0:
                        self.labels[wolf_tuple[0] - 1 +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(self.combined_pixmap_LVU2)
                    else:
                        self.labels[wolf_tuple[0] - 1 +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(self.combined_pixmap_LVU)
                    self.tablero_grande[wolf_tuple[0] - 1 +
                                        wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = 'vertical_wolf_up'
                    wolf_tuple[2].counter_mov_wolf_down -= 1

        except IndexError as e:
            print('down WOLF', 'indexerror', e)
            
    def horizontal_wolf_mov(self, wolf_tuple: tuple):
        wolf_direction = wolf_tuple[2].direction
        wolf_position = (wolf_tuple[0],wolf_tuple[1]+wolf_tuple[2].counter_mov_wolf_down)

        try:
            if validar_direccion_wolf(self.tablero_grande, wolf_direction,wolf_position,self.carrot_positions)[0] == False and wolf_direction == 'horizontal_wolf_right':
                self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = '-'
                wolf_tuple[2].counter_mov_wolf_down -= 1
                if wolf_tuple[2].counter_mov_wolf_down%2 == 0:
                    self.labels[wolf_tuple[0]][wolf_tuple[1]+wolf_tuple[2].counter_mov_wolf_down
                                                                                ].setPixmap(self.combined_pixmap_LHL)
                else:
                                        self.labels[wolf_tuple[0]][wolf_tuple[1]+wolf_tuple[2].counter_mov_wolf_down
                                                                                ].setPixmap(self.combined_pixmap_LHL2)

                self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+wolf_tuple[2].counter_mov_wolf_down] = 'horizontal_wolf_left'
                wolf_tuple[2].direction = 'horizontal_wolf_left'
            elif validar_direccion_wolf(self.tablero_grande, wolf_direction,wolf_position,self.carrot_positions)[0] == False and wolf_direction == 'horizontal_wolf_left':
                
                self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = '-'
                wolf_tuple[2].counter_mov_wolf_down += 1
                if wolf_tuple[2].counter_mov_wolf_down%2 == 1:
                    self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down
                                                                                ].setPixmap(self.combined_pixmap_LHR)
                else:
                    self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down
                                                                                ].setPixmap(self.combined_pixmap_LHR2)

                self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = 'horizontal_wolf_right'
                wolf_tuple[2].direction = 'horizontal_wolf_right'

            else:
                if wolf_direction == 'horizontal_wolf_right':
                    self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(
                        self.piso_pixmap)
                    self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = '-'
                    if wolf_tuple[2].counter_mov_wolf_down%2 == 1:
                        self.labels[wolf_tuple[0]][wolf_tuple[1]+ 1 +
                                    wolf_tuple[2].counter_mov_wolf_down].setPixmap(self.combined_pixmap_LHR)
                    else:
                        self.labels[wolf_tuple[0] ][wolf_tuple[1]+ 1 + wolf_tuple[2].counter_mov_wolf_down].setPixmap(self.combined_pixmap_LHR2)
                    self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ 1 +
                                    wolf_tuple[2].counter_mov_wolf_down] = 'horizontal_wolf_right'
                    wolf_tuple[2].counter_mov_wolf_down += 1
                elif wolf_direction == 'horizontal_wolf_left':
                    self.labels[wolf_tuple[0] ][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(
                        self.piso_pixmap)
                    self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = '-'
                    if wolf_tuple[2].counter_mov_wolf_down%2 == 0:
                        self.labels[wolf_tuple[0]][wolf_tuple[1]-1+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(self.combined_pixmap_LHL2)
                    else:
                        self.labels[wolf_tuple[0]][wolf_tuple[1]-1+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(self.combined_pixmap_LHL)
                    self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]-1+ wolf_tuple[2].counter_mov_wolf_down] = 'horizontal_wolf_left'
                    wolf_tuple[2].counter_mov_wolf_down -= 1

        except IndexError as e:
            print('down WOLF', 'indexerror', e)

    def move_carrot_up(self, canyon_pos: tuple):
        try:
            if validar_direccion_carrot(self.tablero_grande, "carrot_up")[0] == False:
                self.labels[canyon_pos[0]-1-self.counter_mov_carrot_down][canyon_pos[1]].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[canyon_pos[0]-1 -
                                    self.counter_mov_carrot_down][canyon_pos[1]] = '-'

                self.counter_mov_carrot_down = 0
                self.tablero_grande[canyon_pos[0]-1 -
                                    self.counter_mov_carrot_down][canyon_pos[1]] = 'carrot_up'
                self.labels[canyon_pos[0]-1 -
                            self.counter_mov_carrot_down][canyon_pos[1]].setPixmap(self.combined_pixmap_CU)

            else:
                self.labels[canyon_pos[0] - 2 -
                            self.counter_mov_carrot_down][canyon_pos[1]].setPixmap(self.combined_pixmap_CU)
                self.labels[canyon_pos[0] - 1-self.counter_mov_carrot_down][canyon_pos[1]].setPixmap(
                    self.piso_pixmap)
                self.counter_mov_carrot_down += 1
                self.tablero_grande[canyon_pos[0] -
                                    self.counter_mov_carrot_down][canyon_pos[1]] = '-'
                self.tablero_grande[canyon_pos[0] - 1 -
                                    self.counter_mov_carrot_down][canyon_pos[1]] = 'carrot_up'
        except IndexError as e:
            print('up', 'indexerror', e)

    def move_carrot_down(self, canyon_pos: tuple):
        try:
            if validar_direccion_carrot(self.tablero_grande, "carrot_down")[0] == False:
                self.labels[canyon_pos[0]+1+self.counter_mov_carrot_down][canyon_pos[1]].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[canyon_pos[0]+1 +
                                    self.counter_mov_carrot_down][canyon_pos[1]] = '-'
                self.counter_mov_carrot_down = 0
                self.tablero_grande[canyon_pos[0] + 1 +
                                    self.counter_mov_carrot_down][canyon_pos[1]] = 'carrot_down'
                self.labels[canyon_pos[0]+1 +
                            self.counter_mov_carrot_down][canyon_pos[1]].setPixmap(self.combined_pixmap_CD)

            else:
                self.labels[canyon_pos[0] + 2 +
                            self.counter_mov_carrot_down][canyon_pos[1]].setPixmap(self.combined_pixmap_CD)
                self.labels[canyon_pos[0] + 1+self.counter_mov_carrot_down][canyon_pos[1]].setPixmap(
                    self.piso_pixmap)
                self.counter_mov_carrot_down += 1
                self.tablero_grande[canyon_pos[0] +
                                    self.counter_mov_carrot_down][canyon_pos[1]] = '-'
                self.tablero_grande[canyon_pos[0] + 1 +
                                    self.counter_mov_carrot_down][canyon_pos[1]] = 'carrot_down'
        except IndexError as e:
            print('down', 'indexerror', e)

    def move_carrot_right(self, canyon_pos: tuple):
        try:
            if validar_direccion_carrot(self.tablero_grande, "carrot_right")[0] == False:
                self.labels[canyon_pos[0]][canyon_pos[1]+1+self.counter_mov_carrot_up].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[canyon_pos[0]][canyon_pos[1] +
                                                   1+self.counter_mov_carrot_up] = '-'

                self.counter_mov_carrot_up = 0
                self.tablero_grande[canyon_pos[0]][canyon_pos[1] +
                                                   1+self.counter_mov_carrot_up] = 'carrot_right'
                self.labels[canyon_pos[0]][canyon_pos[1]+1 +
                                           self.counter_mov_carrot_up].setPixmap(self.combined_pixmap_CR)

            else:
                self.labels[canyon_pos[0]][canyon_pos[1]+2 +
                                           self.counter_mov_carrot_up].setPixmap(self.combined_pixmap_CR)
                self.labels[canyon_pos[0]][canyon_pos[1]+1+self.counter_mov_carrot_up].setPixmap(
                    self.piso_pixmap)
                self.counter_mov_carrot_up += 1
                self.tablero_grande[canyon_pos[0]][canyon_pos[1] +
                                                   self.counter_mov_carrot_up] = '-'
                self.tablero_grande[canyon_pos[0]][canyon_pos[1] +
                                                   1+self.counter_mov_carrot_up] = 'carrot_right'
        except IndexError as e:
            print('right', 'indexerror', e)

    def move_carrot_left(self, canyon_pos: tuple):
        try:
            if validar_direccion_carrot(self.tablero_grande, "carrot_left")[0] == False:
                self.labels[canyon_pos[0]][canyon_pos[1]-1+self.counter_mov_carrot_left].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[canyon_pos[0]-1 +
                                    self.counter_mov_carrot_up][canyon_pos[1]] = '-'

                self.counter_mov_carrot_left = 0
                self.tablero_grande[canyon_pos[0]][canyon_pos[1] -
                                                   1+self.counter_mov_carrot_up] = 'carrot_left'
                self.labels[canyon_pos[0]][canyon_pos[1]-1+self.counter_mov_carrot_left
                                           ].setPixmap(self.combined_pixmap_CL)

            else:
                self.labels[canyon_pos[0]][canyon_pos[1]-2 +
                                           self.counter_mov_carrot_left].setPixmap(self.combined_pixmap_CL)
                self.labels[canyon_pos[0]][canyon_pos[1]-1+self.counter_mov_carrot_left].setPixmap(
                    self.piso_pixmap)
                self.counter_mov_carrot_left -= 1
                self.tablero_grande[canyon_pos[0]][canyon_pos[1] +
                                                   self.counter_mov_carrot_left] = '-'
                self.tablero_grande[canyon_pos[0]][canyon_pos[1] -
                                                   1+self.counter_mov_carrot_left] = 'carrot_left'
        except IndexError as e:
            print('right', 'indexerror', e)

    def vertical_wolf_mov(self, wolf_tuple: tuple):
        # Inicia moviendose hacia abajo por default
        wolf_direction = wolf_tuple[2].direction
        wolf_position = (wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down,wolf_tuple[1])
        try:
            if validar_direccion_wolf(self.tablero_grande, wolf_direction,wolf_position,self.carrot_positions)[0] == False and wolf_direction == 'vertical_wolf_down':
                self.labels[wolf_tuple[0] + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[wolf_tuple[0] +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = '-'
                wolf_tuple[2].counter_mov_wolf_down -= 1
                if wolf_tuple[2].counter_mov_wolf_down%2 == 0:
                    self.labels[wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]
                                                                                ].setPixmap(self.combined_pixmap_LVU)
                else:
                                        self.labels[wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]
                                                                                ].setPixmap(self.combined_pixmap_LVU2)

                self.tablero_grande[wolf_tuple[0] +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = 'vertical_wolf_up'
                wolf_tuple[2].direction = 'vertical_wolf_up'
            elif validar_direccion_wolf(self.tablero_grande, wolf_direction,wolf_position,self.carrot_positions)[0] == False and wolf_direction == 'vertical_wolf_up':
                
                self.labels[wolf_tuple[0] + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[wolf_tuple[0] +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = '-'
                wolf_tuple[2].counter_mov_wolf_down += 1
                if wolf_tuple[2].counter_mov_wolf_down%2 == 1:
                    self.labels[wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]
                                                                                ].setPixmap(self.combined_pixmap_LVD)
                else:
                    self.labels[wolf_tuple[0]+wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]
                                                                                ].setPixmap(self.combined_pixmap_LVD2)

                self.tablero_grande[wolf_tuple[0] +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = 'vertical_wolf_down'
                wolf_tuple[2].direction = 'vertical_wolf_down'

            else:
                if wolf_direction == 'vertical_wolf_down':
                    self.labels[wolf_tuple[0] + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(
                        self.piso_pixmap)
                    self.tablero_grande[wolf_tuple[0] +
                                        wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = '-'
                    if wolf_tuple[2].counter_mov_wolf_down%2 == 1:
                        self.labels[wolf_tuple[0] + 1 +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(self.combined_pixmap_LVD)
                    else:
                        self.labels[wolf_tuple[0] + 1 + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(self.combined_pixmap_LVD2)
                    self.tablero_grande[wolf_tuple[0] + 1 +
                                        wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = 'vertical_wolf_down'
                    wolf_tuple[2].counter_mov_wolf_down += 1
                elif wolf_direction == 'vertical_wolf_up':
                    self.labels[wolf_tuple[0] + wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(
                        self.piso_pixmap)
                    self.tablero_grande[wolf_tuple[0] +
                                        wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = '-'
                    if wolf_tuple[2].counter_mov_wolf_down%2 == 0:
                        self.labels[wolf_tuple[0] - 1 +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(self.combined_pixmap_LVU2)
                    else:
                        self.labels[wolf_tuple[0] - 1 +
                                    wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]].setPixmap(self.combined_pixmap_LVU)
                    self.tablero_grande[wolf_tuple[0] - 1 +
                                        wolf_tuple[2].counter_mov_wolf_down][wolf_tuple[1]] = 'vertical_wolf_up'
                    wolf_tuple[2].counter_mov_wolf_down -= 1

        except IndexError as e:
            print('down WOLF', 'indexerror', e)
            
    def horizontal_wolf_mov(self, wolf_tuple: tuple):
        wolf_direction = wolf_tuple[2].direction
        wolf_position = (wolf_tuple[0],wolf_tuple[1]+wolf_tuple[2].counter_mov_wolf_down)

        try:
            if validar_direccion_wolf(self.tablero_grande, wolf_direction,wolf_position,self.carrot_positions)[0] == False and wolf_direction == 'horizontal_wolf_right':
                self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = '-'
                wolf_tuple[2].counter_mov_wolf_down -= 1
                if wolf_tuple[2].counter_mov_wolf_down%2 == 0:
                    self.labels[wolf_tuple[0]][wolf_tuple[1]+wolf_tuple[2].counter_mov_wolf_down
                                                                                ].setPixmap(self.combined_pixmap_LHL)
                else:
                                        self.labels[wolf_tuple[0]][wolf_tuple[1]+wolf_tuple[2].counter_mov_wolf_down
                                                                                ].setPixmap(self.combined_pixmap_LHL2)

                self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+wolf_tuple[2].counter_mov_wolf_down] = 'horizontal_wolf_left'
                wolf_tuple[2].direction = 'horizontal_wolf_left'
            elif validar_direccion_wolf(self.tablero_grande, wolf_direction,wolf_position,self.carrot_positions)[0] == False and wolf_direction == 'horizontal_wolf_left':
                
                self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(
                    self.piso_pixmap)
                self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = '-'
                wolf_tuple[2].counter_mov_wolf_down += 1
                if wolf_tuple[2].counter_mov_wolf_down%2 == 1:
                    self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down
                                                                                ].setPixmap(self.combined_pixmap_LHR)
                else:
                    self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down
                                                                                ].setPixmap(self.combined_pixmap_LHR2)

                self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = 'horizontal_wolf_right'
                wolf_tuple[2].direction = 'horizontal_wolf_right'

            else:
                if wolf_direction == 'horizontal_wolf_right':
                    self.labels[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(
                        self.piso_pixmap)
                    self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = '-'
                    if wolf_tuple[2].counter_mov_wolf_down%2 == 1:
                        self.labels[wolf_tuple[0]][wolf_tuple[1]+ 1 +
                                    wolf_tuple[2].counter_mov_wolf_down].setPixmap(self.combined_pixmap_LHR)
                    else:
                        self.labels[wolf_tuple[0] ][wolf_tuple[1]+ 1 + wolf_tuple[2].counter_mov_wolf_down].setPixmap(self.combined_pixmap_LHR2)
                    self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ 1 +
                                    wolf_tuple[2].counter_mov_wolf_down] = 'horizontal_wolf_right'
                    wolf_tuple[2].counter_mov_wolf_down += 1
                elif wolf_direction == 'horizontal_wolf_left':
                    self.labels[wolf_tuple[0] ][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(
                        self.piso_pixmap)
                    self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]+ wolf_tuple[2].counter_mov_wolf_down] = '-'
                    if wolf_tuple[2].counter_mov_wolf_down%2 == 0:
                        self.labels[wolf_tuple[0]][wolf_tuple[1]-1+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(self.combined_pixmap_LHL2)
                    else:
                        self.labels[wolf_tuple[0]][wolf_tuple[1]-1+ wolf_tuple[2].counter_mov_wolf_down].setPixmap(self.combined_pixmap_LHL)
                    self.tablero_grande[wolf_tuple[0]][wolf_tuple[1]-1+ wolf_tuple[2].counter_mov_wolf_down] = 'horizontal_wolf_left'
                    wolf_tuple[2].counter_mov_wolf_down -= 1

        except IndexError as e:
            print('down WOLF', 'indexerror', e)

    def start_carrot_motion(self, carrot_velocity: int, wolf_velocity: int, tablero_grande: list, labels: list) -> None:
        with QMutexLocker(self.my_lock):
            self.carrot_velocity = carrot_velocity
            self.wolf_velocity = int(2000/wolf_velocity)
            self.tablero_grande = tablero_grande
            self.labels = labels
            self.canyons = []  # (row,col,type))
            self.canyon_counter = 0
            for idx_row, row in enumerate(self.tablero_grande):
                for idx_col, col in enumerate(row):
                    if col == 'CD':
                        self.canyon_counter += 1
                        canyon_pos = (idx_row, idx_col, 'CD')
                        self.canyons.append(canyon_pos)
                        self.piso_pixmap = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'bloque_fondo.jpeg')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        pixmap_zanahoria = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'zanahoria_abajo.png'))
                        pixmap_zanahoria = pixmap_zanahoria.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                        self.combined_pixmap_CD = QPixmap(
                            self.piso_pixmap.size())
                        with QPainter(self.combined_pixmap_CD) as painter:
                            painter.drawPixmap(0, 0, self.piso_pixmap)
                            painter.drawPixmap(12, 0, pixmap_zanahoria)
                        # tablero_grande[idx_row + 1][idx_col] == 'carrot'
                        self.tablero_grande[idx_row][idx_col] = 'CD'
                        self.tablero_grande[idx_row+1][idx_col] = 'carrot_down'
                        self.labels[idx_row +
                                    1][idx_col].setText('carrot_down')
                        self.labels[idx_row +
                                    1][idx_col].setPixmap(self.combined_pixmap_CD)
                        self.timer.timeout.connect(
                            lambda canyon=canyon_pos: self.move_carrot_down(canyon))
                        self.timer.start(self.carrot_velocity)
                    if col == 'CU':
                        canyon_pos = (idx_row, idx_col, 'CU')
                        self.canyons.append(canyon_pos)
                        self.piso_pixmap = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'bloque_fondo.jpeg')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        pixmap_zanahoria = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'zanahoria_arriba.png'))
                        pixmap_zanahoria = pixmap_zanahoria.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                        self.combined_pixmap_CU = QPixmap(
                            self.piso_pixmap.size())
                        with QPainter(self.combined_pixmap_CU) as painter:
                            painter.drawPixmap(0, 0, self.piso_pixmap)
                            painter.drawPixmap(12, 0, pixmap_zanahoria)
                        self.tablero_grande[idx_row][idx_col] = 'CU'
                        self.tablero_grande[idx_row-1][idx_col] = 'carrot_up'
                        self.labels[idx_row -
                                    1][idx_col].setText('carrot_up')
                        self.labels[idx_row -
                                    1][idx_col].setPixmap(self.combined_pixmap_CU)
                        self.timer.timeout.connect(
                            lambda canyon=canyon_pos: self.move_carrot_up(canyon))
                        self.timer.start(self.carrot_velocity)
                    if col == 'CR':
                        canyon_pos = (idx_row, idx_col, 'CR')
                        self.canyons.append(canyon_pos)
                        self.piso_pixmap = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'bloque_fondo.jpeg')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        pixmap_zanahoria = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'zanahoria_derecha.png'))
                        pixmap_zanahoria = pixmap_zanahoria.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        self.combined_pixmap_CR = QPixmap(
                            self.piso_pixmap.size())
                        with QPainter(self.combined_pixmap_CR) as painter:
                            painter.drawPixmap(0, 0, self.piso_pixmap)
                            painter.drawPixmap(0, 12, pixmap_zanahoria)
                        self.tablero_grande[idx_row][idx_col] = 'CR'
                        self.tablero_grande[idx_row][idx_col +
                                                     1] = 'carrot_right'
                        self.labels[idx_row][idx_col+1].setText('carrot_right')
                        self.labels[idx_row][idx_col +
                                             1].setPixmap(self.combined_pixmap_CR)
                        self.timer.timeout.connect(
                            lambda canyon=canyon_pos: self.move_carrot_right(canyon))
                        self.timer.start(self.carrot_velocity)
                        #This avoids the carrot to be deleted when the wolf moves
                        self.carrot_positions.append((idx_row,idx_col+1))
                        self.carrot_positions.append((idx_row,idx_col+0))
                        self.carrot_positions.append((idx_row,idx_col-1))
                        self.carrot_positions.append((idx_row,idx_col-1))
                        self.carrot_positions.append((idx_row,idx_col-3))
                        self.carrot_positions.append((idx_row,idx_col-4))
                    if col == 'CL':
                        canyon_pos = (idx_row, idx_col, 'CL')
                        self.canyons.append(canyon_pos)
                        self.piso_pixmap = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'bloque_fondo.jpeg')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        pixmap_zanahoria = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'zanahoria_izquierda.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        self.combined_pixmap_CL = QPixmap(
                            self.piso_pixmap.size())
                        with QPainter(self.combined_pixmap_CL) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 12, pixmap_zanahoria)
                        self.tablero_grande[idx_row][idx_col] = 'L'
                        self.tablero_grande[idx_row][idx_col-1] = 'carrot_left'
                        self.labels[idx_row][idx_col-1].setText('carrot_left')
                        self.labels[idx_row][idx_col -
                                             1].setPixmap(self.combined_pixmap_CL)
                        self.timer.timeout.connect(
                            lambda canyon=canyon_pos: self.move_carrot_left(canyon))
                        self.timer.start(self.carrot_velocity)
                    if col == 'LV':
                        self.wolf_id_counter += 1
                        wolf_class = Wolf()
                        wolf_class.direction = 'vertical_wolf_down'
                        wolf_tuple = (idx_row, idx_col,
                                      wolf_class, self.wolf_id_counter)
                        piso_pixmap = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'bloque_fondo.jpeg'))
                        piso_pixmap = piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        lobo_vertical_pixmap_DOWN = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'lobo_vertical_abajo_1.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        lobo_vertical_pixmap_DOWN2 = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'lobo_vertical_abajo_2.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        self.combined_pixmap_LVD = QPixmap(piso_pixmap.size())
                        self.combined_pixmap_LVD2 = QPixmap(piso_pixmap.size())
                        
                        with QPainter(self.combined_pixmap_LVD) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, lobo_vertical_pixmap_DOWN)
                            
                        with QPainter(self.combined_pixmap_LVD2) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, lobo_vertical_pixmap_DOWN2)
                            
                        labels[idx_row][idx_col].setPixmap(
                            self.combined_pixmap_LVD)

                        lobo_vertical_pixmap_UP = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'lobo_vertical_arriba_1.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        lobo_vertical_pixmap_UP2 = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'lobo_vertical_arriba_2.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        self.combined_pixmap_LVU = QPixmap(piso_pixmap.size())
                        self.combined_pixmap_LVU2 = QPixmap(piso_pixmap.size())
                        with QPainter(self.combined_pixmap_LVU) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, lobo_vertical_pixmap_UP)
                            
                        with QPainter(self.combined_pixmap_LVU2) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, lobo_vertical_pixmap_UP2)
                            
                        labels[idx_row][idx_col].setPixmap(
                            self.combined_pixmap_LVU)

                        self.tablero_grande[idx_row][idx_col] = 'vertical_wolf_down'
                        self.labels[idx_row][idx_col].setPixmap(
                            self.combined_pixmap_LVD)
                        self.wolves_array.append(wolf_tuple)
                        timer_wolf = QTimer()
                        timer_wolf.timeout.connect(
                            lambda wolf=wolf_tuple: self.vertical_wolf_mov(wolf))
                        self.wolves_timers.append(timer_wolf)
                    if col == 'LH':
                        self.wolf_id_counter += 1
                        wolf_class = Wolf()
                        wolf_class.direction = 'horizontal_wolf_right'
                        wolf_tuple = (idx_row, idx_col,
                                      wolf_class, self.wolf_id_counter)
                        piso_pixmap = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'bloque_fondo.jpeg'))
                        piso_pixmap = piso_pixmap.scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        lobo_horizontal_pixmap_RIGHT = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'lobo_horizontal_derecha_1.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        lobo_horizontal_pixmap_RIGHT2 = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'lobo_horizontal_derecha_2.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        self.combined_pixmap_LHR = QPixmap(piso_pixmap.size())
                        self.combined_pixmap_LHR2 = QPixmap(piso_pixmap.size())
                        
                        with QPainter(self.combined_pixmap_LHR) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, lobo_horizontal_pixmap_RIGHT)
                            
                        with QPainter(self.combined_pixmap_LHR2) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, lobo_horizontal_pixmap_RIGHT2)
                            
                        labels[idx_row][idx_col].setPixmap(
                            self.combined_pixmap_LHR)

                        lobo_horizontal_pixmap_LEFT = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'lobo_horizontal_izquierda_1.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        lobo_horizontal_pixmap_LEFT2 = QPixmap(os.path.join(
                            project_root, 'frontend', 'assets', 'sprites', 'lobo_horizontal_izquierda_2.png')).scaled(
                            100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                        self.combined_pixmap_LHL = QPixmap(piso_pixmap.size())
                        self.combined_pixmap_LHL2 = QPixmap(piso_pixmap.size())
                        with QPainter(self.combined_pixmap_LHL) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, lobo_horizontal_pixmap_LEFT2)
                            
                        with QPainter(self.combined_pixmap_LHL2) as painter:
                            painter.drawPixmap(0, 0, piso_pixmap)
                            painter.drawPixmap(0, 0, lobo_horizontal_pixmap_LEFT)
                            
                        labels[idx_row][idx_col].setPixmap(
                            self.combined_pixmap_LHL)

                        self.tablero_grande[idx_row][idx_col] = 'horizontal_wolf_right'
                        self.labels[idx_row][idx_col].setPixmap(
                            self.combined_pixmap_LHR)
                        self.wolves_array.append(wolf_tuple)
                        timer_wolf = QTimer()
                        timer_wolf.timeout.connect(
                            lambda wolf=wolf_tuple: self.horizontal_wolf_mov(wolf))
                        self.wolves_timers.append(timer_wolf)
            for timer in self.wolves_timers:
                timer.start(self.wolf_velocity)
                
    def delete_mobs(self) -> None:
        for idx, row in enumerate(self.tablero_grande):
            for idx_item, item in enumerate(row):
                if item == 'vertical_wolf_down' or item == 'LV' or item == 'vertical_wolf_up' or \
                        item == 'horizontal_wolf_left' or item == 'horizontal_wolf_right' or \
                            item == 'LH' or item == 'carrot_up' or item == 'carrot_down' or \
                                item == 'carrot_right' or item == 'carrot_left' or item == 'CD' or \
                                    item == 'CU' or item == 'CR' or item == 'CL':
                    self.labels[idx][idx_item].setPixmap(self.piso_pixmap)
                    self.tablero_grande[idx][idx_item] = '-'
        self.timer.stop()
        for timer in self.wolves_timers:
            timer.stop()