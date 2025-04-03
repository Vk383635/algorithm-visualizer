import tkinter as tk
from tkinter import ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

# Sorting Algorithms

def bubble_sort(arr, draw_array, delay):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                if j % 5 == 0:  # Optimize UI updates
                    draw_array(arr, ["blue" if x == j or x == j+1 else "red" for x in range(len(arr))])
                    time.sleep(delay)

def insertion_sort(arr, draw_array, delay):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            draw_array(arr, ["blue" if x == j or x == i else "red" for x in range(len(arr))])
            time.sleep(delay)
        arr[j + 1] = key

def merge_sort(arr, draw_array, delay):
    def merge(arr, left, mid, right):
        left_part = arr[left:mid+1]
        right_part = arr[mid+1:right+1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            if left_part[i] < right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1
            draw_array(arr, ["blue" if x >= left and x <= right else "red" for x in range(len(arr))])
            time.sleep(delay)
        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1

    def merge_sort_helper(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_helper(arr, left, mid)
            merge_sort_helper(arr, mid + 1, right)
            merge(arr, left, mid, right)

    merge_sort_helper(arr, 0, len(arr) - 1)

def draw_array(arr, color_array):
    ax.clear()
    ax.bar(range(len(arr)), arr, color=color_array)
    canvas.draw()

def generate_array():
    global arr
    arr = [random.randint(10, 100) for _ in range(30)]
    draw_array(arr, ["red" for _ in range(len(arr))])

def start_sorting():
    global arr
    sorting_algo = algo_menu.get()
    speed = speed_slider.get()
    start_time = time.time()
    
    def run_sort():
        if sorting_algo == "Bubble Sort":
            bubble_sort(arr, draw_array, speed)
        elif sorting_algo == "Insertion Sort":
            insertion_sort(arr, draw_array, speed)
        elif sorting_algo == "Merge Sort":
            merge_sort(arr, draw_array, speed)
        draw_array(arr, ["green" for _ in range(len(arr))])
        end_time = time.time()
        time_label.config(text=f"Time Taken: {end_time - start_time:.4f} sec")
    
    threading.Thread(target=run_sort, daemon=True).start()

def set_custom_array():
    global arr
    input_text = input_entry.get()
    try:
        arr = list(map(int, input_text.split(',')))
        draw_array(arr, ["red" for _ in range(len(arr))])
    except ValueError:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, "Invalid Input!")

# Main GUI Setup
root = tk.Tk()
root.title("Sorting Algorithm Visualizer")
root.geometry("800x700")

frame = tk.Frame(root)
frame.pack(pady=10)

algo_menu = ttk.Combobox(frame, values=["Bubble Sort", "Insertion Sort", "Merge Sort"], state="readonly")
algo_menu.set("Bubble Sort")
algo_menu.grid(row=0, column=0, padx=10)

speed_slider = tk.Scale(frame, from_=0.01, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, label="Speed")
speed_slider.set(0.1)
speed_slider.grid(row=0, column=1, padx=10)

generate_button = tk.Button(frame, text="Generate Array", command=generate_array)
generate_button.grid(row=0, column=2, padx=10)

start_button = tk.Button(frame, text="Start Sorting", command=start_sorting)
start_button.grid(row=0, column=3, padx=10)

input_entry = tk.Entry(root)
input_entry.pack()
input_button = tk.Button(root, text="Set Custom Array", command=set_custom_array)
input_button.pack()

time_label = tk.Label(root, text="Time Taken: 0 sec")
time_label.pack()

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

arr = []
generate_array()

root.mainloop()
