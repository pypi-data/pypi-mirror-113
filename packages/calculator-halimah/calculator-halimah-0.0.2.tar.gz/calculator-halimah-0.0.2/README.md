# Calculator
This is a lightweight calculator package for performing simple calculation operations such as addition, subtraction, multiplication, division, root, and reset. For each operation, it takes only one input number and combines it with the current value in the calculator memory. The memory value can be reset at any time.


---
## Features

- Addition : Adds input value to memory value
- Subtraction : Subtracts input value from memory value
- Multiplication : Multiplies input value by memory value
- Division : Divides input value by memory value
- Root : Returns the input value root of the memory value
- Reset : Resets memory value to zero


---
## Technology/Tools
- Python : To build the package
- Docker : To containerize the package 
- Pytest : To test the package


---
## Installation
> Run any of the commands below for installation:

- To install the package from PyPI

```shell
$ python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps calculator-halimah
```

- To install from github

```shell
$ pip install git+https://github.com/halimahO/calculator.git
```

- To get image from dockerhub 

```shell
$ FROM haleemah/calculator
```


---
## Contribution
To contribute or extend this package 
- Clone the package using `git clone https://github.com/halimahO/calculator.git`
- Install dependencies using `pip install -r requirements.txt`
- Run the project using `src/calculator/python calculator.py`
- Run the tests using `tests/pytest`
- Add contributions or make changes
- Write tests if required
- Run tests again to ensure the changes doesn't break anything
- Push the changes to a new branch 
- Raise a pull request 


---
## Sample Usage 
 
This calculator always uses the memory value as the start value, remember to reset to start a new calculation. For example: 
> - 2 + 3 -- Will start by running add 2, then add 3
> - 4 - 2 -- Will start by running add 4, then subtract 2
> - 2 * 5 -- Will start by running add 2, then multiply 5
> - 6 * 3 -- Will start by running add 6, then divide 3
> - 3√4 -- Will start by running add 4, then root 3

Usage example for each method is given below

```shell
from calculator.calculator import Calculator
calculator = Calculator()

$ calculator.add(5)

$ calculator.subtract(3)

$ calculator.multiply(3)

$ calculator.divide(3)

$ calculator.root(2)

$ calculator.reset()
```


---
## Testing
To run the tests, cd to 'tests' directory and run

```shell
$ pytest
```


---
## Acknowledgement 

Turing College


---
## License 
This project is licensed under the terms of the MIT license

---
## Author

Halimah Oladosu
