#! /usr/bin/env python3
from base import Base


class TargetCLIConfig:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger

    def configure_targetcli(self, buffer):
        try:
            # 配置 targetcli
            command = f"sudo targetcli set global {buffer}"
            self.base.com(command)
            self.logger.log(f"执行命令：{command}")
            return True
        except Exception as e:
            self.logger.log(f"配置targetcli失败: {e}")
            return False

    def check_targetcli_configuration(self, buffer):
        try:
            # 检查 targetcli 配置
            command = f"sudo targetcli get global {buffer}"

            if buffer == "auto_add_default_portal" or "auto_add_mapped_luns":
                if "false" not in self.base.com(command):
                    self.logger.log(f"auto_add_default_portal配置失败：{command}")
                    return False
                else:
                    return True
            if buffer == "auto_enable_tpgt":
                if "True" not in self.base.com(command):
                    self.logger.log(f"auto_enable_tpgt配置失败：{command}")
                    return False
                else:
                    return True

        except Exception as e:
            self.logger.log(f"检查 targetcli 配置失败: {e}")
            return False
