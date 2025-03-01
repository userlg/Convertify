from src.helpers import methods as m

import psutil

import os

if __name__ == "__main__":

    location = "W:/4. PREPARAR RESUMEN"

    if os.path.exists(location):
       m.explore_directories(location)
    else:
      m.explore_directories(os.getcwd())
