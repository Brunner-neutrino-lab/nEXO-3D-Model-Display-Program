#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import tkinter as tk
import time
import numpy as np
from numpy.random import exponential #for exponential distribution (distribution of distance between events in Poisson process)


# LED setup: wall/floor for outer detector, RGB for colours in TPC

""""
wallGPIO = 17 #physical/board pin 11
floorGPIO = 27 #physical/board pin 13
redGPIO = 9 #physical/board pin 21
greenGPIO = 11 #physical/board pin 23
blueGPIO = 25 #physical/board pin 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(wallGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(floorGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(redGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(greenGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(blueGPIO, GPIO.OUT, initial=GPIO.LOW)

RED = GPIO.PWM(redGPIO,100)
GREEN = GPIO.PWM(greenGPIO,100)
BLUE = GPIO.PWM(blueGPIO,100)

RED.start(0)
GREEN.start(0)
BLUE.start(0)

"""

def flash(events): #run this every time an LED flashes. 
    
    flashtime = 0.5 #s that LEDs should flash

    #turn LEDs on
    for event in events:
        if event == "ROI_background": 
            #RED.ChangeDutyCycle(0)
            #GREEN.ChangeDutyCycle(240/255 * 100)
            #BLUE.ChangeDutyCycle(40/255 * 100)
            print("ROI_background on")
        if event == "0vbb":
            #RED.ChangeDutyCycle(255/255 * 100)
            #GREEN.ChangeDutyCycle(69/255 * 100)
            #BLUE.ChangeDutyCycle(0) 
            print("0vbb on")
        if event == "2vbb": 
            #RED.ChangeDutyCycle(255/255 * 100)
            #GREEN.ChangeDutyCycle(20/255 * 100)
            #BLUE.ChangeDutyCycle(147/255 * 100)   
            print("2vbb on")
        if event == "Xe137": 
            #RED.ChangeDutyCycle(200/255 * 100)
            #GREEN.ChangeDutyCycle(200/255 * 100)
            #BLUE.ChangeDutyCycle(200/255 * 100)  
            print("Xe137 on")
        if event == "solar v": 
            #RED.ChangeDutyCycle(245/255 * 100)
            #GREEN.ChangeDutyCycle(235/255 * 100)
            #BLUE.ChangeDutyCycle(10/255 * 100)   
            print("solar v on")
        if event == "TPC_muon": # turn on bottom of outer detector
            #GPIO.output(floorGPIO, GPIO.HIGH)
            print("TPC_muon on")
        if event == "cryostat_muon": # turn on whole outer detector
            #GPIO.output(floorGPIO, GPIO.HIGH)
            #GPIO.output(wallGPIO, GPIO.HIGH)
            print("cryostat muon on")
    
    time.sleep(flashtime)

    #turn LEDs off
    #RED.ChangeDutyCycle(0)
    #GREEN.ChangeDutyCycle(0)
    #BLUE.ChangeDutyCycle(0)
    #GPIO.output(floorGPIO, GPIO.LOW)
    #GPIO.output(wallGPIO, GPIO.LOW)

def main_loop(): 

    ## first calculate expected event rates

    rates_per_year = np.zeros(7) #array to store events/year for each type
    #event_types = ["0vbb", "2vbb", "Xe 137", "solar v", "ROI background", "TPC muon", "cryostat muon"]


    # 0vbb: 
    #ROI: energy range of 0vbb FWHM, inner 2t of xenon
    #FWHM is approx. 76.1% of area under Gaussian

    Xe_mass = 0.1*133.9053945 + 0.9*135.407219 #in g/mol; for 90% Xe 136, 10% Xe 134
    if selection_volume.get() == 1: #1 ton inner volume
        n_xenon = 10**6 / Xe_mass * 6.022*10**23
    elif selection_volume.get()==2: #default inner volume is 2 tons
        n_xenon = 2 * 10**6 / Xe_mass * 6.022*10**23 #2 tons * 10^6 g/tons
    
    if selection_half_life.get() == 2: #shorter half-life
        half_life = 1 * 10**27 #years
    elif selection_half_life.get() == 3: #half-life sensitivity
        half_life = 1.35 * 10**28
    elif selection_half_life.get() == 1: #3 sigma discovery potential half-life
        half_life = 7.4 * 10**27 
    
    mean_lifetime = half_life/np.log(2)  #years
    mean_decays = n_xenon/mean_lifetime # particles/year
    mean_decays_ROI = mean_decays * 0.761 #events in ROI
    rates_per_year[0] = mean_decays_ROI


    # background
    if selection_volume.get() == 1: #inner 1t
        total_bgd = 1.4 * 10**-4 #events/(FHWM kg yr)
    elif selection_volume.get() == 2: #inner 2t
        total_bgd = 3.6 * 10**-4 #events/(FHWM kg yr)
    bgd_rate = total_bgd * 2 * 10**3 #events/yr
    rate_2vbb = bgd_rate * 0.008 #2vbb is about 0.8% of background
    rate_solar_v = bgd_rate * 0.021 #solar neutrino is roughly 2.1% of background
    rate_Xe137 = bgd_rate * 0.024 #xe 137 is about 2.4% of background
    bgd_remaining = bgd_rate * 0.947
    rates_per_year[1] = rate_2vbb
    rates_per_year[2] = rate_Xe137
    rates_per_year[3] = rate_solar_v
    rates_per_year[4] = bgd_remaining

    # muon through TPC
    mean = 0.6 * 365.25  #muons/year (0.6/day)
    rates_per_year[5] = mean

    # muon through cryostat
    mean = 5 * 365.25 #muons/year (5/day)
    rates_per_year[6] = mean

    # time scale: 2 min = 10 years, so 1 year = 12 seconds
    # events/year * 1 year/12 seconds = events/second. take reciprocal for seconds/event
    # seconds/event is expected (mean) time between successive events
    mean_times = 1/(rates_per_year/12)
    mean_0vbb, mean_2vbb, mean_Xe137, mean_solar_v, mean_ROI_background, mean_TPC_muon, mean_cryostat_muon = mean_times

    ## now simulate events

    # generate time until first event for each event type
    time_0vbb = exponential(mean_0vbb) # time in seconds
    time_2vbb = exponential(mean_2vbb)
    time_Xe137 = exponential(mean_Xe137)
    time_solar_v = exponential(mean_solar_v)
    time_ROI_background = (mean_ROI_background)
    time_TPC_muon = exponential(mean_TPC_muon)
    time_cryostat_muon = exponential(mean_cryostat_muon)

    # initialize timer for each event type
    timer_0vbb = time.time()
    timer_2vbb = time.time()
    timer_Xe137 = time.time()
    timer_solar_v = time.time()
    timer_ROI_background = time.time()
    timer_TPC_muon = time.time()
    timer_cryostat_muon = time.time()

    start_time = time.time()
    events_triggered = [] #list of LEDs to flash

    while True:
        try: 
            time_now = time.time() #current time

            #for each event type, check if an LED should flash
            if time_now - timer_0vbb > time_0vbb: #check if timer for each event has elapsed
                events_triggered.append("0vbb") #if timer has elapsed, trigger LED flash
                time_0vbb = exponential(mean_0vbb) #generate new time until next event
                timer_0vbb = time.time() #reset timer
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
        
        
            #flash all triggered LEDs (if any are triggered)
            if events_triggered != []:
                flash(events_triggered)
                events_triggered = [] #reset triggered events list


        except KeyboardInterrupt:
            break


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

print_button = tk.Button(choices_frame, text="Submit Selections", command=main_loop) #put the function here
print_button.pack(pady=10)

root.mainloop()



#GPIO.cleanup()


