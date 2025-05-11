import asyncio
from tasks import CollectStudiesTask


async def main() -> None:
    print("Scraper service was started!")
    await asyncio.gather(CollectStudiesTask.collect())


if __name__ == "__main__":
    asyncio.run(main())
