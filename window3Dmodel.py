import tkinter as tk

def print_selection():
    print("selection_half_life =", selection_half_life.get(), "selection_volume =", selection_volume.get())
    
root = tk.Tk()
root.title("Test")

main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

cases = [
    ("Muons", "blue"),
    ("Xe137", "white"),
    ("0vbb", "orange"),
    ("2vbb", "purple"),
    ("Background", "cyan"),
    ("Solar v", "yellow"),
]

selection_half_life = tk.IntVar()
selection_volume = tk.IntVar()

table_frame = tk.Frame(main_frame)
table_frame.pack(side=tk.LEFT, padx=20, pady=20)

tk.Label(table_frame, text="Color Coding", font=('Arial', 16, 'bold')).grid(row=0, columnspan=2, pady=10)

for i, (case, color) in enumerate(cases, start=1):
    tk.Label(table_frame, text=case, font=('Arial', 12)).grid(row=i, column=0, padx=5, pady=5, sticky='w')
    color_label = tk.Label(table_frame, text=color, font=('Arial', 12), bg=color, fg='black', width=10)
    color_label.grid(row=i, column=1, padx=5, pady=5, sticky='w')

choices_frame = tk.Frame(main_frame)
choices_frame.pack(side=tk.RIGHT, padx=20)

checkbox_frame = tk.Frame(choices_frame)
checkbox_frame.pack(pady=10)

tk.Label(checkbox_frame, text="Choose Half Life:", font=('Arial', 14, 'bold')).pack(pady=5)

checkbox1 = tk.Radiobutton(checkbox_frame, text="Half Life 1", variable=selection_half_life, value=1, font=('Arial', 12))
checkbox1.pack(anchor='w')
checkbox2 = tk.Radiobutton(checkbox_frame, text="Half Life 2", variable=selection_half_life, value=2, font=('Arial', 12))
checkbox2.pack(anchor='w')
checkbox3 = tk.Radiobutton(checkbox_frame, text="Half Life 3", variable=selection_half_life, value=3, font=('Arial', 12))
checkbox3.pack(anchor='w')

volume_frame = tk.Frame(choices_frame)
volume_frame.pack(pady=10)

tk.Label(volume_frame, text="Choose Volume:", font=('Arial', 14, 'bold')).pack(pady=5)

radio1 = tk.Radiobutton(volume_frame, text="1 ton", variable=selection_volume, value=1, font=('Arial', 12))
radio1.pack(anchor='w')
radio2 = tk.Radiobutton(volume_frame, text="2 tons", variable=selection_volume, value=2, font=('Arial', 12))
radio2.pack(anchor='w')

print_button = tk.Button(choices_frame, text="Submit Selections", command=print_selection) #put the function here
print_button.pack(pady=10)

root.mainloop()








