import tkinter as tk
from tkinter import ttk
import ttkbootstrap


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

root = tk.Tk()
style = ttkbootstrap.Style(theme='vapor')
root.title('Cheapest Price for Each Item')

root.geometry('1600x1200')

style.configure('Treeview', font=('Helvetica', 12), rowheight=50)
style.configure('Treeview.Heading', font=('Helvetica', 12))

treeview = ttk.Treeview(root, columns=('Item Name', 'Stars', 'Cheapest Provider', 'Cheapest Price'), show='headings')
treeview.heading('Item Name', text='Item Name')
treeview.heading('Stars', text='Stars')
treeview.heading('Cheapest Provider', text='Cheapest Provider')
treeview.heading('Cheapest Price', text='Cheapest Price')

treeview.place(x=0, y=50, width=1600, height=1150)

search_text = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_text, font=('Helvetica', 12))
search_entry.place(x=1150, y=5, width=400, height=40)

search_label = tk.Label(root, text="Search:", font=('Helvetica', 12))
search_label.place(x=1020, y=5, height=40)


def search_treeview(*args):
    search_text = search_entry.get().lower()
    for row in treeview.get_children():
        treeview.delete(row)
    if search_text:
        for key, data in cheapest_prices.items():
            name, stars = key
            provider, price = data
            if search_text in name.lower():
                treeview.insert('', 'end', values=(name, '☭' * int(stars), provider, str(price) + "zł"))
        if not treeview.get_children():
            treeview.insert('', 'end', values=("No results found", "", "", ""))
    else:
        for key, data in cheapest_prices.items():
            name, stars = key
            provider, price = data
            treeview.insert('', 'end', values=(name, '☭' * int(stars), provider, str(price) + "zł"))


search_text.trace("w", search_treeview)


def find_cheapest_provider(all_items):
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

current_col = None
current_col_dir = False

def treeview_sort_column(tv, col, reverse):
    global current_col
    global current_col_dir

    l = [(tv.set(k, col), k) for k in tv.get_children('')]

    if col == 'Cheapest Price':
        l = [(int(val.replace('zł', '')), k) for val, k in l]

    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    if current_col:
        tv.heading(current_col, text=current_col)

    sort_indicator = ' ↓' if reverse else ' ↑'
    tv.heading(col, text=col + sort_indicator)

    current_col = col
    current_col_dir = reverse

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

for col in ['Item Name', 'Stars', 'Cheapest Provider', 'Cheapest Price']:
    treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))

cheapest_prices = find_cheapest_provider(all_items)
for key, data in cheapest_prices.items():
    name, stars = key
    provider, price = data
    treeview.insert('', 'end', values=(name, '☭' * int(stars), provider, str(price) + "zł"))


root.mainloop()
