#! /usr/bin/env python3
import os
from base import Base


class NetworkManager:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger
        self.network_manager_config = "/etc/NetworkManager/NetworkManager.conf"
        # self.netplan_file = '/etc/netplan/01-netcfg.yaml'
        
        self.netplan_dir = '/etc/netplan'
        self.netplan_file = None

        self.find_main_config()

    def find_main_config(self):
        # 获取目录下的所有文件
        files = os.listdir(self.netplan_dir)

        # 根据文件名排序
        files.sort()

        for file in files:
            if file.endswith('.yaml'):
                # 找到第一个以 .yaml 结尾的文件，即主要配置文件
                self.netplan_file = os.path.join(self.netplan_dir, file)
                break

    def set_network_manager_interfaces(self):
        try:
            # 修改 NetworkManager 配置文件
            config_content = ""
            with open(self.network_manager_config, "r") as f:
                config_content = f.read()

            config_content = config_content.replace(
                "managed=false", "managed=true")

            with open(self.network_manager_config, "w") as f:
                f.write(config_content)

            return True
        except Exception as e:
            print(f"配置 NetworkManager 管理接口失败：{e}")
            return False

    def restart_network_manager_service(self):
        try:
            # 重启 NetworkManager 服务
            self.base.com("systemctl restart NetworkManager.service")
            self.logger.log(f"执行命令：systemctl restart NetworkManager.service")
            return True
        except Exception as e:
            self.logger.log(f"重启 NetworkManager 服务失败：{e}")
            return False

    def update_netplan_config(self):
        try:

            # 打开 netplan 配置文件进行修改
            with open(self.netplan_file, 'r') as file:
                lines = file.readlines()

            updated_lines = []
            delete_lines = False

            for line in lines:
                # 将 renderer:networkd 更改为 renderer:NetworkManager
                if 'renderer: networkd' in line:
                    updated_lines.append(line.replace(
                        'renderer: networkd', 'renderer: NetworkManager'))
                elif 'ethernets:' in line:
                    delete_lines = True  # 遇到ethernets时，设置标志为True，开始删除
                elif delete_lines and line.strip():  # 如果标志为True，且当前行不是空行
                    continue  # 跳过该行
                else:
                    delete_lines = False  # 如果不是ethernets下的行，取消删除标志
                    updated_lines.append(line)

            # 将更新后的内容写回文件
            with open(self.netplan_file, 'w') as file:
                file.writelines(updated_lines)

            return True
        except Exception as e:
            self.logger.log(f"修改 Netplan 配置失败：{e}")
            return False

    def apply_netplan_config(self):
        try:
            # 应用 Netplan 配置
            self.base.com("netplan apply")
            self.logger.log(f"执行命令：netplan apply")
            return True
        except Exception as e:
            self.logger.log(f"应用 Netplan 配置失败：{e}")
            return False
