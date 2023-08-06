<!-- ABOUT THE PROJECT -->

## About The Project

This project provides functions in Python for estimating the MAWP for pressure vessels. The intention is to use the routines in a Jupyter Notebook file for documenting engineering work.  

The calculations should be adequate for engineering consulting work and preliminary sizing or rating. Be careful that you use the correct values for maximum stress.


### Built With

The code is written in Python. The code is intended to be used in a Jupyter Notebook. I have not used the routines in a stand-alone Python environment.


<!-- GETTING STARTED -->
## Getting Started

The following lines of code are needed in a Jupyter Notebook (Python shell) to pull the _unregistered_ package from GitHub and use the package.

~~~~
TBD
~~~~

### Prerequisites

The package requires the following packages

* numpy
* math
* scipy
* pandas

<!-- TESTING -->
### Testing

The following code tests are available

* not sure if I have a test


<!-- USAGE EXAMPLES -->
## Usage

Refer to the Jupyter Notebook file for an example of how the code is used.

_For more examples, please refer to the [Documentation](https://example.com)_

Units of measure used in the package are:

* Diametr and wall thickness, mm
* Stress, kPa
* Pressure, kPaa
* Temperature, deg C

Functions

* PSVsteamRate(areaMM2, Pkpa, State)
    * areaMM2 is the API flow area in mm2
    * State is either a temperature in deg C (superheated steam) or a string ("Sat", saturated steam).
    * return value is kg/h
* PSVsteamSize(Wkg, Pkpa, State)
    * Wkg is mass flow rate in kg/h
    * State is either a temperature in deg C (superheated steam) or a string ("Sat", saturated steam).
    * return value is orifice area mm2
* PSVsteamFlux(Pkpa, State)
    * this is the main function for steam PSV calculations
    * the return value is mass flux in kg/hr.mm2
    * this is used to calculate either the area (given the flow rate) or the flow rate (given the area)

    $$
    K_d = 0.975 \\
	K_{sh} = \mbox{Superheat derating (lookup table)} \\
    K_b = 1.0 \, \mbox{(no backpressure derating)} \\
    K_n = \frac{2.7644 \times Pkpa/100.0 - 1000.0}{3.3242 \times Pkpa/100.0 - 1061.0}, P > 10300 \mbox{kPa} \\
    Ppsi = Pkpa \times (14.503773800721813/100) \\
    flux_{kg/hr.mm^2} = 51.45 \times K_d \times Ppsi \times K_{sh} \times K_b \times K_n / (2.205 \times 25.4^2)
    $$ 
  
Refer to the Jupyter notebook file PSVreliefExample.ipynb for working examples.

<!-- ROADMAP -->
## Roadmap

* implement more complete values for maximum stress



<!-- CONTRIBUTING -->
## Contributing

Send me a note.



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Kevin Dorma - [@kevindorma](https://twitter.com/KevinDorma) - kevin@kevindorma.ca

Project Link: [https://github.com/kevindorma/pyMAWP](https://github.com/kevindorma/pyMAWP)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

Not sure who to acknowledge.