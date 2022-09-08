#!/bin/bash 

PYTHON_TGT_VER="3.10"

header () {
    printf "\n\n********************************************************************************\n"
    printf "* %s\n" "$1"
    printf "********************************************************************************\n"
}


header "Checking Python"

python_ver=$(python -c "import sys;print('%d.%d' % sys.version_info[:2])")
python_ver_full=$(python -c "import sys;print('%d.%d.%d' % sys.version_info[:3])")
python_loc=$(which python) 
printf "Your python version: $python_ver_full\n"
printf "Your python location: $python_loc\n"
# check if python installation looks right
if [ "$python_ver" != "$PYTHON_TGT_VER" ]; then
    printf "python version incorrect. Should be $PYTHON_TGT_VER\n"
    return
fi

header "Installing Python virtual environment"
python -m venv venv

header "Activating Python virtual environment"
source venv/bin/activate

header "Installing Python packages"
pip install -r requirements.txt

header "Installing npm packages"
npm ci

header "Copying launch configurations"

if [ ! -d "./.vscode" ] 
then
    mkdir .vscode
fi
cp install/launch.json ./.vscode/launch.json

header "ALL DONE!"
