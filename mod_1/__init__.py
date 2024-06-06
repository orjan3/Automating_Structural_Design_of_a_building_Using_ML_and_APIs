import sys
from pathlib import Path

# Añade el directorio raíz del proyecto a la ruta de búsqueda
sys.path.append(str(Path(__file__).resolve().parents[1]))
# Aquí, para importar modelos de otras carpetas, necesito agregar los directorios
# de estas carpetas a sys.path. Así, podré usarlas sin dificultad y estas carpetas
# podrán estar en otras carpetas lejos, incluso dentro de C: 

from mod_1 import config  # noqa: F401