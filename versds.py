#! /usr/bin/env python3
from base import Base


class VersaSDS:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger

    def implementation_methods(self):
        note = "程序将继续执行后续部分"
        services_to_disable = [
            "drbd",
            "linstor-controller",
            "rtslib-fb-targetctl",
            "linstor-satellite",
            "pacemaker",
            "corosync"
        ]

        for service in services_to_disable:
            if self.disable_service(service):
                if not self.is_service_disabled(service):
                    print(f"禁用{service}服务失败，{note}")
                else:
                    print(f"禁用{service}服务成功")
            else:
                print(f"禁用{service}服务失败，{note}")
        
        self.logger.space()

    # 禁用系统服务
    def disable_service(self, service_name):
        try:
            command = f"systemctl disable {service_name}"
            result = self.base.com(command)
            self.logger.log(f"执行命令：{command}")
            return True
        except Exception as e:
            print(f"禁用{service_name}发生错误：{e}")
            self.logger.log(f"ERROR - 禁用{service_name}发生错误：{e}")  # debug
            return False

    # 检查服务是否已禁用
    def is_service_disabled(self, service_name):
        try:
            command = f"systemctl is-enabled {service_name}"
            result = self.base.com(command).stdout
            self.logger.log(f"执行命令：{command} 结果：{result.strip()}")
            if result.strip() == "disabled":
                self.logger.log(f"{service_name} 已禁用")
                return True
            else:
                self.logger.log(f"ERROR - {service_name} 禁用失败")
                return False
        except Exception as e:
            print(f"检查{service_name}状态发生错误：{e}")
            self.logger.log(f"ERROR - 检查{service_name}状态发生错误：{e}")  # debug
            return False

    # 设置指定服务开机自启
    def set_service_autostart(self):
        note = "程序将继续执行后续部分"
        services_to_enable = [
            "linstor-satellite",
            "pacemaker",
            "corosync"
        ]
        services_to_disable = [
            "drbd",
            "linstor-controller",
            "rtslib-fb-targetctl"
        ]

        for service in services_to_disable:
            if self.disable_service(service):
                if not self.is_service_disabled(service):
                    print(f"禁用{service}服务失败，{note}")
                else:
                    print(f"禁用{service}服务成功")
            else:
                print(f"禁用{service}服务失败，{note}")
        for service in services_to_enable:
            if self.enable_service(service):
                if not self.is_service_enabled(service):
                    print(f"设置{service}开机自启失败，{note}")
                else:
                    print(f"设置{service}开机自启成功")
            else:
                print(f"设置{service}开机自启失败，{note}")
        
        self.logger.space()

    # 启用系统服务
    def enable_service(self, service_name):
        try:
            command = f"systemctl enable {service_name}"
            result = self.base.com(command)
            self.logger.log(f"执行命令：{command}")
            return True
        except Exception as e:
            print(f"启用{service_name}发生错误：{e}")
            self.logger.log(f"ERROR - 启用{service_name}发生错误：{e}")  # debug
            return False
        
    # 检查服务是否已开机自启
    def is_service_enabled(self, service_name):
        try:
            command = f"systemctl is-enabled {service_name}"
            result = self.base.com(command).stdout
            self.logger.log(f"执行命令：{command} 结果：{result.strip()}")
            if result.strip() == "enabled":
                self.logger.log(f"{service_name} 已开机自启")
                return True
            else:
                self.logger.log(f"ERROR - {service_name} 开机自启失败")
                return False
        except Exception as e:
            print(f"检查{service_name}状态发生错误：{e}")
            self.logger.log(f"ERROR - 检查{service_name}状态发生错误：{e}")  # debug
            return False
