# 主要是补充，主教程不写在这里

# docker的核心概念
就是用win下的资源跑linux
虽然可以在多个平台下运行，但是镜像的核心还是linux
所以要更新wsl

2. 可以在docker中包装conda
但是docker本身就是隔离得了，没必要

3. 编写两个文件只是制作好了图纸

4. 报错说
(base) PS C:\lxt\svn_study\save\0223\yolo0213> docker-compose up -d --build
unable to get image 'yolo0213-yolo-dev': error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.51/images/yolo0213-yolo-dev/json": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
是电脑没开docker desktop