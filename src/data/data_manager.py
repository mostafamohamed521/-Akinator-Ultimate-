"""
إدارة البيانات - تحميل وحفظ البيانات
"""

import json
from pathlib import Path
from typing import List, Dict
from ..models.character import Character
from ..models.question import Question
from ..utils.logger import setup_logger

class DataManager:
    """
    إدارة تحميل وحفظ البيانات من وإلى الملفات
    """
    
    def __init__(self, data_path: str = "data"):
        """
        تهيئة مدير البيانات
        
        Args:
            data_path: مسار مجلد البيانات
        """
        self.data_path = Path(data_path)
        self.logger = setup_logger('data_manager')
        
        # التأكد من وجود المجلدات
        self.characters_path = self.data_path / "characters"
        self.questions_path = self.data_path / "questions"
        
        self.characters_path.mkdir(parents=True, exist_ok=True)
        self.questions_path.mkdir(parents=True, exist_ok=True)
    
    def load_all_characters(self) -> List[Character]:
        """تحميل جميع الشخصيات"""
        characters = []
        
        for file_path in self.characters_path.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if 'characters' in data:
                    for char_data in data['characters']:
                        characters.append(Character.from_dict(char_data))
                else:
                    # ملف واحد لشخصية واحدة
                    characters.append(Character.from_dict(data))
                    
            except Exception as e:
                self.logger.error(f"خطأ في تحميل {file_path}: {e}")
        
        self.logger.info(f"تم تحميل {len(characters)} شخصية")
        return characters
    
    def load_all_questions(self) -> List[Question]:
        """تحميل جميع الأسئلة"""
        questions = []
        
        for file_path in self.questions_path.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if 'questions' in data:
                    for q_data in data['questions']:
                        questions.append(Question.from_dict(q_data))
                        
            except Exception as e:
                self.logger.error(f"خطأ في تحميل {file_path}: {e}")
        
        self.logger.info(f"تم تحميل {len(questions)} سؤال")
        return questions
    
    def save_character(self, character: Character):
        """حفظ شخصية جديدة"""
        try:
            # تحديد التصنيف المناسب
            category_file = self._get_category_file(character.category)
            
            # تحميل الملف الحالي
            if category_file.exists():
                with open(category_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {'characters': []}
            
            # إضافة الشخصية
            data['characters'].append(character.to_dict())
            
            # حفظ الملف
            with open(category_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"تم حفظ الشخصية {character.name}")
            
        except Exception as e:
            self.logger.error(f"خطأ في حفظ الشخصية: {e}")
    
    def _get_category_file(self, category: str) -> Path:
        """الحصول على مسار ملف التصنيف"""
        # تحويل اسم التصنيف إلى اسم ملف مناسب
        category_map = {
            'رياضة': 'sports.json',
            'فن': 'entertainment.json',
            'علوم': 'science.json',
            'سياسة': 'politics.json',
            'أدب': 'literature.json',
            'دين': 'religion.json',
            'تاريخ': 'historical.json',
            'غير مصنف': 'others.json'
        }
        
        filename = category_map.get(category, 'others.json')
        return self.characters_path / filename