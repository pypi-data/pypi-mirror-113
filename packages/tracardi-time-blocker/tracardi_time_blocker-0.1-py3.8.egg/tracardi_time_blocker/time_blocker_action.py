from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, MetaData, Spec
from tracardi_plugin_sdk.domain.result import Result


class TimeBlockerAction(ActionRunner):

    def __init__(self, *args, **kwargs):
        print(kwargs)

    async def run(self, void):
        return None


def register() -> Plugin:
    return Plugin(
        start=False,
        debug=False,
        spec=Spec(
            module='tracardi_time_blocker.time_blocker_action',
            className='TimeBlockerAction',
            inputs=["void"],
            outputs=["Block", "DoNotBlock"],
            init={
              "block":  {
                  "start": None,
                  "end": None
              }
            }
        ),
        metadata=MetaData(
            name='Time blocker',
            desc='It blocks execution of workflow within given time.',
            type='flowNode',
            width=200,
            height=100,
            icon='start',
            group=["Time"]
        )
    )
