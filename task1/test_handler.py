import asyncio
from handler import handle_message
async def main():
    response = await handle_message(
        "My internet is very slow today",
        "cust123",
        "chat"
    )
    print(response)
asyncio.run(main())