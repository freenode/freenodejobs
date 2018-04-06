from email_from_template import send_mail

from django.contrib.auth import get_user_model

from freenodejobs.utils import log

from .enums import StateEnum

UserModel = get_user_model()

TRANSITIONS = []


def dispatch(job, old_state, new_state, actor, description):
    history = job.state_history.create(
        actor=actor,
        old_state=old_state,
        new_state=new_state,
        description=description,
    )

    log.info("Job #{} state {} -> {}", job.pk, old_state, new_state)

    for x, y, fn in TRANSITIONS:
        if (old_state, new_state) == (x, y):
            fn(job, history)


class Transition(object):
    def __init__(self, old_state, new_state):
        self.old_state = old_state
        self.new_state = new_state

    def __call__(self, fn):
        TRANSITIONS.append((self.old_state, self.new_state, fn))

        return fn


@Transition(StateEnum.NEW, StateEnum.WAITING_FOR_APPROVAL)
@Transition(StateEnum.LIVE, StateEnum.WAITING_FOR_APPROVAL)
def submitted_for_approval(job, _):
    for x in UserModel.objects.filter(is_staff=True):
        send_mail((x.email,), 'jobs/submitted_for_approval.email', {
            'job': job,
        }, fail_silently=True)


@Transition(StateEnum.WAITING_FOR_APPROVAL, StateEnum.LIVE)
def approved(job, _):
    send_mail((job.user.email,), 'jobs/approved.email', {
        'job': job,
    }, fail_silently=True)


@Transition(StateEnum.WAITING_FOR_APPROVAL, StateEnum.NEW)
def rejected(job, history):
    send_mail((job.user.email,), 'jobs/rejected.email', {
        'job': job,
        'reason': history.description,
    }, fail_silently=True)


@Transition(StateEnum.LIVE, StateEnum.REMOVED)
def removed(job, history):
    send_mail((job.user.email,), 'jobs/removed.email', {
        'job': job,
        'reason': history.description,
    }, fail_silently=True)
