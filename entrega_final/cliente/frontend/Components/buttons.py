from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton


class Enter_Button(QPushButton):
    login_signal = pyqtSignal(str, str)
    pause_game_signal = pyqtSignal()
    close_prompt_signal = pyqtSignal()

    def __init__(self, name: str, text: str, username: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.text = text
        self.username = username
        self.args = args
        self.resize(self.sizeHint())
        self.setGeometry(300, 250, 400, 150)
        self.clicked.connect(self.button_clicked)

    def button_clicked(self) -> None:
        status_login = True  # Check through the server if the user is valid
        if status_login and self.name == 'exitButton':
            self.login_signal.emit('logout', self.username)
        elif status_login and self.name == 'loginButton':
            self.login_signal.emit('login', self.username)
        if self.name == 'closeButton':
            self.close_prompt_signal.emit()
        if self.name == 'pauseButton':
            self.pause_game_signal.emit()

    #     # Login successfull sound
    #         self.media_player = QMediaPlayer(self)
    #         self.media_player.setAudioOutput(QAudioOutput(self))
    #         file_url = QUrl.fromLocalFile(os.path.join(
    #             'Music', 'mixkit-fantasy-game-sweep-notification-255.wav'))
    #         self.media_player.setSource(file_url)
    #         # self.media_player.mediaStatusChanged.connect(self.handle_media_status)
    #         self.media_player.play()
    #     elif status_login:
    #         self.username = form_username
    #         print('SELF.USERNAME ', self.username)
    #         self.login_status = True
    #         self.login_signal.emit()
    #         print('Login status:', self.login_status)
    #     else:
    #         # Login unsuccessfull sound
    #         self.media_player = QMediaPlayer(self)
    #         self.media_player.setAudioOutput(QAudioOutput(self))
    #         file_url = QUrl.fromLocalFile(os.path.join(
    #             'Music', 'mixkit-alert-bells-echo-765.wav'))
    #         self.media_player.setSource(file_url)
    #         # self.media_player.mediaStatusChanged.connect(self.handle_media_status)
    #         self.media_player.play()
    #         self.login_status = False
    #         print(f"No login with username {form_username}")
