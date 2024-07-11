import tkinter as tk
import time
import numpy as np
from numpy.random import exponential
import threading


import RPi.GPIO as GPIO

wallGPIO = 17  # physical/board pin 11
floorGPIO = 27  # physical/board pin 13
redGPIO = 9  # physical/board pin 21
greenGPIO = 11  # physical/board pin 23
blueGPIO = 25  # physical/board pin 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(wallGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(redGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(greenGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(blueGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(floorGPIO, GPIO.OUT, initial=GPIO.LOW)

RED = GPIO.PWM(redGPIO, 100)
GREEN = GPIO.PWM(greenGPIO, 100)
BLUE = GPIO.PWM(blueGPIO, 100)

RED.start(0)
GREEN.start(0)
BLUE.start(0)

# Global variables for threading and simulation control
simulation_thread = None
stop_simulation_event = threading.Event()
is_simulation_running = False

def flash(events):
    flashtime = 0.5  # s that LEDs should flash

    # Turn LEDs on
    for event in events:
        if event == "ROI_background":
            RED.ChangeDutyCycle(0)
            GREEN.ChangeDutyCycle(240 / 255 * 100)
            BLUE.ChangeDutyCycle(40 / 255 * 100)
            print("ROI_background on")
        if event == "0vbb":
            RED.ChangeDutyCycle(255 / 255 * 100)
            GREEN.ChangeDutyCycle(69 / 255 * 100)
            BLUE.ChangeDutyCycle(0)
            print("0vbb on")
        if event == "2vbb":
            RED.ChangeDutyCycle(255 / 255 * 100)
            GREEN.ChangeDutyCycle(20 / 255 * 100)
            BLUE.ChangeDutyCycle(147 / 255 * 100)
            print("2vbb on")
        if event == "Xe137":
            RED.ChangeDutyCycle(200 / 255 * 100)
            GREEN.ChangeDutyCycle(200 / 255 * 100)
            BLUE.ChangeDutyCycle(200 / 255 * 100)
            print("Xe137 on")
        if event == "solar v":
            RED.ChangeDutyCycle(245 / 255 * 100)
            GREEN.ChangeDutyCycle(235 / 255 * 100)
            BLUE.ChangeDutyCycle(10 / 255 * 100)
            print("solar v on")
        if event == "TPC_muon":  # turn on bottom of outer detector
            GPIO.output(floorGPIO, GPIO.HIGH)
            print("TPC_muon on")
        if event == "cryostat_muon":  # turn on whole outer detector
            GPIO.output(floorGPIO, GPIO.HIGH)
            GPIO.output(wallGPIO, GPIO.HIGH)
            print("cryostat muon on")

    time.sleep(flashtime)

    # Turn LEDs off
    RED.ChangeDutyCycle(0)
    GREEN.ChangeDutyCycle(0)
    BLUE.ChangeDutyCycle(0)
    GPIO.output(floorGPIO, GPIO.LOW)
    GPIO.output(wallGPIO, GPIO.LOW)

def main_loop():
    global stop_simulation_event, is_simulation_running
    is_simulation_running = True
    
    rates_per_year = np.zeros(7)  # array to store events/year for each type

    # 0vbb:
    Xe_mass = 0.1 * 133.9053945 + 0.9 * 135.407219  # in g/mol; for 90% Xe 136, 10% Xe 134
    if selection_volume.get() == 1:  # 1 ton inner volume
        n_xenon = 10 ** 6 / Xe_mass * 6.022 * 10 ** 23
    elif selection_volume.get() == 2:  # default inner volume is 2 tons
        n_xenon = 2 * 10 ** 6 / Xe_mass * 6.022 * 10 ** 23  # 2 tons * 10^6 g/tons

    if selection_half_life.get() == 2:  # shorter half-life
        half_life = 1 * 10 ** 27  # years
    elif selection_half_life.get() == 3:  # half-life sensitivity
        half_life = 1.35 * 10 ** 28
    elif selection_half_life.get() == 1:  # 3 sigma discovery potential half-life
        half_life = 7.4 * 10 ** 27

    mean_lifetime = half_life / np.log(2)  # years
    mean_decays = n_xenon / mean_lifetime  # particles/year
    mean_decays_ROI = mean_decays * 0.761  # events in ROI
    rates_per_year[0] = mean_decays_ROI

    if selection_volume.get() == 1:  # inner 1t
        total_bgd = 1.4 * 10 ** -4  # events/(FHWM kg yr)
    elif selection_volume.get() == 2:  # inner 2t
        total_bgd = 3.6 * 10 ** -4  # events/(FHWM kg yr)
    bgd_rate = total_bgd * 2 * 10 ** 3  # events/yr
    rate_2vbb = bgd_rate * 0.008  # 2vbb is about 0.8% of background
    rate_solar_v = bgd_rate * 0.021  # solar neutrino is roughly 2.1% of background
    rate_Xe137 = bgd_rate * 0.024  # xe 137 is about 2.4% of background
    bgd_remaining = bgd_rate * 0.947
    rates_per_year[1] = rate_2vbb
    rates_per_year[2] = rate_Xe137
    rates_per_year[3] = rate_solar_v
    rates_per_year[4] = bgd_remaining

    mean = 0.6 * 365.25  # muons/year (0.6/day)
    rates_per_year[5] = mean

    mean = 5 * 365.25  # muons/year (5/day)
    rates_per_year[6] = mean

    mean_times = 1 / (rates_per_year / 12)
    mean_0vbb, mean_2vbb, mean_Xe137, mean_solar_v, mean_ROI_background, mean_TPC_muon, mean_cryostat_muon = mean_times

    time_0vbb = exponential(mean_0vbb)  # time in seconds
    time_2vbb = exponential(mean_2vbb)
    time_Xe137 = exponential(mean_Xe137)
    time_solar_v = exponential(mean_solar_v)
    time_ROI_background = mean_ROI_background
    time_TPC_muon = exponential(mean_TPC_muon)
    time_cryostat_muon = exponential(mean_cryostat_muon)

    timer_0vbb = time.time()
    timer_2vbb = time.time()
    timer_Xe137 = time.time()
    timer_solar_v = time.time()
    timer_ROI_background = time.time()
    timer_TPC_muon = time.time()
    timer_cryostat_muon = time.time()

    start_time = time.time()
    events_triggered = []

    elapsed_time = 0

    while elapsed_time < timer_duration.get()*12 and not stop_simulation_event.is_set():  # 120 seconds = 10 years (1yr = 12s)
        try:
            time_now = time.time()

            if time_now - timer_0vbb > time_0vbb:
                events_triggered.append("0vbb")
                time_0vbb = exponential(mean_0vbb)
                timer_0vbb = time.time()
            if time_now - timer_2vbb > time_2vbb:
                events_triggered.append("2vbb")
                time_2vbb = exponential(mean_2vbb)
                timer_2vbb = time.time()
            if time_now - timer_Xe137 > time_Xe137:
                events_triggered.append("Xe137")
                time_Xe137 = exponential(mean_Xe137)
                timer_Xe137 = time.time()
            if time_now - timer_solar_v > time_solar_v:
                events_triggered.append("solar v")
                time_solar_v = exponential(mean_solar_v)
                timer_solar_v = time.time()
            if time_now - timer_ROI_background > time_ROI_background:
                events_triggered.append("ROI_background")
                time_ROI_background = exponential(mean_ROI_background)
                timer_ROI_background = time.time()
            if time_now - timer_TPC_muon > time_TPC_muon:
                events_triggered.append("TPC_muon")
                time_TPC_muon = exponential(mean_TPC_muon)
                timer_TPC_muon = time.time()
            if time_now - timer_cryostat_muon > time_cryostat_muon:
                events_triggered.append("cryostat_muon")
                time_cryostat_muon = exponential(mean_cryostat_muon)
                timer_cryostat_muon = time.time()

            if events_triggered:
                flash(events_triggered)
                events_triggered = []

            elapsed_time = time.time() - start_time

        except KeyboardInterrupt:
            break
    print("end")
    stop_simulation_event.clear()  # Clear the stop event flag
    is_simulation_running = False

def update_timer_label(start_years=10):
    global timer_label_text
    
    elapsed_seconds = 0  # initialize elapsed seconds
    
    def update(): # Update timer on the display
        nonlocal elapsed_seconds
        if elapsed_seconds <= start_years * 12:  # Convert years to seconds (1yr = 12s)
            years_remaining = start_years - elapsed_seconds / 12
            timer_label.config(text=f"Time remaining: {years_remaining:.2f} years")
            elapsed_seconds += 1
            if is_simulation_running:
                root.after(1000, update)
    
    update()


def start_simulation():
    global simulation_thread, stop_simulation_event, is_simulation_running
    
    # Get selected timer duration (5 or 10 years)
    start_years = timer_duration.get()
    
    # Update timer label with selected duration
    update_timer_label(start_years)

    # Check if a simulation is already running
    if is_simulation_running:
        # Set the stop event to signal the thread to stop
        stop_simulation_event.set()
        
        # Wait for the simulation thread to finish
        if simulation_thread:
            simulation_thread.join()
    
    # Clear the stop event for a new simulation
    stop_simulation_event.clear()

    # Reset timer label
    timer_label.config(text="Time remaining: 0.00 years")
    
    # Start a new simulation thread
    simulation_thread = threading.Thread(target=main_loop)
    simulation_thread.start()

def stop_simulation():
    global simulation_thread, stop_simulation_event, is_simulation_running
    
    # Set the stop event to signal the thread to stop
    stop_simulation_event.set()


root = tk.Tk()
root.title("Command Window")
root.geometry("800x480")
root.configure(bg='#2874A6')

main_frame = tk.Frame(root, bg='lightblue')
main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Color Coding Labels
cases = [
    ("Muons", 'blue', 'blue'),
    ("ROI_background", "green", "#00F028"),  # RGB(0, 240, 40)
    ("0vbb", "orange", "#FF4500"),           # RGB(255, 69, 0)
    ("2vbb", "pink", "#FF1493"),             # RGB(255, 20, 147)
    ("Xe137", "white", "white"),            # RGB(200, 200, 200)
    ("Solar v", "yellow", "#F5EB0A"),        # RGB(245, 235, 10)
]


# Frame for Color Coding (Left)
table_frame = tk.Frame(main_frame)
table_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Building the color coding
tk.Label(table_frame, text="Color Coding", font=('Arial', 16, 'bold')).grid(row=0, columnspan=2, pady=8)
for i, (case, color_name, color_hex) in enumerate(cases, start=1):
    tk.Label(table_frame, text=case, font=('Arial', 12)).grid(row=i, column=0, padx=4, pady=4, sticky='w')
    color_label = tk.Label(table_frame, text=color_name, bg=color_hex, fg='black', font=('Arial', 12), width=8, height=1)
    color_label.grid(row=i, column=1, padx=8, pady=8, sticky='w')


# Frame for Selection Choices 
choices_frame = tk.Frame(main_frame)
choices_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Frame for Half-life Selection
checkbox_frame = tk.Frame(choices_frame)
checkbox_frame.pack(padx=10, pady=10)

tk.Label(checkbox_frame, text="Choose Half Life:", font=('Arial', 16, 'bold')).pack(pady=2)

# text for exponents
text1 = "7.4²⁷ years (3\u03C3)"  # 7.4^27
text2 = "1.0²⁷ years (Shorter)"  # 1.0^27
text3 = "1.35²⁸ years (90% CL)"  # 1.35^28

# Variables for radio buttons
selection_half_life = tk.IntVar()

# Create radio buttons with formatted text
checkbox1 = tk.Radiobutton(checkbox_frame, text=text1, variable=selection_half_life, value=1, font=('Arial', 14))
checkbox1.pack(anchor='w')
checkbox2 = tk.Radiobutton(checkbox_frame, text=text2, variable=selection_half_life, value=2, font=('Arial', 14))
checkbox2.pack(anchor='w')
checkbox3 = tk.Radiobutton(checkbox_frame, text=text3, variable=selection_half_life, value=3, font=('Arial', 14))
checkbox3.pack(anchor='w')

# Frame for Volume Selection
volume_frame = tk.Frame(choices_frame)
volume_frame.pack(padx=10, pady=40)

tk.Label(volume_frame, text="Choose Volume:", font=('Arial', 16, 'bold')).pack(pady=2)

selection_volume = tk.IntVar()

radio1 = tk.Radiobutton(volume_frame, text="1 ton", variable=selection_volume, value=1, font=('Arial', 12))
radio1.pack(anchor='w')
radio2 = tk.Radiobutton(volume_frame, text="2 tons", variable=selection_volume, value=2, font=('Arial', 12))
radio2.pack(anchor='w')



# Frame for Submit Button and Timer Label (Right)
choices_frame2 = tk.Frame(main_frame)
choices_frame2.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Frame for Timer Duration Selection
timer_frame = tk.Frame(choices_frame2)
timer_frame.pack(padx=10, pady=10)

tk.Label(timer_frame, text="Choose Timer Duration:", font=('Arial', 16, 'bold')).pack(pady=2)

timer_duration = tk.IntVar()

radio5 = tk.Radiobutton(timer_frame, text="5 years", variable=timer_duration, value=5, font=('Arial', 12))
radio5.pack(anchor='w')
radio10 = tk.Radiobutton(timer_frame, text="10 years", variable=timer_duration, value=10, font=('Arial', 12))
radio10.pack(anchor='w')


# Button to Start Simulation
start_button = tk.Button(choices_frame2, text="Start Simulation", command=start_simulation, width=15, height=2, padx = 10, pady = 10, font = ('Arial', 18, 'bold'))
start_button.pack(padx=10, pady=10)

# Button to Stop Simulation
stop_button = tk.Button(choices_frame2, text="Stop", command=stop_simulation, width=8, height=1, padx=10, pady=10, font=('Arial', 16, 'bold'))
stop_button.pack(padx=10, pady=10)

# Label to Display Timer
timer_label = tk.Label(choices_frame2, text="Time remaining: 0.00 years", font=('Arial', 14, 'bold'))
timer_label.pack(pady=10)

# Configuring expansion options for main_frame
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

root.mainloop()

#GPIO.cleanup()


