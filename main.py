from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QVBoxLayout, QWidget, QMenu
from PyQt6.QtCore import Qt

class Item:
    def __init__(self, id, provider, name, stars, price):
        self.id = id
        self.provider = provider
        self.name = name
        self.stars = stars
        self.price = price

    def __str__(self):
        return f"ID: {self.id}, Provider: {self.provider}, Name: {self.name}, Stars: {'⭐' * int(self.stars)}, Price: {self.price}zł"

all_items = []

with open('item_details.txt', 'r') as file:
    for line in file:
        components = line.split(',')
        components = [component.strip() for component in components]
        item = Item(components[0], components[1], components[2], components[3], components[4])
        all_items.append(item)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cheapest Price for Each Item')
        self.setGeometry(100, 100, 1600, 1200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.search_label = QLabel("Search:", self)
        self.layout.addWidget(self.search_label)

        self.search_entry = QLineEdit(self)
        self.search_entry.textChanged.connect(self.search_treeview)
        self.layout.addWidget(self.search_entry)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Item Name', 'Stars', 'Cheapest Provider', 'Cheapest Price'])
        self.layout.addWidget(self.table_widget)

        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)

        self.pinned_items = set()
        self.cheapest_prices = self.find_cheapest_provider(all_items)
        self.populate_table()

    def show_context_menu(self, position):
        menu = QMenu()
        pin_unpin_action = menu.addAction("Pin/Unpin")
        pin_unpin_action.triggered.connect(lambda: self.pin_unpin_item(self.table_widget.currentRow()))
        menu.exec(self.table_widget.viewport().mapToGlobal(position))

    def pin_unpin_item(self, row):
        item = self.table_widget.item(row, 0).text()
        if item in self.pinned_items:
            self.pinned_items.remove(item)
        else:
            self.pinned_items.add(item)
        self.populate_table()

    def search_treeview(self):
        search_text = self.search_entry.text().lower()
        self.table_widget.setRowCount(0)
        for key, data in self.cheapest_prices.items():
            name, stars = key
            provider, price = data
            if search_text in name.lower():
                self.add_table_row(name, stars, provider, price)
        if self.table_widget.rowCount() == 0:
            self.add_table_row("No results found", "", "", "")

    def find_cheapest_provider(self, all_items):
        items_by_name_and_stars = {}
        for item in all_items:
            key = (item.name, item.stars)
            if key not in items_by_name_and_stars:
                items_by_name_and_stars[key] = []
            items_by_name_and_stars[key].append(item)

        cheapest_prices = {}
        for key, items in items_by_name_and_stars.items():
            cheapest_item = min(items, key=lambda item: int(item.price))
            cheapest_prices[key] = (cheapest_item.provider, int(cheapest_item.price))

        return cheapest_prices

    def populate_table(self):
        self.table_widget.setRowCount(0)
        for key, data in self.cheapest_prices.items():
            name, stars = key
            provider, price = data
            self.add_table_row(name, stars, provider, price)

    def add_table_row(self, name, stars, provider, price):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(name))
        self.table_widget.setItem(row_position, 1, QTableWidgetItem('⭐' * int(stars)))
        self.table_widget.setItem(row_position, 2, QTableWidgetItem(provider))
        self.table_widget.setItem(row_position, 3, QTableWidgetItem(f"{price}zł"))

app = QApplication([])
window = MainWindow()
window.show()
app.exec()