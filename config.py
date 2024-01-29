import sys
import os

directorio_actual = os.path.dirname(os.path.abspath(__file__))
directorio_proyecto = os.path.dirname(directorio_actual)
sys.path.append(directorio_proyecto)