import os
# import sys
# project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(project_path)

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from openapi_client.api import multimediafile_api
import openapi_client

class DownloadFromBaiduCloud():
    '''
    从网盘下载文件的热NAS
    '''
    def __init__(self, fs_id, file_check_md5, save_path, access_token):
        self.fs_id = fs_id
        self.file_check_md5 = file_check_md5
        self.save_path = save_path
        self.access_token = access_token

    def download_from_baidu_cloud(self):
    # Step 1: 检查本地文件并确定起始字节
        if os.path.exists(self.save_path):
            start_byte = os.path.getsize(self.save_path)
        else:
            start_byte = 0

        print(f"发现下载文件，从{start_byte}B开始下载")
        headers = {
            'Range': f'bytes={start_byte}-',
            'User-Agent': "pan.baidu.com"
            }
        download_url, file_size = self._get_file_download_url()

        try:
            if start_byte == file_size:
                return f"检测到文件已经下载完毕。"
            
            # Step 2: 发送带 Range 头的请求
            with requests.get(download_url, headers=headers, stream=True) as response:
                response.raise_for_status()  # 确保请求成功
                
                # Step 3: 以追加模式打开文件继续写入数据
                with open(self.save_path, 'ab') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # 过滤掉 keep-alive 新块
                            file.write(chunk)
                    print(f'下载完成，文件保存到 {self.save_path}')
        except KeyboardInterrupt:
            print('下载被中断，下次将从断点继续')

        except Exception as e:
            print(f'下载失败：{e}')

    def _get_file_download_url(self):
        '''
        调用api获取文件详情信息得到 dlink 和 file size
        '''
        with openapi_client.ApiClient() as api_client:
            # Create an instance of the API class
            api_instance = multimediafile_api.MultimediafileApi(api_client)
            at = self.access_token
            fsids = f"[{self.fs_id}]"
            dlink = "1"

            try:
                api_response = api_instance.xpanmultimediafilemetas(
                    at, fsids, dlink=dlink
                )
                # 现在默认成功，后续要加上错误处理

                dlink = api_response.get('list')[0].get('dlink')
                download_url = f"{dlink}&access_token={at}"
                file_size = api_response.get('list')[0].get('size')

                return download_url, file_size
            
            except openapi_client.ApiException as e:
                pass
        
    