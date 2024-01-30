# Autoback Huey Worker
用于部署Autoback后台的worker

## 安装依赖
```shell
pip install -r reqirements.txt
```
## 选择需要函数
去`autoback/tasks.py`里注释掉不需要的工作函数

## 运行worker（单线程）
```shell
huey_consumer.py autoback.tasks.HUEY
```
更丰富的`huey`参数可以去查看[文档](https://huey.readthedocs.io/en/latest/)