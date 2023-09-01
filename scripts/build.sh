mkdir dist

apt update
apt install rsync -y

rsync -av --exclude='*/__pycache__*' --exclude='__pycache__' ./src/ ./dist/
cp -r ./user_config ./dist/
