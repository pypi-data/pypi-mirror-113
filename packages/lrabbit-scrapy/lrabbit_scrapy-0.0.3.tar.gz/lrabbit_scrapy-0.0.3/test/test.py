import sys
from pathlib import Path
import os

base_dir = (Path(__file__).resolve()).parent

lrabbit_scrapy_path = os.path.join(base_dir, 'src')
print(lrabbit_scrapy_path)
sys.path.insert(0, str(lrabbit_scrapy_path))
print(sys.path)

from src.lrabbit_scrapy import BaseSpider
import sqlalchemy as sa


class Spider(BaseSpider):
    # setup
    is_drop_tables = True
    reset_task_list = False

    # datastore
    table_table1 = [
        sa.Column('val', sa.String(255)),
        sa.Column('val2', sa.String(255))
    ]

    file_file1 = [
        'name', 'age', 'sex'
    ]

    def __init__(self, spider_name):
        super(Spider, self).__init__(spider_name)

    async def worker(self, task):
        """

        code your worker method

        :param task:
        :return:
        """
        # await self.insert_one(self.tables['table1'].insert().values(val=str(task)))
        # await self.insert_one(self.tables['table2'].insert().values(val=str(task)))
        # res = await self.query(self.tables['table1'].select())
        # res = await res.fetchall()

        data = {"name": task, 'age': 0, 'sex': 'male'}
        self.files['file1'].write(data)

    async def create_tasks(self):
        return [i for i in range(5000)]


if __name__ == '__main__':
    s = Spider(__file__)
    s.run()
