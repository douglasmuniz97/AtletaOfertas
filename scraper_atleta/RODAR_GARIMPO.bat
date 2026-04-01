@echo off
title MOTOR ATLETA OFERTAS - GARIMPO AUTOMATICO
color 0B

:: Entra na pasta onde o projeto Scrapy realmente mora
cd /d C:\AtletaOfertas\core\scraper_atleta

echo ======================================================
echo           INICIANDO MOTOR ATLETA OFERTAS
echo ======================================================
echo.

:: 1. Ativa a venv usando o caminho fixo do seu PC
echo [1/3] Ativando Ambiente Virtual (venv)...
if exist "C:\AtletaOfertas\venv\Scripts\activate.bat" (
    call "C:\AtletaOfertas\venv\Scripts\activate.bat"
) else (
    echo [ERRO] Nao achei a venv em C:\AtletaOfertas\venv
    pause
    exit
)

:: 2. Executa o Crawler (O -O garante que o JSON seja limpo)
echo [2/3] Rodando Crawler no Mercado Livre...
scrapy crawl atleta_spider -O ofertas_academia.json

:: 3. Executa o Postador
echo [3/3] Formatando ofertas para o WhatsApp...
echo.
if exist "postador.py" (
    python postador.py
) else (
    echo [ERRO] postador.py nao encontrado nesta pasta!
)

echo.
echo ======================================================
echo   PROCESSO CONCLUIDO! COPIE AS OFERTAS ACIMA.
echo ======================================================
pause