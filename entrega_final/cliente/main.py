from backend.sockets import nivel_aumentado, send_message
import sys
import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from cliente.frontend.Frames.frame_window import Frame_Window
from cliente.frontend.Frames.frame_game import Frame_Game
from backend.sockets import connect_user
from PyQt6.QtCore import Qt
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Debes usar: python main.py PORT, siendo PORT un entero.")
    try:
        port = int(sys.argv[1])
        if len(sys.argv) != 2:
            print("Debes usar: python main.py PORT, siendo PORT un entero.")
        # Debug functionn
        def hook(type, value, traceback) -> None:
            print(type)
            print(traceback)

        sys.__excepthook__ = hook
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(os.path.join(project_root,'frontend','assets','sprites', 'logo32.png')))
        window = Frame_Window()
        frame_game = Frame_Game()
        # login_window.setStyleSheet(global_style)
        window.show()
        window.login_button.close_prompt_signal.connect(window.close)
        window.signal_open_game.connect(frame_game.init_gui)
        window.login_button.login_signal.connect(window.login_user)
        window.port = port
        frame_game.port = port # asignamos el puerto para usarlo
        window.signal_send_username.connect(
            frame_game.receive_username)
        frame_game.signal_user_valid.connect(send_message)
        frame_game.signal_user_valid.connect(connect_user)
        frame_game.login_button.login_signal.connect(window.login_user)
        frame_game.login_button.login_signal.connect(frame_game.close)
        # Signal to delete the mobs
        frame_game.signal_cheat_delete.connect(
            frame_game.Carrot_Motion2.delete_mobs)
        # Signal to activate the infinite cheat
        frame_game.signal_infinite_cheat.connect(
            frame_game.infinite_cheat)
        frame_game.signal_cheat_delete.connect(
            frame_game.Carrot_Motion2.timer_wolf.stop)
        #Signals to pause the game
        frame_game.signal_pause_game.connect(frame_game.Carrot_Motion2.timer.stop)
        frame_game.pause_button.pause_game_signal.connect(
            frame_game.pause_game)
        frame_game.signal_pause_game.connect(frame_game.pause_game)
        window.login_button.login_signal.connect(
            frame_game.Carrot_Motion2.timer.start)
        frame_game.signal_user_valid.connect(connect_user)


        #Pickup an item an added to the inventory
        frame_game.signal_pickup_item.connect(frame_game.pickup_item)
        #Signal that the user has lost the game
        frame_game.signal_has_lost.connect(frame_game.has_lost)
        
        frame_game.level_up.connect(nivel_aumentado)

        def keyPressEvent(self, event) -> None:
            if event.key() == Qt.Key.Key_Return or event.key() == 16777220:
                pass

        sys.exit(app.exec())
    except KeyboardInterrupt as e:
        window.timer.stop()
        print(e)
