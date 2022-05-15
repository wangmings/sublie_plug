# -*- coding: utf-8 -*-
import sys
sys.path.append("/Users/mac/Library/Application Support/Sublime Text 3/Packages/demo/packages")
import sublime
import sublime_plugin
import os   #导入系统模块
import re   #导入正则表达式模块
import time 
import requests 
from bs4 import BeautifulSoup


# 包路径
def packPaths(t='obj'):

    paths = sublime.packages_path()
    # paths = paths.replace(' ','\\ ')
    if t == 'packages':
        return paths
    else:
        return paths + '/demo'




# 爬虫翻译
def translation(args,option):
    
    # 存储翻译数据
    storage = packPaths() +'/translation/storage_translation_data'

    # 接收传入的参数
    args = args.strip()  # 去掉前后空白符

    # 处理接收到的参数
    def str_processing(argv):
        _str = argv.replace('.', ' ').replace('_', ' ').replace('-', ' ')
        num = 0
        string = ''
        for s in _str:
            num += 1
            if s.isupper():
                if num == 1:
                    string = s
                else:
                    string += ' ' + s
            else:
                string += s

        return string.replace('  ', ' ')

    f_text = str_processing(args)


    # 判断是否连接网络
    def server():
        try:
            html = requests.get("http://www.baidu.com", timeout=2)
        except:
            return False
        return True






    # 在线翻译
    def run_translation():
        data = {
            'inputtext': f_text,
            'type': 'AUTO'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
            'Origin': 'http://m.youdao.com',  # 请求头最初是从youdao发起的，Origin只用于post请求
            'Referer': 'http://m.youdao.com/translate',  # Referer则用于所有类型的请求
        }

        # 接口
        post = 'http://m.youdao.com/translate'

        if server():

            # 发送请求
            r = requests.post(post, headers=headers, data=data)
            content = r.content

            # 判断是否响应数据成功
            if r.status_code == requests.codes.ok:
                soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
                getText = soup.find(id="translateResult").li.get_text()
                # print(getText)

                if option == 'pass':  
                    return getText
                else:
                    getText = getText.replace('\n',',')
                    double = "{'double':'"+args.replace('\n',',').replace('  ','')+"','translation':'"+getText+"'}"

                    with open(storage, 'a+',encoding='utf-8') as f:
                        f.write(double + '\n')     
                    return eval(double)

            else:
                # '请检查网络是否正常!'
                return 404
        else:
            return 404




    if option == 'pass':
        return run_translation()

    else:

        # 读取本地翻译
        Num = 0
        path = os.path.exists(storage)
        if path:
            args = args.replace('\n',',').replace('  ','')
            for line in open(storage, 'r', encoding='utf-8'):
                double = eval(line)['double']
                if double == args:
                    Num = 1
                    return eval(line)
                    break

            if Num != 1:
                return run_translation()
        else:
            return run_translation()




# 在终端打开当前文件路径<弃用>
class demoCommand(sublime_plugin.TextCommand):
    
    def run(self, edit):
        
        # 获取文件路径
        getFilePath = self.view.file_name()
        
        # 使用正则表达式处理文件路径：替换字符
        newFilePath = re.sub(r'\ ', "\\ ", getFilePath)

        # 反向查找切割字符串：获取数组第一个路径
        openFile = newFilePath.rsplit('/', maxsplit=1 )[0]

        # 使用shell命令启动终端并且切换到当前文件路径下
        os.system('open -a /Applications/Utilities/Terminal.app ' + openFile)



# 在终端执行当前文件代码<弃用>
class openCommand(sublime_plugin.TextCommand):
    
    def run(self, edit):

        # 获取文件路径
        getFilePath = self.view.file_name()
        
        # 使用正则表达式处理文件路径：替换字符
        newFilePath = re.sub(r'\ ', "\\ ", getFilePath) 

        # 反向查找切割字符串：获取数组第一个路径
        openFile = newFilePath.rsplit('/', maxsplit=1 )

        url = os.popen('sh ../demo/open.sh ' + openFile[0] +' ' + openFile[1]).read()
        # self.view.insert(edit, 0, url )





# 在游览器打开当前文件
class htmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        
        # 获取文件路径
        getFilePath = self.view.file_name()

        openHtml = ''' open -a "Google Chrome" "file://'''+getFilePath+ '''" '''
        
        os.popen(openHtml)

        # self.view.insert(edit, 0, openHtml )





# 获取鼠标选中的字符
def getStr(self):

    # 判断字符串是否是英文
    def language(char):
        if (char >= '\u0041' and char <= '\u005a') or (char >= '\u0061' and char <= '\u007a'):
            return True
        else:
            return False

    for s in self.view.sel():
        # 获取鼠标选中的字符
        getChar = self.view.substr(s)       
        # 判断鼠标选中的是否是空字符
        def p_char(char):
            num = 0
            for _char in char:
                if _char == ' ':
                    num += 1
            if num != len(char):
                return True
            else:
                return False

        if p_char(getChar):
            getChar = getChar.strip() #去掉前后空白符
            _bool = language(getChar)
            return [getChar,_bool]

        else:
            os.system('say 没有查找的单词')



# 朗读鼠标选中的单词
class readCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        getChar = getStr(self)

        if getChar[1]:

            err = '朗读模式开启!'
            self.view.show_popup(
                err, sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 400, 500)

            def loop():
                for i in range(0,2):
                    os.system('say '+getChar[0])
                 

                content = translation(getChar[0],'')
                f_content = '翻译: '+content['double']+' '+'译文: '+content['translation']
                self.view.show_popup(
                    f_content, sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 400, 500)
            

            # 500毫秒后启动线程执行 
            sublime.set_timeout_async(loop,500)

        else:
            os.system('say 朗读的单词不是英文')







# 翻译鼠标选中的单词
class doubleCommand(sublime_plugin.TextCommand):
    def run(self, edit):  

        getChar = getStr(self)
                
        # 判断鼠标选中的是否是英文 
        if getChar[1]: 
            def loop():
                os.system('say '+getChar[0])

            # 500毫秒后启动线程执行 
            sublime.set_timeout_async(loop,500)

            tag = 1
        else:
            tag = 0
      
        content = translation(getChar[0],'')
        if content == 404:
            err = '无法查找单词,请检查网络是否连接成功!'
            self.view.show_popup(
                err, sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 400, 500)
       
        else:

            f_content = '翻译: '+content['double']+' '+'译文: '+content['translation']
            self.view.show_popup(
                f_content, sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 400, 500)
            
            if tag == 0:
                def loop():
                    os.system("say "+content['translation'])

                # 500毫秒后启动线程执行 
                sublime.set_timeout_async(loop,500)
           
                    

                

# 鼠标选中文字翻译的英文
class replaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for char in self.view.sel():
            getChar = getStr(self)
            # if getChar[1] == False:
            content = translation(getChar[0],'')
            content = content['translation']
            # 替换选中的文本
            self.view.replace(edit, char, content)

            # else:
            #     os.system('say 无法替换中文以外的单词')








# 翻译文本的注释英文
class englishCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        # 金山词霸翻译文件
        def translation2(text):
            url = "http://fy.iciba.com/ajax.php?a=fy"
            data = {
                'f': 'auto',
                't': 'auto',
                'w': text   
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            }

            response = requests.post(url, data=data, headers=headers)

            if response.status_code == requests.codes.ok:
                JsonData = response.content.decode('unicode_escape') # 中文转码
                listData = eval(JsonData)['content']['out'].replace('#','\n# ').strip().split('\n')
                return listData


        

        getFilePath = self.view.file_name()
        filePath = getFilePath.split('.')
        newFile = filePath[0]+'2.'+filePath[1]

        strData = ''
        for line in open(getFilePath,'r',encoding='utf-8'):
            dy = line.strip()
            if len(dy) != 0:
                if dy[0] == '#':
                    strData += line
        
      
        content2 = translation2(strData)
        lineNum = len(content2)
       
        num = -1
        contentList = ''
        for line in open(getFilePath,'r',encoding='utf-8'):
            dy = line.strip()
            if len(dy) != 0:
                if dy[0] == '#':
                    num += 1

                    if num < lineNum: 
                        content = content2[num]
                    

                    if content[0] != '#':
                        content = '# '+ content
                    contentList += content+'\n'
                else:
                    contentList += line
            else:
                contentList += line

        with open(newFile, 'w',encoding='utf-8') as f:
            f.write(contentList)







# 记录存储的代码段
class regCommand(sublime_plugin.TextCommand):
    def run(self, edit,args):
        args = eval(args)
        rep = args['replace']
        pos = args['position']

        if rep == 'rep':     
            replaceChar = sublime.Region(int(pos)-3,int(pos))
            self.view.replace(edit, replaceChar, '')

        elif rep == 'find':
            content = pos[2]

            if len(content) > 3:
                sublime.message_dialog('记录代码的格式不正确!')
            else:
                      
                # 获取文件路径
                ftype = self.view.file_name()
                ftype = ftype.split('.')

                replaceChar = sublime.Region(pos[0],pos[1])
                self.view.replace(edit, replaceChar,pos[2][2])

                pack = sublime.packages_path()
                pack = pack + '/demo/Record/'

                fileType = ftype[1]
                if fileType == 'html':
                    codeType = content[1].strip()

                    if len(codeType) == 0 or codeType == '填写':
                        storePath = ''
                        sublime.message_dialog('HTML文件没有填写代码格式！')
                    else:
                        storePath = pack + codeType +'_data' 
                else:
                    storePath = pack + fileType +'_data' 

             

                if storePath != '':

                    # 处理获取的代码段
                    def handleChar(listChar):

                        arr = listChar[2].split('\n')

                        count = 0
                        char = ''
                        blank = ''
                        for line in arr:
                            reg = re.search('\\S',line)

                            if reg != None:
                                if count == 0:
                                    count = 1
                                    num = int(reg.span()[0])
                                    for i in range(num):
                                        blank += ' ' 
                
                                char += line.replace(blank,'',1) + '\n'        

                            else:
                                char += line + '\n'
                        listChar[1] = char
                        
                        return listChar

                    content = handleChar(content)

                    # 存储代码段
                    with open(storePath, 'a+',encoding='utf-8') as f:
                        f.write(str(content)+'\n')

                    sublime.message_dialog('记录存储成功!')
                








# sublime事件监听
class sublimeEvent(sublime_plugin.EventListener):
    global input_num, enter_num, position, numk, calc
    # 存储输入时开始位置
    position = 0
    input_num = 0
    enter_num = 0
    numk = 0
    start = 0
    calc = 0

    # 保存文件时触发
    # def on_post_save_async(self,view):
        

    # 实时监听窗口文本输入时触发
    def on_modified_async(self,view):
        global input_num, enter_num, position, start, calc
        input_num += 1
        point = view.sel()[0].begin()

        line = view.line(point)
        line_char = view.substr(line)
        line_char_length = len(line_char)   
        print('输入字符长度: '+ str(line_char_length))


        # 处理输入事件        
        if re.search('>\\*>',line_char) :

            # 执行命令《替换》
            line = str(line).replace('(','').replace(')','').split(',')
            args = {"replace":"rep","position":line[1]}
            view.run_command('reg',{"args":str(args)})

            # 获取Python模块的路径
            list_path = []
            package_path = os.popen('python -c "import sys;print(sys.path)"').read()
            for _path in eval(package_path):
                arr = _path.split('/')
                site_pack = arr[len(arr) - 1]
                if site_pack == 'site-packages':
                    list_path.append(_path)
            
            # 获取Python模块的路径
            module_path = list_path[len(list_path) - 1]

            import_pack = line_char.strip()
    
            if import_pack[0:6] == 'import':
                pack_name = import_pack.replace('>','').split('import')[1].strip()

            elif import_pack[0:4] == 'from':
                pack_name = import_pack.replace('>','').split('import')[0].split('from')[1].strip()

            try:
                packa = len(pack_name)
                packax = 1
            except:
                packax = 0
            
            # 导入Python包
            if packax == 1:
                pack_path = module_path + '/' + pack_name
                pack_file = os.path.isdir(pack_path)

                if pack_file:

                    def packName(r_name,k):

                        pack_name = r_name
                        pack_Rely = os.popen('pip show '+pack_name).read()
                        if len(pack_Rely) == 0:
                            pack_Rely = os.popen('pip install '+pack_name+';pip show '+pack_name).read()
                          
                        _list = pack_Rely.split('\n')
                        
                        for li in _list:
                            if re.match('Requires',li):
                                get_pack_Rely = li.replace(' ','').split(':')[1].split(',')
            
                                for pack in get_pack_Rely:
                                    p_pack = os.path.isdir(module_path +'/'+pack)
                                    
                                    if p_pack:
                                        if k == 1:
                                            pack_name = ''
                                        pack_name += ' '+pack
            
                                    else:
                                        pack_name += ' '+packName(pack,1)

                                return pack_name               

                    pack_name = packName(pack_name,0)


                    # 获取当前文件路径
                    t_file_path = view.file_name()
                    thisFilePath = t_file_path.split('/')
        
                    this_paths = ''
                    for thisPath in range(len(thisFilePath)-1):
                        this_paths += '/'+thisFilePath[thisPath]
                    this_path = this_paths.replace('//','/').replace(' ','\\ ')

                    
                    shell = '''
                        cd '''+this_path+'''
                        if [[ ! -d './packages' ]]; then
                            mkdir packages
                        fi
                        cd '''+module_path+'''
                        cp -r '''+pack_name+''' '''+this_path+'''/packages

                    '''
        
                    os.system(shell)

                    find = 0
                    # 按行读取当前文件
                    for line in open(t_file_path, 'r', encoding='utf-8'):
                        line = line.strip()
                        if line[0:6] == 'import':
                            if re.search('sublime',line):
                                find = 1
                    
                   
                    def p_import(view,paths):
                        global numk
                        numk += 1
                        if numk == 1:     
                            line = view.line(0)
                            line_char = view.substr(line)
                            if str(line_char).strip()[0] == '#':
                                _len = len(line_char)
                                content = '\nimport sys\nsys.path.append("'+paths+'")'
                                args = {"replace":"find","position":[_len,_len,content]}
                                view.run_command('reg',{"args":str(args)})
                            else:
                                content = '# -*- coding: utf-8 -*-\nimport sys\nsys.path.append("'+paths+'")\n'
                                args = {"replace":"find","position":[0,0,content]}
                                view.run_command('reg',{"args":str(args)})       
                   
                    if find == 1:
                        this_paths = this_paths.replace('//','/')+'/packages'
                        p_import(view,this_paths)
                    else:
                        p_import(view,'./packages')


                else:
                    sublime.message_dialog('在Python包里面没有查找到: '+pack_name+' 模块!')
            else:
                sublime.error_message('没有需要导入的Python包!')
        

        # 处理记录
        def fun(self,view,_char):
            if re.search('<END>',_char):

                _content = _char.split('<END>')
                p1 = re.compile(r'[\{](.*?)[\}]', re.S) #最小匹配
                data = re.findall(p1, _content[0])

                if len(data) < 2:
                    _text = '没有代码段描述说明'
                    view.show_popup(
                    _text, sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 400, 500)
                else:
                    char = _content[1].replace('EOF>>','')
                    # 需要存储的文档
              
                    data.append(char)
                   
                    if len(data) == 3:    
                        args = {"replace":"find","position":[start, end, data]}
                        view.run_command('reg',{"args":str(args)})
                        
                    else:
                        sublime.message_dialog('记录存储失败!')
            else:
                _text = '不存在文档说明结束符:<END>'
                view.show_popup(
                _text, sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 400, 500) 

       
        # 记录代码
        if re.search('<<EOF',line_char) :
            end = int(str(line).split(',')[0].replace('(',''))         
            start = end
            while True:
                start += 1
                _char = view.substr(sublime.Region(start,end))
                if re.search('EOF>>',_char) :
                    fun(self,view,_char)    
                    break  
                
                elif start == view.size():
                    _text = '没有找到结尾符: EOF>>'
                    print(_text)
                    break


        if re.search('EOF>>',line_char) :
            end = int(str(line).split(',')[1].replace(')',''))
            start = end
            while True:
                start -= 1
                _char = view.substr(sublime.Region(start,end))
                if re.search('<<EOF',_char) :
                    fun(self,view,_char)  
                    break

                elif start == 0:
                    _text = "没有找到开始符: 左双箭头EOF"
                    print(_text)
                    break










        if input_num == 1:
            position = point - 1

        if position > point:
            input_num = 0


        # 获取鼠标选中的字符
        getChar = view.substr(sublime.Region( position, point))
        
        char_len = len(line_char)
        # print(getChar.split('\n'))
        # print(line_char.split('\n'))
        reg = re.search('\n', getChar)
        # print(reg)
        if reg:      
            input_num = 0
            enter_num += 1 

            print('触发回车成功\n回车次数: ' + str(enter_num))
            view.run_command('terminal',{'args':[point,getChar]})
        



        print('------------------') 
        print('获取输入字符: \n' + getChar)
        print('------------------')
        print('开始位置坐标: ' + str(position))
        print('------------------')
        print('结束位置坐标: ' + str(point))
        print('******************')


        





# 打开视图终端
class openviveCommand(sublime_plugin.WindowCommand):
    def run(self, reverse=False): 
        window = self.window
        window.run_command('terminus_close_all')
        window.run_command('terminus_open')   


# 打开面板终端
class openpanleCommand(sublime_plugin.WindowCommand):
    def run(self, reverse=False): 
        window = self.window
        window.run_command('terminus_close_all')
        window.run_command('terminus_open',{"panel_name": "Terminus"})
        


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





# 自定义代码补全 
class SymbolComplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        global num
        name = view.file_name()
        ftype = name.split('.')[1]
        _list = [
            ["_js"+"\tCODE (查找)","JS:${1:查找代码段}"],
            ["_css"+"\tCODE (查找)","CSS:${1:查找代码段}"],
            ["print"+"\tabc (打印)", "print(${1:打印})"],
            ["_e"+"\t<<EOF (开始)", "<<EOF: 代码描述: {${1:填写}} 语言类型: {填写} <END>"],
            ["_f"+"\tEOF>> (结束)", "EOF>>"]
        ]
       
        return (
            _list,
            sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS
        )

  



     
                                
        
















