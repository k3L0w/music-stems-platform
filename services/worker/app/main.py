import logging

from app.core.settings import get_settings
from app.metrics import collect_startup_metrics

settings = get_settings()

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(settings.worker_name)


def main() -> None:
    metrics = collect_startup_metrics(settings.worker_name)
    logger.info(
        "Worker scaffold carregado",
        extra={
            "worker_name": settings.worker_name,
            "environment": settings.environment,
            "metrics": metrics,
        },
    )


if __name__ == "__main__":
    main()
