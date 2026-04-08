@echo off
title MOTOR ATLETA OFERTAS - PROD
color 0A

:: Garante que o terminal execute na pasta correta
cd /d "%~dp0"

echo ======================================================
echo           INICIANDO MOTOR ATLETA OFERTAS
echo ======================================================

:: 1. Ativa o ambiente virtual
echo [1/4] Ativando Venv...
call venv\Scripts\activate.bat

:: 2. Limpeza de dados antigos para não misturar ofertas
if exist "scraper_atleta\ofertas_academia.json" del "scraper_atleta\ofertas_academia.json"
if exist "POSTAGENS_WHATSAPP.txt" del "POSTAGENS_WHATSAPP.txt"

:: 3. Roda o Scraper (Lendo o scrapy.cfg da raiz)
echo [2/4] Garimpando ofertas no Mercado Livre...
scrapy crawl atleta_spider -O scraper_atleta/ofertas_academia.json

:: 4. Roda o formatador de postagens
echo [3/4] Gerando cards para o WhatsApp...
python postador.py

:: 5. Finalização
echo [4/4] Processo concluido!
timeout /t 2 >nul

if exist "POSTAGENS_WHATSAPP.txt" (
    echo ✅ Abrindo Bloco de Notas...
    start notepad.exe "POSTAGENS_WHATSAPP.txt"
) else (
    echo ❌ ERRO: O arquivo final nao foi gerado. Verifique o log acima.
    pause
)