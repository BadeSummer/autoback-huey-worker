from autoback_huey_task import RedisHuey, crontab
from download import DownloadFromBaiduCloud

# 配置Huey实例
# host 填 redis 的地址
HUEY = RedisHuey('autoback', host='localhost', port=6379)

@HUEY.task()
def download_from_baidu_cloud(fs_id, file_check_md5, save_path, access_token):
    dl = DownloadFromBaiduCloud(fs_id, file_check_md5, save_path, access_token)
    dl.download_from_baidu_cloud()

@HUEY.task()
def test(s):
    print(s)
    return True