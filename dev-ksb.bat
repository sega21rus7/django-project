echo off

pushd %~dp0
if not exist venv c:\python36\python.exe -m venv venv
if errorlevel 1 goto ending
call venv\Scripts\activate
if errorlevel 1 goto ending

SET NO_PROXY=%NO_PROXY%,*.keysystems.local
SET PIP_INDEX_URL=http://ksb-dev.keysystems.local:8808/simple/
SET PIP_TRUSTED_HOST=ksb-dev.keysystems.local
SET PIP_TIMEOUT=120

python -m pip install --upgrade -r requirements.txt --retries 2 --timeout 5
if errorlevel 1 goto ending

pushd frontend
call npm config set registry http://ksb-dev.keysystems.local:4873/
call npm config set "strict-ssl" false
call npm install --no-progress --non-interactive
if errorlevel 1 goto ending
popd

python backend\manage.py migrate
if errorlevel 1 goto ending

:ending
popd
