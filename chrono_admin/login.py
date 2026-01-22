"""
Login okno pro admin aplikaci
"""
from admin_panel import AdminPanel

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from database import get_connection
from werkzeug.security import check_password_hash


class LoginWindow(QWidget):
    """
    Okno pro přihlášení admina.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CHRONO Admin – Přihlášení")
        self.setGeometry(400, 250, 350, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Uživatelské jméno")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Heslo")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Přihlásit se")
        login_btn.clicked.connect(self.login)

        layout.addWidget(QLabel("Přihlášení admina"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM user WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            QMessageBox.warning(self, "Chyba", "Uživatel neexistuje")
            return

        if not check_password_hash(row[0], password):
            QMessageBox.warning(self, "Chyba", "Špatné heslo")
            return

        QMessageBox.information(self, "OK", "Přihlášení úspěšné (admin)")
        self.admin_panel = AdminPanel()
        self.admin_panel.show()
        self.close()

