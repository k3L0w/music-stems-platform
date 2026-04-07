from dataclasses import dataclass

from app.domain.enums import PlanCode


@dataclass(frozen=True)
class PlanLimits:
    max_stems_per_job: int
    max_active_jobs: int


PLAN_LIMITS = {
    PlanCode.FREE: PlanLimits(max_stems_per_job=2, max_active_jobs=1),
    PlanCode.SOLO: PlanLimits(max_stems_per_job=4, max_active_jobs=2),
    PlanCode.PRO: PlanLimits(max_stems_per_job=6, max_active_jobs=5),
}


class PlanEligibilityError(Exception):
    pass


def validate_job_creation_for_plan(
    *,
    plan_code: PlanCode,
    requested_stems_count: int,
    active_jobs_count: int,
) -> None:
    limits = PLAN_LIMITS[plan_code]

    if requested_stems_count > limits.max_stems_per_job:
        raise PlanEligibilityError(
            f"Plan limit exceeded: {plan_code.value} allows up to "
            f"{limits.max_stems_per_job} stems per job."
        )

    if active_jobs_count >= limits.max_active_jobs:
        raise PlanEligibilityError(
            f"Plan limit exceeded: {plan_code.value} allows up to "
            f"{limits.max_active_jobs} active jobs at the same time."
        )
