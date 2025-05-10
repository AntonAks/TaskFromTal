import asyncio
from tasks import CollectStudiesTask, DummyTestTask


async def main():
    print("Scraper service was started!")
    await asyncio.gather(
        # DummyTestTask.collect()
        CollectStudiesTask.collect()
    )


if __name__ == '__main__':
    asyncio.run(main())
