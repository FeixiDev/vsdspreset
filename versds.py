#! /usr/bin/env python3
from base import Base


class VersaSDS:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger

    # 禁用系统服务
    def disable_service(self, service_name):
        try:
            command = f"systemctl disable {service_name}"
            result = self.base.com(command)
            self.logger.log(f"执行结果：{result}")
            return True
        except Exception as e:
            print(f"禁用{service_name}发生错误：{e}")
            self.logger.log(f"禁用{service_name}发生错误：{e}")  # debug
            return False

    # 检查服务是否已禁用
    def is_service_disabled(self, service_name):
        try:
            command = f"systemctl is-enabled {service_name}"
            result = self.base.com(command)
            if result.strip() == "disabled":
                self.logger.log(f"{service_name} 已禁用")
                return True
            else:
                self.logger.log(f"{service_name} 未禁用")
                return False
        except Exception as e:
            print(f"检查{service_name}状态发生错误：{e}")
            self.logger.log(f"检查{service_name}状态发生错误：{e}")  # debug
            return False
