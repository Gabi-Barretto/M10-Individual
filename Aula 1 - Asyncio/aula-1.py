import asyncio

async def soma(a, b):
    print(F"{asyncio.get_event_loop().time()}")
    await asyncio.sleep(1)
    print(F"tchau {asyncio.get_event_loop().time()}")
    return a + b


async def main():
    operacoes = [

        soma(1,2),
        soma(3,4),
    ]
    await asyncio.gather(*operacoes)


asyncio.run(main())