@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
title RAG项目一键启动
echo ======================================
echo   正在启动 RAG 问答系统
echo ======================================

:: 1. 加载 Anaconda 环境
call "D:\Anaconda\Anaconda\Scripts\activate.bat"

:: 2. 进入项目目录
cd /d "D:\rag_project"

:: 3. 直接运行项目
"D:\Anaconda\Anaconda\python.exe" app.py

pause