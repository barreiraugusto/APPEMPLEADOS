import logging


def registrar_info(func):
    def envoltura(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.info(f"Resultado del método {func.__name__}: {result}")
        return result

    return envoltura
