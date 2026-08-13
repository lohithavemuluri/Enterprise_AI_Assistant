import logging

# LOG FILE


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# LOG FUNCTIONS

def log_info(message):
    logging.info(message)


def log_error(message):
    logging.error(message)