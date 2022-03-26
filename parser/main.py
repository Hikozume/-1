import asyncio
from dromparser import parse
from datebase import DateBase



datebase = DateBase('DESKTOP-SI0JD8G', 'Auto')
datebase.clear_table('Auto')
print('[INFO] Очистил таблицу')
main_loop = asyncio.get_event_loop()
tasks = [main_loop.create_task(parse(10000, 20000, 1000000)),
         main_loop.create_task(parse(1000000, 1002000, 2000000)),
         main_loop.create_task(parse(2000000, 2005000, 3000000, step=5000)),
         main_loop.create_task(parse(3000000, 3005000, 4000000, step=5000)),
         main_loop.create_task(parse(4000000, 4010000, 5000000, step=10000)),
         main_loop.create_task(parse(5000000, 5010000, 6000000, step=10000)),
         main_loop.create_task(parse(6000000, 6010000, 7000000, step=10000)),
         main_loop.create_task(parse(7000000, 7010000, 8000000, step=10000)),
         main_loop.create_task(parse(8000000, 8010000, 9000000, step=10000)),
         main_loop.create_task(parse(9000000, 9010000, 10000000, step=10000)),
         main_loop.create_task(parse(10000000, 10020000, 11000000, step=20000))]
wait_tasks = asyncio.wait(tasks)
main_loop.run_until_complete(wait_tasks)

