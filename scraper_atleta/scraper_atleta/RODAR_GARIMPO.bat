@echo off
title MOTOR ATLETA OFERTAS
color 0A

:: 1. Ativa o ambiente virtual
call venv\Scripts\activate.bat

:: 2. Entra na pasta do Scrapy e Garimpa
cd scraper_atleta
scrapy crawl atleta_spider -O ofertas_academia.json

:: 3. Volta para a raiz e formata as ofertas
cd ..
python postador.py

:: 4. Finalização
echo Processo concluido!
start notepad.exe POSTAGENS_WHATSAPP.txt