@echo off
setlocal

echo Baixando o instalador mais recente do Python...

:: Define a URL da versão mais recente (alterável se quiser uma versão fixa)
set "url=https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
set "arquivo=python-installer.exe"

:: Baixar com curl (funciona no Windows 10+)
curl -L -o %arquivo% %url%

if exist %arquivo% (
    echo Instalando Python...
    %arquivo% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    echo Python instalado com sucesso!
    del %arquivo%
) else (
    echo Falha ao baixar o instalador.
)

endlocal
pause
