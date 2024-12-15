# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-15

解碼參考來源: https://cloud.tencent.com/developer/article/2258872
"""
from tqdm import tqdm
import os, requests, subprocess
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from rich.console import Console
from subprocess import PIPE, STDOUT
from concurrent.futures import ThreadPoolExecutor, wait

class ParsingMediaLogic:
    def __init__(self, obj):
        self.type = obj.type
        self.url = obj.url
        self.path = os.getcwd() + '\\' + obj.path
        self.console = Console()

        self.todo_list = []
        self.headers = ParsingMediaLogic.update_headers()
        self.session = requests.Session()
        self.cryptor = None
        self.base_url = None
        self.timeout = 20

        fe = '.ts' if self.type in ['ts', 'video', 'mp4'] else '.jpg'
        check_list =  sorted([int(i.split(fe)[0]) for i in os.listdir(self.path) if fe in i]) if os.path.exists(self.path) else []
        self.count = 0 if len(check_list) == 0 else check_list[-1]+1

    @staticmethod
    def check_folder(path: str):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    @staticmethod
    def update_headers() -> dict:
        txt = [i for i in open(os.getcwd() + '\\Depend\\permissions.txt', 'r')]
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'authorization': txt[0].split(',')[-1].replace('\n', ''),
            'cookie': txt[1].split(',')[-1].replace('\n', ''),
            }
        return headers

    @staticmethod
    def get_target_title(soup: BeautifulSoup) -> str:
        get_title = soup.find('title').text
        for symbol in ['/', '<' , '>', ':', '|', '?', '*', '"']:
            get_title = get_title.replace(symbol, '')
        return get_title

    def progress_bar(self, task: str, symbol: str='━'):
        if task == 'Args':
            self.console.print(f'Get Parameter... {symbol * 46} 100%')
        elif task == 'Get_Downloads_List':
            self.console.print(f'Get Downloads List... {symbol * 41} 100%')
        elif task == 'Finish_Task':
            self.console.print('Finish Task ! Exit Program ...')

    def use_executor(self, function_obj):
        get_inpt = str(input('是否使用 [非同步多執行緒] ?\n1: 使用 2: 不使用\n'))
        if get_inpt == '1':
            self.create_executor(function_obj)
        else:
            for url in tqdm(self.todo_list, position=0, desc='Downloads Schedule: '):
                ret = function_obj(url)
                if ret == -1:
                    self.console.print(f'下載過程有檔案未載成功: index[{self.todo_list.index(url)}/{len(self.todo_list)}] -> {url}')
                    break

    def remove_temp_file(self):
        get_inpt = str(input('是否刪除 [媒體影片暫存檔] ?\n1: 刪除 2: 保留\n'))
        if get_inpt == '1':
            for i in [i for i in os.listdir(self.path) if i.split('.')[-1] in ['ts', 'm3u8', 'txt']]:
                os.remove(self.path + '\\' + i)

    def identify_type_operation(self):
        res = self.session.get(self.url, headers=self.headers, timeout=self.timeout)
        soup = BeautifulSoup(res.text, 'html.parser')
        self.path += f'\\{ParsingMediaLogic.get_target_title(soup)}'
        if not os.path.exists(self.path):
            ParsingMediaLogic.check_folder(self.path)
        if self.type in ['ts', 'video', 'mp4']:
            # FIXME m3u8 串流媒體
            # m3u8 位置不固定，目前跑幾個頁面就有 2 個版本，不排除更多...
            content_check = [i['content'] for i in soup.find_all('meta') if 'transcode' in str(i)]
            if len(content_check) != 0:
                self.url = content_check[0]
            else:
                content_check = []
                for div in soup.find_all('div', {'class', 'w-full'}):
                    if 'm3u8' in str(div) and 'playList' in str(div) and 'transcode_video' in str(div):
                        content_check += [str(div)]
                if len(content_check) != 0:
                    self.url = content_check[0].split('vidSrc=')[-1].split('.m3u8')[0] + '.m3u8'
                else:
                    self.url = None

            if self.url is None:
                self.console.print('not find m3u8 file')
            else:
                self.base_url = self.url.replace(self.url.split('/')[-1], '')
                res = self.session.get(self.url, headers=self.headers, timeout=self.timeout)
                with open(self.path + '\\media.m3u8', 'w') as f:
                    for line in res.text:
                        f.write(line)

                # 讀取 m3u8 密鑰 & 目標清單
                media = [i for i in open(self.path + '\\media.m3u8', 'r')]
                key = ''.join([i for i in media if '#EXT-X-KEY' in i]).split(',')[1].split('URI=')[-1][1:-1]

                res = self.session.get(self.base_url + key, headers=self.headers, timeout=self.timeout)
                self.cryptor = AES.new(res.content, AES.MODE_CBC)

                media = [i for i in open(self.path + '\\media.m3u8', 'r')]
                self.todo_list = [self.base_url + i for i in ''.join(media).split('\n') if '#EXT' not in i and i != '']
                self.progress_bar('Get_Downloads_List')

                self.use_executor(self.create_ts_media)

                with open(self.path + '\\media.txt', 'w') as f:
                    for i in range(0, self.count+1):
                        f.write(f"file '{i}.ts'\n")

                self.combine_ts_to_mp4() # 合併 ts 檔並轉為 mp4
                self.remove_temp_file() # 是否刪除暫存檔

        elif self.type in ['img', 'image', 'images']:
            # FIXME 靜態圖片
            table = soup.find_all('div', {'class': 'w-full lightbox_fancybox'})[0]
            for div in table.find_all('div'):
                try:
                    if div['data-src'][:5] == 'https':
                        self.todo_list += [div['data-src']]
                except:
                    pass

            self.progress_bar('Get_Downloads_List')
            self.use_executor(self.create_image)

        else:
            self.console.print(f'match type error: {self.type}')

    def create_ts_media(self, url) -> int:
        ret = -1
        try:
            res = self.session.get(url, headers=self.headers, timeout=self.timeout)
            if res.status_code == 200:
                with open(self.path + '\\' + str(self.count) + '.ts', 'wb') as f:
                    decrypto = self.cryptor.decrypt(res.content)
                    f.write(decrypto)
                self.count += 1
                ret = 0
        except:
            pass
        finally:
            return ret

    def combine_ts_to_mp4(self):
        cmdline = 'ffmpeg -f concat -i media.txt -c copy media.mp4'
        pop = subprocess.Popen(cmdline,
                               stdout=PIPE,
                               stderr=STDOUT,
                               cwd=self.path.lower(),
                               shell=True)

        while pop.poll() is None:
            line = pop.stdout.readline()
            try:
                line = line.decode('utf8')
                print(line)

            except UnicodeDecodeError as e:
                pass
            except IOError as e:
                print(e)

    def create_image(self, url) -> int:
        ret = -1
        try:
            res = self.session.get(url, headers=self.headers, timeout=self.timeout)
            if res.status_code == 200:
                with open(f'{self.path}/{self.count}.jpg', 'wb') as f:
                    f.write(res.content)
                self.count += 1
                ret = 0
        except:
            pass
        finally:
            return ret

    def create_executor(self, function_obj, max_workers: int=5):
        # FIXME 建立非同步的多執行緒的啟動器 -> 非同步下載檔案
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            new_task = {}
            task = {executor.submit(function_obj, url):
                        url for url in self.todo_list}

            schedule = tqdm(total=len(task), desc='Downloads Schedule: ')
            while len(task) > 0:
                callback, _ = wait(task, timeout=self.timeout, return_when='FIRST_COMPLETED')
                if callback != set():
                    for future in callback:
                        job = task[future]
                        ret = future.result()
                        del task[future]
                        if ret in [0]:
                            schedule.update(1)
                        elif ret in [-1]:
                            if future not in new_task:
                                new_task[future] = job  # 先儲存[需再 submit 的需求]
                        else:
                            pass

                        schedule.display()

                if len(task) == 0:
                    for future, job in new_task.items():
                        task[executor.submit(function_obj, job[0])] = job
                    new_task = {}

    def main(self):
        ParsingMediaLogic.check_folder(self.path)
        self.progress_bar('Args')
        self.identify_type_operation()
        self.progress_bar('Finish_Task')