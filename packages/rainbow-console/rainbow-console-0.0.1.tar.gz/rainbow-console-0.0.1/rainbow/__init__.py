"""
This module is designed to color the information displayed in the console.

import rainbow

rainbow.print("#F07427example #F4CA16print")
rainbow.print("example print", color="#CC397B")
print(rainbow.paint("Hello, world!", color="#318CE7"))

Colored line example: "#318CE7Hello #FECF3DWorld#309831!#r default colored text"
Use #xxxxx to set color
Use #r to reset color to console default
Flag #r automatically appends to end of string
"""

from .rainbow_console import paint, rainbow_print
from .rainbow_console import rainbow_print as print