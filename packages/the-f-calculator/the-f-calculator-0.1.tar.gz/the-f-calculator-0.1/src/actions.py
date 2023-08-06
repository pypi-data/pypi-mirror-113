from typing import List

#create a calculator class
class Calculator():
    """
    Simple (but sophisticated) calculator class that can:
    Addition / Subtraction
    Multiplication / Division
    Take (n) root of number

    All results are stored in memory and can be used for additional computations
    Able to reset memory to 0 for a fresh start
    """

    def __init__(self, mem_value: float=0.0):
        """create and set memory default to 0.0"""
        self.__memory = mem_value


    def add(self, l: List[float]) -> float:
        """
        Add any number of numerals (decimals or whole numbers) with themselves and to figure in memory\n
        Memory default is 0.0 \n
        Call clear_mem() function to reset memory back to zero
        """

        if not l:
            return self.__memory
        else:
            for item in l:
                try:
                    float(item)
                except TypeError:
                    pass
                else:
                    for x in l:
                        self.__memory += x
                return self.__memory


    def subtract(self, l: List[float]) -> float:
        """
        Subtract any number of numerals from themselves and from figure in memory (if memory not default\n
        Memory default is 0.0 \n
        Call clear_mem() function to reset memory back to zero
        """

        if not l:
            return self.__memory
        else:
            for item in l:
                try:
                    float(item)
                except TypeError:
                    pass
                else:
                    if not self.__memory:
                        if len(l) == 1:
                            self.__memory = self.__memory - l[0]
                        elif len(l) == 2:
                            self.__memory = l[0] - l[1]
                        else:
                            for i in range(len(l)):
                                if i == 0:
                                    self.__memory = l[0]
                                else:
                                    self.__memory -=l[i]
                            
                    else:
                        if len(l) == 1:
                            self.__memory -= l[0]
                        elif len(l) > 1:
                            for x in l:
                                self.__memory -= x
                    return self.__memory


    def multiply(self, l: List[float]) -> float:
        """
        Multiply any number of numerals with themselves and with figure in memory\n
        Memory default is 0.0 \n
        Call clear_mem() function to reset memory back to zero
        """

        if not l:
            return self.__memory
        elif not self.__memory:
            for item in l:
                try:
                    float(item)
                except TypeError:
                    pass
                else:
                    if len(l) == 1:
                        self.__memory *= l[0]
                    elif len(l) > 1 or self.__memory:
                        product = self.__memory + 1
                        for x in l:
                            product *= x
                            self.__memory = product
                return self.__memory
        else:
            for item in l:
                try:
                    float(item)
                except TypeError:
                    pass
                else:
                    product = self.__memory
                    for x in l:
                        product *= x
                        self.__memory = product
                return self.__memory

        
    def divide(self, a: float = 0.0, b: float = 0.0) -> float:
        """Divides first argument by the second, 
        or the number in memory by first argument if only first argument is provided\n
        Key arguments are optional with defaults set to 0.0\n
        Function divides number in memory by argument if only one arguument is provided when called\n
        Function cannot divide by 0 and returns figuure in memory if second argument is 0\n
        If no arguument is provided, function returns number in memory\n
        Memory default is 0.0 \n
        Call clear_mem() function to reset memory back to zero
        Enter numbers > 0 for a and b if you would like to perform division on a new set of numerals
        """
       
        if a and not b: 
            try:
                float(a)
            except TypeError:
                pass
            else:
                self.__memory = self.__memory/a
        elif a and b:
            try:
                float(a)
                float(b)
            except TypeError:
                pass
            else:
                self.__memory = a/b
        else:
            pass
        return self.__memory


    def root(self, n: float = 0.0, nth: int = 0) -> float:
        """Computes the nth root of any number,\n
        Key arguments are optional:\n
        First argument n is the number. Default is 0.0\n
        Second argument nth is the nth root to be taken. Default is 0\n
        Function returns (first argument)th root of number in memory if only one argument is provided when called,
        or if second argument provided is 0\n
        Providing two arguments overrides number in memory (second argument)th root of first argument\n
        Function cannot take the 0th root of any number and returns the value in memory instead\n
        Memory default is 0.0 \n
        Call clear_mem() function to reset memory back to zero
        If no arguument is provided, function returns number in memory\n
        """

        if n and not nth:
            try:
                n = int(n) 
            except TypeError:
                pass
            else:
                if self.__memory < 0:
                    print("cannot take the nth root of a negative number")
                    raise ValueError
                else:
                    self.__memory = self.__memory**(1/n)
        elif n and nth:
            try: 
                n = float(n)
                nth = int(nth)
            except TypeError:
                pass
            else:
                if n < 0:
                    print("cannot take the nth root of a negative number")
                    raise ValueError
                else:
                    self.__memory = n**(1/nth)
        else:
            pass
        return self.__memory
        

    def clear_mem(self):
        """resets memory value back to zero"""

        self.__memory = 0.0
        
      
