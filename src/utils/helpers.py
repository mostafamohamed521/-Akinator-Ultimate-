"""
دوال مساعدة للعبة
"""

import os
import sys
from typing import Optional

def clear_screen():
    """مسح الشاشة"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text: str, color: str = 'white', bold: bool = False):
    """
    طباعة نص ملون
    
    Args:
        text: النص المراد طباعته
        color: اللون (red, green, yellow, blue, purple, cyan, white)
        bold: هل النص عريض
    """
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m'
    }
    
    if bold:
        print(f"{colors['bold']}{colors.get(color, colors['white'])}{text}{colors['reset']}")
    else:
        print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def get_terminal_size() -> tuple:
    """الحصول على حجم الطرفية"""
    try:
        columns, rows = os.get_terminal_size()
        return columns, rows
    except:
        return 80, 24

def validate_yes_no(answer: str) -> Optional[bool]:
    """
    التحقق من إجابة بنعم/لا
    
    Args:
        answer: الإجابة المدخلة
        
    Returns:
        True لنعم، False للا، None إذا كانت الإجابة غير صالحة
    """
    answer = answer.strip().lower()
    if answer in ['نعم', 'ن', 'yes', 'y', '1']:
        return True
    elif answer in ['لا', 'ل', 'no', 'n', '0']:
        return False
    return None