import logging


class Logger:
    def __init__(self, name, level=logging.DEBUG, file='az_optpy.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        fh = logging.FileHandler(file)
        fh.setLevel(level)
       
        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)


if __name__ == "__main__":
    log = Logger('myapp')
    log.debug("Esta é uma mensagem em debug.")
    log.info("Esta é uma mensagem de Informação.")
    log.warning("Esta é uma mensagem de Alerta.")
    log.error("Esta é uma mensagem de Erro.")
