@echo off
title MOTOR ATLETA OFERTAS
color 0A

:: Gante que o terminal trabalhe na pasta onde o .bat está
cd /d "%~dp0"

echo ======================================================
echo           INICIANDO MOTOR ATLETA OFERTAS
echo ======================================================

:: 1. Ativação do Venv (Usando o caminho absoluto do diretório atual)
echo [1/4] Ativando Ambiente Virtual...
set VENV_PATH=%~dp0venv\Scripts\activate.bat
if exist "%VENV_PATH%" (
    call "%VENV_PATH%"
) else (
    echo [ERRO] Nao encontrei o venv em: %VENV_PATH%
    pause
    exit
)

:: 2. Limpeza de dados antigos
echo [2/4] Limpando arquivos temporarios...
if exist "scraper_atleta\ofertas_academia.json" del "scraper_atleta\ofertas_academia.json"

:: 3. Execução do Scrapy
echo [3/4] Garimpando ofertas no Mercado Livre...
:: Usamos 'call scrapy' para garantir que o script continue após o comando
call scrapy crawl atleta_spider -O scraper_atleta/ofertas_academia.json

:: 4. Execução do Postador
echo [4/4] Gerando cards para o WhatsApp...
if exist "postador.py" (
    python postador.py
) else (
    echo [ERRO] O arquivo postador.py nao foi encontrado na raiz!
)

:: 5. Finalização
echo.
if exist "POSTAGENS_WHATSAPP.txt" (
    echo ✅ SUCESSO! Abrindo o arquivo de postagens...
    start notepad.exe "POSTAGENS_WHATSAPP.txt"
) else (
    echo ❌ ERRO: O processo terminou mas o arquivo final nao apareceu.
    echo Verifique se o Scrapy encontrou produtos.
)

pause