import logging
from videosdk.agents import Agent, AgentSession, CascadingPipeline, function_tool, WorkerJob ,ConversationFlow, JobContext, RoomOptions
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.google import GoogleLLM
from videosdk.plugins.cartesia import CartesiaTTS
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model

pre_download_model()


class HealthcareAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""
You are a general healthcare assistant. Help users with medical inquiries, 
guide them to the right specialist, and route them to appointment booking or medical support when needed.
Respond clearly, calmly, and professionally.
""",
        )

    async def on_enter(self) -> None:
        await self.session.reply(
            instructions="Greet the user politely and ask how you can assist with their health-related concern today."
        )

    async def on_exit(self) -> None:
        await self.session.say("Take care and stay healthy!")

    @function_tool()
    async def transfer_to_appointment(self) -> Agent:
        """Transfer to the healthcare appointment specialist for scheduling or changes."""
        return AppointmentAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_medical_support(self) -> Agent:
        """Transfer to medical support for symptoms, reports, or health guidance."""
        return MedicalSupportAgent(inherit_context=True)


class AppointmentAgent(Agent):
    def __init__(self, inherit_context: bool = False):
        super().__init__(
            instructions="""
You are an appointment specialist. Help users schedule, modify, or cancel 
doctor visits, follow-ups, tests, or telehealth appointments.
""",
            inherit_context=inherit_context,
        )

    async def on_enter(self) -> None:
        await self.session.say(
            "You’re connected with appointments. What would you like to schedule or update today?"
        )

    async def on_exit(self) -> None:
        await self.session.say("Your appointment request is complete. Wishing you good health!")


class MedicalSupportAgent(Agent):
    def __init__(self, inherit_context: bool = False):
        super().__init__(
            instructions="""
You are a medical support specialist. Help users with symptoms, 
health concerns, basic guidance, or understanding reports. 
You are NOT a doctor — provide general support and routing only.
""",
            inherit_context=inherit_context,
        )

    async def on_enter(self) -> None:
        await self.session.say(
            "You’re now connected with medical support. How can I help with your health concern?"
        )

    async def on_exit(self) -> None:
        await self.session.say("Glad I could help. Take care and stay well!")


async def entrypoint(ctx: JobContext):
    agent = HealthcareAgent()
    conversation_flow = ConversationFlow(agent)

    pipeline = CascadingPipeline(
        stt=DeepgramSTT(),
        llm=GoogleLLM(),
        tts=CartesiaTTS(),
        vad=SileroVAD(),
        turn_detector=TurnDetector()
    )
    session = AgentSession(
        agent=agent, 
        pipeline=pipeline,
        conversation_flow=conversation_flow
    )

    await session.start(wait_for_participant=True, run_until_shutdown=True)

def make_context() -> JobContext:
    room_options = RoomOptions(room_id="<room_id>", name="Multi Agent Switch Agent", playground=True)
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=entrypoint, jobctx=make_context)
    job.start()
