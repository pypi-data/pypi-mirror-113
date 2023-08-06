from . import color_print
import sys

def cprint():
    try:
        text=sys.argv[1]
        color_name=sys.argv[2]
    except:
        text="Hello World!"
        color_name="green"
    color_print.Color.output_color.cprint_name(text,color_name)

def colorprint(text,color_name):
    color_print.Color.output_color.cprint_name(text,color_name)

def codecprint(text,color_name):
    color_print.Color.output_color.color_print(text,color_name)

def setcolor(color_name):
    color_print.Color.output_color.setcolor(color_name)