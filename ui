import subprocess
import sys
import os
import ipywidgets as widgets
from IPython.display import display


class ClashLinux:
    def __init__(self):
        self.explanation_text_a = widgets.HTML(
            value="<p style='color: orange;'>提示：批量转换文件，自动保存到同目录下的 __pycache__ 文件夹中</p>"
        )
        
        # 分割线
        self.explanation_line = widgets.HTML(value="<hr style='height: 1px; background-color: #616161; border: none;' />")
        
        self.subscribe_input = widgets.Textarea(
            placeholder='输入你的clash订阅地址', description='订阅地址:',
            layout=widgets.Layout(width='600px')
        )
        
        self.password_input = widgets.Text(
            placeholder='输入密码，不填写则随机生成', description='密码:',
            layout=widgets.Layout(width='600px')
        )
        
        self.confi_button = widgets.Button(description="激活并开启", button_style='info')
        self.confi_button.on_click(self.confi_clash)
        
        self.closure_button = widgets.Button(description="全局取消", button_style='danger')
        self.closure_button.on_click(self.closure_clash)
        
        self.tem_open_button = widgets.Button(description="临时开启", button_style='success')
        self.tem_open_button.on_click(self.tem_open)
        
        self.tem_closed_button = widgets.Button(description="临时关闭", button_style='warning')
        self.tem_closed_button.on_click(self.tem_closed)
        
        self.button_box = widgets.HBox([self.confi_button, self.closure_button], layout=widgets.Layout(height='35px'))
        
        
        self.tem_button_box = widgets.HBox([self.tem_open_button, self.tem_closed_button])

        self.output = widgets.Output()
        self.tem_output = widgets.Output()

        self.interface = widgets.VBox([
            self.explanation_text_a,
            self.subscribe_input,
            self.password_input,
            self.button_box,
            self.tem_button_box,
            self.output,
            self.explanation_line,
            self.tem_output
        ])
        # 创建折叠按钮
        self.accordion = widgets.Accordion(children=[self.interface])
        self.accordion.set_title(0, '启用 Clash')
        
        self.closure_button.layout.display = 'none'
        self.tem_button_box.layout.display = 'none'

    def confi_clash(self, button):
        self.output.clear_output()  # 清空输出信息
        params = self.subscribe_input.value.strip()
        keys =  self.password_input.value.strip()
        
        script_content = f"""
# Clash 订阅地址
export CLASH_URL='{params}'
export CLASH_SECRET='{keys}'
        """
        script_content = script_content.strip()
        
        start_command_a = "bash start.sh && bash -c \"source /etc/profile.d/clash.sh && proxy_on\""
        
        if not params:
            print("请填写订阅地址！")
        else:
            with open(".env", "w") as f:
                f.write(script_content)

            with self.output:
                print("已写入配置信息") 
                # 执行start_command_a
                process_a = subprocess.Popen(start_command_a, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
                for line in iter(process_a.stdout.readline, ''):
                    line = line.strip()
                    if "已开启代理" in line:
                        print(line)
                        self.tem_open_button.click()
                        self.closure_button.layout.display = ''
                        self.tem_button_box.layout.display = ''
                        print("\n请打开网址：http://127.0.0.1:9090/ui")
                    else:
                        print(line)
                process_a.wait()  # 等待process_b完成
            

    def closure_clash(self, button):
        self.output.clear_output()  # 清空输出信息
        self.tem_output.clear_output()  # 清空输出信息
        with self.output:
            # 启用代理
            # proxy_on_command = "bash start.sh && bash -c \"source /etc/profile.d/clash.sh && bash shutdown.sh && proxy_off\""
            proxy_on_command = "bash shutdown.sh && bash -c \"source /etc/profile.d/clash.sh && proxy_off\""
            process_proxy_on = subprocess.Popen(proxy_on_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

            for line in iter(process_proxy_on.stdout.readline, ''):
                line = line.strip()
                if "服务关闭成功" in line:
                    print(line)
                    if "http_proxy" in os.environ:
                        del os.environ["http_proxy"]
                    if "https_proxy" in os.environ:
                        del os.environ["https_proxy"]
                    self.tem_button_box.layout.display = 'none'
                else:  # 如果已经找到了目标字符串
                    print(line)

            process_proxy_on.wait()  # 等待process_proxy_on完成
            
    def tem_open(self, button):
        self.tem_output.clear_output()  # 清空输出信息
        with self.tem_output:
            os.environ["http_proxy"] = "http://127.0.0.1:7890"
            os.environ["https_proxy"] = "http://127.0.0.1:7890"
            print("HTTP Proxy:", os.environ.get("http_proxy"))
            print("HTTPS Proxy:", os.environ.get("https_proxy"))
            print("已打开代理")
            # print("\n请打开网址：http://127.0.0.1:9090/ui")
            
    def tem_closed(self, button):
        self.tem_output.clear_output()  # 清空输出信息
        with self.tem_output:
            if "http_proxy" in os.environ:
                del os.environ["http_proxy"]
            if "https_proxy" in os.environ:
                del os.environ["https_proxy"]
            print("HTTP Proxy:", os.environ.get("http_proxy"))
            print("HTTPS Proxy:", os.environ.get("https_proxy"))
            print("已临时关闭代理")


clash_linux = ClashLinux()
display(clash_linux.accordion)
