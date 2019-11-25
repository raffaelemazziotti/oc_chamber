# Operant Conditioning Chamber
Operant conditioning is a classical paradigm used in experimental psychology in which animals learn to perform an action in order to achieve a reward. By using this paradigm, it is possible to extract learning curves and measure accurately reaction times.
Here we describe a fully 3D printable device that is able to perform operant conditioning on  freely moving mice, while performing real-time tracking of the animal position.

## Assembling & Installation

You can find 3D printed models [here](https://www.thingiverse.com/thing:3975752)
In figures/EXPLODED VIEW.jpg there is an intuiteve diagram of the assembling scheme.

A list of all the components can be found here: [Bill of materials](https://docs.google.com/spreadsheets/d/19AH2Pe1oMEcGUEE4mrs1yGA2-vNfwtRM7asQJUQdpgM/edit?usp=sharing) 

Then you need:
* a 1000 µF capacitor
* two 25 Mohm resistors for the touch buttons
* a 220 ohm resistor for the LED matrix
* a piece of M8 thread (~15 cm) 

Connect all the components as described in figures/diagram_scheme.png

To install the software Raspberry Pi just download or copy the entire code in a folder of the raspian OS.

run the command:

```
python3 cvConditioningTracking.py
```



## Authors

* **Raffaele Mazziotti**  [raffapaz](https://github.com/raffapaz) 
* **Giulia Sagona**  
* **Leonardo Lupori**
* **Virginia Martini**
* **Tommaso Pizzorusso**  

## References

Detailed instructions for the construction of the apparatus can be found here:
[Fully 3D printable device for automated operant conditioning in the mouse](https://docs.google.com/document/d/1ROyHVp2HN-OSPP7uKdv-rDPUn_NWunvdGDlKdQuhvm4/edit?usp=sharing)


