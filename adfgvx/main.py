import tkinter as tk
from tkinter import ttk


adfgvx_table = {
    'A': ['0', '5', 'D', 'E', '1', 'F'],
    'D': ['C', 'K', '9', '6', 'G', 'L'],
    'F': ['8', 'O', 'R', '2', 'M', 'Q'],
    'G': ['T', '3', 'X', 'U', 'W', 'S'],
    'V': ['Y', 'Z', '7', '4', 'B', 'A'],
    'X': ['N', 'P', 'H', 'V', 'J', 'I']
}

# Функция для получения координат в таблице шифра
def get_adfgvx_coordinates(char):
    for row_key, row_values in adfgvx_table.items():
        if char.upper() in row_values:
            col_index = row_values.index(char.upper())
            return row_key, list(adfgvx_table.keys())[col_index]
    raise ValueError(f"Character '{char}' not found in ADFGVX table.")


# Функция для нахождения символа по координатам в таблице шифра
def get_char_from_coordinates(row, col):
    row_values = adfgvx_table[row]
    col_index = list(adfgvx_table.keys()).index(col)
    return row_values[col_index]


# Функция шифрования
def adfgvx_encrypt(text, key):
    # Первый этап: замена символов на пары
    pairs = []
    for char in text:
        if char.isalnum():
            row, col = get_adfgvx_coordinates(char)
            pairs.append(row + col)
    # Промежуточное сообщение
    intermediate_message = ''.join(pairs)
    # Дополнение символами, чтобы длина делилась на длину ключа
    while len(intermediate_message) % len(key) != 0:
        intermediate_message += '0'  # Маркер дополняет сообщение
    # Второй этап: перестановка по ключу
    sorted_key = ''.join(sorted(key))
    columns = {k: [] for k in sorted_key}
    for i, char in enumerate(intermediate_message):
        columns[key[i % len(key)]].append(char)
    encrypted_message = ''.join([''.join(columns[k]).rstrip('0') for k in sorted_key])
    return encrypted_message

# Функция дешифрования
def adfgvx_decrypt(encrypted_message, key):
    # Первый этап: восстановление столбцов
    sorted_key = ''.join(sorted(key))
    col_lengths = [len(encrypted_message) // len(key)] * len(key)
    # Дополнительная длина в случае остатка
    for i in range(len(encrypted_message) % len(key)):
        col_lengths[i] += 1
    columns = {}
    index = 0
    # Считывание по длинам колонок
    for k, length in zip(sorted_key, col_lengths):
        columns[k] = encrypted_message[index:index + length]
        index += length
    # Восстановление промежуточного сообщения по ключу
    ordered_columns = [columns[k] for k in key]
    intermediate_message = ''
    for t in zip(*ordered_columns):
        intermediate_message += ''.join(t)
    # Добавление оставшихся символов (если длина не кратна ключу)
    remaining_chars = len(encrypted_message) % len(key)
    if remaining_chars > 0:
        intermediate_message += ''.join([col[len(encrypted_message) // len(key)] for col in ordered_columns[:remaining_chars]])
    # Восстановление исходного текста
    decrypted_message = []
    for i in range(0, len(intermediate_message), 2):
        try:
            row = intermediate_message[i]
            col = intermediate_message[i + 1]
            decrypted_message.append(get_char_from_coordinates(row, col))
        except IndexError:
            # Игнорирование дополняющих символов
            break
    return ''.join(decrypted_message).rstrip('0')  # Убираем маркеры


def encrypt_message():
    text = message_input.get("1.0", tk.END).strip()
    key = key_input.get()
    if not key:
        result_output.set("Введите ключ!!1")
        return
    encrypted_text = adfgvx_encrypt(text, key)
    result_output.set(encrypted_text)

def decrypt_message():
    text = encrypted_input.get("1.0", tk.END).strip()
    key = key_input.get()
    if not key:
        decrypted_output.set("Введите ключ!!1")
        return
    decrypted_text = adfgvx_decrypt(text, key)
    decrypted_output.set(decrypted_text)

def copy(content):
    root.clipboard_clear()
    root.clipboard_append(content)
    root.update()

def paste(entry):
    entry.delete("1.0", tk.END)
    entry.insert("1.0", root.clipboard_get())

# Создание окна приложения
root = tk.Tk()
root.title("Шифр ADFGVX")
root.geometry("600x550")

# Ввод сообщения
message_frame = ttk.Frame(root)
message_frame.pack(pady=5, fill=tk.X)
ttk.Label(message_frame, text="Введите сообщение для шифрования:").pack(anchor=tk.W)
message_input = tk.Text(message_frame, height=4, wrap=tk.WORD)
message_input.pack(fill=tk.BOTH, padx=5, expand=True)
ttk.Button(message_frame, text="Копировать", command=lambda: copy(message_input.get("1.0", tk.END).strip())).pack(side=tk.LEFT, padx=2)
ttk.Button(message_frame, text="Вставить", command=lambda: paste(message_input)).pack(side=tk.LEFT, padx=2)

# Ввод ключа
ttk.Label(root, text="Введите ключ для шифрования/дешифрования:").pack(pady=5)
key_input = ttk.Entry(root, width=20)
key_input.pack(pady=5)

# Кнопка для шифрования
encrypt_button = ttk.Button(root, text="Зашифровать!!!1", command=encrypt_message)
encrypt_button.pack(pady=5)

# Поле для вывода зашифрованного текста
result_frame = ttk.Frame(root)
result_frame.pack(pady=5, fill=tk.X)
result_output = tk.StringVar()
result_label = ttk.Label(result_frame, textvariable=result_output, foreground="blue", wraplength=550, anchor=tk.W, justify=tk.LEFT)
result_label.pack(fill=tk.BOTH, padx=5, expand=True)
ttk.Button(result_frame, text="Копировать", command=lambda: copy(result_output.get())).pack(side=tk.LEFT, padx=5)

# Ввод зашифрованного сообщения
encrypted_frame = ttk.Frame(root)
encrypted_frame.pack(pady=5, fill=tk.X)
ttk.Label(encrypted_frame, text="Введите сообщение для дешифрования:").pack(anchor=tk.W)
encrypted_input = tk.Text(encrypted_frame, height=4, wrap=tk.WORD)
encrypted_input.pack(fill=tk.BOTH, padx=5, expand=True)
ttk.Button(encrypted_frame, text="Копировать", command=lambda: copy(encrypted_input.get("1.0", tk.END).strip())).pack(side=tk.LEFT, padx=2)
ttk.Button(encrypted_frame, text="Вставить", command=lambda: paste(encrypted_input)).pack(side=tk.LEFT, padx=2)

# Кнопка для дешифрования
decrypt_button = ttk.Button(root, text="Расшифровать!1!", command=decrypt_message)
decrypt_button.pack(pady=5)

# Поле для вывода расшифрованного текста
decrypted_output = tk.StringVar()
decrypted_label = ttk.Label(root, textvariable=decrypted_output, foreground="green", wraplength=550, anchor=tk.W, justify=tk.LEFT)
decrypted_label.pack(fill=tk.BOTH, padx=5, expand=True)

# Запуск приложения
root.mainloop()
