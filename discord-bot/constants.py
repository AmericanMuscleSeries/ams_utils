import dotenv
import os


dotenv.load_dotenv()
_DNE = ' does not exist as envvar'
TOKEN = os.getenv('TOKEN', 'TOKEN' + _DNE)
GUILD = os.getenv('GUILD', 'GUILD' + _DNE)
LOGO = os.getenv('LOGO_URL', 'LOGO_URL' + _DNE)
LOG_DIR = os.getenv('LOG_DIR', './')
ADMIN_CH = os.getenv('ADMIN_CH', 'admin')
BROADCAST_ROLE = os.getenv('BROADCAST_ROLE_ID', 'BROADCAST_ROLE_ID' + _DNE)
