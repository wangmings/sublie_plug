# -*- coding: utf-8 -*-
import os,sys,re,time
import sublime
import sublime_plugin
from subprocess import Popen, PIPE
import codecs



# 打印输出结果
class sublimeprintCommand(sublime_plugin.TextCommand):
    def run(self, edit, prints):
        os.popen('say 输出')
        html = """
            <body id=show-scope>
                <style> h1 { font-size: 1.1rem; font-weight: 500; margin: 0 0 0.5em 0; font-family: system; } </style>
                <h1>Sublime__Print</h1> %s
            </body>
        """ % (prints)
        self.view.show_popup(html,max_width=512, max_height=512, on_navigate=lambda x: 0)





# 打印输出结果:必须在sublime_plugin.TextCommand对象下调用
def prints(self,_print):
    if isinstance(_print,str):
        self.view.run_command("sublimeprint",{"prints":_print})
    else:
        os.popen('say 不是字符串类型')





# 创建获取当前文件父路径类
class Path:
    def __new__(self, FileName=''):
        path = os.path.split(os.path.abspath(__file__))[0]
        if FileName != '': 
            path += '/' + FileName.replace(' ','').replace('./','')  
        return path
    
    # 获取Python包路径
    def bagPath(self):
        pprint(sys.path)    






# 实时预览Markdown文件
# /Applications/Typora.app/Contents/MacOS/Typora
class markdownCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        thisFile = self.view.file_name()
        types=thisFile.split('.')
        types=types[len(types)-1]
        # prints(self,str(types))
        
        if types == 'md':
            app = '''
                osascript -e "
                    tell application \\"Typora\\"
                        activate
                        close every window
                        open \\"%s\\"
                    end tell
                "
            ''' % (thisFile)
            # prints(self,app)
            # os.popen(app)
            os.system(app)



# Markdown文件导出成HTML文件
class mdhtmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("markdown")
        thisFile = self.view.file_name()
        types=thisFile.split('.')
        types=types[len(types)-1]
 
        if types == 'md':
            apps = Path()+'/menu.scpt'
            apps = 'osascript "'+apps+'"' 
            # prints(self,apps)
            # 同步
            os.system(apps)
            # 异步
            # os.popen(apps) 
           




# 在游览器打开当前文件
class htmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # 获取文件路径
        getFilePath = self.view.file_name()
        openHtml = ''' open -a "Google Chrome" "file://'''+getFilePath+ '''" '''
        os.popen(openHtml)
        # self.view.insert(edit, 0, getFilePath )




# 创建输出执行shell:获取参数
class bashCommand(sublime_plugin.TextCommand):
    def run(self, edit, path='file path null'):
        path = 'im ' + path.replace(' ','\\ ')
         
        
        self.view.insert(edit, 0, self.Shell(edit,path) ) 

    def Shell(self,edit,cmd):
 
        cmd = Popen(cmd, 
            stdin=PIPE, 
            stderr=PIPE,
            stdout=PIPE,
            env={"LANG": "en_US.UTF-8"},
            universal_newlines=True, 
            shell=True, 
            bufsize=0) 

        decoder = codecs.getincrementaldecoder('utf-8')('replace')

        
        while True:
            # lists = decoder.decode(cmd.stdout.read(2**16))
            line = cmd.stdout.readline()
             
            print(line, end='')
            if Popen.poll(cmd) == 0:  # 判断子进程是否结束
                break


        return cmd.returncode
     
  

  



# 创建显示输出的控制台
class consoleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file = self.view.file_name()
        
        self.panel = self.view.window().create_output_panel('bash_output')
        self.panel.settings().set("line_numbers", False)
        self.panel.settings().set("gutter", False)
        self.panel.settings().set("scroll_past_end", False)
        self.view.window().run_command('show_panel', { 'panel': 'output.bash_output' })

        self.panel.run_command('bash',{'path':file}) 

        # sublime text 打开行号和关闭行号命令
        # self.view.run_command('toggle_setting',{ "setting": "line_numbers" })




 



# 打开视图终端 
class openviveCommand(sublime_plugin.WindowCommand):
    def run(self, reverse=False): 
        window = self.window
        window.run_command('terminus_close_all')
        window.run_command('terminus_open',{"cwd": "${file_path:${folder}}"})   


# 打开面板终端
class openpanleCommand(sublime_plugin.WindowCommand):
    def run(self, reverse=False): 
        window = self.window
        window.run_command('terminus_close_all')
        window.run_command('terminus_open',{"cwd": "${file_path:${folder}}","panel_name": "Terminus"})
        


# 设置终端主题
class setthemeCommand(sublime_plugin.WindowCommand):
    def run(self,reverse=False):
        window = self.window
        window.run_command('terminus_close_all')
        window.run_command('terminus_open',{"panel_name": "Terminus","auto_close":True})
        def loop():
            window.run_command('terminus_select_theme')   
        
        # 500毫秒后启动线程执行 
        sublime.set_timeout_async(loop,500)





# 代码格式化
class codeformattingCommand(sublime_plugin.TextCommand):   
    def run(self, edit):
        self.view.run_command("select_all") #选中全部
        # self.view.run_command("reindent")
        self.view.run_command("htmlprettify")
        self.view.run_command("expand_tabs")
        
    






# 多个光标编辑数字叠加：super+shfit+l
class numberCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selection = view.sel()
        for i in range(0,len(selection)):
            view.insert(edit,selection[i].begin(),str(i))






# class msxxxCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         apps = self.window.project_file_name()
#         prints(self,apps)                        
        
















