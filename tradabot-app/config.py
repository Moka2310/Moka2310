# TRADABOT Configuration
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
CONFIG_FILE = DATA_DIR / "config.encrypted"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://auto-trader-70.preview.emergentagent.com')
API_TRADABOT_ACCESS = f"{API_BASE_URL}/api/tradabot/access"
API_TRADABOT_CONFIG = f"{API_BASE_URL}/api/tradabot/config"
API_TRADABOT_STATUS = f"{API_BASE_URL}/api/tradabot/status"

# Telegram Channels (from backend .env)
TELEGRAM_CHANNELS = {
    'forex': -1002425540174,
    'crypto': -1002279973041,
    'gold': -1002355600472,
    'indices': -1002339785500,
    'actions': -1002376632406,
    'commodites': -1002368060694
}

# Trading Configuration
DEFAULT_LOT_SIZE = 0.01
MAX_SLIPPAGE = 3  # pips
MAGIC_NUMBER = 12345  # Unique identifier for bot trades

# Update intervals
ACCESS_CHECK_INTERVAL = 3600  # 1 hour
CONFIG_SYNC_INTERVAL = 300  # 5 minutes
POSITION_CHECK_INTERVAL = 1  # 1 second

# App Info
APP_NAME = "TRADABOT"
APP_VERSION = "1.0.0"
