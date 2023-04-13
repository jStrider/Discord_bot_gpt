from bot import jrw_bot
import logging

logging.warning("make sure the environment variables are set.  See README.md for more info.")
logging.info("initializing jrw bot")
logging.info("loading config")
jrw_bot_instance = jrw_bot()
jrw_bot_instance.load_config()
logging.info("config loaded")
logging.info("initializing bot")
jrw_bot_instance.init_bot()
