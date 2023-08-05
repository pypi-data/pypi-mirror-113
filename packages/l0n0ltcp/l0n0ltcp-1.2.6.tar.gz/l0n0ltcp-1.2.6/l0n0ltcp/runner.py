import asyncio


def run_forever():
    try:
        print("Press Ctrl+C to Close.")
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop = asyncio.get_event_loop()
        for task in asyncio.Task.all_tasks(loop):
            task.cancel()
        loop.stop()
