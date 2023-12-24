import dotenv
import os


dotenv.load_dotenv()
_DNE = ' does not exist as envvar'
TOKEN = os.getenv('TOKEN', 'TOKEN' + _DNE)
GUILD = os.getenv('GUILD', 'GUILD' + _DNE)
LOGO = os.getenv('LOGO_URL', 'LOGO_URL' + _DNE)
LOG_DIR = os.getenv('LOG_DIR', './')