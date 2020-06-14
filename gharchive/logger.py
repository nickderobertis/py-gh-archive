import logging
import sys

logger = logging.getLogger('gharchive')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(name)s - %(filename)s L%(lineno)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)