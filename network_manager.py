#! /usr/bin/env python3
from base import Base


class NetworkManager:
    def __init__(self, logger):
        self.base = Base(logger)
        self.logger = logger
        self.network_manager_config = "/etc/NetworkManager/NetworkManager.conf"
        self.netplan_file = '/etc/netplan/01-netcfg.yaml'

    def set_network_manager_interfaces(self):
        try:

            # 修改权限
            # command = (f"sudo chmod 666 {self.network_manager_config}")
            # self.base.com(command)
            # self.logger.log("修改/etc/fstab文件权限为666")

            # 修改 NetworkManager 配置文件
            config_content = ""
            with open(self.network_manager_config, "r") as f:
                config_content = f.read()

            config_content = config_content.replace(
                "managed=false", "managed=true")

            with open(self.network_manager_config, "w") as f:
                f.write(config_content)

            # 修改权限
            # command = (f"sudo chmod 644 {self.network_manager_config}")
            # self.base.com(command)
            # self.logger.log("修改/etc/fstab文件权限为644")

            return True
        except Exception as e:
            print(f"配置 NetworkManager 管理接口失败：{e}")
            return False

    def restart_network_manager_service(self):
        try:
            # 重启 NetworkManager 服务
            self.base.com("sudo systemctl restart NetworkManager.service")
            return True
        except Exception as e:
            self.logger.log(f"重启 NetworkManager 服务失败：{e}")
            return False

    def update_netplan_config(self):
        try:

            # 修改权限
            # command = (f"sudo chmod 666 {self.netplan_file}")
            # self.base.com(command)
            # self.logger.log("修改/etc/fstab文件权限为666")

            # 打开 netplan 配置文件进行修改
            with open(self.netplan_file, 'r') as file:
                lines = file.readlines()

            updated_lines = []
            for line in lines:
                # 将 renderer:networkd 更改为 renderer:NetworkManager
                if 'renderer: networkd' in line:
                    updated_lines.append(line.replace(
                        'renderer: networkd', 'renderer: NetworkManager'))
                # 删除 ethernets 和其他配置
                elif 'ethernets' in line:
                    while '  ' in line:
                        line = line.replace('  ', ' ')
                    if line.strip() == 'ethernets:':
                        continue
                updated_lines.append(line)

            # 将更新后的内容写回文件
            with open(self.netplan_file, 'w') as file:
                file.writelines(updated_lines)

            # 修改权限
            # command = (f"sudo chmod 644 {self.netplan_file}")
            # self.base.com(command)
            # self.logger.log("修改/etc/fstab文件权限为644")

            return True
        except Exception as e:
            self.logger.log(f"修改 Netplan 配置失败：{e}")
            return False

    def apply_netplan_config(self):
        try:
            # 应用 Netplan 配置
            self.base.com("sudo netplan apply")
            return True
        except Exception as e:
            self.logger.log(f"应用 Netplan 配置失败：{e}")
            return False
