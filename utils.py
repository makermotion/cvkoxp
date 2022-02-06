from ahk import AsyncAHK
import asyncio

ahk = AsyncAHK()

async def main():
    x, y = await ahk.get_mouse_position()
    print(x, y)

asyncio.run(main())