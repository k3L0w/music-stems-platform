import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Worker scaffold carregado. Nenhuma tarefa de negocio foi configurada ainda.")


if __name__ == "__main__":
    main()
