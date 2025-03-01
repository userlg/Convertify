from src.helpers import methods as m

import psutil

import os

if __name__ == "__main__":

    location = "W:/4. PREPARAR RESUMEN"

    m.explore_directories(location)

    # This opcion is only for tests
    # m.explore_directories(os.getcwd())
