import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(__file__).parents[1]))

def show_matrixes(cur_comp):
    return cur_comp.show_matrixes()