#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Akinator Ultimate - لعبة تخمين الشخصيات الذكية
النسخة الموسعة - الرئيسية
"""

import sys
import os
import argparse
from pathlib import Path

# إضافة المسار الرئيسي للـ PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ui.console_ui import ConsoleUI
from src.core.game_engine import GameEngine
from src.utils.logger import setup_logger
from src.data.data_generator import DataGenerator

def parse_arguments():
    """تحليل وسائط سطر الأوامر"""
    parser = argparse.ArgumentParser(
        description='Akinator Ultimate - لعبة تخمين الشخصيات الذكية',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة للاستخدام:
  python main.py                    # تشغيل اللعبة
  python main.py --new-game         # بدء لعبة جديدة مباشرة
  python main.py --generate-data    # توليد بيانات إضافية
  python main.py --stats             # عرض الإحصائيات
  python main.py --load-game save.json  # تحميل لعبة محفوظة
        """
    )
    
    parser.add_argument('--new-game', '-n', 
                       action='store_true',
                       help='بدء لعبة جديدة')
    
    parser.add_argument('--generate-data', '-g',
                       action='store_true',
                       help='توليد بيانات إضافية')
    
    parser.add_argument('--stats', '-s',
                       action='store_true',
                       help='عرض إحصائيات اللعبة')
    
    parser.add_argument('--load-game', '-l',
                       type=str,
                       metavar='FILE',
                       help='تحميل لعبة محفوظة من ملف')
    
    parser.add_argument('--data-path', '-d',
                       type=str,
                       default='data',
                       help='مسار مجلد البيانات (افتراضي: data)')
    
    parser.add_argument('--debug',
                       action='store_true',
                       help='تفعيل وضع التصحيح')
    
    return parser.parse_args()

def main():
    """الدالة الرئيسية"""
    # تحليل الوسائط
    args = parse_arguments()
    
    # إعداد التسجيل
    log_level = 'DEBUG' if args.debug else 'INFO'
    logger = setup_logger('main', level=log_level)
    
    logger.info("=" * 50)
    logger.info("Akinator Ultimate - النسخة الموسعة")
    logger.info("=" * 50)
    
    try:
        # التحقق من مجلد البيانات
        data_path = Path(args.data_path)
        if not data_path.exists():
            logger.warning(f"مجلد البيانات {data_path} غير موجود. سيتم إنشاؤه.")
            data_path.mkdir(parents=True, exist_ok=True)
        
        # تهيئة محرك اللعبة
        logger.info("جاري تهيئة محرك اللعبة...")
        engine = GameEngine(str(data_path))
        
        # معالجة الأوامر
        if args.generate_data:
            logger.info("بدء توليد بيانات إضافية...")
            generator = DataGenerator(data_path)
            generator.generate_all()
            logger.info("تم توليد البيانات بنجاح")
            return
        
        if args.stats:
            stats = engine.get_statistics()
            print("\n" + "=" * 40)
            print("إحصائيات اللعبة".center(40))
            print("=" * 40)
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print("=" * 40 + "\n")
            return
        
        # تهيئة واجهة المستخدم
        ui = ConsoleUI(engine)
        
        # بدء اللعبة
        if args.new_game:
            ui.start_new_game()
        elif args.load_game:
            ui.load_and_play(args.load_game)
        else:
            ui.show_main_menu()
    
    except KeyboardInterrupt:
        logger.info("\nتم إيقاف اللعبة بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        logger.error(f"خطأ غير متوقع: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

    #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Akinator Ultimate - لعبة تخمين الشخصيات الذكية
"""

import sys
import os
import argparse
from pathlib import Path

# إضافة المسار الرئيسي للـ PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.ui.console_ui import ConsoleUI
    from src.core.game_engine import GameEngine
    from src.utils.logger import setup_logger
except ImportError as e:
    print(f"❌ خطأ في استيراد الملفات: {e}")
    print("تأكد من وجود جميع الملفات في المجلد src/")
    sys.exit(1)

def main():
    """الدالة الرئيسية"""
    # إعداد التسجيل
    logger = setup_logger('main')
    
    print("\n" + "=" * 50)
    print("🎯 Akinator Ultimate - النسخة الموسعة".center(50))
    print("=" * 50 + "\n")
    
    try:
        # تهيئة محرك اللعبة
        print("جاري تحميل البيانات...")
        engine = GameEngine("data")
        
        # تهيئة واجهة المستخدم
        ui = ConsoleUI(engine)
        
        # بدء اللعبة
        ui.show_main_menu()
        
    except KeyboardInterrupt:
        print("\n\n👋 مع السلامة!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"خطأ غير متوقع: {e}", exc_info=True)
        print(f"\n❌ حدث خطأ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()