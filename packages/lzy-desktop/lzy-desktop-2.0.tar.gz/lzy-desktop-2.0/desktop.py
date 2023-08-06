import winreg
def desktop(name):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)
    return winreg.QueryValueEx(key, "Desktop")[0]+RF'\{name}'
