


-- 获取当前执行脚本的父文件夹路径: 
set UnixPath to POSIX path of ((path to me as text) & "::")
set posPath to UnixPath & "position.menu"
global posPath
log posPath



-- 字符串分割
on strSplit(_str,_char) 
    set AppleScript's text item delimiters to ""&_char&""
    set myList to every text item of _str
    return myList
end strSplit


-- 替换字符串
on strReplace(str,char,replace)
    set num to 0
    set _str to ""
    set _list to strSplit(str,char)
    set _len to length of _list
    repeat with _name in _list
        set num to num + 1
        set _str to _str & _name
        if num < _len then
            set _str to _str & replace
        end if
    end repeat
    return _str

end strReplace

-- strReplace(posPath,"mac","hello")



-- 判断文件是否存在
on fileSy(fliePath)
    set _shell to "[ -f \""&fliePath&"\" ] && echo \"yes\" || echo \"on\""
    set _sc to do shell script _shell
    return _sc
end fileSy



-- 存储数据
on echoSy(fliePath, _data)
    set x to the first item of _data
    set y to the last item of _data
    set _pos to ""&x&", "&y&""
    do shell script "echo \""&_pos&"\" >> \""&fliePath&"\" "
end echoSy



-- 读取文件
on readFile(fliePath, readType)    
    set FileData to do shell script "cat \""&fliePath&"\" "
    if readType is equal to "list" then
        set FileData to paragraphs of (FileData)
    end if
    return FileData
end readFile




-- 定义函数: cliclick命令模拟鼠标点击
on mouseClick(pos)
    set x to the first item of pos + 8
    set y to the last item of pos + 8
    set _click to "/usr/local/bin/cliclick c:" & (x as text) & "," & (y as text)
    do shell script _click
end mouseClick






-- 定义函数: 模拟回车键
on mouseEnter()
    tell application "System Events"
        key code 36     
        delay 0.5
        key code 36      
    end tell
end mouseEnter





-- 获取菜单栏坐标
on getMenuPosition(_title)
    tell application "System Events"
        tell process "Typora"
            set frontmost to true
            tell its menu bar 1
                set num to 0
                repeat with all in entire contents as list
                    set _name to name of all
                    -- log _name
                    if _name is equal to _title then
                        set _pos to position of all
                        log _title 
                        my mouseClick(_pos)
                        my echoSy(posPath,_pos)
                        exit repeat
                    end if
                end repeat
            end tell
        end tell
    end tell
end getMenuPosition



-- 点击菜单
on clickMenuPosition(_pos)
    tell application "System Events"
        tell process "Typora"
            set frontmost to true
            my mouseClick(_pos)
        end tell
    end tell
end clickMenuPosition




-- 主函数
on main()
    set menuPath to "文件,导出,HTML"
    if fileSy(posPath) is equal to "on" then
        say "第一次执行请稍等"
        epeat with _name in strSplit(menuPath,",")
            getMenuPosition(""&_name&"")
        end repeat
        delay 0.5
        mouseEnter()
        delay 0.5
        quit application "Typora"
    else
        -- set posPath to strReplace(posPath," ","\\ ")
        set _posAll to readFile(posPath,"list")                
        repeat with _pos in _posAll                               
            if length of _pos is greater than 0 then              
                set _pos to strSplit(_pos,",")
                clickMenuPosition(_pos)
                delay 0.5
            end if
        end repeat
        delay 0.5
        mouseEnter() 
        delay 0.5
        quit application "Typora"
    end if
end main

main()

















