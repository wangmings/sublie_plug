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


# 爬虫翻译
def translation(args,option):
    
    # 存储翻译数据
    storage = 'storage_translation_data'

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
                double = "{'double':'"+args+"','translation':'"+getText+"'}"

                if option == 'pass':  
                    return getText
                else:
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




# 在终端打开当前文件路径
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



# 在终端执行当前文件代码
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
                    newStr = '' 
                    counter = 0

                    for _char in getChar[0]:
                        if _char != ' ' :
                            newStr += '-' + _char
                        
                    if newStr[0] == '-':
                        newStr = newStr.split('-', 1)[1]
                        os.system('say '+newStr)
                        if i == 1:
                            time.sleep(2)

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
            os.system('say '+getChar[0])
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
            if getChar[1] == False:
                content = translation(getChar[0],'')
                content = content['translation']
                # 替换选中的文本
                self.view.replace(edit, char, content)

            else:
                os.system('say 无法替换中文以外的单词')



# 翻译文本的注释英文
class englishCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        getFilePath = self.view.file_name()
        filePath = getFilePath.split('.')
        newFile = filePath[0]+'2.'+filePath[1]

        strData = ''
        for line in open(getFilePath,'r',encoding='utf-8'):
            dy = line.strip()
            if len(dy) != 0:
                if dy[0] == '#':
                    strData += line
       
        content2 = translation(strData,'pass')
        content2 = content2.split('\n')
      
        num = -1
        contentList = ''
        for line in open(getFilePath,'r',encoding='utf-8'):
            dy = line.strip()
            if len(dy) != 0:
                if dy[0] == '#':
                    num += 1
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







# Python《模块导入》 替换导入模块符号: >> import 模块
class regCommand(sublime_plugin.TextCommand):
    def run(self, edit,args):
        # argv = args.replace('(','').replace(')','').split(',')
        args = eval(args)
        rep = args['replace']
        pos = args['position']

        if rep == 'rep':     
            replaceChar = sublime.Region(int(pos)-3,int(pos))
            self.view.replace(edit, replaceChar, '')

        elif rep == 'find':
            replaceChar = sublime.Region(pos[0],pos[1])
            self.view.replace(edit, replaceChar,pos[2])



# sublime事件监听
class sublimeEvent(sublime_plugin.EventListener):
    global input_num, enter_num, position, numk
    # 存储输入时开始位置
    position = 0
    input_num = 0
    enter_num = 0
    numk = 0

    # 保存文件时触发
    # def on_post_save_async(self,view):
        

    # 实时监听窗口文本输入时触发
    def on_modified_async(self,view):
        global input_num, enter_num, position
        input_num += 1
        point = view.sel()[0].begin()

        line = view.line(point)
        line_char = view.substr(line)
        line_char_length = len(line_char)   
        print('输入字符长度: '+ str(line_char_length))


        # 处理输入事件
        _import = re.search('>>>',line_char)
        if _import :

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
                sublime.message_dialog('没有需要导入的Python包6666!')






        if input_num == 1:
             position = point - 1



        # 获取鼠标选中的字符
        getChar = view.substr(sublime.Region( position, point))
        reg = re.search('\n', getChar)
        if reg:
            input_num = 0
            enter_num += 1 
            print('------------------') 
            print('触发回车成功\n回车次数: ' + str(enter_num))
          

        print('------------------') 
        print('获取输入字符: \n' + getChar)
        print('------------------')
        print('开始位置坐标: ' + str(position))
        print('------------------')
        print('结束位置坐标: ' + str(point))
        print('******************')











        
































         
     









        

