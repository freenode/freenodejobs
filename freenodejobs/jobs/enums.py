from enumfields import Enum


class JobTypeEnum(Enum):
    FULL_TIME = 10
    PART_TIME = 20
    CONTRACT = 30
    VOLUNTEER = 40

    class Labels:
        FULL_TIME = "Full-time"
        PART_TIME = "Part-time"
        CONTRACT = "Contract"
        VOLUNTEER = "Volunteer"


class StateEnum(Enum):
    NEW = 10
    WAITING_FOR_APPROVAL = 20
    LIVE = 30
    REMOVED = 40

    class Labels:
        new = "New"
        waiting_for_approval = "Waiting for approval"
        live = "Live"
        removed = "Removed"


JOB_TYPE_MAP = {
    JobTypeEnum.FULL_TIME: 'full-time',
    JobTypeEnum.PART_TIME: 'part-time',
    JobTypeEnum.CONTRACT: 'contract',
    JobTypeEnum.VOLUNTEER: 'volunteer',
}
