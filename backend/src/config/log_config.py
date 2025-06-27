import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s\n-----------'
)
logger = logging.getLogger(__name__)

