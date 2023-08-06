class Calculator:
    """
    A class to represent a calculator.

    ...

    Attributes
    ----------
    memory_value : float
        value in calculator memory

    Methods
    -------
    add(self, input_value):
        Adds input value to memory value.

    subtract(self, input_value):
        Subtracts input value from memory value.

    divide(self, input_value):
        Divides input value by memory value.

    multiply(self, input_value):
        Multiplies input value by memory value.

    root(self, input_value):
        Returns the input value root of the memory value.

    reset(self):
        Resets memory value to zero.
        """

    def __init__(self, memory_value: float = 0):
        self._memory_value = memory_value
        """
        Constructs the necessary attributes for the calculator object.

        Parameters
        ----------
        memory_value : float
            value of the memory
        """

    def add(self, input_value: float) -> float:
        """Takes in a value and add it to the value in memory, returns the addition."""
        try:
            self._memory_value += input_value
        except Exception as e:
            return "Please input a valid number"
        return self._memory_value

    def subtract(self, input_value: float) -> float:
        """Takes in a value and subtract it from the value in memory, returns the subtraction."""
        try:
            self._memory_value -= input_value
        except Exception as e:
            return "Please input a valid number"
        return self._memory_value

    def multiply(self, input_value: float) -> float:
        """Takes in a value and multiply it with the value in memory, returns the multiplication."""
        try:
            int(input_value)
            self._memory_value *= input_value
        except Exception as e:
            return "Please input a valid number"
        return self._memory_value

    def divide(self, input_value: float) -> float:
        """Takes in a value and divide it by the value in memory, returns the division."""
        try:
            self._memory_value /= input_value
        except Exception as e:
            return "Please input a valid number! Note that division by zero is invalid"
        return self._memory_value

    def root(self, input_value: float) -> float:
        """Takes in a value n, return the nth root of the value in memory."""
        try:
            self._memory_value = self._memory_value ** (1.0 / input_value)
        except Exception as e:
            return "Please input a valid number!"
        return self._memory_value


    def reset(self):
        """Resets the value in memory to zero."""
        self._memory_value = 0
        return self._memory_value
