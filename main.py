import os

from src.helpers import methods as m

if __name__ == "__main__":

    location = "W:/4. PREPARAR RESUMEN"

    if os.path.exists(location):
        m.explore_directories(location)
