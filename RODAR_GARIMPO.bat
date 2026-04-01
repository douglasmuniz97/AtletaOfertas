@echo off
title MOTOR ATLETA OFERTAS
color 0A

:: 1. Ativa o ambiente virtual
call venv\Scripts\activate.bat

:: 2. Roda o Scraper (Agora rodando da raiz onde estara o scrapy.cfg)
echo Garimpando ofertas...
scrapy crawl atleta_spider -O scraper_atleta/ofertas_academia.json

:: 3. Roda o Postador
echo Formatando mensagens...
python postador.py

:: 4. Finalizacao
start notepad.exe POSTAGENS_WHATSAPP.txt