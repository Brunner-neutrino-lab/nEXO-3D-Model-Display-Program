
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import numpy as np
from numpy.random import exponential #for exponential distribution (distribution of distance between events in Poisson process)


# LED setup: wall/floor for outer detector, RGB for colours in TPC

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

GPIO.PWM(redGPIO,1000).start(0)
GPIO.PWM(greenGPIO,1000).start(0)
GPIO.PWM(blueGPIO,1000).start(0)



def flash(events): #run this every time an LED flashes. 
    
    flashtime = 0.5 #s that LEDs should flash

    #turn LEDs on
    for event in events:
        if event == "ROI_background": #R204; G121; B167. #CC79A7
            GPIO.PWM(redGPIO,1000).ChangeDutyCycle(204/255 * 100)
            GPIO.PWM(greenGPIO,1000).ChangeDutyCycle(121/255 * 100)
            GPIO.PWM(blueGPIO,1000).ChangeDutyCycle(167/255 * 100)
            print("ROI_background on")
        if event == "0vbb": #R000; G158; B115. #009E73
            GPIO.PWM(redGPIO,1000).ChangeDutyCycle(0)
            GPIO.PWM(greenGPIO,1000).ChangeDutyCycle(158/255 * 100)
            GPIO.PWM(blueGPIO,1000).ChangeDutyCycle(115/255 * 100)
            print("0vbb on")
        if event == "2vbb": #R213; G094; B000. #D55E00
            GPIO.PWM(redGPIO,1000).ChangeDutyCycle(213/255 * 100)
            GPIO.PWM(greenGPIO,1000).ChangeDutyCycle(94/255 * 100)
            GPIO.PWM(blueGPIO,1000).ChangeDutyCycle(0)  
            print("2vbb on")
        if event == "Xe137": #R230; G159; B000. #E69F00
            GPIO.PWM(redGPIO,1000).ChangeDutyCycle(230/255 * 100)
            GPIO.PWM(greenGPIO,1000).ChangeDutyCycle(159/255 * 100)
            GPIO.PWM(blueGPIO,1000).ChangeDutyCycle(0)   
            print("Xe137 on")
        if event == "solar v": #R240; G228; B066. #F0E442
            GPIO.PWM(redGPIO,1000).ChangeDutyCycle(240/255 * 100)
            GPIO.PWM(greenGPIO,1000).ChangeDutyCycle(228/255 * 100)
            GPIO.PWM(blueGPIO,1000).ChangeDutyCycle(66/255 * 100)  
            print("solar v on")
        if event == "TPC_muon": # turn on bottom of outer detector
            GPIO.output(floorGPIO, GPIO.HIGH)
            print("TPC_muon on")
        if event == "cryostat_muon": # turn on whole outer detector
            GPIO.output(floorGPIO, GPIO.HIGH)
            GPIO.output(wallGPIO, GPIO.HIGH)
            print("cryostat muon on")
    
    time.sleep(flashtime)

    #turn LEDs off
    GPIO.PWM(redGPIO,1000).ChangeDutyCycle(0)
    GPIO.PWM(greenGPIO,1000).ChangeDutyCycle(0)
    GPIO.PWM(blueGPIO,1000).ChangeDutyCycle(0)
    GPIO.output(floorGPIO, GPIO.LOW)
    GPIO.output(wallGPIO, GPIO.LOW)

def event_rates(half_life:int=0, inner_vol:int=0): #change 0vbb half-life, inner volume to consider
    rates_per_year = np.zeros(7) #array to store events/year for each type
    #event_types = ["0vbb", "2vbb", "Xe 137", "solar v", "ROI background", "TPC muon", "cryostat muon"]


    # 0vbb: 
    #ROI: energy range of 0vbb FWHM, inner 2t of xenon
    #FWHM is approx. 76.1% of area under Gaussian

    Xe_mass = 0.1*133.9053945 + 0.9*135.407219 #in g/mol; for 90% Xe 136, 10% Xe 134
    if inner_vol == 1: #1 ton inner volume
        n_xenon = 10**6 / Xe_mass * 6.022*10**23
    else: #default inner volume is 2 tons
        n_xenon = 2 * 10**6 / Xe_mass * 6.022*10**23 #2 tons * 10^6 g/tons
    
    if half_life == 1: #shorter half-life
        half_life = 1 * 10**27 #years
    elif half_life == 2: #half-life sensitivity
        half_life = 1.35 * 10**28
    else: #deault to 3 sigma discovery potential half-life
        half_life = 7.4 * 10**27 
    
    mean_lifetime = half_life/np.log(2)  #years
    mean_decays = n_xenon/mean_lifetime # particles/year
    mean_decays_ROI = mean_decays * 0.761 #events in ROI
    rates_per_year[0] = mean_decays_ROI


    # background
    if inner_vol == 1: #inner 1t
        total_bgd = 1.4 * 10**-4 #events/(FHWM kg yr)
    else: #default to inner 2t
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
    return mean_times


def main_loop(runtime, mean_times):
    count_0vbb = 0
    count_2vbb = 0
    count_Xe137 = 0
    count_solar_v = 0
    count_ROI_background = 0
    count_TPC_muon = 0
    count_cryostat_muon = 0

    # mean times between events (in seconds)
    mean_0vbb, mean_2vbb, mean_Xe137, mean_solar_v, mean_ROI_background, mean_TPC_muon, mean_cryostat_muon = mean_times

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
                count_0vbb+=1
            if time_now - timer_2vbb > time_2vbb:
                events_triggered.append("2vbb")
                time_2vbb = exponential(mean_2vbb)
                timer_2vbb = time.time()
                count_2vbb+=1
            if time_now - timer_Xe137 > time_Xe137:
                events_triggered.append("Xe137")
                time_Xe137 = exponential(mean_Xe137)
                timer_Xe137 = time.time()
                count_Xe137+=1
            if time_now - timer_solar_v > time_solar_v:
                events_triggered.append("solar v")
                time_solar_v = exponential(mean_solar_v)
                timer_solar_v = time.time()
                count_solar_v+=1
            if time_now - timer_ROI_background > time_ROI_background:
                events_triggered.append("ROI_background")
                time_ROI_background = exponential(mean_ROI_background)
                timer_ROI_background = time.time()
                count_ROI_background+=1
            if time_now - timer_TPC_muon > time_TPC_muon:
                events_triggered.append("TPC_muon")
                time_TPC_muon = exponential(mean_TPC_muon)
                timer_TPC_muon = time.time()
                count_TPC_muon+=1
            if time_now - timer_cryostat_muon > time_cryostat_muon:
                events_triggered.append("cryostat_muon")
                time_cryostat_muon = exponential(mean_cryostat_muon)
                timer_cryostat_muon = time.time()
                count_cryostat_muon+=1
        
        
            #flash all triggered LEDs (if any are triggered)
            if events_triggered != []:
                flash(events_triggered)
                events_triggered = [] #reset triggered events list

            # temporary way to break loop
            if time_now - start_time > runtime:
                print(count_0vbb, count_2vbb, count_Xe137, count_solar_v, count_ROI_background, count_TPC_muon, count_cryostat_muon)
                break

        except KeyboardInterrupt:
            GPIO.cleanup()
            break


mean_times = event_rates()
main_loop(120, mean_times)