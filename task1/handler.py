import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

from models import MessageResponse

# load .env variables
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SYSTEM_PROMPT = """
You are a telecom customer support assistant.
Help customers with:
- slow internet
- no internet
- billing issues
- router troubleshooting
- service outages
Be polite and helpful.
If the channel is voice → respond in maximum 2 sentences.
If the channel is chat or whatsapp → you can provide detailed help.
"""
async def call_ai(message: str):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
async def handle_message(customer_message: str, customer_id: str, channel: str):
    # empty message error
    if not customer_message.strip():
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="none",
            channel_formatted_response="",
            error="Empty customer message"
        )

    try:
        # timeout protection
        response_text = await asyncio.wait_for(
            call_ai(customer_message),
            timeout=10
        )
    except asyncio.TimeoutError:
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="retry",
            channel_formatted_response="",
            error="AI API timeout"
        )

    except Exception as e:
        # rate limit retry
        if "rate" in str(e).lower():
            await asyncio.sleep(2)
            try:
                response_text = await call_ai(customer_message)

            except Exception as retry_error:
                return MessageResponse(
                    response_text="",
                    confidence=0.0,
                    suggested_action="retry",
                    channel_formatted_response="",
                    error=str(retry_error)
                )
        else:
            return MessageResponse(
                response_text="",
                confidence=0.0,
                suggested_action="error",
                channel_formatted_response="",
                error=str(e)
            )

    # format for voice channel
    if channel == "voice":
        sentences = response_text.split(".")
        channel_response = ".".join(sentences[:2]).strip() + "."
    else:
        channel_response = response_text

    return MessageResponse(
        response_text=response_text,
        confidence=0.9,
        suggested_action="respond_to_customer",
        channel_formatted_response=channel_response,
        error=None
    )