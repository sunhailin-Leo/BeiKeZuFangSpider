@echo off

::设置宽度和高度
mode con cols=109

::设置颜色
color 2e
echo.
echo ############################################## Python 打包程序 ##############################################
echo. 
set /p is_build=是否开始打包(Y或y为是, N或n为否):
echo. 
echo 你的选择是：%is_build%
echo.

::判断选项
if /i "%is_build%" == "Y" goto :start_build_project
if /i "%is_build%" == "y" goto :start_build_project
if /i "%is_build%" == "N" goto :close_build_project
if /i "%is_build%" == "n" goto :close_build_project
goto error_choice_end


:start_build_project
echo 准备开始打包环境...
echo.

::打包方法 -- 开始

::清空build_path下的所有文件
del /f /s /q .\build_path\*
echo.
echo 删除文件成功!

::删除build_path文件夹
rd /s /q  .\build_path\
echo.
echo 删除文件夹成功!

::重建build_path文件夹
md build_path
echo.
echo 重建打包文件夹

::打包命令
::命令1 -- 会重新生成spec文件 pyinstaller -F spider_starter.py --workpath ./build_path --distpath ./build_path
::命令2 -- 有问题: pyinstaller -F spider_starter.spec --workpath ./build_path --distpath ./build_path (会报win32错误)
echo.
echo 开始打包
C:\\Python\\Python36\\Scripts\\pyinstaller.exe -F cmdline_start_spider.py --workpath ./build_path --distpath ./build_path
::pyinstaller -F spider_starter.spec --workpath ./build_path --distpath ./build_path
::打包方法 -- 结束

pause
echo.
goto end

:close_build_project
echo 退出打包程序!
echo.
goto end

:error_choice_end
echo 你的选择有误!
pause > nul

:end
echo 程序结束!
pause > nul