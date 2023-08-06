import asyncio.queues
import asyncio
import time
import os
from pathlib import Path
import datetime
import sys
import sqlalchemy as sa
from sqlalchemy import MetaData, Table, Column, Integer, String
from aiomysql.sa import create_engine as aio_create_engine
from sqlalchemy import create_engine
from configparser import ConfigParser
from typing import Dict
import inspect
import csv
import os

pwd_dir = os.path.abspath(os.getcwd())
metadata = MetaData()

config = None


class TermColor:
    ATTRIBUTES = dict(
        list(zip([
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
        ],
            list(range(1, 9))
        ))
    )
    del ATTRIBUTES['']

    HIGHLIGHTS = dict(
        list(zip([
            'on_grey',
            'on_red',
            'on_green',
            'on_yellow',
            'on_blue',
            'on_magenta',
            'on_cyan',
            'on_white'
        ],
            list(range(40, 48))
        ))
    )

    COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
        ],
            list(range(30, 38))
        ))
    )

    RESET = '\033[0m'

    @staticmethod
    def colored(text, color=None, on_color=None, attrs=None):

        if os.getenv('ANSI_COLORS_DISABLED') is None:
            fmt_str = '\033[%dm%s'
            if color is not None:
                text = fmt_str % (TermColor.COLORS[color], text)

            if on_color is not None:
                text = fmt_str % (TermColor.HIGHLIGHTS[on_color], text)

            if attrs is not None:
                for attr in attrs:
                    text = fmt_str % (TermColor.ATTRIBUTES[attr], text)

            text += TermColor.RESET
        return text


class CommonUtils:

    def __init__(self):
        pass

    @staticmethod
    def fix_str_args(args):
        return list(map(lambda x: str(x).strip(), args))

    @staticmethod
    def get_format_time(for_mat='%Y-%m-%d %H:%M:%S'):
        return TermColor.colored(datetime.datetime.now().strftime(for_mat), 'yellow').encode('utf8')

    @staticmethod
    def space_join_line_arg(*args):
        return ' '.join(args) + '\n'


class LogUtils:

    def __init__(self):
        pass

    @staticmethod
    def log_now_time_str():
        sys.stdout.buffer.write(CommonUtils.get_format_time())

    @staticmethod
    def log_str(color_str, args):
        args = CommonUtils.fix_str_args(args)
        text = ' '.join(args)
        text = color_str + ' ' + text + '\n'
        sys.stdout.buffer.write(text.encode('utf8'))

    @staticmethod
    def log_info(*args):
        color_str = TermColor.colored('[*INFO*]', 'cyan')
        LogUtils.log_str(color_str, args)

    @staticmethod
    def log_running(*args):
        color_str = TermColor.colored('[*RUNNING*]', 'yellow')
        LogUtils.log_str(color_str, args)

    @staticmethod
    def log_finish(*args):
        color_str = TermColor.colored('*FINISH*', 'green')
        LogUtils.log_str(color_str, args)

    @staticmethod
    def log_error(*args):
        color_str = TermColor.colored('[*ERROR*]', 'red')
        LogUtils.log_str(color_str, args)

    @staticmethod
    def log_to_file(file_path, line):
        with open(file_path, 'a', encoding='utf8') as f:
            line = CommonUtils.space_join_line_arg(LogUtils.get_format_time(), line)
            f.write(line)


class DbUtils(LogUtils):
    all_tables: Dict[str, sa.Table] = {}

    def __init__(self, spider_name):
        spider_name = spider_name.split(".")[0]
        super(DbUtils, self).__init__()
        global config
        config = ConfigParser()
        config_path = os.path.join(pwd_dir, f'{spider_name}.ini')
        config.read(config_path)
        env = os.getenv('ENV', 'test')
        config = config[env]
        self.engine = None

    async def init_engine(self):
        self.engine = await aio_create_engine(
            user=config['db_user'],
            password=config['db_password'],
            port=3306,
            host=config['db_host'],
            db=config['db_database'],
            autocommit=True
        )
        engine = create_engine(
            f'mysql+pymysql://{config["db_user"]}:{config["db_password"]}@{config["db_host"]}/{config["db_database"]}',
            echo=True,

        )
        metadata.bind = engine
        try:
            if self.__getattribute__('is_drop_tables'):
                metadata.drop_all()
                LogUtils.log_finish('已清空表')
        except Exception as e:
            LogUtils.log_info("not found is_drop_tables")
        self._generate_tables()
        metadata.create_all(engine)

    def _generate_tables(self):
        for k, v in inspect.getmembers(self):
            if k.startswith('table'):
                table_name = k.split('_')[-1]
                try:
                    tbl = Table(table_name, metadata, Column('id', Integer, primary_key=True), *v)
                except Exception as e:
                    pass
                self.all_tables[table_name] = tbl
                LogUtils.log_finish(table_name, '创建完成')

    @asyncio.coroutine
    def insert_one(self, sql):
        with (yield from self.engine) as conn:
            yield from conn.execute(sql)

    @asyncio.coroutine
    def query(self, sql):
        with (yield from self.engine) as conn:
            res = yield from conn.execute(sql)
            res = yield from res.fetchall()
            return res


class FileStore:

    def __init__(self, file_name, headers, reset_task_list):
        self.file_name = f'{file_name}.csv'
        self.headers = headers
        self.reset_task_list = reset_task_list
        self.write_headers()

    def write_headers(self):
        if not os.path.exists(os.path.join(pwd_dir, self.file_name)) or self.reset_task_list:
            with open(os.path.join(pwd_dir, self.file_name), 'w', encoding='utf8', newline='') as f:
                dict_write = csv.DictWriter(f, fieldnames=self.headers)
                dict_write.writeheader()

    def write(self, d):
        with open(os.path.join(pwd_dir, self.file_name), 'a', encoding='utf8', newline='') as f:
            dict_write = csv.DictWriter(f, fieldnames=self.headers)
            dict_write.writerow(d)


class WriteUtil(LogUtils):
    all_files: [str, FileStore] = {}

    def __init__(self):

        super(WriteUtil, self).__init__()
        self._generate_files()

    def _generate_files(self):
        try:
            reset_task_list = self.__getattribute__('reset_task_list')
        except Exception as e:
            self.log_info('not found reset_task_list option ')
            return
        for k, v in inspect.getmembers(self):
            if k.startswith('file'):
                file_name = k.split("_")[-1]
                self.all_files[file_name] = FileStore(file_name, v, reset_task_list)
                LogUtils.log_finish(f'创建{file_name}存储文件成功')


class BaseSpider(DbUtils, WriteUtil):

    def __init__(self, spider_name):
        spider_name = spider_name.split('.')[0]
        DbUtils.__init__(self, spider_name)
        WriteUtil.__init__(self)
        self.task_queue = asyncio.queues.Queue()

        self.redis = None
        self.db = None
        self.spider_name = spider_name
        self.start_time = None
        self.finish_file_name = None
        self.all_file_name = None
        self.init_file_name(spider_name)

        self.config = ConfigParser()
        config_path = os.path.join(pwd_dir, f'{spider_name}.ini')
        self.config.read(config_path)
        env = os.getenv('ENV', 'test')
        self.config = self.config[env]

    def init_file_name(self, spider_name):
        spider_name = spider_name.split('.')[0]
        self.finish_file_name = f'{spider_name}_finish.log'
        self.all_file_name = f'{spider_name}_all.log'

    def get_tasks_list_by_file(self):
        finish_set = set()
        all_set = set()
        if os.path.exists(os.path.join(pwd_dir, self.all_file_name)):
            with open(self.all_file_name, 'r', encoding='utf8') as f:
                for line in f.readlines():
                    all_set.add(line)
        if os.path.exists(os.path.join(pwd_dir, self.finish_file_name)):
            with open(self.finish_file_name, 'r', encoding='utf8') as f:
                for line in f.readlines():
                    finish_set.add(line)
        return list(all_set.difference(finish_set))

    async def _generate_task(self):
        try:
            reset_task_list = self.__getattribute__('reset_task_list')
        except Exception as e:
            LogUtils.log_info("not found reset_task_list")
            return
        if not os.path.exists(os.path.join(pwd_dir, self.all_file_name)) or reset_task_list:
            if os.path.exists(os.path.join(pwd_dir, self.all_file_name)):
                os.remove(os.path.join(pwd_dir, self.all_file_name))
            if os.path.exists(os.path.join(pwd_dir, self.finish_file_name)):
                os.remove(os.path.join(pwd_dir, self.finish_file_name))
            try:
                generate_callback = self.__getattribute__('create_tasks')
            except Exception as e:
                LogUtils.log_info("not found create_tasks")
                return
            task_lists = await generate_callback()
            task_lists = list(set(task_lists))
            for task in task_lists:
                with open(os.path.join(pwd_dir, self.all_file_name), 'a', encoding='utf8') as f:
                    f.write(str(task))
                    f.write('\n')
        else:
            task_lists = self.get_tasks_list_by_file()
        for task in task_lists:
            self.task_queue.put_nowait(str(task).strip())

    async def base_worker(self):
        try:
            worker_callback = self.__getattribute__('worker')
        except Exception as e:
            LogUtils.log_info("not found worker")
        while True:
            task = await self.task_queue.get()
            self.log_running(task)
            result = await worker_callback(task)
            self.task_queue.task_done()
            if result:
                with open(self.finish_file_name, 'a', encoding='utf8') as f:
                    f.write(str(task).strip())
                    f.write('\n')
                self.log_finish(task)

    async def wait_all_task(self):
        await self.task_queue.join()

    def run(self):
        loop = asyncio.get_event_loop()
        is_open_mysql = self.__getattribute__("is_open_mysql")
        if is_open_mysql:
            loop.run_until_complete(self.init_engine())
        loop.run_until_complete(self._generate_task())
        task_list = []
        for i in range(int(self.config['workers_num'])):
            task = loop.create_task(self.base_worker())
            task_list.append(task)
        started_time = time.monotonic()
        loop.run_until_complete(self.wait_all_task())
        total_time = time.monotonic() - started_time
        for task in task_list:
            task.cancel()
        print(f"本次花费时间为: {total_time}")
