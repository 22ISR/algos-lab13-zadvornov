from PIL import Image, ImageTk
from io import BytesIO
import requests
import json
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

def search_song(event=None):
    search_term = search.get().lower()
    if search_term:
        # Очистить предыдущие результаты
        for item in table.get_children():
            table.delete(item)

        # Добавить новые результаты
        for item in data:
            track_name = item['track']['name'].lower()
            artist_name = item['track']['artists'][0]['name'].lower()
            album_name = item['track']['album']['name'].lower()
            if search_term in track_name or search_term in artist_name or search_term in album_name:
                table.insert('', tk.END, values=(item['track']['name'], item['track']['artists'][0]['name'], item['track']['duration_ms'] // 1000, item['track']['album']['name']))
    else:
        # Если поле поиска пустое, отобразить все песни
        for item in data:
            table.insert('', tk.END, values=(item['track']['name'], item['track']['artists'][0]['name'], item['track']['duration_ms'] // 1000, item['track']['album']['name']))


def sort_by_column(tree, col, reverse):
    # Получение данных из таблицы
    data = [(tree.item(item, 'values'), item) for item in tree.get_children('')]
    
    # Сортировка данных
    data.sort(key=lambda x: x[0][columns.index(col)], reverse=reverse)
    
    # Перестановка элементов
    for index, (values, item) in enumerate(data):
        tree.move(item, '', index)
    
    # Следующий вызов метода изменит направление сортировки
    tree.heading(col, command=lambda: sort_by_column(tree, col, not reverse))



def on_item_select(event):
    # Получение выделенных элементов
    selected_items = table.selection()
    if selected_items:  # Проверка, что что-то выбрано
        # photo_image = ImageTk.PhotoImage(load_image_from_url(image_url))
        item = selected_items[0]  # Берем первый выбранный элемент
        values = table.item(item, 'values')
        print(f"Выбран: {values}")

def sort_song(event=None):
    selected_sort = sort.get()
    for item in table.get_children():
        table.delete(item)


    if selected_sort == 'По дате выхода':
        data.sort(key=lambda x: x['track']['album']['release_date'], reverse=True)
    elif selected_sort == 'По популярности':
        data.sort(key=lambda x: x['track']['popularity'], reverse=True)
        
    elif selected_sort == 'По длительности':
        data.sort(key=lambda x: x['track']['duration_ms'], reverse=True)
    
    
    for item in data:
        table.insert('', tk.END, values=(item['track']['name'], item['track']['artists'][0]['name'], item['track']['duration_ms'] // 1000, item['track']['album']['name']))

#Получение ответа 
try:
    response = requests.get('http://omsktec-playgrounds.ru/algos/lab13')
    data = response.json()
except:
    print('error')


def load_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    return None

def on_item_select(event):
    # Получение выделенных элементов
    selected_items = table.selection()
    if selected_items:  # Проверка, что что-то выбрано
        item = selected_items[0]  # Берем первый выбранный элемент
        values = table.item(item, 'values')
        print(f"Выбран: {values}")
        
        # Получение URL-адреса изображения
        album_name = values[3]
        for track in data:
            if track['track']['album']['name'] == album_name:
                image_url = track['track']['album']['images'][1]['url']
                photo_image = ImageTk.PhotoImage(load_image_from_url(image_url))
                image_label.config(image=photo_image)
                image_label.image = photo_image
                break




# Создание окна
root = tk.Tk()
root.title("Spotik")
root.geometry("1200x700")
root.configure(bg="#ffffff")


# Создание метки для отображения
# image_label = ttk.Label(root)
# image_label.pack()

image_frame = ttk.Frame(root)
image_frame.pack(side=tk.RIGHT, padx=20, expand=True)

image_label = ttk.Label(image_frame)
image_label.pack(fill=tk.BOTH, expand=True)




# Настройка шрифтов
title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
label_font = tkfont.Font(family="Helvetica", size=14)
entry_font = tkfont.Font(family="Helvetica", size=14)

sort_value = ['По дате выхода', 'По популярности', 'По длительности']
sort_value_var = (sort_value[0])

labelSearch = ttk.Label(root, font='label_font', text='Search', background="#ffffff")
search = ttk.Entry(root, font=entry_font)
labelSort = ttk.Label(root, font='label_font', text='Sort', background="#ffffff")
sort = ttk.Combobox(root, textvariable=sort_value_var, values=sort_value)



labelSearch.pack(pady=10)
search.pack(pady=10)
labelSort.pack(pady=10)
sort.pack(pady=10)


# Создание таблицы с указанием колонок
columns = ('title', 'name', 'time', 'album')
table = ttk.Treeview(root, columns=columns, show='headings')


# Привязка события выбора элемента
table.bind('<<TreeviewSelect>>', on_item_select)


# Размещение таблицы
table.pack(fill=tk.BOTH, expand=True)

# Настройка заголовков
table.heading('title', text='Название песни')
table.heading('name', text='Исполнитель')
table.heading('time', text='Длительность')
table.heading('album', text='Альбом')

# Настройка ширины колонок
table.column('title', width=150, anchor=tk.CENTER)
table.column('name', width=150)
table.column('time', width=50, anchor=tk.CENTER)
table.column('time', width=50, anchor=tk.CENTER)

search.bind('<Return>', search_song)
sort.bind("<<ComboboxSelected>>", sort_song)
# Привязка сортировки к заголовкам колонок
for col in columns:
    table.heading(col, command=lambda c=col: sort_by_column(table, c, False))


# Добавление данных в таблицу

for item in data:
    table.insert('', tk.END, values=(item['track']['name'], item['track']['artists'][0]['name'], item['track']['duration_ms'] // 1000, item['track']['album']['name']))

root.mainloop()