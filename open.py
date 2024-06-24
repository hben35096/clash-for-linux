import os
import ipywidgets as widgets
import time
import requests
from IPython.display import display

class OpenAndClosed:
    def __init__(self):

        self.tem_open_button = widgets.Button(description="开启当前页面代理", button_style='success', layout=widgets.Layout(width='180px'))
        self.tem_open_button.on_click(self.tem_open)
        
        self.tem_closed_button = widgets.Button(description="临时关闭当前页面代理", button_style='warning', layout=widgets.Layout(width='180px'))
        self.tem_closed_button.on_click(self.tem_closed)
        
        # 创建输出框
        self.tem_output = widgets.Output()
        # 将按钮水平排列
        self.buttons_box = widgets.HBox([self.tem_open_button, self.tem_closed_button])
        
        # 将按钮和输出框放入垂直箱子中
        self.interface_box = widgets.HBox([self.buttons_box, self.tem_output])
        
    def tem_open(self, button):
        self.tem_output.clear_output()  # 清空输出信息
        with self.tem_output:
            os.environ["http_proxy"] = "http://127.0.0.1:7890"
            os.environ["https_proxy"] = "http://127.0.0.1:7890"
            # print("HTTP Proxy:", os.environ.get("http_proxy"))
            # print("HTTPS Proxy:", os.environ.get("https_proxy"))
            print("✔已启用魔法代理")
            # print("\n请打开网址：http://127.0.0.1:9090/ui")
            
    def tem_closed(self, button):
        self.tem_output.clear_output()  # 清空输出信息
        with self.tem_output:
            if "http_proxy" in os.environ:
                del os.environ["http_proxy"]
            if "https_proxy" in os.environ:
                del os.environ["https_proxy"]
            # print("HTTP Proxy:", os.environ.get("http_proxy"))
            # print("HTTPS Proxy:", os.environ.get("https_proxy"))
            print("✘已关闭魔法代理")
            
# 测网速
class NetSpeedTest:
    def __init__(self):
        self.explanation_text = widgets.HTML(
            value="<p style='color: orange;'>注意这是在开启全局代理之后才有效的，而“临时开启”和“临时关闭”按钮，只作用于当前页面</p>"
        )
        # 创建按钮
        self.net_speed_button = widgets.Button(description='检测网速', button_style='success')
        self.net_speed_button.on_click(self.test_speed)  # 将按钮与测试网速函数关联
        
        # 创建输出框
        self.output = widgets.Output()
        
        # 创建网站选择控件
        self.websites = widgets.Dropdown(
            options=['https://github.com', 'https://huggingface.co', 'https://civitai.com'],
            description='测试网站:', layout=widgets.Layout(width='446px')
        )
        
        self.button_box = widgets.HBox([self.websites, self.net_speed_button])
        # 将按钮、网站选择控件和输出框放入垂直箱子中
        self.interface_box = widgets.VBox([self.explanation_text, self.button_box, self.output])
        # 创建折叠按钮
        self.accordion = widgets.Accordion(children=[self.interface_box]) # 非折叠状态
        self.accordion.set_title(0, '测网速')  # 设置折叠按钮的标题
    
    def test_speed(self, b):
        with self.output:
            self.output.clear_output()  # 清空输出框内容
            
            print("\n开始测速，总过程不会超出12秒，请等待测试结束后再进行其他操作，或点击“中断内核”结束当前操作")
            url = self.websites.value  # 获取用户选择的网站
            try:
                start_time = time.time()
                response = requests.get(url, timeout=12)  # 设置超时时间为 30 秒
                end_time = time.time()
                if response.status_code == 200:
                    elapsed_time = end_time - start_time
                    speed = len(response.content) / elapsed_time / 1024 / 1024  # 将速度转换为 Mbps
                    print(f"连接到 {url} 的速度: {speed:.2f} Mb/s")
                else:
                    print(f"无法连接到 {url}，状态码: {response.status_code}")
            except KeyboardInterrupt:
                print("\n用户中断了进程")
            except requests.Timeout:
                print(f"连接 {url} 超时")
            except Exception as e:
                print(f"连接 {url} 时发生错误: {e}")
            
            print("\n网速测试已结束！")

# 创建实例
open_and_closed = OpenAndClosed()
net_speed_test = NetSpeedTest()

# 显示折叠按钮和操作界面
display(open_and_closed.interface_box)
display(net_speed_test.accordion)