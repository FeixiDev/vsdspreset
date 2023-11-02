
#! /usr/bin/env python3

import subprocess

class Base:
    def __init__(self, logger):
        self.logger = logger
    
    def com(self, command):
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, shell=True, check=True, text=True).stdout 
            self.logger.log(f"执行命令：{command}")
            return result
        except subprocess.CalledProcessError as e:
            self.logger.log(f"命令 {command} 执行失败 {e}")
            return f"命令执行失败: {str(e)}"
    
    
