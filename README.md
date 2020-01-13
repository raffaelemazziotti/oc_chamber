# Operant Conditioning Chamber

Operant conditioning is a classical paradigm used in experimental psychology in which animals learn to perform an action in order to achieve a reward. By using this paradigm, it is possible to extract learning curves and measure accurately reaction times.
Here we describe a fully 3D printable device that is able to perform operant conditioning on  freely moving mice, while performing real-time tracking of the animal position.

## Assembling & Installation

You can find 3D printed models [here](https://github.com/raffaelemazziotti/oc_chamber/tree/master/3D_models) or [here](https://www.thingiverse.com/thing:3975752).  
In [figures/EXPLODED VIEW.jpg](https://github.com/raffaelemazziotti/oc_chamber/blob/master/figures/EXPLODED%20VIEW.jpg) there is an intuitive diagram of the assembling scheme.
We printed all the components using Cura 4.0 with a medium resolution (100 µm), a speed of 90 mm/s and an infill of 20%. The design of the OC chamber is quite simple so almost all the printers are sufficiently precise to successfully print the entire chamber.

A list of all the components can be found here: [Bill of materials](https://docs.google.com/spreadsheets/d/19AH2Pe1oMEcGUEE4mrs1yGA2-vNfwtRM7asQJUQdpgM/edit?usp=sharing)

In addition you need:

* a 1000 µF capacitor
* two 25 Mohm resistors for the touch buttons
* a 220 ohm resistor for the LED matrix
* a piece of M8 thread (~15 cm) for reward delivery

Connect all the components as described in [figures/diagram_scheme.png](https://github.com/raffapaz/oc_chamber/blob/master/figures/diagram_scheme.png)

To install the software in the Raspberry Pi(RPI) just download or copy the entire code in a folder of the Raspian OS.  

### Required libraries

Python

* [picamera](https://picamera.readthedocs.io/en/release-1.13/)
* [pySerial](https://pythonhosted.org/pyserial/)
* [openCV](https://pypi.org/project/opencv-python/)
* [Tkinter](https://tkdocs.com/tutorial/install.html)

Arduino

* [CapacitiveSensor](https://playground.arduino.cc/Main/CapacitiveSensor/)
* [Adafruit_NeoPixel](https://learn.adafruit.com/adafruit-neopixel-uberguide/arduino-library-use)
* [Stepper](https://www.arduino.cc/en/reference/stepper)

### Arduino Configuration

Compile and load on the [Arduino UNO](https://store.arduino.cc/arduino-uno-rev3) the sketch called [skinner.ino](https://github.com/raffaelemazziotti/oc_chamber/tree/master/arduino_files/skinner)

### Capacitive Sensors calibration

To calibrate [capacitive sensors](https://en.wikipedia.org/wiki/Capacitive_sensing) thresholds load the Arduino sketch called [skinnerCapacitiveTest](https://github.com/raffaelemazziotti/oc_chamber/tree/master/arduino_files/skinnerCapacitiveTest). This function just prints on the serial port capacitive sensor values. It is helpful to set the proper threshold value to detect mouse touches.

### Running Python code

To run the code type in terminal:

```python3
cd path\of\oc_chamber\folder\
python3 cvConditioningTracking.py
```

Alternatively open cvConditioningTracking.py in IDLE [IDLE](https://en.wikipedia.org/wiki/IDLE) IDE and push F5.

## LCD oc_chamber

To allow the use of more complex visual stimuli you can find a backbone version of the code that works with an [LCD display](http://kookye.com/2016/08/01/kookye-3-5-touch-screen-for-raspberry-pi-display-monitor-480x320-lcd-touchscreen-kit-3-5lcd-pi-2-board-case/). To run the code [Psychopy2](https://www.psychopy.org/) is required. To install psychopy on RPI follow [these](https://www.psychopy.org/download.html) instructions. Once Psychopy is installed open cvConditioningTracking.py in the Psychopy IDE and run the code. This code contains a module called LCD.py that can be used to show selected images. For now, the code is a stub, an untested version and runs for demonstrative purposes.

## Keyboard Shortcuts

* **p**: exit from program
* **s**: stop a trial

## Dataset & Data Analysis

[Dataset](https://github.com/raffaelemazziotti/oc_chamber/tree/master/dataset) folder contains our raw data, described in this [paper](#references), with 6 subjects. Each subject is contained in its own folder and coded using the scheme: CAGE-LABEL-GENO. Furthermore, there are two Jupyter Notebooks with an example on how you can read txt output files in Python as [pandas](https://pandas.pydata.org/) dataframes.

* **data:** contains folders representing subjects. In the folder there are .txt files with fields
  * Event - the type of event (both,single)
  * Answer - the answer provided by the subject (both_sx,both_dx,yes,no)
  * RT - Reaction time
  * Time - Timestamp
* **data_track:** contains the real time tracking of the animal position. The first row represents the borders of the arena (rect x y width height).
The rest of the lines contain
  * timestamp - timmestamp
  * x - x coordinate
  * y - y coordinate
  * event - type of event (both,left,right)

## Authors

* [**Raffaele Mazziotti**](https://github.com/raffaelemazziotti)
* **Giulia Sagona**  
* [**Leonardo Lupori**](https://github.com/leonardolupori)
* **Virginia Martini**
* [**Tommaso Pizzorusso**](https://www.researchgate.net/profile/Tommaso_Pizzorusso)

## References

Detailed description of the apparatus can be found here:
[3D printable device for automated operant conditioning in the mouse](https://docs.google.com/document/d/1ROyHVp2HN-OSPP7uKdv-rDPUn_NWunvdGDlKdQuhvm4/edit?usp=sharing)

## Contacts

For any info don't hesitate to contact us at raffaele.mazziotti@in.cnr.it
