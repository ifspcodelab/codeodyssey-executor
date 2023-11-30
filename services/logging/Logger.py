import logging


class Logger:
    def __init__(self) -> None:
        self.__logger = self.get_logger()

    
    def get_logger():
        logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)



        logger = logging.getLogger('')
        logger.addHandler(console_handler)

        return logger
    
    def get_logger_without_handler():
        logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

        return logging.getLogger('')