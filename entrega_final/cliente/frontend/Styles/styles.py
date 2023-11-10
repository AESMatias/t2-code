fama_style = """
QLabel {
    color: white;
    font-size: 25px;
    background-color: rgba(20, 80, 100, 70);
    border: 1px solid black;
    padding: 30px;
    border-radius: 5px;
}
QLabel:hover {
    background-color: rgba(120, 20, 80, 200);
    border: 1.5px solid white;
    font-weight: bold;
    font-size: 35px;
}
"""
qlabel_style = """
QLabel {
    color: white;
    font-size: 20px;
    background-color: rgba(20, 80, 100, 70);
    border: 1px solid rgba(255, 150, 150, 100);
    padding: 5px;
    border-radius: 2px;
}
"""
qlineedit_style = """
QLineEdit {
    color: white;
    font-size: 20px;
    background-color: rgba(20, 80, 100, 70);
    border: 1px solid rgba(255, 150, 150, 100);
    padding: 5px;
    border-radius: 2px;
}
"""

button_style = """
    QPushButton {
        border: 1px solid black;
        border-radius: 5px;
        font-size: 40px;
        font-weight: 550;
        color: white;
        padding: 10px 10px;
        margin: 2px 2px;
        background: qradialgradient(cx: 0.5, cy: 0.5, fx: 0.5, fy: 0.5, radius: 1, stop: 0 #800080, stop: 0.7 #AA00AA, stop: 1 #880088);

    }
    
    QPushButton:hover {
        font-size: 38px;
        border: 2px solid white;
        font-weight: bold;
        background: qradialgradient(cx: 0.5, cy: 0.5, fx: 0.5, fy: 0.5, radius: 1, stop: 0 #800080, stop: 0.7 #AA00AA, stop: 1 #880088);
    }
    QPushButton:pressed {
        padding:5px;
        font-size: 30px;
        font-weight: bold;
        border: 3px solid white;
}
"""
