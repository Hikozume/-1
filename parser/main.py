import asyncio
from dromparser import parse
from datebase import DateBase



datebase = DateBase(r'Autos.db')
datebase.clear_table('Auto')
print('[INFO] Очистил таблицу')
main_loop = asyncio.get_event_loop()
tasks = [
            main_loop.create_task(parse(10000, 20000, 1000000)),
            main_loop.create_task(parse(1000000, 1002000, 2000000))]
wait_tasks = asyncio.wait(tasks)
main_loop.run_until_complete(wait_tasks)

