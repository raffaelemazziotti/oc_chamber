# Operant Conditioning Chamber

Operant conditioning is a classical paradigm used in experimental psychology in which animals learn to perform an action in order to achieve a reward. By using this paradigm, it is possible to extract learning curves and measure accurately reaction times.
Here we describe a fully 3D printable device that is able to perform operant conditioning on  freely moving mice, while performing real-time tracking of the animal position.

## Assembling & Installation

You can find 3D printed models [here](https://www.thingiverse.com/thing:3975752).  
In [figures/EXPLODED VIEW.jpg](https://github.com/raffapaz/oc_chamber/blob/master/figures/EXPLODED%20VIEW.jpg) there is an intuitive diagram of the assembling scheme.

A list of all the components can be found here: [Bill of materials](https://docs.google.com/spreadsheets/d/19AH2Pe1oMEcGUEE4mrs1yGA2-vNfwtRM7asQJUQdpgM/edit?usp=sharing)

Then you need:

* a 1000 µF capacitor
* two 25 Mohm resistors for the touch buttons
* a 220 ohm resistor for the LED matrix
* a piece of M8 thread (~15 cm)

Connect all the components as described in [figures/diagram_scheme.png](https://github.com/raffapaz/oc_chamber/blob/master/figures/diagram_scheme.png)

To install the software in the Raspberry Pi just download or copy the entire code in a folder of the raspian OS.  

Required libraries:

* [picamera](https://picamera.readthedocs.io/en/release-1.13/)
* [pySerial](https://pythonhosted.org/pyserial/)
* [openCV](https://pypi.org/project/opencv-python/)
* [Tkinter](https://tkdocs.com/tutorial/install.html)

Compile and load on the Arduino UNO the sketch called [skinner.ino](https://github.com/raffapaz/oc_chamber/tree/master/arduino_files/skinner)

To run the code type in terminal:

```python3
python3 cvConditioningTracking.py
```

## Keyboard Shortcuts

* **p**: exit
* **s**: stop trial

## Dataset & Data Analysis

[Dataset]() folder contains our raw data described in this [paper](#references) and composed of 6 subjects. Each subject is containet in its own folder and coded using the scheme: CAGE-LABEL-GENO. Furthermore, there are two Jupyter Notebooks with an example on how you can read txt output files in python as [pandas](https://pandas.pydata.org/) datasets.

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
    * event - type of event (both,simple)

## Authors

* **Raffaele Mazziotti**  - [raffapaz](https://github.com/raffapaz)
* **Giulia Sagona**  
* **Leonardo Lupori** - [leonardolupori](https://github.com/leonardolupori)
* **Virginia Martini**
* **Tommaso Pizzorusso**  

## References

Detailed description of the apparatus can be found here:
[Fully 3D printable device for automated operant conditioning in the mouse](https://docs.google.com/document/d/1ROyHVp2HN-OSPP7uKdv-rDPUn_NWunvdGDlKdQuhvm4/edit?usp=sharing)

## Contacts

For any info don't hesitate to contact us at raffaele.mazziotti@in.cnr.it
