"""
Admin panel – přidání hodinek
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem,
    QHBoxLayout, QPushButton,
    QLineEdit, QMessageBox, QTextEdit
)
from database import get_connection


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_products()

    def init_ui(self):
        self.setWindowTitle("CHRONO Admin – Přidání hodinek")
        self.setGeometry(300, 150, 1100, 650)

        layout = QVBoxLayout()

        title = QLabel("Přidání nových hodinek")
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        layout.addWidget(title)

        # FORMULÁŘ
        form = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Název hodinek")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Cena")

        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("Skladem")

        self.image_input = QLineEdit()
        self.image_input.setPlaceholderText("Cesta k obrázku (např. obrazky/rolex.webp)")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Popis hodinek")

        add_btn = QPushButton("Přidat hodinky")
        add_btn.clicked.connect(self.add_product)

        form.addWidget(self.name_input)
        form.addWidget(self.price_input)
        form.addWidget(self.stock_input)
        form.addWidget(self.image_input)
        form.addWidget(add_btn)

        layout.addLayout(form)
        layout.addWidget(self.desc_input)

        # TABULKA
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Název", "Cena", "Skladem", "Popis"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(QLabel("Aktuální hodinky v databázi"))
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_products(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nazev, cena, skladem, popis FROM product"
        )
        products = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(products))

        for r, product in enumerate(products):
            for c, value in enumerate(product):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

    def add_product(self):
        name = self.name_input.text()
        price = self.price_input.text()
        stock = self.stock_input.text()
        image = self.image_input.text()
        desc = self.desc_input.toPlainText()

        if not name or not price or not stock:
            QMessageBox.warning(self, "Chyba", "Vyplň název, cenu a sklad")
            return

        try:
            price = int(price)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(self, "Chyba", "Cena a sklad musí být číslo")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO product (nazev, cena, skladem, popis, image)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, price, stock, desc, image)
        )

        conn.commit()
        conn.close()

        QMessageBox.information(self, "OK", "Hodinky byly přidány")

        self.name_input.clear()
        self.price_input.clear()
        self.stock_input.clear()
        self.image_input.clear()
        self.desc_input.clear()

        self.load_products()
