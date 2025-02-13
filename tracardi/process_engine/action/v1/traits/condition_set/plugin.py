from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, FormField, FormComponent
from tracardi.service.plugin.runner import ActionRunner
from tracardi.process_engine.tql.condition import Condition
from .model.config import Config
from tracardi.service.plugin.domain.result import Result


def validate(config: dict) -> Config:
    return Config(**config)


class ConditionSetPlugin(ActionRunner):

    def __init__(self, **kwargs):
        self.config = Config(**kwargs)

    async def run(self, payload):
        condition = Condition()
        dot = self._get_dot_accessor(payload)

        for key, value in self.config.conditions.items():
            self.config.conditions[key] = await condition.evaluate(value, dot)

        return Result(port='result', value=self.config.conditions)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='ConditionSetPlugin',
            inputs=["payload"],
            outputs=["result"],
            version='0.6.2.1',
            license="MIT",
            author="Daniel Demedziuk",
            init={
                'conditions': {}
            },
            manual="condition_set_action",
            form=Form(
                groups=[
                    FormGroup(
                        name='Plugin configuration',
                        fields=[
                            FormField(
                                id='conditions',
                                name='Conditions to evaluate',
                                description='Provide key - value pairs where key is your custom name for a condition and value is a condition to evaluate (e.g. profile@consents.marketing EXISTS).',
                                component=FormComponent(
                                    type='keyValueList',
                                    props={
                                        'label': 'condition'
                                    }
                                )
                            )
                        ]
                    )
                ]
            )
        ),
        metadata=MetaData(
            name='Check conditions',
            desc='That plugin creates an object with results for given conditions.',
            icon='plugin',
            group=["Conditions"],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "result": PortDoc(desc="This port returns object with evaluated conditions.")
                }
            )
        )
    )