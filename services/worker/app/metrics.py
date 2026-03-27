from collections.abc import Mapping


def collect_startup_metrics(worker_name: str) -> Mapping[str, int | str]:
    return {
        "worker": worker_name,
        "startup_count": 1,
        "jobs_in_progress": 0,
    }
