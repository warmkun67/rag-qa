@echo off
chcp 65001
set PYTHONIOENCODING=utf-8
title 启动 RAG 问答系统网页端
echo ==============================================
echo       正在启动 RAG 问答系统网页端...
 echo ==============================================
echo 请不要关闭此窗口，关闭窗口会停止服务。
echo 启动成功后，浏览器会自动打开页面。
echo ==============================================

:: 切换到当前目录
cd /d "%~dp0"

:: 激活 conda/base 环境（如果你用的是默认 base 环境）
call conda activate

:: 启动 streamlit
streamlit run web.py

pause