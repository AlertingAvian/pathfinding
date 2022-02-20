import logging
import logging.config
from dotenv import load_dotenv
from pathlib import Path
from os import environ

from manage_map import map_manager

load_dotenv()
logging.config.fileConfig(Path(environ['LOGGING_CONFIG_PATH']))
logger = logging.getLogger('root')
logger.debug('logger initialized')


def main():
    logger.info('Starting main')
    map = map_manager.create_map(10, 10)
    display_manager = map_manager.MapDisplay(map)
    display_manager.update_display()
    display_manager.move('down')
    display_manager.update_display()
    display_manager.move('right')
    display_manager.update_display()

if __name__ == '__main__':
    main()