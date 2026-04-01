@echo off
title MOTOR ATLETA OFERTAS - GARIMPO ATIVO
color 0A

echo ======================================================
echo           INICIANDO MOTOR ATLETA OFERTAS
echo ======================================================

:: 1. Ativa o ambiente virtual (venv)
echo [1/4] Ativando ambiente virtual...
call C:\AtletaOfertas\venv\Scripts\activate.bat

:: 2. Roda o Scraper do Mercado Livre
echo [2/4] Garimpando ofertas no Mercado Livre...
cd C:\AtletaOfertas\core\scraper_atleta
scrapy crawl atleta_spider -O ofertas_academia.json

:: 3. Roda o Postador Inteligente (Ajustado para caminho absoluto)
echo [3/4] Gerando cards de oferta para WhatsApp...
:: Aqui usamos o caminho completo do arquivo para nao ter erro de diretorio
python C:\AtletaOfertas\postador.py

:: 4. Finalização e Entrega
echo [4/4] Operacao concluida com sucesso!
echo ======================================================
echo.
echo Pressione qualquer tecla para abrir as ofertas geradas...
pause > nul

:: Abre o arquivo de postagens automaticamente
if exist C:\AtletaOfertas\POSTAGENS_WHATSAPP.txt (
    start notepad.exe C:\AtletaOfertas\POSTAGENS_WHATSAPP.txt
) else (
    echo [ERRO] O arquivo de postagens nao foi gerado. verifique o postador.py
    pause
)

exit