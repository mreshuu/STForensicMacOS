"""
Kullanıcı Analizi Modülü
"""

import os
import pwd
import grp
from typing import Dict, Any, List
from .base_module import BaseModule
from ..utils.helpers import run_command


class UsersModule(BaseModule):
    """Kullanıcı analizi modülü"""
    
    description = "Kullanıcı analizi"
    version = "1.0.0"
    
    def _analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Kullanıcı bilgilerini analiz et"""
        data = {}
        
        try:
            # Kullanıcı hesapları
            data["user_accounts"] = self._get_user_accounts()
            
            # Grup bilgileri
            data["group_info"] = self._get_group_info()
            
            # Yetki seviyeleri
            data["permissions"] = self._get_permissions()
            
            # Oturum bilgileri
            data["session_info"] = self._get_session_info()
            
            # Kullanıcı aktiviteleri
            data["user_activities"] = self._get_user_activities()
            
            # Sistem kullanıcıları
            data["system_users"] = self._get_system_users()
            
        except Exception as e:
            self.add_error(f"Kullanıcı analizi sırasında hata: {str(e)}")
        
        return data
    
    def _get_user_accounts(self) -> List[Dict[str, Any]]:
        """Kullanıcı hesapları"""
        users: List[Dict[str, Any]] = []
        
        try:
            # dscl ile kullanıcı listesini al
            code, stdout, stderr = run_command("dscl . -list /Users")
            if code == 0:
                user_list = stdout.strip().split('\n')
                for username in user_list:
                    if username.strip():
                        user_info = self._get_user_details(username.strip())
                        if user_info:
                            users.append(user_info)
            
            # Alternatif olarak pwd modülünü kullan
            if not users:
                for user in pwd.getpwall():
                    users.append({
                        "username": user.pw_name,
                        "uid": user.pw_uid,
                        "gid": user.pw_gid,
                        "home": user.pw_dir,
                        "shell": user.pw_shell,
                        "description": user.pw_gecos
                    })
            
        except Exception as e:
            self.add_error(f"Kullanıcı hesapları alınırken hata: {str(e)}")
        
        return users
    
    def _get_user_details(self, username: str) -> Dict[str, Any]:
        """Kullanıcı detayları"""
        user_info: Dict[str, Any] = {"username": username}
        
        try:
            # dscl ile kullanıcı detaylarını al
            code, stdout, stderr = run_command(f"dscl . -read /Users/{username}")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        user_info[key.strip()] = value.strip()
            
            # UID bilgisi
            code, stdout, stderr = run_command(f"id -u {username}")
            if code == 0:
                try:
                    user_info['uid'] = int(stdout.strip())
                except ValueError:
                    pass
            
            # Grup bilgisi
            code, stdout, stderr = run_command(f"id -g {username}")
            if code == 0:
                try:
                    user_info['gid'] = int(stdout.strip())
                except ValueError:
                    pass
            
            # Grup listesi
            code, stdout, stderr = run_command(f"id -G {username}")
            if code == 0:
                try:
                    user_info['groups'] = [int(g) for g in stdout.strip().split()]
                except ValueError:
                    pass
            
        except Exception as e:
            self.add_warning(f"Kullanıcı {username} detayları alınırken hata: {str(e)}")
        
        return user_info
    
    def _get_group_info(self) -> List[Dict[str, Any]]:
        """Grup bilgileri"""
        groups: List[Dict[str, Any]] = []
        
        try:
            # dscl ile grup listesini al
            code, stdout, stderr = run_command("dscl . -list /Groups")
            if code == 0:
                group_list = stdout.strip().split('\n')
                for groupname in group_list:
                    if groupname.strip():
                        group_info = self._get_group_details(groupname.strip())
                        if group_info:
                            groups.append(group_info)
            
            # Alternatif olarak grp modülünü kullan
            if not groups:
                for group in grp.getgrall():
                    groups.append({
                        "groupname": group.gr_name,
                        "gid": group.gr_gid,
                        "members": group.gr_mem
                    })
            
        except Exception as e:
            self.add_error(f"Grup bilgileri alınırken hata: {str(e)}")
        
        return groups
    
    def _get_group_details(self, groupname: str) -> Dict[str, Any]:
        """Grup detayları"""
        group_info: Dict[str, Any] = {"groupname": groupname}
        
        try:
            # dscl ile grup detaylarını al
            code, stdout, stderr = run_command(f"dscl . -read /Groups/{groupname}")
            if code == 0:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        group_info[key.strip()] = value.strip()
            
            # GID bilgisi
            code, stdout, stderr = run_command(f"dscl . -read /Groups/{groupname} PrimaryGroupID")
            if code == 0:
                try:
                    gid = stdout.strip().split()[-1]
                    group_info['gid'] = int(gid)
                except (ValueError, IndexError):
                    pass
            
            # Üye listesi
            code, stdout, stderr = run_command(f"dscl . -read /Groups/{groupname} GroupMembership")
            if code == 0:
                try:
                    members = stdout.strip().split()[1:]  # İlk kelime "GroupMembership"
                    group_info['members'] = members
                except IndexError:
                    pass
            
        except Exception as e:
            self.add_warning(f"Grup {groupname} detayları alınırken hata: {str(e)}")
        
        return group_info
    
    def _get_permissions(self) -> Dict[str, Any]:
        """Yetki seviyeleri"""
        permissions: Dict[str, Any] = {}
        
        try:
            # Sudo yetkisi olan kullanıcılar
            code, stdout, stderr = run_command("dscl . -read /Groups/admin GroupMembership")
            if code == 0:
                admin_users = stdout.strip().split()[1:]  # İlk kelime "GroupMembership"
                permissions['admin_users'] = admin_users
            
            # Wheel grubu üyeleri
            code, stdout, stderr = run_command("dscl . -read /Groups/wheel GroupMembership")
            if code == 0:
                wheel_users = stdout.strip().split()[1:]
                permissions['wheel_users'] = wheel_users
            
            # Sudoers dosyası
            code, stdout, stderr = run_command("cat /etc/sudoers")
            if code == 0:
                permissions['sudoers'] = stdout.strip()
            
            # Sudoers.d dizini
            code, stdout, stderr = run_command("ls -la /etc/sudoers.d/")
            if code == 0:
                permissions['sudoers_d'] = stdout.strip()
            
        except Exception as e:
            self.add_error(f"Yetki seviyeleri alınırken hata: {str(e)}")
        
        return permissions
    
    def _get_session_info(self) -> Dict[str, Any]:
        """Oturum bilgileri"""
        session: Dict[str, Any] = {}
        
        try:
            # Aktif oturumlar
            code, stdout, stderr = run_command("who")
            if code == 0:
                session['active_sessions'] = stdout.strip()
            
            # Son giriş bilgileri
            code, stdout, stderr = run_command("last")
            if code == 0:
                session['login_history'] = stdout.strip()
            
            # Şu anki kullanıcı
            session['current_user'] = os.getenv('USER', 'unknown')
            session['current_uid'] = os.getuid()
            session['current_gid'] = os.getgid()
            
            # Çevre değişkenleri
            session['environment'] = {
                'HOME': os.getenv('HOME'),
                'SHELL': os.getenv('SHELL'),
                'PATH': os.getenv('PATH'),
                'TERM': os.getenv('TERM')
            }
            
        except Exception as e:
            self.add_error(f"Oturum bilgileri alınırken hata: {str(e)}")
        
        return session
    
    def _get_user_activities(self) -> Dict[str, Any]:
        """Kullanıcı aktiviteleri"""
        activities: Dict[str, Any] = {}
        
        try:
            # Son komutlar (bash history)
            code, stdout, stderr = run_command("tail -50 ~/.bash_history")
            if code == 0:
                activities['bash_history'] = stdout.strip()
            
            # Zsh history
            code, stdout, stderr = run_command("tail -50 ~/.zsh_history")
            if code == 0:
                activities['zsh_history'] = stdout.strip()
            
            # Login window durumu
            code, stdout, stderr = run_command("defaults read /Library/Preferences/com.apple.loginwindow")
            if code == 0:
                activities['loginwindow_prefs'] = stdout.strip()
            
            # Otomatik giriş
            code, stdout, stderr = run_command("defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser")
            if code == 0:
                activities['auto_login_user'] = stdout.strip()
            
        except Exception as e:
            self.add_error(f"Kullanıcı aktiviteleri alınırken hata: {str(e)}")
        
        return activities
    
    def _get_system_users(self) -> List[Dict[str, Any]]:
        """Sistem kullanıcıları"""
        system_users: List[Dict[str, Any]] = []
        
        try:
            # Sistem kullanıcılarını filtrele
            for user in pwd.getpwall():
                if user.pw_uid < 500:  # Sistem kullanıcıları genellikle 500'den küçük UID'ye sahiptir
                    system_users.append({
                        "username": user.pw_name,
                        "uid": user.pw_uid,
                        "gid": user.pw_gid,
                        "home": user.pw_dir,
                        "shell": user.pw_shell,
                        "description": user.pw_gecos
                    })
            
        except Exception as e:
            self.add_error(f"Sistem kullanıcıları alınırken hata: {str(e)}")
        
        return system_users 