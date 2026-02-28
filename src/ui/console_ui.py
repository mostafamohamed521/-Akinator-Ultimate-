"""
واجهة المستخدم النصية - تفاعل مع اللاعب عبر سطر الأوامر
"""

import os
import sys
import time
from typing import Optional
from datetime import datetime

from ..core.game_engine import GameEngine
from ..models.character import Character
from ..utils.helpers import clear_screen, print_colored, get_terminal_size

class ConsoleUI:
    """
    واجهة المستخدم النصية - تدير التفاعل مع اللاعب
    """
    
    # ألوان النصوص
    COLORS = {
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
    
    def __init__(self, engine: GameEngine):
        """
        تهيئة واجهة المستخدم
        
        Args:
            engine: محرك اللعبة
        """
        self.engine = engine
        self.state = None
    
    def show_main_menu(self):
        """عرض القائمة الرئيسية"""
        while True:
            clear_screen()
            self._print_logo()
            
            print("\n" + "=" * 50)
            print("القائمة الرئيسية".center(50))
            print("=" * 50)
            print("\n1. 🎮 لعبة جديدة")
            print("2. 📖 تعليمات اللعبة")
            print("3. 📊 إحصائيات")
            print("4. 💾 تحميل لعبة محفوظة")
            print("5. ➕ إضافة شخصية جديدة")
            print("6. 🏆 قائمة الشخصيات")
            print("7. ⚙️ إعدادات")
            print("8. 🚪 خروج")
            
            choice = input("\n🔹 اختر رقم: ").strip()
            
            if choice == '1':
                self.start_new_game()
            elif choice == '2':
                self.show_instructions()
            elif choice == '3':
                self.show_statistics()
            elif choice == '4':
                self.load_game_menu()
            elif choice == '5':
                self.add_character_menu()
            elif choice == '6':
                self.show_characters_list()
            elif choice == '7':
                self.show_settings()
            elif choice == '8':
                self._confirm_exit()
            else:
                self._show_error("اختيار غير صحيح. حاول مرة أخرى.")
    
    def start_new_game(self):
        """بدء لعبة جديدة"""
        clear_screen()
        print_colored("🎮 لعبة جديدة", 'green', bold=True)
        print("=" * 40)
        
        print("\n🔹 فكر في شخصية مشهورة...")
        print("🔹 سأطرح عليك أسئلة وأحاول تخمينها!")
        input("\nاضغط Enter للبدء...")
        
        # بدء اللعبة
        self.state = self.engine.new_game()
        self.play_game()
    
    def play_game(self):
        """تشغيل اللعبة"""
        question_count = 0
        
        while True:
            clear_screen()
            
            # عرض التقدم
            self._show_progress()
            
            # الحصول على السؤال التالي
            question = self.engine.get_next_question(self.state)
            
            if question is None:
                # محاولة التخمين
                self._make_guess()
                break
            
            question_count += 1
            
            # عرض السؤال
            print_colored(f"\n📝 سؤال {question_count}:", 'cyan', bold=True)
            print(f"   {question.text}\n")
            
            # عرض الإجابات المحتملة
            print("الإجابات:")
            print("   [1] ✅ نعم")
            print("   [2] ❌ لا")
            print("   [3] 🤔 مش عارف")
            print("   [4] 💾 حفظ اللعبة")
            print("   [5] 🚪 إنهاء")
            
            # الحصول على إجابة المستخدم
            answer = self._get_answer()
            
            if answer == 'save':
                self._save_game()
                continue
            elif answer == 'quit':
                if self._confirm_quit():
                    break
                else:
                    continue
            
            # معالجة الإجابة
            self.state = self.engine.process_answer(self.state, answer)
            
            # التحقق من عدم وجود شخصيات
            if not self.state.possible_characters:
                self._show_no_characters()
                break
    
    def _make_guess(self):
        """محاولة تخمين الشخصية"""
        guess = self.engine.make_guess(self.state)
        
        print_colored("\n🔮 أنا جاهز للتخمين!", 'purple', bold=True)
        time.sleep(1)
        
        if guess:
            print_colored(f"\n🎯 أنا أعتقد أن الشخصية هي: {guess.name}", 'green', bold=True)
            
            if guess.bio:
                print(f"\n📖 {guess.bio}")
            
            print("\nهل توقعتي صحيح؟")
            print("[1] ✅ نعم!")
            print("[2] ❌ لا")
            
            choice = input("\nاختر: ").strip()
            
            if choice == '1':
                self._handle_correct_guess()
            else:
                self._handle_wrong_guess()
        else:
            print_colored("\n❌ لم أستطع تخمين الشخصية!", 'red', bold=True)
            self._learn_character()
    
    def _handle_correct_guess(self):
        """معالجة التخمين الصحيح"""
        print_colored("\n🎉 رائع! لقد فزت!", 'green', bold=True)
        self.engine.stats['successful_guesses'] += 1
        
        # لعب مرة أخرى
        if self._ask_play_again():
            self.start_new_game()
    
    def _handle_wrong_guess(self):
        """معالجة التخمين الخاطئ"""
        self.engine.stats['failed_guesses'] += 1
        print_colored("\n😔 آسف على التخمين الخاطئ!", 'yellow')
        self._learn_character()
    
    def _learn_character(self):
        """تعلم شخصية جديدة من اللاعب"""
        print_colored("\n📚 ساعدني في التعلم!", 'cyan', bold=True)
        
        name = input("🔹 ما اسم الشخصية التي كنت تفكر فيها؟ ").strip()
        
        if not name:
            return
        
        # إضافة الشخصية
        success = self.engine.learn_new_character({
            'id': len(self.engine.characters) + 1,
            'name': name,
            'category': 'غير مصنف',
            'attributes': {
                'is_famous': True,
                'is_alive': self._ask_yes_no("هل الشخصية على قيد الحياة؟")
            }
        })
        
        if success:
            print_colored("✅ شكراً! تعلمت شخصية جديدة!", 'green')
        else:
            print_colored("⚠️ الشخصية موجودة مسبقاً", 'yellow')
        
        if self._ask_play_again():
            self.start_new_game()
    
    def _show_progress(self):
        """عرض تقدم اللعبة"""
        total = len(self.engine.characters)
        remaining = len(self.state.possible_characters)
        percentage = (remaining / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 50)
        print(f"📊 تقدم اللعبة".center(50))
        print("=" * 50)
        
        # شريط التقدم
        bar_length = 30
        filled = int((1 - remaining/total) * bar_length) if total > 0 else 0
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"\n[{bar}] {percentage:.1f}%")
        print(f"🎯 الشخصيات المتبقية: {remaining}")
        print(f"📝 الأسئلة المطروحة: {len(self.state.asked_questions)}")
    
    def _get_answer(self) -> str:
        """الحصول على إجابة المستخدم"""
        while True:
            choice = input("\n➡️ اختر رقم: ").strip()
            
            if choice == '1':
                return 'نعم'
            elif choice == '2':
                return 'لا'
            elif choice == '3':
                return 'مش عارف'
            elif choice == '4':
                return 'save'
            elif choice == '5':
                return 'quit'
            else:
                print_colored("❌ اختيار غير صحيح", 'red')
    
    def _print_logo(self):
        """طباعة شعار اللعبة"""
        logo = """
    ╔═══════════════════════════════════════╗
    ║     🎯 Akinator Ultimate 🎯           ║
    ║     النسخة الموسعة - 1000+ شخصية     ║
    ╚═══════════════════════════════════════╝
        """
        print_colored(logo, 'cyan', bold=True)
    
    def show_instructions(self):
        """عرض تعليمات اللعبة"""
        clear_screen()
        print_colored("📖 تعليمات اللعبة", 'blue', bold=True)
        print("=" * 50)
        print("""
🎯 فكرة اللعبة:
   - فكر في شخصية مشهورة (حقيقية أو خيالية)
   - سأطرح عليك أسئلة للإجابة بنعم/لا/مش عارف
   - بناءً على إجاباتك، سأحاول تخمين الشخصية

💡 نصائح:
   - اختر شخصيات معروفة جيداً
   - أجب بصدق للحصول على نتائج أفضل
   - استخدم "مش عارف" إذا لم تكن متأكداً

🎮 طريقة اللعب:
   1. اختر "لعبة جديدة" من القائمة الرئيسية
   2. فكر في شخصية
   3. أجب على الأسئلة التي أطرحها
   4. شاهد كيف أتتبع الشخصية خطوة بخطوة

➕ إضافة شخصيات:
   - يمكنك إضافة شخصيات جديدة لقاعدة المعرفة
   - ساعدني في التعلم لتحسين دقة التخمين

💾 حفظ اللعبة:
   - يمكنك حفظ اللعبة في أي وقت
   - استكمل اللعب لاحقاً من حيث توقفت

📊 الإحصائيات:
   - تابع إحصائيات أدائي ونسبة نجاحي

🏆 قائمة الشخصيات:
   - تصفح جميع الشخصيات في قاعدة المعرفة

⭐ استمتع باللعبة! ⭐
        """)
        input("\nاضغط Enter للعودة...")
    
    def show_statistics(self):
        """عرض الإحصائيات"""
        clear_screen()
        stats = self.engine.get_statistics()
        
        print_colored("📊 إحصائيات اللعبة", 'purple', bold=True)
        print("=" * 50)
        print(f"""
🎮 عدد الألعاب:          {stats['games_played']}
✅ تخمينات صحيحة:        {stats['successful_guesses']}
❌ تخمينات خاطئة:        {stats['failed_guesses']}
📊 نسبة النجاح:          {stats['success_rate']:.1f}%
📚 عدد الشخصيات:         {stats['total_characters']}
❓ عدد الأسئلة:          {stats['total_questions']}
📝 متوسط الأسئلة:        {stats['average_questions']:.1f}
        """)
        
        input("\nاضغط Enter للعودة...")
    
    def add_character_menu(self):
        """قائمة إضافة شخصية جديدة"""
        clear_screen()
        print_colored("➕ إضافة شخصية جديدة", 'green', bold=True)
        print("=" * 50)
        print("""
📝 أدخل بيانات الشخصية الجديدة:
   (اترك أي حقل فارغاً لتخطيه)
        """)
        
        name = input("🔹 اسم الشخصية: ").strip()
        if not name:
            return
        
        # التحقق من عدم التكرار
        if any(c.name.lower() == name.lower() for c in self.engine.characters):
            print_colored("⚠️ هذه الشخصية موجودة مسبقاً", 'yellow')
            input("\nاضغط Enter للعودة...")
            return
        
        category = input("🔹 التصنيف (فن/رياضة/سياسة/علم/أدب...): ").strip() or "غير مصنف"
        
        # جمع الصفات
        attributes = {}
        
        print("\n🔹 الصفات الأساسية:")
        attributes['gender'] = input("   الجنس (ذكر/أنثى): ").strip()
        attributes['is_alive'] = self._ask_yes_no("   على قيد الحياة؟")
        attributes['is_arab'] = self._ask_yes_no("   عربي/عربية؟")
        
        if attributes['is_arab']:
            attributes['is_egyptian'] = self._ask_yes_no("   مصري/مصرية؟")
        
        attributes['is_famous'] = True
        
        # إنشاء الشخصية
        new_character = {
            'id': len(self.engine.characters) + 1,
            'name': name,
            'category': category,
            'attributes': attributes
        }
        
        if self.engine.learn_new_character(new_character):
            print_colored("\n✅ تم إضافة الشخصية بنجاح!", 'green')
        else:
            print_colored("\n❌ فشل في إضافة الشخصية", 'red')
        
        input("\nاضغط Enter للعودة...")
    
    def show_characters_list(self):
        """عرض قائمة الشخصيات"""
        clear_screen()
        print_colored("🏆 قائمة الشخصيات", 'cyan', bold=True)
        print("=" * 50)
        
        # تجميع الشخصيات حسب التصنيف
        categories = {}
        for char in self.engine.characters:
            if char.category not in categories:
                categories[char.category] = []
            categories[char.category].append(char)
        
        for category, chars in categories.items():
            print_colored(f"\n📁 {category}:", 'yellow', bold=True)
            for i, char in enumerate(chars[:10], 1):  # عرض أول 10 فقط
                status = "✓" if char.get_attribute('is_alive') else "✗"
                print(f"   {i}. {char.name} [{status}]")
            
            if len(chars) > 10:
                print(f"   ... و {len(chars) - 10} أخرى")
        
        print(f"\n📊 إجمالي الشخصيات: {len(self.engine.characters)}")
        input("\nاضغط Enter للعودة...")
    
    def show_settings(self):
        """عرض الإعدادات"""
        clear_screen()
        print_colored("⚙️ الإعدادات", 'blue', bold=True)
        print("=" * 50)
        
        print("""
🔹 قريباً في التحديثات القادمة:
   - تغيير اللغة
   - تخصيص عدد الأسئلة
   - وضع صعوبة
   - تصدير/استيراد البيانات
   - نسخ احتياطي
        """)
        
        input("\nاضغط Enter للعودة...")
    
    def load_game_menu(self):
        """قائمة تحميل لعبة محفوظة"""
        clear_screen()
        print_colored("💾 تحميل لعبة محفوظة", 'purple', bold=True)
        print("=" * 50)
        
        saves_dir = Path("saves")
        if not saves_dir.exists():
            print("\n📂 لا توجد ألعاب محفوظة")
            input("\nاضغط Enter للعودة...")
            return
        
        saves = list(saves_dir.glob("*.json"))
        if not saves:
            print("\n📂 لا توجد ألعاب محفوظة")
            input("\nاضغط Enter للعودة...")
            return
        
        print("\n🔹 الألعاب المحفوظة:")
        for i, save in enumerate(saves, 1):
            modified = datetime.fromtimestamp(save.stat().st_mtime)
            print(f"   {i}. {save.name} ({modified.strftime('%Y-%m-%d %H:%M')})")
        
        print("\n0. العودة")
        
        choice = input("\n🔹 اختر رقماً: ").strip()
        if choice == '0':
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(saves):
                self.load_and_play(saves[idx].name)
            else:
                print_colored("❌ اختيار غير صحيح", 'red')
        except ValueError:
            print_colored("❌ اختيار غير صحيح", 'red')
        
        input("\nاضغط Enter للعودة...")
    
    def load_and_play(self, filename: str):
        """تحميل لعبة واللعب"""
        self.state = self.engine.load_game(filename)
        if self.state:
            print_colored("✅ تم تحميل اللعبة بنجاح!", 'green')
            input("اضغط Enter للمتابعة...")
            self.play_game()
    
    def _save_game(self):
        """حفظ اللعبة الحالية"""
        filename = f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.engine.save_game(self.state, filename)
        print_colored(f"\n✅ تم حفظ اللعبة في {filename}", 'green')
        input("اضغط Enter للمتابعة...")
    
    def _show_no_characters(self):
        """عرض رسالة عدم وجود شخصيات"""
        print_colored("\n❌ لا توجد شخصيات تطابق إجاباتك!", 'red')
        print("🔹 ربما فكرت في شخصية غير موجودة في قاعدة البيانات.")
        
        if self._ask_yes_no("🔹 هل تريد إضافتها؟"):
            self._learn_character()
        elif self._ask_play_again():
            self.start_new_game()
    
    def _ask_play_again(self) -> bool:
        """سؤال اللاعب إذا كان يريد اللعب مرة أخرى"""
        print("\n🔹 هل تريد اللعب مرة أخرى؟")
        return self._ask_yes_no("")
    
    def _ask_yes_no(self, prompt: str) -> bool:
        """سؤال بنعم/لا"""
        while True:
            answer = input(f"{prompt} (نعم/لا): ").strip().lower()
            if answer in ['نعم', 'ن', 'yes', 'y']:
                return True
            elif answer in ['لا', 'ل', 'no', 'n']:
                return False
            print_colored("❌ الرجاء الإجابة بنعم أو لا", 'red')
    
    def _confirm_quit(self) -> bool:
        """تأكيد الخروج من اللعبة"""
        print("\n🔹 هل أنت متأكد من إنهاء اللعبة؟")
        return self._ask_yes_no("")
    
    def _confirm_exit(self):
        """تأكيد الخروج من البرنامج"""
        if self._ask_yes_no("\n🔹 هل أنت متأكد من الخروج؟"):
            print_colored("\n👋 مع السلامة!", 'cyan')
            sys.exit(0)
    
    def _show_error(self, message: str):
        """عرض رسالة خطأ"""
        print_colored(f"\n❌ {message}", 'red')
        time.sleep(2)