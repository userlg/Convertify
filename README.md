# Convertify
![Static Badge](https://img.shields.io/badge/Python-F6D346)
![Static Badge](https://img.shields.io/badge/Script-blue)
![Static Badge](https://img.shields.io/badge/Moviepy-green)
-----------------------------------------------
### Un servicio para convertir de forma automatica videos de formato avi a mp4.
----------------------------------------------
# Requirments

+ Python 3.12

+ Pip 

+ Pyinstaller

+ Moviepy 

+ Pytest

+ Windows Operative System
---------------------------------------------
# Usage
```bash
# Install all packages

pip install -r requirements.txt

# Generate the file .exe

pyinstaller --onefile --icon=favicon.ico main.py --collect-all moviepy

# Run the tests
pytest --cov -v

#Generate Report Coverage
pytest --cov --cov-report=html:coverage_re

```
-------------------------------------------
# Screenshots
+ Map Application
![ map ](screenshots/map.png)
+ Running all tests
![ test ](screenshots/test.png)


------------------------------------------
### Created by
## [ userlg ](https://github.com/userlg)
