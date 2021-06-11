'''
Author: 程东洲
Date: 2021-05-19 21:33:22
LastEditTime: 2021-06-11 11:16:35
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \testcamera\testCamera03.py
'''

from typing import List
import numpy as np
from PIL import Image
import base64
import time
from aip import AipFace, face
import os
import sys
# print(sys.path)
from PyQt5.QtCore import  QThread, QTimer, Qt, pyqtSignal
import cv2
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QDialog, QRadioButton, QWidget,QApplication,QLabel,QHBoxLayout,QVBoxLayout,\
    QPushButton,QMessageBox,QLineEdit,QGridLayout,QInputDialog

from urllib import request

######################################################################################
# 这些路径是使用在树莓派上的，也就是说在树莓派上将这几行变量给启用，将下面的
# cap_id = 0
# user_pw={ 'cheng':'123456' }
# path = 'haarcascade_frontalface_default.xml'
# user_path= "user_names.txt"
# passwd_path = 'password.txt'
# trainer_path = r'face_trainer\trainer.yml'
# data_path = 'Facedata'
# image_name = 'youtemp.png'


#这里的路径是不对的，请自行修改对应的路径，在电脑端的vscode上使用时就启用这些变量，将上方的变量进行注释
cap_id = 0
#人脸检测器路径
path = r'D:\Pyqt5\testcamera\haarcascade_frontalface_default.xml'
#数据库路径
user_path= r"D:\Pyqt5\testcamera\testDIR.txt"
# passwd_path = r'D:\Pyqt5\testcamera\password.txt'
#模型路径
trainer_path = r'D:\Pyqt5\testcamera\trainer.yml'
#本地识别收集图片路径
data_path = r'D:\Pyqt5\testcamera\Facedata'
#网络识别图片路径
image_name = r'D:\Pyqt5\testcamera\youtemp.png'

#######################################################################################

""" 你的 APPID AK SK """
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
#图像编码方式
IMAGE_TYPE='BASE64'
#填写你的用户组信息
GROUP = ''

######################################################################################
#判断网络状态，我设置的也只是一开始判断一次，之后不会更换网络状态，如果想要启用程序后能无间断
#检测网络状态，可以使用threading多线程一下

#照片名字
# exit_code = os.system('ping www.baidu.com')
try:
    ret = request.urlopen(url="https://www.baidu.com", timeout=3.0)
    exit_code = 0
    print("开启网络识别")
except:
    exit_code = 1
    print( "开启本地识别 ")


######################################################################################

#这个类是用来管理登录逻辑
class Demo( QWidget ):
    def __init__( self ):

        super().__init__() 
        #控件的初始化
        self.resize(  800 , 500 )
        self.setWindowTitle( '基于Opencv和树莓派的人脸识别系统')
        self.user_name_label = QLabel( "用户名:" ,self )
        self.user_line = QLineEdit( self )
        self.passwd_label = QLabel( '密码:' , self )
        self.passwd_line = QLineEdit( self )

        self.login_button  =  QPushButton( 'log in' , self )
        self.signin_button =  QPushButton( "sign in" ,self )
        self.face_recongition_button = QPushButton( "人脸识别" ,self )
        self.collect_buttton = QPushButton( "人脸录入" , self )
        #将布局类实例化
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
        self.h_face_layout = QHBoxLayout()
        self.grid_layout = QGridLayout()

        #初始化布局
        self.layput_init()
        #初始化输入框的隐含信息
        self.line_init()
        #初始化登录按钮的不可用，等待登录框有值时才会启用
        self.login_input_init()
        #初始化按下登录按钮后与数据库的检查程序,初始化按下注册按钮的注册页面的逻辑
        self.button_init()

        #实例化signin按钮按下后的管理页面
        self.sginin_page = Signin_Dialog()

        #实例化face recongition按钮按下的管理页面
        self.face_page = Face_start( )

        #实例化收集人脸数据集的管理页面
        self.colleet_page = CollectPicture_Page( )
        

    def layput_init( self ):
        self.grid_layout.addWidget( self.user_name_label , 0 , 0 )
        self.grid_layout.addWidget( self.user_line , 0 , 1 )
        self.grid_layout.addWidget( self.passwd_label , 1 , 0 )
        self.grid_layout.addWidget( self.passwd_line , 1 , 1 )
        self.h_layout.addWidget( self.login_button )
        self.h_layout.addWidget( self.signin_button )
        self.h_face_layout.addWidget( self.face_recongition_button )
        self.h_face_layout.addWidget( self.collect_buttton )


        self.v_layout.addLayout( self.grid_layout )
        self.v_layout.addLayout( self.h_layout )
        self.v_layout.addLayout( self.h_face_layout )

        self.setLayout( self.v_layout )

    def line_init( self ):
        self.user_line.setPlaceholderText( "请输入你的用户账号" )
        self.passwd_line.setPlaceholderText( "请输入你的密码")
        self.passwd_line.setEchoMode( QLineEdit.Password )

        self.user_line.textChanged.connect( self.check_input )
        self.passwd_line.textChanged.connect( self.check_input )
    #检查输入信息，两个框有值就对按钮进行使能，单一或者无值就将其停滞
    def check_input( self ):

        if self.user_line.text() and self.passwd_line.text() :
            self.login_button.setEnabled( True )
        else:
            self.login_button.setEnabled( False )

    def button_init( self ):
        self.login_button.clicked.connect( self.check_login_info )
        self.signin_button.clicked.connect( self.SigninPage_exe )
        self.face_recongition_button.clicked.connect( self.Face_start_exe )
        self.collect_buttton.clicked.connect( self.Collect_page_exe )

    def SigninPage_exe( self ):
        self.sginin_page.exec( )#启动注册页面
    # 人脸识别页面
    def Face_start_exe( self ):
        self.face_page.exec( )
    # 人脸收集页面启动
    def Collect_page_exe( self ):
        self.colleet_page.exec( )

    def check_login_info( self ):
        f_all = open( user_path , 'r+')
        read_dict = eval( f_all.read( ) ) 
        f_all.close()
        

        if self.user_line.text() not in read_dict:
            QMessageBox.critical( self , '登录消息' , "登录失败,请填写正确的用户名" , QMessageBox.Ok )
        elif read_dict[ self.user_line.text() ] == self.passwd_line.text():
            QMessageBox.information( self , '登录消息' , "登录成功" , QMessageBox.Ok  )
        else:
            QMessageBox.critical( self , '登录消息' , "登录失败,请填写正确的密码" , QMessageBox.Ok )


    def login_input_init( self ):
        self.login_button.setEnabled( False )

    

    # def facepass( self ):
    #     get_name=self.recognize_face()#返回识别的人名
    #     if get_name=="unknown":
    #         reply = QMessageBox.information(self, '提示', '人脸识别失败', QMessageBox.Close)
    #     else:
    #         reply = QMessageBox.information(self, '提示', "欢迎您："+get_name, QMessageBox.Ok)
    #         print("编写其他程序")


# #多线程进行网络监听
# class My_theard( QThread ):
#     my_signal = pyqtSignal( int )
#     def __init__( self  ):
#         super().__init__()


#     def run( self ):
#         while True:
#             exit_code = os.system('ping www.baidu.com')
#             if exit_code:
#                 print("----------没网，启动本地识别-------------------")
#             else:
#                 print("----------有网，启动网络识别-------------------")
#             self.my_signal.emit( exit_code )
#             self.sleep( 10 )



faceCascade = cv2.CascadeClassifier( path )
class Face_start( QDialog ):
    def __init__( self ):
        super().__init__()
        self.setWindowTitle( '人脸识别' )
        self.resize( 1000 ,500 )
        self.cameraLabel = QLabel( 'camera', self )
        self.cameraLabel.resize(480 ,320 )
        self.cameraLabel.setAlignment( Qt.AlignCenter )
        self.timer_camera = QTimer()


        
        self.cap = cv2.VideoCapture() #初始化摄像头
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read( trainer_path )
        #识别时间10秒；如果置信度大于60%，则识别成功并退出界面；否则至10秒后识别失败并退出
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        #初始化多线程，进行网络监听
        # self.my_thread = My_theard( )
        # self.my_thread.start()

        fl = open( user_path , 'r+')
        read_dict = eval( fl.read() )
        self.names = list( read_dict.keys( ) )
        fl.close()
        # tag = []
        # for i in range( len( names ) ) :
        #     tag.append( eval("False") )

        self.minW = 0.1 * self.cap.get(3)
        self.minH = 0.1 * self.cap.get(4)

        #网络识别一次的初始化标志位
        self.OnceBaiduAPI_flag = False

        self.layout_main = QVBoxLayout()
        self.layout_fun_button = QHBoxLayout()
        self.layout_data_show = QHBoxLayout()
        self.cameraButton = QPushButton(u'打开相机')

        # self.button_close.setMinimumHeight(50)

        self.layout_init()
        self.slot_init()

    def layout_init( self ):
        self.layout_data_show.addWidget( self.cameraLabel )
        self.layout_fun_button.addWidget( self.cameraButton )
        # self.layout_fun_button.addStretch(1)
        self.layout_main.addLayout( self.layout_data_show )
        self.layout_main.addLayout( self.layout_fun_button )

        self.setLayout( self.layout_main )


    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)
                #信号和槽连接
        # self.returnButton.clicked.connect(self.returnSignal)
        self.cameraButton.clicked.connect(self.slotCameraButton)
        # self.cameraButton.clicked.connect( self.recognize_face )
        # self.my_thread.my_signal.connect( self.get_Intnet_code )


    def get_Intnet_code( self , exitcode ):
        self.exit_code = exitcode

    #打开关闭摄像头控制
    def slotCameraButton(self):
        if self.timer_camera.isActive() == False:
                    #打开摄像头并显示图像信息
            self.openCamera()
        else:
        #关闭摄像头并清空显示信息
            self.closeCamera()

    def show_camera(self):

        if exit_code :#没网就用OpenCV
            
            self.recognize_face()
        else:   #有网的用百度api

            self.recognize_face_intnet()

        self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB ) #视频色彩转换回RGB，这样才是现实的颜色
        #pyqt显示逻辑
        showImage = QImage( self.image.data, self.image.shape[1] , self.image.shape[0], QImage.Format_RGB888 )
        self.cameraLabel.setPixmap(QPixmap.fromImage(showImage)) 

    #打开摄像头
    def openCamera(self):
        flag = self.cap.open( cap_id )
        if flag == False:
            msg = QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',\
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok)
        else:
            self.timer_camera.start(30)
            self.cameraButton.setText('关闭摄像头')

    def face_recongnition_start( self ):
        faces = faceCascade.detectMultiScale(         
        self.gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20) )
 
        for (x,y,w,h) in faces:
            cv2.rectangle(self.gray, (x, y), (x + w, y + w), (255,0,0),2 )
            roi_gray = self.gray [y:y+h, x:x+w]
            roi_color = self.image [y:y+h, x:x+w]  

    def recognize_face( self ):
        flag,self.image = self.cap.read()  #从视频流中读取
 
        self.image = cv2.resize(self.image,(480,320))     #把读到的帧的大小重新设置为 640x480

        result = "unknown"   #初始化识别失败
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int( self.minW), int( self.minH ) )
        )
        face_num= None  #初始化人脸序号

        for (x, y, w, h) in faces:
            cv2.rectangle( self.image , (x, y), (x + w, y + h), (0, 0 , 255), 2)
            id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 100 : #50%的识别置信度
                
                result= self.names[id]
                confidencestr = "{0}%".format(round(100 - confidence))
                # go_api( round(100 - confidence) , int( idnum  ) , tag  , names)

            else:
                confidencestr = "{0}%".format(round(100 - confidence))
            cv2.putText( self.image, result , (x + 5, y - 5), self.font, 1, (0, 0, 255), 2 )
            cv2.putText( self.image, confidencestr , (x + 5, y + h - 5), self.font, 1, (0, 0, 0), 1)
    
    #网络识别的工具函数
        #对图片的格式进行转换
    def transimage( self , image_name ):
        
        f = open( image_name ,'rb')
        img = base64.b64encode(f.read())
        return img

    def logging( self , name ):
        curren_time = time.asctime(time.localtime(time.time()))
        f = open('Log.txt','a+')
        f.write("Person: " + name + "     " + "Time:" + str(curren_time)+'\n')
        f.close()

    #上传到百度api进行人脸检测
    def go_api( self , image):
        result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP)
        if result['error_msg'] == 'SUCCESS':
            name = result['result']['user_list'][0]['user_id']
            score = result['result']['user_list'][0]['score']
            if score > 80:
                print("Welcome %s !" % name)
                self.logging( name )
                # recong_result=QMessageBox.information( self ,\
                #      "登录消息" , "识别成功，是否进入相应功能区" , QMessageBox.Ok |QMessageBox.Cancel )
                # if recong_result == QMessageBox.Ok :
                #     pass
                # else:
                #     self.close()
                #     self.closeCamera()
            else:
                print("Sorry...I don't know you !")
                name = 'Unknow'
            return name,score 

        if result['error_msg'] == 'pic not has face':
            print('There is no face in image!')
            return "NO FACE", None
        else:
            print(result['error_code']+' ' + result['error_code'])
            return "ERROR" , None
    
    
    def recognize_face_intnet( self ):
        font = cv2.FONT_HERSHEY_SIMPLEX  
        flag,self.image = self.cap.read()  #从视频流中读取
 
        self.image = cv2.resize(self.image, (480,320) )     #把读到的帧的大小重新设置为 480*320 
        gray = cv2.cvtColor( self.image , cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        if self.OnceBaiduAPI_flag == False :
            self.OnceBaiduAPI_flag = True 
            cv2.imwrite("youtemp.png", self.image )
            self.name , self.score = self.go_api( self.transimage(  image_name ) )  

            
        for (x,y,w,h) in faces:
            cv2.rectangle(self.image,(x,y),(x+w,y+h), (0, 0 , 255), 2)
            # roi_gray = gray[y:y+h, x:x+w]
            roi_color = self.image[y:y+h, x:x+w]  
            cv2.putText(self.image, self.name , (x+5,y-5), font, 1, (255,255,255), 2 )
            cv2.putText(self.image, str( self.score ), (x+5,y+h-5), font, 1, (255,255,0), 1 )  


    def closeCamera(self):
        self.timer_camera.stop()
        self.cap.release()
        self.OnceBaiduAPI_flag = False 
        self.cameraLabel.clear()
        self.cameraButton.setText('打开摄像头')

        # self.my_thread.terminate()
#这里作为功能启动区，代表着识别成功后就启动该功能
    def Function_run( self ):
        pass



#这个类主要是管理注册逻辑,这里为什么要用QDialog呢，当然也可以用Qwidget,这俩都是毛坯房，但是
#QDialog有exec方法，Qwidget是没有的。exec_()方法可以让窗口成为模态窗口，而调用show()方法，
#窗口是非模态的。模态窗口将程序控制权占据，只有对当前窗口关闭后才能操作其他窗口；
class Signin_Dialog( QDialog ):

    def __init__( self ):

        super().__init__() 
        #控件的初始化
        self.setWindowTitle('注册系统')
        self.resize(  300 , 250 )
        self.user_name_label = QLabel( "user_namer:" ,self )
        self.user_line_dialog = QLineEdit( self )
        self.passwd_label = QLabel( 'password:' , self )
        self.passwd_line_dialog = QLineEdit( self )
        self.passwd_re_label = QLabel( 're_password' , self )
        self.passwd_re_line = QLineEdit( self )
        self.sure_signin_botton = QPushButton( '确认' , self )
        self.cancel_button = QPushButton( '取消', self )

        #将布局类实例化
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
        self.grid_layout = QGridLayout()

        #将布局初始化
        self.__layput_init()

        #将确认按钮初始化
        self.sure_siginin_botton_init()

        self.line_init()

        self.sure_botton_init()

    def __layput_init( self ):
        self.grid_layout.addWidget( self.user_name_label , 0 , 0 )
        self.grid_layout.addWidget( self.user_line_dialog , 0 , 1 )
        self.grid_layout.addWidget( self.passwd_label , 1 , 0 )
        self.grid_layout.addWidget( self.passwd_line_dialog , 1 , 1 )
        self.grid_layout.addWidget( self.passwd_re_label , 2 , 0 )
        self.grid_layout.addWidget( self.passwd_re_line , 2 , 1 )

        self.h_layout.addWidget( self.sure_signin_botton )
        self.h_layout.addWidget( self.cancel_button )
        self.v_layout.addLayout( self.grid_layout )
        self.v_layout.addLayout( self.h_layout )
        self.setLayout( self.v_layout  )

    def line_init( self ):
        self.user_line_dialog.setPlaceholderText( "请输入你的用户账号" )
        self.passwd_line_dialog.setPlaceholderText( "请输入你的密码")
        self.passwd_re_line.setPlaceholderText( '请再次输入你的密码' )
        self.passwd_line_dialog.setEchoMode( QLineEdit.Password )
        self.passwd_re_line.setEchoMode( QLineEdit.Password )

        self.user_line_dialog.textChanged.connect( self.check_input )
        self.passwd_line_dialog.textChanged.connect( self.check_input )
        self.passwd_re_line.textChanged.connect( self.check_input )

    def check_input( self ):
        if self.user_line_dialog.text() and self.passwd_line_dialog.text() and self.passwd_re_line.text():
            self.sure_signin_botton.setEnabled( True )
        else:
            self.sure_signin_botton.setEnabled( False )

    def sure_siginin_botton_init( self ):
        self.sure_signin_botton.setEnabled( False )

    #确认按钮与数据库的关联初始化
    def sure_botton_init( self ):
        self.sure_signin_botton.clicked.connect( self.check_data )
        
    # def clearText( text_path ):
    #     with open(text_path, 'w') as f1:
    #         f1.seek(0)
    #         f1.truncate()
    #         # print("清空数据")
    #如果按钮按下
    def check_data( self ):
        #--------判断用户是否存在--------------
        f_all = open( user_path , 'r+')
        read_dict = eval( f_all.read() )
        f_all.close()
        
        if self.passwd_line_dialog.text( ) != self.passwd_re_line.text( ) :
            QMessageBox.critical( self , '注册消息' ,'两次密码输入不一致' , QMessageBox.Ok | QMessageBox.Cancel )
        
        elif self.user_line_dialog.text()  not in read_dict :
            read_dict[self.user_line_dialog.text()] = self.passwd_line_dialog.text()
            # self.clearText( user_path )
            
            with open(user_path, 'w') as f1:
                f1.write( str( read_dict ) )

            QMessageBox.information( self , '注册消息' , '注册成功' , QMessageBox.Ok )
            self.close()
        else:
            QMessageBox.critical( self , '注册消息', '注册失败，操作有误' , QMessageBox.Ok )
     
        
        self.user_line_dialog.clear()
        self.passwd_line_dialog.clear()
        self.passwd_re_line.clear()










class CollectPicture_Page( QDialog ):
    mysignal = pyqtSignal( )

    def __init__( self ):
        super().__init__()
        self.setWindowTitle('人脸数据集收集和训练')
        self.resize( 1000 ,500 )

        self.IsHome_button = QRadioButton( "本地收集" , self)
        self.IsInternet_button = QRadioButton( "网络收集" ,self )
        self.collect_start_button = QPushButton("开始收集", self )
        self.train_run_button = QPushButton( "开始训练" ,self )
        self.return_button = QPushButton( "取消" , self )
        self.cameraLabel = QLabel( 'camera' ,self )
        self.cameraLabel.resize( 480,320 )
        self.cameraLabel.setAlignment( Qt.AlignCenter )

        self.h_col_style_layout = QHBoxLayout()
        self.v_col_styly_layout = QVBoxLayout()
        self.h_col_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        
        self.cap = cv2.VideoCapture( )
        self.collect_time = QTimer()

        self.layout_init()
        self.button_init()
        self.slot_init()


    def layout_init( self ):
        self.h_col_style_layout.addWidget( self.IsHome_button )
        self.h_col_style_layout.addWidget( self.IsInternet_button )
        self.h_col_style_layout.addStretch(1)
        
        self.h_col_layout.addWidget( self.collect_start_button )
        self.h_col_layout.addWidget( self.train_run_button )
        self.h_col_layout.addWidget( self.return_button )

        self.v_layout.addWidget( self.cameraLabel )
        self.v_layout.addLayout( self.h_col_style_layout )
        self.v_layout.addLayout( self.h_col_layout )

        self.setLayout( self.v_layout )

    def button_init( self ):
        self.return_button.clicked.connect( self.cancel_task )
        self.collect_start_button.clicked.connect( self.openCamera )
        self.train_run_button.clicked.connect( self.Training_faces )

        self.IsHome_button.setChecked( True )

    def slot_init( self ):
        self.collect_time.timeout.connect( self.show_camera )
        self.mysignal.connect( self.collect_signal_run )
    
    def camera_init( self ):

        self.unregisterFlag = False 
        
        self.face_detector = cv2.CascadeClassifier(  path )
        self.count = 0
        fl = open( user_path , 'r+')
        real_dict = eval( fl.read() )
        names = list( real_dict.keys() )
        fl.close()
        self.collect_name , ok =  QInputDialog.getText( self , '请输入你的名字' ,'必须是已经注册的名字!' )

        if self.collect_name in names:
            self.face_id = names.index( self.collect_name ) + 1
                    #face_id = input('\n enter user id:')  #输入序号，表示某人的一些列照片
            print('\n Initializing face capture. Look at the camera and wait ...')
            
        else:
            QMessageBox.warning( self ,'异常状态' , '请去注册' , QMessageBox.Ok )

            self.unregisterFlag = True



    def cancel_task( self ):
        self.collect_time.stop()
        self.cap.release()
        self.cameraLabel.clear()
        self.close() 

        #打开摄像头
    def openCamera(self):
        flag = self.cap.open( cap_id )
        self.camera_init()

        if flag == False:
            msg = QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',\
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok)
        elif self.unregisterFlag == True:
            pass
        else:
            self.Intnet_flag = False
            self.collect_time.start(30)

    def show_camera(self):
        # self.face_recongnition_start()
        sucess, self.img = self.cap.read()
        self.collect_result = None
        if self.IsHome_button.isChecked():
            if self.count < 30 :
                self.Collect_faces()
            else:
                self.collect_time.stop()
                self.mysignal.emit()
        else:
            if self.Intnet_flag == False :
                cv2.imwrite( image_name , self.img )
                self.baidu_addUser()
                self.collect_result = QMessageBox.information( self , '注册消息','注册完毕', QMessageBox.Ok )
        
        if self.collect_result == QMessageBox.Ok:
            self.closeCamera()
            self.collect_result = None

        self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB ) #视频色彩转换回RGB，这样才是现实的颜色
        #pyqt显示逻辑
        showImage = QImage( self.img.data, self.img.shape[1] , self.img.shape[0], QImage.Format_RGB888 )
        self.cameraLabel.setPixmap( QPixmap.fromImage(showImage) ) 


    def Collect_faces( self ):
        # 转为灰度图片

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # 检测人脸

        faces = self.face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(self.img, (x, y), (x + w, y + w), (255, 0, 0) , 2 )
            self.count += 1

            # 保存图像,从原始照片中截取人脸尺寸
            cv2.imwrite("Facedata/User." +str(self.face_id) + '.' + str(self.count) + '.jpg', gray[y: y + h, x: x + w])

            

    def Training_faces( self ):
    # 人脸数据路径
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(path )

        def getImagesAndLabels( data_path ):
            imagePaths = [os.path.join( data_path , f) for f in os.listdir( data_path )]  # join函数的作用？
            faceSamples = []
            ids = []
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
                img_numpy = np.array(PIL_img, 'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x: x + w])
                    ids.append(id)
            return faceSamples, ids

        print('Training faces. It will take a few seconds. Wait ...')
        faces, ids = getImagesAndLabels( data_path )
        recognizer.train(faces, np.array(ids))

        recognizer.write( trainer_path )
        print("{0} faces trained. Exiting Program".format(len(np.unique(ids))))
        QMessageBox.information( self , "训练消息","训练完毕" , QMessageBox.Ok )


    def collect_signal_run( self ):
        self.collect_result = QMessageBox.information( self , '训练' , '收集完成' , QMessageBox.Ok )

        #对图片的格式进行转换
    def transimage( self , image_name ):
        
        f = open( image_name ,'rb')
        img = base64.b64encode(f.read())
        return img

    def baidu_addUser( self ):
        client.addUser( str( self.transimage(image_name) , 'utf-8') , IMAGE_TYPE, GROUP , self.collect_name )
        self.Intnet_flag = True

    def closeCamera(self):
        self.collect_time.stop()
        self.cap.release()
        self.cameraLabel.clear()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())