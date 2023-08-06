# @Time     : 2021/7/19
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
# import asyncio
#
# from common.f1z1_common.src.ammeter import AsyncMessageCounter
# from common.f1z1_common.src.utils import UnitOfTime
#
#
# def output(count: int):
#     print("resp", count)
#
#
# flow = AsyncMessageCounter(
#     output,
#     1000,
#     UnitOfTime.MILLISECOND
# )
#
#
# @flow.tracking
# async def send():
#     await asyncio.sleep(0.5)
#     return 1
#
#
# async def request(count: int):
#     s = 0
#     while s <= count:
#         await send()
#         s += 1
#
#
# async def emit_request():
#     t = []
#     for i in range(5):
#         t.append(asyncio.create_task(request(5)))
#
#     await asyncio.wait(t)
#
#
# def main():
#     asyncio.run(emit_request())
#
#
# if __name__ == '__main__':
#     main()
