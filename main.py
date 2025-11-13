import os

from src.helpers import methods as m

if __name__ == "__main__":
    location1 = "Z:/8. Base Datos Unica"

    location2 = "Z:/4. PREPARAR RESUMEN"

    if os.path.exists(location1):
        m.explore_directories(location1)

    if os.path.exists(location2):
        m.explore_directories(location2)
