@echo off
title MOTOR ATLETA OFERTAS
color 0A

:: Define a pasta atual como base para evitar erros de caminho
set BASE_DIR=%~dp0
cd /d "%BASE_DIR%"

:: 1. Ativa o ambiente
echo [1/4] Ativando ambiente...
call venv\Scripts\activate.bat

:: 2. Roda o Scrapy
echo [2/4] Garimpando ofertas...
scrapy crawl atleta_spider -O "scraper_atleta/ofertas_academia.json"

:: 3. Roda o Postador
echo [3/4] Formatando mensagens...
python postador.py

:: 4. Finalizacao
echo [4/4] Processo concluido!

:: Pequena pausa para o Windows liberar o arquivo
timeout /t 2 >nul

:: Abre o arquivo de postagens de forma explicita
if exist "POSTAGENS_WHATSAPP.txt" (
    echo Abrindo ofertas no Bloco de Notas...
    start notepad.exe "POSTAGENS_WHATSAPP.txt"
) else (
    echo.
    echo [ERRO] O arquivo "POSTAGENS_WHATSAPP.txt" nao foi encontrado na pasta:
    echo %cd%
    pause
)