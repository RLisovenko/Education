
-------------------------Setting
Step Curs:
- Start venv
- check 
	pip - python.exe -m pip install --upgrade pip
	where pip
	python 	--vesion
	git 	--version
	psql 	--vesion
	$env:Path - прочиттать что переменной окружения или - $i=1; $env:Path -split ';' | ForEach-Object { "$i. $_"; $i++ }

----------------------python----------------------------
какой пайтон исп. в тек переменых
python -c "import sys; print(sys.executable)"

check version 
# 1. Проверить установленный Python 3.14.
winget list --exact --id Python.Python.3.14 --source winget

# 2. Установить именно 3.14.6, если ещё не установлен.
winget install --exact --id Python.Python.3.14 --version 3.14.6 --source winget

# 3. Из корня проекта создать/активировать .venv.
# В скрипте BasePython должен указывать на нужный Python.
.\scripts\ps\start_py_3_146.ps1

# 4. Проверить версию и путь активного Python.
python --version
python -c "import sys; print(sys.executable)"

# 5. Обновить pip внутри окружения.
python -m pip install --upgrade pip

# 6. Установить зависимости, если список проверен и нужен.
python -m pip install -r requirements.txt

# 7. Показать установленные пакеты окружения.
python -m pip list

------------------------GIT--------------------------
# 1. Проверить текущую версию Git.
git --version

# 2. Установить Git, если его нет.
winget install --exact --id Git.Git --source winget

# 3. Если Git уже установлен — обновить вместо шага 2.
winget upgrade --exact --id Git.Git --source winget

# 4. После установки перезапустить VS Code и проверить.
git --version

------------------------PSQL--------------------------
# Проверить версию
psql --version
если нет найти где лежит на ПК
Get-ChildItem "C:\Program Files\PostgreSQL\17\bin\psql.exe" 	#Check where on PS
------------------------------или постоянно для пользователя
[Environment]::SetEnvironmentVariable(
  "Path",
  [Environment]::GetEnvironmentVariable("Path","User") + ";C:\Program Files\PostgreSQL\17\bin",
  "User"
)
------------------------------
#добавить  
$env:Path += ";C:\Program Files\PostgreSQL\17\bin"

psql --version

winget search PostgreSQL							#Search versions
winget install --id PostgreSQL.PostgreSQL.17 -e

# Подключиться к базе postgres
psql -U postgres -h localhost -p 5432 -d postgres

# Выполнить SQL из файла
psql -U postgres -d mydb -f .\script.sql


--------------------------panda
python.exe -m pip install --upgrade pip
pip --version
pip install pandas
python -c "import pandas; print(pandas.__version__)"

--------------------------requirements.txt	
all install from requirements.txt
- python -m pip install -r requirements.txt

---------------------------Working
mkdir raw
mkdir processed
pwd - project root
New-Item data\raw\sample.csv -ItemType File
Rename-Item data\raw\sample.csv sales_data.csv
Copy-Item data\raw\sales_data.csv data\processed\sales_data_copy.csv
Rename-Item data\processed\sales_data_copy.csv processed_sales.csv

---------------------------Managing Git and GitHUB
git init
git status
------------------если нужно 
git config --global user.name "LiR"
git config --global user.email "LiR@example.com"
------------------
git add .
git status
git branch -M main		
----------------------Мое
Локально	                     На GitHub
5_1_DataEng_Fund_SQL_Python\ ->	Education/main/DataEngineering/DataEng-Fund-SQL-Python/

cd C:\SourceCode\PSC\2025_2026\coursera\5_DataEng\5_1_DataEng_Fund_SQL_Python

git init
git add .
git commit -m "Add Data Engineering Foundations SQL Python course"

"edu/DataEng-Fund-SQL-Python" -  название ветки для ссылки https://github.com/RLisovenko/Education/tree/edu/DataEng-Fund-SQL-Python
git branch -M edu/DataEng-Fund-SQL-Python

origin -  на сторне ПС
git remote add origin https://github.com/RLisovenko/Education.git
git add DataEngineering/DataEng-Fund-SQL-Python  - а папке
git remote -v				- ПРОВЕРКА

git push -u origin edu/DataEng-Fund-SQL-Python	- шлет в папку edu/DataEng-Fund-SQL-Python
git push 										- просто в шлет origin https://github.com/RLisovenko/Education.git

---------------для папки

LOCAL:
5_DataEng/
└─ 5_1_DataEng_Fund_SQL_Python/
   ├─ data/
   ├─ docs/
   ├─ scripts/
   └─ ...

                ↓

GITHUB:
Education / main
└─ DataEngineering/
   └─ DataEng-Fund-SQL-Python/
      ├─ data/
      ├─ docs/
      ├─ scripts/
      └─ ...
	  
cd C:/SourceCode/PSC/2025_2026/coursera/5_DataEng/5_1_DataEng_Fund_SQL_Python
git init
git add .
git commit -m "Data Engineering Foundations course"
git status
git branch -M 5_1_DataEng

git remote add course "C:/SourceCode/PSC/2025_2026/coursera/5_DataEng/5_1_DataEng_Fund_SQL_Python"
git fetch course
git subtree add --prefix=DataEngineering/DataEng-Fund-SQL-Python course master --squash
git push origin main


-------------comment
# Work inside the local Education repository
cd C:\...\Education

# Make sure we are on main
git switch main

# Update local main
git pull origin main

# Add only the Data Engineering course folder
git add DataEngineering/DataEng-Fund-SQL-Python

# Check staged changes
git status

# Commit the course materials
git commit -m "Add Data Engineering Foundations SQL Python course"

# Push changes to main
git push origin main


!!!!!!!!!!!!!!!!!!!!!!!для папки не нужны
git branch -M edu/DataEng-Fund-SQL-Python
git push -u origin edu/DataEng-Fund-SQL-Python
!!!!!!!!!!!!!!!!!!!!!!!


---------------
--------------- потом обычный цикл
git add .
git commit -m "Update course materials"
git push
---------------
---------------для ветки
cd /c/SourceCode/PSC/2025_2026/coursera/5_DataEng/5_1_DataEng_Fund_SQL_Python

# Initialize local repository
git init

# Add course files
git add .

# Commit course files
git commit -m "Add Data Engineering Foundations SQL Python course"

# Name local branch like the GitHub branch
git branch -M edu/DataEng-Fund-SQL-Python

# Connect to Education repository
git remote add origin https://github.com/RLisovenko/Education.git

# Check connection
git remote -v

забирает инфо с гита
git fetch origin

обыкновенный пуш
git push -u origin edu/DataEng-Fund-SQL-Python

пуш с заменить содержимое удалённой ветки локальной версией
git push -u origin edu/DataEng-Fund-SQL-Python --force-with-lease