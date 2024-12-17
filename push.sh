# 快捷提交到github脚本
git pull

git add .
# 使用输入参数作为提交信息，并加上时间戳

if [ $# -eq 0 ]; then   # 如果没有输入参数
    git commit -m "update at `date +'%Y-%m-%d %H:%M:%S'`"
else
    git commit -m "$1 at `date +'%Y-%m-%d %H:%M:%S'`"
fi

git push