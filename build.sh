# conda run -n rosetta --no-capture-output pyinstaller --name 复制搜索 main.py 
# conda run -n rosetta --no-capture-output pyinstaller --noupx --name 复制搜索 main.py 

conda run -n rosetta --no-capture-output pyinstaller --noconfirm --windowed --name 复制搜索 main.py

cd dist
rm 复制搜索.7z
7z a 复制搜索.7z 复制搜索.app