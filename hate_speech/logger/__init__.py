import logging
import os
import from_root
from datetime import datetime

logs_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S_')}.log"
logs_path = os.path.join(os.getcwd(), "logs", logs_file)

os.makedirs(logs_path, exist_ok=True)

logs_file_path = os.path.join(logs_path, logs_file)

logging.basicConfig(
    filename = logs_file_path,
    format = "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level = logging.DEBUG)