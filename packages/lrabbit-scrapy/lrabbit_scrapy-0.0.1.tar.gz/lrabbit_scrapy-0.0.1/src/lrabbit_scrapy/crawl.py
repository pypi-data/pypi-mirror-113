from lrabbit_scrapy import BaseSpider
import traceback
import aiohttp
import sqlalchemy as sa
from parsel import Selector


class Spider(BaseSpider):
    # setup
    is_open_mysql = False
    is_drop_tables = True
    # reset all tasks,files,this is may delete all data files
    reset_task_list = True

    """
        not call a method or attribute start_with of 'file','table'
    """
    # datastore
    # table_table1 = [
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('val', sa.String(255)),
    #     sa.Column('val2', sa.String(255))
    # ]

    # file_store
    file_blogPost = [
        'id', 'title', 'datetime', 'content'
    ]

    def __init__(self, spider_name):
        super(Spider, self).__init__(spider_name)

    async def worker(self, task):
        """

        code your worker method

        :param task:
        :return:
        """
        """
         mysql work method
        """
        # await self.insert_one(self.tables['table1'].insert().values(val=str(task)))
        # res = await self.query(self.tables['table1'].select())
        # res = await res.fetchall()

        """
         want to see how to work,uncomment beyond code
        """
        url = f"http://www.lrabbit.life/post_detail/?id={task}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as res:
                    text = await res.text()
                    selector = Selector(text)
                    title = selector.css(".detail-title h1::text").get()
                    datetime = selector.css(".detail-info span::text").get()
                    content = ''.join(selector.css(".detail-content *::text").getall())
                    data = {"id": task, 'title': title, 'datetime': datetime, 'content': content}
                    if title:
                        self.all_files['blogPost'].write(data)
        except Exception as e:
            traceback.print_exc()
            return False
        return True

    async def create_tasks(self):
        return [i for i in range(100)]


if __name__ == '__main__':
    s = Spider(__file__)
    s.run()
