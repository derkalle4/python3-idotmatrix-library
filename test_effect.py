import asyncio
import time
from idotmatrix import ConnectionManager
from idotmatrix import Effect

async def main():
    # connect
    conn = ConnectionManager()
    await conn.connectBySearch()

    colours = [(255,0,0), (255,162,0), (255,255,0), (0,255,0), (0,0,255), (255,0,255), (255,255,255)] #default colours used in the app.

    #Effect
    test = Effect()
    for i in range(0, 7):
        await test.setMode(i, colours[:2]) # this should work
        time.sleep(5)
        await test.setMode(i, colours[:3]) # this should work
        time.sleep(5)
        await test.setMode(i, colours[:4]) # this should work
        time.sleep(5)
        await test.setMode(i, colours[:5]) # this should work
        time.sleep(5)
        await test.setMode(i, colours[:6]) # this should work
        time.sleep(5)
        await test.setMode(i, colours[:7]) # this should work
        time.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        quit()
