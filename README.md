# Operant Conditioning Chamber

Operant conditioning is a classical paradigm used in experimental psychology in which animals learn to perform an action in order to achieve a reward. By using this paradigm, it is possible to extract learning curves and measure accurately reaction times.
Here we describe a fully 3D printable device that is able to perform operant conditioning on  freely moving mice, while performing real-time tracking of the animal position.

## Assembling & Installation

You can find 3D printed models [here](https://github.com/raffaelemazziotti/oc_chamber/tree/master/3D_models) or [here](https://www.thingiverse.com/thing:3975752).  
In [figures/EXPLODED VIEW.jpg](https://github.com/raffaelemazziotti/oc_chamber/blob/master/figures/EXPLODED%20VIEW.jpg) there is an intuitive diagram of the assembling scheme.
We printed all the components using Cura 4.0 with a medium resolution (100 µm), a speed of 90 mm/s and an infill of 20%. The design of the OC chamber is quite simple so almost all the printers are sufficiently precise to successfully print the entire chamber.

A list of all the components can be found here: [Bill of materials](https://docs.google.com/spreadsheets/d/19AH2Pe1oMEcGUEE4mrs1yGA2-vNfwtRM7asQJUQdpgM/edit?usp=sharing)

### 3D printed parts

* **OC CHAMBER**
  * **arena:** main arena
  * **arena_holes:** main arena with holes on the floor
  * **barrier_posterior:** posterior barrier for jumpig mice
  * **frontal_wall_LED:** interface wall for LED matrix
  * **frontal_wall_LCD:** interface wall for LCD screen
  * **mask_dots:** mask for LED matrix
  * **touch_sensor:** button
* **CAMERA**
  * **cam_barrier:** camera holder with frontal barrrier for jumping mice
  * **cam_ladder:** 3d printed arm
  * **cam_holder:** camera holder
  
* **DELIVERY**
  * **delivery_base:** syringe and motor holders
  * **delivery_motor2thread:** thread to motor adapter
  * **delivery_piston:** syringe piston

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

```bash
cd \home\pi\oc_chamber\         \\ or replace with the folder path containing the scpript
python3 cvConditioningTracking.py
```

Alternatively open cvConditioningTracking in [IDLE](https://en.wikipedia.org/wiki/IDLE) IDE and push F5.

The user can customize some of the low-level parameters of the experiments by editing the value of the variables in the first 25 lines of the file [cvConditioningTracking](https://github.com/raffaelemazziotti/oc_chamber/blob/master/cvConditioningTracking.py).py. A more detailed explanation of those parameters is given in the file itself.

The chamber can run experiments in 2 modes: **Training** mode and **Permutation** mode. The user can select one of the two modes by editing the parameter **task** in the cvConditioningTracking file. The details and differences of the 2 modes can be found in the [paper](#references).

### Experiment info GUI

At the start of the experiments, the user is prompted with a GUI that collects some basic informations about the experiments that is about to run.

![Screenshot of the GUI for selecting some basic experiment informations.](https://github.com/raffaelemazziotti/oc_chamber/blob/master/%20gui_example.png)

* **Subject:** A string containing an identifier for the current mouse. If left empty no file is saved.
* **File Path:** Location to save experiment file. The output consists of two .txt files containing the dataset of the experiment as described in the [dataset](#dataset) section,stored inside DATA and DATAtracker folder. The user can browser for a location on the PC, if the field is left empty the default is the current working directory.
* **REC file name:** A string containing the name to use for saving the video recording. If left empty no file is saved.
* **REC file path:** Location to save the video recording with an overlay containing the mouse position and the active area. The user can browser for a location on the PC, if the field is left empty the default is the current working directory.
* **Conditions:** Experimental conditions. The list of stimuli that will be presented in the experiment. One or more conditions, divided by a comma, can be specified:

  * right: right dot
  * left: left dot
  * both: dots on the right and left simultaneously

  All the conditions specified here will be presented in a random order.

* **Criterion:** Number of frames necessary for the mouse to stay in the active area to activate a trial. 20 frames = 1 sec
* **Level:** Select the vertical position of the line segregating the active area of the chamber from the inactive one. The value is normalized to the chamber height. 0 = bottom of the chamber, 1 = top of the chamber, 0.5(default) = middle of the chamber
* **Calibration:** Number of frames to be used at the beginning of the experiment for camera calibration. Calibrating the camera at the beginning of the experiment is important to better track the mouse over the background.

### Other Settings

Other customization options are available by editing the first lines of the following files:

* **cvConditioningTracking** (to change computer vision parameters and type of procedure between TRAINING or PERMUTATION )
* **skinner** (stimulus permanence, button threshold)
* **skinnerCapacitiveSensor** (change the button to check and the threshold)

## LCD_oc_chamber

To allow the use of more complex visual stimuli you can find a backbone version of the code that works with an [LCD display](http://kookye.com/2016/08/01/kookye-3-5-touch-screen-for-raspberry-pi-display-monitor-480x320-lcd-touchscreen-kit-3-5lcd-pi-2-board-case/). To run the code [Psychopy2](https://www.psychopy.org/) is required. To install Psychopy on RPI follow [these](https://www.psychopy.org/download.html) instructions. Once Psychopy is installed open cvConditioningTracking.py in the Psychopy IDE and run the code. This code contains a module called LCD.py that can be used to show selected images. For now, the code is a stub, an untested version and runs for demonstrative purposes.

## Keyboard Shortcuts

* **p**: exit from program (p keypress skips camera calibration when in the "camera calibration" phase, otherwise it closes the program)
* **s**: stop a trial

## Dataset

[Dataset](https://github.com/raffaelemazziotti/oc_chamber/tree/master/dataset) folder contains our raw data, described in this [paper](#references), with 6 subjects. Each subject is contained in its own folder and coded using the scheme: CAGE-LABEL-GENO. Furthermore, there are two Jupyter Notebooks with an example on how you can read txt output files in Python as [pandas](https://pandas.pydata.org/) dataframes.

* **data:** contains folders representing subjects. In the folder there are .txt files with fields
  * Event - the type of event (both,single)
  * Answer - the answer provided by the subject (both_sx,both_dx,yes,no)
  * RT - Reaction time
  * Time - Timestamp
* **data_track:** contains the real time tracking of the animal position. The first row represents the borders of the arena (rect x, y, x+width, y+height).
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
[3D printable device for automated operant conditioning in the mouse](https://www.eneuro.org/content/early/2020/04/06/ENEURO.0502-19.2020)

## Contacts

For any info and troubleshooting don't hesitate to contact us at

* raffaele.mazziotti@in.cnr.it
* leonardo.lupori@sns.it
* giulia.sagona@in.cnr.it
