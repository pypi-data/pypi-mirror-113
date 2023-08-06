# C互換ライブラリ呼び出しモジュール
from ctypes import windll, Structure, byref, wintypes
# 必要なAPI (kernel32)をロード
class cutil:
    stdout_handle = windll.kernel32.GetStdHandle(-11)
    GetConsoleInfo = windll.kernel32.GetConsoleScreenBufferInfo
    SetConsoleAttribute = windll.kernel32.SetConsoleTextAttribute

    class console_screen_buffer_info(Structure):
        _fields_ = [("dwSize", wintypes._COORD),
                    ("dwCursorPosition", wintypes._COORD),
                    ("wAttributes", wintypes.WORD),
                    ("srWindow", wintypes.SMALL_RECT),
                    ("dwMaximumWindowSize", wintypes._COORD)]

# 現状の色設定を取得
info_ = cutil.console_screen_buffer_info()
cutil.GetConsoleInfo(cutil.stdout_handle, byref(info_))
# 文字色(foreground color)を変更
fg_color = 0x0004 | 0x0008
cutil.SetConsoleAttribute(cutil.stdout_handle,
                           fg_color | info_.wAttributes & 0x0070)
# 標準出力
print("some text")
# もとの色設定に戻す
cutil.SetConsoleAttribute(cutil.stdout_handle, info_.wAttributes)