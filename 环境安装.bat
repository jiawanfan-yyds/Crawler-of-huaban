@echo off
chcp 65001

echo Creating virtual environment...
python -m venv myenv
echo Virtual environment created.

echo Activating environment...
call myenv\Scripts\activate.bat
echo Environment is activated.

python.exe -m pip install --upgrade pip

cd /d "C:\Users\Admin\Desktop\花瓣网爬虫"

pip install -r requirements.txt
