from __future__ import annotations as _annotations

from dataclasses import dataclass, field
from typing import Annotated

import logfire
from pydantic_graph import BaseNode, Edge, End, Graph, GraphRunContext
from pydantic_ai import Agent
from pydantic_ai.format_as_xml import format_as_xml
from pydantic_ai.messages import ModelMessage

# Configure logfire
logfire.configure(send_to_logfire='if-token-present')

def get_azure_gpt_model():
    import os 
    import openai
    import httpx
    from pydantic_ai.models.openai import OpenAIModel

    client = openai.AsyncAzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_BASE_URL"),
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        http_client=httpx.AsyncClient()
    )

    model = OpenAIModel('gpt-4o', openai_client=client)
    return model

@dataclass
class QuestionState:
    question: str | None = None
    ask_agent_messages: list[ModelMessage] = field(default_factory=list)
    evaluate_agent_messages: list[ModelMessage] = field(default_factory=list)

@dataclass
class EvaluationResult:
    correct: bool
    comment: str

# Initialize agents
ask_agent = Agent(
    get_azure_gpt_model(),
    defer_model_check=True,
)

evaluate_agent = Agent(
    get_azure_gpt_model(),
    result_type=EvaluationResult,
    system_prompt='Given a question and answer, evaluate if the answer is correct.',
)

@dataclass
class Ask(BaseNode[QuestionState]):
    async def run(self, ctx: GraphRunContext[QuestionState]) -> Answer:
        result = await ask_agent.run(
            'Ask a simple question with a single correct answer.',
            message_history=ctx.state.ask_agent_messages,
        )
        ctx.state.ask_agent_messages += result.all_messages()
        ctx.state.question = result.data
        return Answer()

@dataclass
class Answer(BaseNode[QuestionState]):
    answer: str | None = None

    async def run(self, ctx: GraphRunContext[QuestionState]) -> Evaluate:
        assert self.answer is not None
        return Evaluate(self.answer)

@dataclass
class Evaluate(BaseNode[QuestionState]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[QuestionState],
    ) -> Congratulate | Reprimand:
        assert ctx.state.question is not None
        result = await evaluate_agent.run(
            format_as_xml({'question': ctx.state.question, 'answer': self.answer}),
            message_history=ctx.state.evaluate_agent_messages,
        )
        ctx.state.evaluate_agent_messages += result.all_messages()
        if result.data.correct:
            return Congratulate(result.data.comment)
        else:
            return Reprimand(result.data.comment)

@dataclass
class Congratulate(BaseNode[QuestionState, None, None]):
    comment: str

    async def run(
        self, ctx: GraphRunContext[QuestionState]
    ) -> Annotated[End, Edge(label='success')]:
        print(f'Correct answer! {self.comment}')
        return End(None)

@dataclass
class Reprimand(BaseNode[QuestionState]):
    comment: str

    async def run(self, ctx: GraphRunContext[QuestionState]) -> Ask:
        print(f'Comment: {self.comment}')
        ctx.state.question = None
        return Ask()

# Create the graph
question_graph = Graph(
    nodes=(Ask, Answer, Evaluate, Congratulate, Reprimand),
    state_type=QuestionState
) 