# RaspiFaceSystem

使用树莓派，OpenCV，Pyqt实现本地+网络的人脸识别

### 0.准备该项目

* 树莓派

  1. 先安装好OpenCV，因为树莓派安装OpenCV过于麻烦，我直接找了有OpenCV的镜像

  2. 安装树莓派的Pyqt

     ~~~ 
     sudo apt install -y python3-pyqt5
     ~~~

     ~~~ 
     sudo apt install -y python3-pyqt5.qsci python3-pyqt5.qtmultimedia python3-pyqt5.qtopengl python3-pyqt5.qtpositioning python3-pyqt5.qtquick python3-pyqt5.qtsensors python3-pyqt5.qtserialport python3-pyqt5.qtsql python3-pyqt5.qtsvg python3-pyqt5.qtwebchannel python3-pyqt5.qtwebkit python3-pyqt5.qtwebsockets python3-pyqt5.qtx11extras python3-pyqt5.qtxmlpatterns
     ~~~

* 电脑端，请提前安装好anaconda

  1. 搭建虚拟环境

     ~~~ 
     conda create -n xxx python=3.6
     ~~~

     xxx是你的虚拟环境名字

  2. 启用虚拟环境

     ~~~
     activate your_env_name(虚拟环境名称)
     ~~~

  3. 在虚拟环境内安装opencv和pyqt

     ~~~
     pip install opencv-python 
     ~~~

     ~~~
     pip install opencv-contrib-python 
     ~~~

     ~~~
     pip install PyQt5 -i https://pypi.douban.com/simple
     ~~~

     ~~~
     pip install PyQt5-tools -i https://pypi.douban.com/simple
     ~~~

  如果安装不成功，请自行百度，我们只确保能安装上OpenCV和PyQT就行

  

* 去百度SDK注册你的账号，具体教程请自行百度，填写好你的 APPID AK SK还有用户组GROUP，然后将文件路径更改完毕  ，如果文件路径不对，项目运行会出错。

### 1. 拉取本项目.

~~~ 
git clone https://github.com/cheng-haha/RaspiFaceSystem.git
~~~

### 2.功能描述

* 本地识别是使用Opencv进行构建，还是传统的统计学习范畴。
* 网络识别是调用百度SDK，注册和识别功能已经集成到GUI的的按钮中
* 本项目一开始运行的时候判断是否有网络，有就优先网络识别，没有网刘使用本地识别进行兜底

### 3. 界面

* 主界面图

  * 电脑端

  ![主界面图](D:\RaspiFaceSystem\RaspiFaceSystem\showImg\主界面图.PNG)

  * 树莓派端

  ![img](file:///C:\Users\ADMINI~1\AppData\Local\Temp\ksohtml13148\wps2.jpg)

* 注册系统

  ![注册界面](D:\RaspiFaceSystem\RaspiFaceSystem\showImg\注册界面.PNG)

  

  使用时一定记住，必须先注册到数据库当中，才能人脸录入，不然没法进行数据标注

* 人脸录入界面

  ![人脸录入界面图](D:\RaspiFaceSystem\RaspiFaceSystem\showImg\人脸录入界面图.PNG)

  当选择本地收集的时候是需要进行训练的，选择网络识别不需要，百度那边直接就训练好了

* 人脸识别界面

  * 网络识别

    ![人脸识别成功图](D:\RaspiFaceSystem\RaspiFaceSystem\showImg\人脸识别成功图.PNG)

    惊人的百分百准确率，百度人脸识别确实可以

  * 本地识别

    ![本地识别](D:\RaspiFaceSystem\RaspiFaceSystem\showImg\本地识别.PNG)

    本地识别置信度就低很多，这是因为统计学习算法的原因，当时本来想搞深度的，但树莓派的性能太低，估计深度跑起来会炸。但是如果识别不出来的话，直接就返回一个负的置信度

    ![img](file:///C:\Users\ADMINI~1\AppData\Local\Temp\ksohtml13148\wps1.jpg)

    

### 4. 文件功能

1. log文件是用来记录网络识别的登录记录，为什么不加入本地识别的登录记录？懒得写。
2. [haarcascade_frontalface_default.xml](https://github.com/cheng-haha/RaspiFaceSystem/blob/main/haarcascade_frontalface_default.xml) 是人脸检测器
3. testDIR.txt里面是记录的字符串化的字典，我在提取的时候eval了一下，登录名和密码还是字典对应关系好用。
4. trainer.yml是训练出的模型
5. youtemp.png是网络识别的图片，将这张图片上传到百度那边进行人脸匹配。