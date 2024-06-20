from PyAibote import AndroidBotMain
import time

# 2. 自定义一个脚本类，继承 AndroidBotMain
class CustomAndroidScript(AndroidBotMain):
    #初始化配置
    Log_Level = "DEBUG"
    Log_Storage = True
    def start_xuexitong(self):
        #打开学习通，进入看课区域
        result = self.start_app("学习通", 5, 0.5)
        print("app运行状态:{}".format(result))
        place=self.get_element_rect("com.chaoxing.mobile/com.chaoxing.mobile:id=tabButton[3]", 15, 0.5)
        self.click((place))
        print("点击任务状态:{}".format(place))
        place=self.get_element_rect("com.chaoxing.mobile/com.chaoxing.mobile:id=myCourse", 15, 0.5)
        self.click((place))
        print("点击任务状态:{}".format(place))

    def select_class(self):
        #选择目标课程，并且判断是否有课程
        self.my_class=input("输入想要刷课的名称:")
        result = self.init_ocr_server("127.0.0.1", False, False, False)
        print("初始化状态:{}".format(result))
        result = self.get_text()
        print(result)
        if self.my_class in result:
            print("发现目标课程")
            result = self.find_text(self.my_class)
            print(result)
            self.click(result)
            time.sleep(1)
            result = self.click_element("com.chaoxing.mobile/android.widget.TextView@text=章节", 5, 0.5)
            print(result)

    def look_class(self):
        #观看课程
        self.current_class=float(input("(示例:2.3)\n输入你当前刷课进度：")) #当前的课程
        self.show_first_class() #自定义的滑动函数(防止开始刷课的节数不在屏幕中)
        while True: #循环执行
            self.cut_class() #自定义切换方法，用来判断当前应该看哪节课，并点进去
            print("start look class")
            time.sleep(2) #防止未加载出页面就文字识别导致错误
            result = self.find_text("视频")#识别文字
            print(result)
            if len(result)==0:
                time.sleep(3)
                self.ago_now()  # 自定义函数，判断这节课是否刷完
            else:
                self.click(result)  # 点击视频进去视频页面
                time.sleep(3)
                self.ago_now()  # 自定义函数，判断这节课是否刷完


    def ago_now(self):
        #判断课程是否看过
        result=self.find_text("任务点已完成")
        if result==():
            result = self.get_element_rect("com.chaoxing.mobile/android.widget.Button@text=播放", 5, 0.5)
            self.click(result)
            time.sleep(3)
            #判断是否看完
            i=1
            while i==1:
                time.sleep(5)
                outline=self.element_exists("com.chaoxing.mobile/android.widget.Button@text=重试", 1, 0.5)
                if outline: #判断是否断网
                    self.click_element("com.chaoxing.mobile/android.widget.Button@text=重试", 1, 0.5)
                result = self.element_exists("com.chaoxing.mobile/com.chaoxing.mobile:id=start", 1, 0.5)
                if result: #判断是否看完
                    self.back()
                    time.sleep(2)
                    result=self.find_text("任务点已完成")
                    if result!=():
                        break
                    else:
                        self.click_element("com.chaoxing.mobile/android.widget.Button@text=播放", 1, 0.5)
        self.back()

    def cut_class(self):
        #看完课程更替视频
        self.infor_dispose() #解决计算机浮点计算偏差问题
        while True:
            #匹配课程
            print(self.current_class)
            result = self.element_exists("com.chaoxing.mobile/android.widget.TextView@text={}".format(self.current_class), 5, 0.5)
            print("当前课程的状态:{}".format(result))
            if result==True: #如果存在课程,就点击进入课程
                result=self.click_element("com.chaoxing.mobile/android.widget.TextView@text={}".format(self.current_class), 5, 0.5)
                self.current_class += 0.1  # 转换到下一门课
                break
            else: #如果不存在，下滑一下屏幕再匹配。
                print("屏幕未找到对应元素，正在执行下滑操作")
                self.swipe((306, 1116), (306, 750), 1)
                result = self.element_exists(
                    "com.chaoxing.mobile/android.widget.TextView@text={:.1f}".format(self.current_class), 5, 0.5)
                print("下滑后匹配元素状态:{}".format(result))
                if result: #如果匹配到了进入
                    self.click_element(
                        "com.chaoxing.mobile/android.widget.TextView@text={:.1f}".format(self.current_class), 5, 0.5)
                    self.current_class += 0.1  # 转换到下一门课
                    break
                else: #匹配不到可能是转换章节
                    self.current_class+=1
                    self.current_class-=(self.current_class%1)
                    self.current_class+=0.1
                    result = self.element_exists(
                        "com.chaoxing.mobile/android.widget.TextView@text={}".format(self.current_class), 5, 0.5)
                    if result: #转换章节后匹配到
                        self.click_element(
                            "com.chaoxing.mobile/android.widget.TextView@text={}".format(self.current_class), 5,
                            0.5)
                        self.current_class += 0.1  # 转换到下一门课
                        break
                    else: #匹配不到的话
                        print("该课程已经刷完，或者程序出错。")
                        break

    def show_first_class(self):
        #防止第一个课程不在屏幕内
        result = self.element_exists(
            "com.chaoxing.mobile/android.widget.TextView@text={}".format(self.current_class), 5, 0.5)
        if result: #判断屏幕中是否有这个课程的元素
            print("初始化目标课程在屏幕内")
        else: #如果没有
            for i in range(15): #下拉寻找
                self.swipe((402, 1404), (402, 564), 2)
                result = self.element_exists(
                    "com.chaoxing.mobile/android.widget.TextView@text={}".format(self.current_class), 3, 0.5)
                if result: #如果该目标进入了屏幕就退出循环
                    break

    def infor_dispose(self):
        #解决python浮点不精准问题
        self.current_class=round(self.current_class,2)
        self.current_class_1=self.current_class%0.1
        if self.current_class_1==0:
            self.current_class=round(self.current_class,1)

    def script_main(self):
        #执行函数
        self.start_xuexitong()
        self.select_class()
        self.look_class()


if __name__ == '__main__':
    CustomAndroidScript.execute("0.0.0.0", 16678)