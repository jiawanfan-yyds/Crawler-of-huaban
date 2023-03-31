call myenv\Scripts\activate.bat

set FLASK_APP=app.py
set FLASK_DEBUG=1

:: 更改IP地址和端口号为您需要的值
set FLASK_RUN_HOST=127.0.0.1
set FLASK_RUN_PORT=5000

:: 在用于运行Flask app的控制台窗口中启动Flask服务器
start cmd.exe /k "flask run"

:: 打开浏览器
start http://%FLASK_RUN_HOST%:%FLASK_RUN_PORT%

