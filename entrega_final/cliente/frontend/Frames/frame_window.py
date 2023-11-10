
import os
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QPalette, QBrush, QIcon, QGuiApplication, QPixmap, QCursor, QFont
from frontend.Components.buttons import Enter_Button
import sys
from cliente.frontend.Styles.styles import *
from PyQt6.QtWidgets import QLineEdit
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

class Frame_Window(QWidget):
    signal_open_game = QtCore.pyqtSignal(str)
    signal_send_username = QtCore.pyqtSignal(str)
    signal_close_window = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.username = ''
        self.init_gui()
        self.port = 0
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        # Monitor dimensions
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        self.setStyleSheet("background-color: rgba(140, 0, 150, 255);")
        self.setWindowIcon(
            QIcon(os.path.join('frontend','assets', 'sprites', 'icon.png')))

    def keyPressEvent(self, event) -> None:
        self.username = self.username_field.text()
        if event.key() == Qt.Key.Key_Return or event.key() == 16777220:
            self.login_button.click()
        else:
            pass
    def close_all(self) -> None:
        self.close()
        self.deleteLater()
    def send_username(self) -> None:
        self.username = self.username_field.text()
        self.signal_send_username.emit(self.username)

    def login_user(self, event) -> None:
        sender = self.sender()
        self.username = self.username_field.text()
        if event == 'login':
            self.signal_open_game.emit('login')
            self.deleteLater()
        elif event == 'logout':
            self.signal_open_game.emit('logout')
            self.show()
        else: #Its the close button at the login window
            self.signal_close_window.emit('close')

    def init_gui(self) -> None:
        # Window Geometry
        self.setFocus()
        self.setGeometry(200, 200, 900, 720)
        self.setWindowTitle('DCConejoChico')
        # Grid Layout
        self.grid = QGridLayout()
        # Labels
        self.labels = {}
        # Logo
        self.labels['logo'] = QLabel(self)

        self.labels['logo'].setPixmap(QPixmap(os.path.join('frontend',
            'assets', 'sprites', 'logo.png')).scaled(400, 150, Qt.AspectRatioMode.KeepAspectRatio))
        self.labels['logo'].setScaledContents(True)
        self.labels['username'] = QLabel('Username', self)
        self.labels['username'].setStyleSheet(qlabel_style)
        self.labels['username_status'] = QLabel('', self)
        self.labels['username'].setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter)
        # Salon de la fama
        self.labels['fama'] = QLabel('Salón de la fama', self)
        self.labels['fama'].setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labels['fama'].setStyleSheet(fama_style)
        # Username field
        self.username_field = QLineEdit('', self)
        self.username_field.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.username_field.setStyleSheet(qlineedit_style)

        self.login_button = Enter_Button(
            name='loginButton', text='¡Jugar!', username=self.username)
        self.login_button.setText('¡Jugar!')
        # exit
        self.exit_button = Enter_Button(
            name='closeButton', text='Salir', username=self.username)
        self.exit_button.clicked.connect(self.login_user)
        self.exit_button.setText('Salir')
        # self.login_button.setStyleSheet(
        #     button_style)
        self.login_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_button.setStyleSheet(button_style)
        self.exit_button.setCursor(
            QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.exit_button.setStyleSheet(button_style)
        self.login_button.clicked.connect(self.send_username)

        # Logo Layout
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.labels['logo'])
        hbox.addStretch(1)
        # Horizontal Layout
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.labels['username'])
        hbox1.addWidget(self.username_field)
        hbox1.addStretch(1)
        # Second Horizontal Layout
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.login_button)
        hbox2.addSpacing(30)
        hbox2.addWidget(self.exit_button)
        hbox2.addStretch(1)
        # Third Horizontal Layout
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.labels['fama'])
        hbox3.addStretch(1)

        # Vertical Layout
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(2)
        vbox.addLayout(hbox1)
        vbox.addSpacing(10)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)
        vbox.addStretch(5)
        self.setLayout(vbox)
        self.show()
