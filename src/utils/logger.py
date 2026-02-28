"""
نظام تسجيل الأحداث
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """
    إعداد logger جديد
    
    Args:
        name: اسم الـ logger
        level: مستوى التسجيل (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        logging.Logger: الـ logger المعد
    """
    # إنشاء مجلد logs إذا لم يكن موجوداً
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # إعداد الـ logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # منع تكرار الـ handlers
    if logger.handlers:
        return logger
    
    # formatter موحد
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler للملف
    log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler للكونسول
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger