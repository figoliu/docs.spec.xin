#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
访问控制配置模块 - 关联需求FR-005

此模块提供静态文档站点的访问控制配置功能，包括：
1. 用户认证配置
2. 基于角色的权限管理
3. API密钥验证
4. 访问日志记录
5. 安全设置
"""

import json
import os
import time
from typing import Dict, List, Optional, Any

class AccessControlConfig:
    """访问控制配置类"""
    
    def __init__(self, config_file: str = None):
        """初始化访问控制配置
        
        Args:
            config_file: 配置文件路径，默认为None
        """
        self.config_file = config_file or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            '.config', 'access_control.json'
        )
        self._config = self._load_config()
        self._ensure_config_directory()
    
    def _ensure_config_directory(self):
        """确保配置目录存在"""
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件
        
        Returns:
            配置字典
        """
        default_config = {
            "authentication": {
                "enabled": True,
                "methods": ["api_key", "basic_auth"],
                "token_expiry": 3600,  # 1小时
                "max_login_attempts": 5,
                "lockout_duration": 300  # 5分钟
            },
            "authorization": {
                "roles": {
                    "admin": {
                        "permissions": ["read:all", "write:all", "admin:all"],
                        "description": "系统管理员，拥有所有权限"
                    },
                    "editor": {
                        "permissions": ["read:all", "write:docs"],
                        "description": "文档编辑者，可以阅读所有内容并编辑文档"
                    },
                    "viewer": {
                        "permissions": ["read:public"],
                        "description": "普通查看者，只能访问公开内容"
                    },
                    "guest": {
                        "permissions": ["read:limited"],
                        "description": "访客，只能访问有限的公开内容"
                    }
                },
                "default_role": "guest"
            },
            "api_keys": {
                "enabled": True,
                "rotation_interval": 2592000,  # 30天
                "required_for": ["search", "api", "admin"]
            },
            "rate_limiting": {
                "enabled": True,
                "limits": {
                    "anonymous": {"requests": 60, "period": 60},  # 每分钟60次
                    "authenticated": {"requests": 300, "period": 60}  # 每分钟300次
                }
            },
            "logging": {
                "enabled": True,
                "log_file": ".logs/access.log",
                "log_level": "INFO",
                "log_format": "%(asctime)s - %(client_ip)s - %(user_id)s - %(action)s - %(status)s - %(message)s",
                "retention_days": 30
            },
            "security": {
                "cors": {
                    "enabled": True,
                    "allowed_origins": ["*"],
                    "allowed_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                    "allowed_headers": ["Authorization", "Content-Type"]
                },
                "ssl": {
                    "required": True,
                    "redirect_http": True
                },
                "x_headers": {
                    "enabled": True,
                    "headers": {
                        "X-Content-Type-Options": "nosniff",
                        "X-Frame-Options": "DENY",
                        "X-XSS-Protection": "1; mode=block",
                        "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
                    }
                }
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并用户配置和默认配置
                    return self._merge_configs(default_config, user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return default_config
        
        return default_config
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """合并配置字典
        
        Args:
            default: 默认配置
            user: 用户配置
            
        Returns:
            合并后的配置
        """
        merged = default.copy()
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    def save(self) -> bool:
        """保存配置到文件
        
        Returns:
            是否保存成功
        """
        try:
            self._ensure_config_directory()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """获取完整配置
        
        Returns:
            配置字典
        """
        return self._config
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """更新配置
        
        Args:
            updates: 要更新的配置项
            
        Returns:
            是否更新成功
        """
        try:
            self._config = self._merge_configs(self._config, updates)
            return self.save()
        except Exception as e:
            print(f"更新配置失败: {e}")
            return False
    
    def add_role(self, role_name: str, permissions: List[str], description: str = "") -> bool:
        """添加新角色
        
        Args:
            role_name: 角色名称
            permissions: 权限列表
            description: 角色描述
            
        Returns:
            是否添加成功
        """
        if role_name in self._config["authorization"]["roles"]:
            print(f"角色 {role_name} 已存在")
            return False
        
        self._config["authorization"]["roles"][role_name] = {
            "permissions": permissions,
            "description": description
        }
        return self.save()
    
    def has_permission(self, role: str, permission: str) -> bool:
        """检查角色是否有指定权限
        
        Args:
            role: 角色名称
            permission: 权限字符串
            
        Returns:
            是否有权限
        """
        if role not in self._config["authorization"]["roles"]:
            role = self._config["authorization"]["default_role"]
        
        role_permissions = self._config["authorization"]["roles"][role]["permissions"]
        
        # 检查精确匹配
        if permission in role_permissions:
            return True
        
        # 检查通配符匹配（如 read:all 匹配所有 read:* 权限）
        for perm in role_permissions:
            if perm.endswith(":all"):
                prefix = perm[:-4]
                if permission.startswith(prefix + ":"):
                    return True
        
        return False
    
    def generate_api_key_config(self, user_id: str, roles: List[str], expiry: Optional[int] = None) -> Dict[str, Any]:
        """生成API密钥配置
        
        Args:
            user_id: 用户ID
            roles: 用户角色列表
            expiry: 过期时间（秒），None表示使用默认值
            
        Returns:
            API密钥配置
        """
        if expiry is None:
            expiry = self._config["authentication"]["token_expiry"]
        
        return {
            "user_id": user_id,
            "roles": roles,
            "created_at": int(time.time()),
            "expires_at": int(time.time()) + expiry,
            "last_used": None,
            "permissions": self._get_effective_permissions(roles)
        }
    
    def _get_effective_permissions(self, roles: List[str]) -> List[str]:
        """获取角色列表的有效权限
        
        Args:
            roles: 角色列表
            
        Returns:
            合并后的权限列表
        """
        permissions = set()
        for role in roles:
            if role in self._config["authorization"]["roles"]:
                permissions.update(self._config["authorization"]["roles"][role]["permissions"])
        return list(permissions)
    
    def validate_access(self, user_roles: List[str], required_permission: str) -> bool:
        """验证用户是否有访问权限
        
        Args:
            user_roles: 用户角色列表
            required_permission: 所需权限
            
        Returns:
            是否有权限访问
        """
        # 检查用户的每个角色是否有指定权限
        for role in user_roles:
            if self.has_permission(role, required_permission):
                return True
        
        # 如果没有指定角色，检查默认角色
        if not user_roles:
            return self.has_permission(self._config["authorization"]["default_role"], required_permission)
        
        return False

def main():
    """主函数 - 用于演示和测试访问控制配置"""
    # 创建访问控制配置实例
    access_config = AccessControlConfig()
    
    # 打印当前配置
    print("当前访问控制配置:")
    print(json.dumps(access_config.get_config(), indent=2, ensure_ascii=False))
    
    # 示例：验证权限
    test_role = "editor"
    test_permission = "write:docs"
    has_perm = access_config.has_permission(test_role, test_permission)
    print(f"\n角色 '{test_role}' 是否有 '{test_permission}' 权限: {has_perm}")
    
    # 示例：验证用户访问
    user_roles = ["viewer"]
    required_perm = "write:docs"
    can_access = access_config.validate_access(user_roles, required_perm)
    print(f"用户角色 {user_roles} 是否可以访问需要 '{required_perm}' 权限的资源: {can_access}")
    
    # 示例：生成API密钥配置
    api_key_config = access_config.generate_api_key_config("test_user", ["editor", "viewer"])
    print("\n生成的API密钥配置:")
    print(json.dumps(api_key_config, indent=2))

if __name__ == "__main__":
    main()