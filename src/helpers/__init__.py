import sys
from loguru import logger

logger.remove(0)
logger.add(
    "data/app.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} {module}:{line} | {message}",
)
logger.add(
    sys.stderr,
    level="DEBUG",
    format="<blue>{module}:{line}</blue> | <green>{message}</green>",
)


logger.info("logger has been initialized")
