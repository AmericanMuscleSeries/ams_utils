import dotenv
import os

dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
LOGO = os.getenv('LOGO_URL')
LOG_DIR = os.getenv('LOG_DIR', './')
ADMIN_CH = os.getenv('ADMIN_CH', 'admin')
BROADCAST_ROLE = os.getenv('BROADCAST_ROLE_ID')
ENTRY_FEE = os.getenv('ENTRY_FEE')
REG_OPEN = os.getenv('REG_OPEN', '0').lower() in ('true', '1')
REG_OPEN_FOR = os.getenv('REG_OPEN_FOR', 'return')
ROSTER_MSG_ID = os.getenv('ROSTER_MSG_ID', '0')
INFO_CH = os.getenv('INFO_CH', 'links-and-info')
INCLUDE_DROPS = os.getenv('INCLUDE_DROPS', '0').lower() in ('true', '1')
POINTS_FILE = os.getenv('POINTS_FILE')
