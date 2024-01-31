# 取得目錄路徑
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 執行
gnome-terminal -- python3 "$DIR/Workday_Notice.py"