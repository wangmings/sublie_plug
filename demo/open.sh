#!/bin/bash

# 超级坑：shell反斜杠需要进行多层《才不会出错》
# 测试方法：echo ///
# 查看输出结果：


path=$(echo $1|sed 's/\ /\\\\\ /g')


file="$2"

#字符串分割选择：右边
fileType=${file#*.}

if [[ "$fileType" = "sh" ]]; then
    type="sh"

elif [[ "$fileType" = "c" || "$fileType" = "cpp" ]]; then
    type="im"

elif [[ "$fileType" = "java" ]]; then
    type="im"

elif [[ "$fileType" = "go" ]]; then
    type="go"

elif [[ "$fileType" = "js" ]]; then
    type="node"

elif [[ "$fileType" = "py" ]]; then 
    type="python"
fi


printn="echo -e '\\\\033[36m[<Run>]\\\\033[0m <<<-*************->>> \\\\033[36m[<Consequence>]\\\\033[34m \n'"



open="cd $path;reset;$printn;$type $file;echo ''"

script='

tell application "Terminal"

--如果窗口1不存在的话：重要点：exists window 1
if not (exists window 1) then

    --如果app窗口没有打开：启动APP窗口到前端
    reopen 
    
    --在终端上执行shell脚本：<in window 1:这里指在第一个窗口上执行>
    do script "'$open'" in window 1
    
    --激活APP到前端
    activate -- makes the app frontmost
    

else

    --在终端上执行shell脚本：<in window 1:这里指在第一个窗口上执行>
    do script "'$open'" in window 1
    
    --如果app窗口最小化：启动APP到前端
    reopen -- unminimizes the first minimized window or makes a new default window 
    
    --激活APP到前端
    activate -- makes the app frontmost

    end if

    end tell
    '

    osascript -e "$script"
    
# echo $path











