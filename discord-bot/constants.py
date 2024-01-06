import dotenv
import os


dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
LOGO = os.getenv('LOGO_URL')
LOG_DIR = os.getenv('LOG_DIR', './')
ADMIN_CH = os.getenv('ADMIN_CH', 'admin')
BROADCAST_ROLE = os.getenv('BROADCAST_ROLE_ID')
ENTRY_FEE=os.getenv('ENTRY_FEE')
