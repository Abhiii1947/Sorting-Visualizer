import tkinter as tk
from tkinter import ttk
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def bubble_sort(data, draw_data, delay):
    for i in range(len(data) - 1):
        for j in range(len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                draw_data(data, [j, j + 1])  # Highlight swapped elements
                time.sleep(delay)
    draw_data(data, range(len(data)))  # Highlight all elements in red at the end

def insertion_sort(data, draw_data, delay):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            draw_data(data, [j + 1, j])  # Highlight the moving element
            time.sleep(delay)
            j -= 1
        data[j + 1] = key
        draw_data(data, [j + 1])
    draw_data(data, range(len(data)))  # Highlight all elements in red at the end

def selection_sort(data, draw_data, delay):
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
                draw_data(data, [min_idx, j])  # Highlight the comparison
                time.sleep(delay)
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_data(data, [i, min_idx])  # Highlight the swap
    draw_data(data, range(len(data)))  # Highlight all elements in red at the end

def merge_sort(data, draw_data, delay):
    def merge_sort_recursive(data, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_recursive(data, left, mid)
            merge_sort_recursive(data, mid + 1, right)
            merge(data, left, mid, right)
            draw_data(data, list(range(left, right + 1)))
            time.sleep(delay)

    def merge(data, left, mid, right):
        left_part = data[left:mid + 1]
        right_part = data[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                data[k] = left_part[i]
                i += 1
            else:
                data[k] = right_part[j]
                j += 1
            k += 1
        while i < len(left_part):
            data[k] = left_part[i]
            i += 1
            k += 1
        while j < len(right_part):
            data[k] = right_part[j]
            j += 1
            k += 1

    merge_sort_recursive(data, 0, len(data) - 1)
    draw_data(data, range(len(data)))  # Highlight all elements in red at the end

# Draw Data Function (Unchanged)
def draw_data(data, color_indices):
    canvas.delete("all")
    canvas_height = canvas.winfo_height()
    canvas_width = canvas.winfo_width()
    bar_width = canvas_width / (len(data) + 1)
    spacing = 5  # Space between bars
    normalized_data = [i / max(data) for i in data]

    for i, value in enumerate(normalized_data):
        x0 = i * bar_width + spacing
        y0 = canvas_height - value * (canvas_height - 20)
        x1 = (i + 1) * bar_width
        y1 = canvas_height
        color = "red" if i in color_indices else "blue"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        canvas.create_text(x0 + bar_width / 2, y0, anchor=tk.S, text=str(data[i]), fill="white")
    root.update_idletasks()

# Start Sorting
def start_sorting():
    global data
    selected_algorithm = algo_combobox.get()
    speed = speed_scale.get()
    if selected_algorithm == "Bubble Sort":
        bubble_sort(data, draw_data, speed)
    elif selected_algorithm == "Insertion Sort":
        insertion_sort(data, draw_data, speed)
    elif selected_algorithm == "Selection Sort":
        selection_sort(data, draw_data, speed)
    elif selected_algorithm == "Merge Sort":
        merge_sort(data, draw_data, speed)



def generate_data():
    global data
    user_input = array_entry.get()
    if user_input.strip():  # If user provides an input array
        try:
            data = list(map(int, user_input.split(',')))  # Parse user input
            draw_data(data, [])
        except ValueError:
            array_entry.delete(0, tk.END)
            array_entry.insert(0, "Invalid input! Use comma-separated numbers.")
            return
    else:  # Generate a random array if no input is provided
        data = [random.randint(1, 100) for _ in range(size_scale.get())]
        draw_data(data, [])


# Main GUI
root = tk.Tk()
root.title("Sorting Visualizer")

# Frame for Controls
frame = tk.Frame(root, padx=10, pady=5)
frame.pack(side=tk.TOP)

# Algorithm Selection
tk.Label(frame, text="Algorithm: ").grid(row=0, column=0, padx=5, pady=5)
algo_combobox = ttk.Combobox(frame, values=["Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort"], state="readonly")
algo_combobox.grid(row=0, column=1, padx=5, pady=5)
algo_combobox.current(0)

# Speed Control
tk.Label(frame, text="Speed: ").grid(row=0, column=2, padx=5, pady=5)
speed_scale = tk.Scale(frame, from_=0.01, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
speed_scale.set(0.1)
speed_scale.grid(row=0, column=3, padx=5, pady=5)

# Size Control
tk.Label(frame, text="Size: ").grid(row=0, column=4, padx=5, pady=5)
size_scale = tk.Scale(frame, from_=5, to=50, resolution=1, orient=tk.HORIZONTAL)
size_scale.set(20)
size_scale.grid(row=0, column=5, padx=5, pady=5)

# Array Input
tk.Label(frame, text="Array: ").grid(row=1, column=0, padx=5, pady=5)
array_entry = tk.Entry(frame, width=50)
array_entry.grid(row=1, column=1, columnspan=5, padx=5, pady=5)

# Buttons
tk.Button(frame, text="Generate", command=generate_data).grid(row=0, column=6, padx=5, pady=5)
tk.Button(frame, text="Start", command=start_sorting).grid(row=0, column=7, padx=5, pady=5)

# Canvas for Visualization
canvas = tk.Canvas(root, width=800, height=400, bg="black")
canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Global Data
data = []

# Run Application
root.mainloop()



