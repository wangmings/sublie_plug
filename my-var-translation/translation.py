
# -*- coding: utf-8 -*-
import os  
import re
import sys
import sublime
import sublime_plugin
from subprocess import Popen, PIPE, STDOUT


# 插件开发调试
# 终端执行: view.run_command('mmsx')
def printf(bug):
    print('\n\n## ------------ << print-bugs >> ------------- ##\n')
    print(bug)








# 执行shell并输出
def exe_command(command):
    shell_data = ''
    process = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            shell_data += line.decode()
    
    exitcode = process.wait()
    return shell_data






# 编辑器里面的字符串处理
class replacestringCommand(sublime_plugin.TextCommand):
    def run(self, edit, string):
        for char in self.view.sel():
            self.view.replace(edit, char, string)








# 显示提示弹窗
def display_popup_window(view,string):
   
    data = ""
    path = sublime.packages_path() + '/my-var-translation/'
    path = path.replace(' ','\\ ')  

    translate = path + 'v3/translate'
    enginePath = path + 'engine.sublime-settings'

    index = exe_command('cat '+ enginePath).strip()
    indexStr = index
    index = int(index)


    title = {
        'baidu':"百度翻译",
        'google':"谷歌翻译",
        'bing':"必应翻译"
    }



    engine = []
    for name in title:
        engine.append(name)


    args = ' %s "%s"' %(engine[index], string)
    var_string = exe_command(translate + args).replace('\n','')

    



    var_name = '''
        camelCase:getData:驼峰(小)
        pascalCase:GetData:驼峰(大)
        noCase:get data:分词(小)
        capitalCase:Get Data:分词(大)
        paramCase:get-data:中划(小)
        headerCase:Get-Data:中划(大)
        snakeCase:get_data:下划(线)
        dotCase:get.data:对象(小)
        pathCase:get/data:路径(小)
        constantCase:GET_DATA:常量(大)
    '''




    def format(string, size, char='_'):
        occupyChar = ''
        length = len(string)
        if length < size:
            for i in range(0,(size - length)):
                occupyChar += char;
            string = '%s<i> %s </i>' %(string,occupyChar)
        return string



    var_name_str = ''
    for str in var_name.strip().split('\n'):
        str = str.split(':')
        var_name_str += str[0].strip() + '\n'
        html_str = format(str[1].strip(),10) + str[2].strip()
        data += '\n<p><a href="%s"> %s </a></p>' % (str[0].strip(), html_str) 
         

    

    html = """
        <body id=show-scope>
            <style> 
                h1 { 
                    text-align:center;
                    font-size: 1.1rem; 
                    margin: 0 0 0.5em 0; 
                    font-family: system;
                }



                h1 a {
                    text-decoration:none;
                    color:#e91e63;
                }

                
                
                h3{
                    text-align:center;
                    font-size: 1.0rem; 
                    font-family: system;
                    color:#00bcd4;
                    
                }

                h3 i {
                    color:#ededed;
                }
             
                div.popup {
                    padding: 10px;
                   
                }

                div.popup a {
                    text-decoration:none;
                    color:#009688;
                    border:2px solid #a1a1a1;
                    border-radius:8px;
                }

                div.popup a i {
                    color:#ededed;
                }

            </style>

           
            <h1><a href="%s">%s</a></h1>
            <h3> 示例 <i>************</i> 变量命名 </h3>
            <div class="popup" >%s</div>
            
           
          
        </body>
    """ % (index, title[engine[index]], data)


    # color:#ededed;
    # border:2px solid #a1a1a1;
    # border:2px solid #a1a1a1;
    # border-radius:8px;
    



    # 监听提示弹窗事件
    def popup_event(href):
        
        if re.search(href, var_name_str):
            args = ' change "%s" %s' %(var_string, href)
            varString = exe_command(translate + args).replace('\n','')
            view.run_command('replacestring',{'string':varString})
        
        else:
            index = int(href) + 1
            if index > 2: index = 0
            shell = 'echo "%s" > %s' %(index, enginePath)
            exe_command(shell)
        
        # 隐藏提示弹窗
        view.hide_popup()


    view.show_popup(html, max_width=512, max_height=400, on_navigate=popup_event)






# 朗读鼠标选中 的单词 
class translateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        getString = self.get_mouse_selected_string()
        if getString:
            if self.is_chinese(getString):
                # 显示提示弹窗
                display_popup_window(self.view, getString)
            else:
                sublime.message_dialog('选中的字符串中没有包含中文字符!')
            
        
    
    # 检查整个字符串是否包含中文
    def is_chinese(self,string):
        boole = False
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                boole = True
        return boole

   
    # 判断字符串否是空
    def if_string_null(self, string):
        length = 0; boole=False
        for char in string:
            if char == ' ': length += 1
        if length != len(string): boole = True
        return boole



    # 获取鼠标选中的字符串
    def get_mouse_selected_string(self):
        getString = False
        for char in self.view.sel():
            # 获取鼠标选中的字符串
            getString = self.view.substr(char)       
            
            if self.if_string_null(getString):
                # 去掉前后空白符
                getString = getString.strip()
            else:
                sublime.message_dialog('鼠标没有选中字符串')
        
        return getString





















