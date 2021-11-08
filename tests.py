"""
Test the tasks
"""
import pytest
from foo.tasks import task_a, big_task


# this class MUST be defined at the top level otherwise pytest won't find it
# with pytest.raises(), probably because of different relative import path.
class ParticularException(Exception):
    """This is a custom exception for testing purposes"""


def test_task_a(mocker, monkeypatch):
    """Very simple test to demonstrate the basic of testing.

    monkeypatch allows to set environment variables and general system
    configuration."""
    monkeypatch.setenv("CELERY_BROKER_URL", "redis://localhost")
    task_a.apply(((1,)))

    assert True


# here an example on using mocker fixture instead of mock.patch
# that doesn't seem to work with the tasks, probably cause of
# some aspects of the importing mechanism inside celery
def test_big_task_create_chain(celery_app, mocker, monkeypatch):
    """Check big_task create the correct signatures.

    Here we are going to use the celery_app fixture to define our own tasks to
    be called as callback.
    """
    # monkeypatch.setenv("CELERY_TASK_ALWAYS_EAGER", True)
    mocked_task_a = mocker.patch('foo.tasks.task_a')
    mocked_task_b = mocker.patch('foo.tasks.task_b')

    is_failed = False

    @celery_app.task
    def normal(*args):
        print("normal %s" % args)

    @celery_app.task
    def on_success(*args):
        print("OK")

    @celery_app.task
    def on_failure(request, exc, traceback):
        nonlocal is_failed
        is_failed = True
        print('--\n\n{0} {1}\n{2}'.format(
            request.id, exc, traceback))

    @celery_app.task
    def will_fail(*args):
        raise ParticularException("It's me! Exception!")

    big_task.apply((on_success, on_failure))

    assert mocked_task_a.si.called
    assert mocked_task_b.si.called

    from foo.tasks import build_chain

    # remember to patch both tasks otherwise doesn't raise
    # why? the "task_a | task_b" construct calls the "__or__()"
    # operator of the mock invalidating the actual implementation
    # of the chaining!
    mocker.patch('foo.tasks.task_a', will_fail)
    mocker.patch('foo.tasks.task_b', normal)
    chain = build_chain('arg1', 'arg2', on_success.si(), on_failure.s())

    with pytest.raises(ParticularException):
        chain.apply()

    assert is_failed

    # reset for the next test
    is_failed = False

    mocker.patch('foo.tasks.task_a', normal)
    mocker.patch('foo.tasks.task_b', will_fail)
    chain = build_chain('arg1', 'arg2', on_success.si(), on_failure.s())

    with pytest.raises(ParticularException):
        chain.apply()

    assert is_failed

