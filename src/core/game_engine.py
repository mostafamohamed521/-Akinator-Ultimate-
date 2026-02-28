"""
محرك اللعبة الرئيسي - يدير تدفق اللعبة بالكامل
"""

import json
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path

from ..models.character import Character
from ..models.question import Question
from ..models.game_state import GameState
from ..ai.decision_tree import DecisionTree
from ..ai.entropy_calculator import EntropyCalculator
from ..data.data_manager import DataManager
from ..utils.logger import setup_logger

class GameEngine:
    """
    المحرك الرئيسي للعبة - مسؤول عن إدارة اللعبة وتدفق الأسئلة
    """
    
    def __init__(self, data_path: str = "data"):
        """
        تهيئة محرك اللعبة
        
        Args:
            data_path: مسار مجلد البيانات
        """
        self.logger = setup_logger('game_engine')
        self.logger.info("جاري تهيئة محرك اللعبة...")
        
        # تحميل البيانات
        self.data_manager = DataManager(data_path)
        self.characters = self.data_manager.load_all_characters()
        self.questions = self.data_manager.load_all_questions()
        self.categories = self.data_manager.load_categories()
        
        # تهيئة مكونات الذكاء الاصطناعي
        self.entropy_calculator = EntropyCalculator()
        self.decision_tree = DecisionTree(self.characters, self.questions)
        
        # إحصائيات اللعبة
        self.stats = {
            'games_played': 0,
            'successful_guesses': 0,
            'failed_guesses': 0,
            'average_questions': 0
        }
        
        self.logger.info(f"تم تحميل {len(self.characters)} شخصية و {len(self.questions)} سؤال")
    
    def new_game(self) -> GameState:
        """
        بدء لعبة جديدة
        
        Returns:
            حالة اللعبة الجديدة
        """
        self.logger.info("بدء لعبة جديدة")
        self.stats['games_played'] += 1
        
        state = GameState(
            game_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            possible_characters=self.characters.copy(),
            asked_questions=[],
            answers={},
            current_question=None
        )
        
        return state
    
    def get_next_question(self, state: GameState) -> Optional[Question]:
        """
        تحديد السؤال التالي بناءً على الإجابات السابقة
        
        Args:
            state: حالة اللعبة الحالية
            
        Returns:
            السؤال التالي أو None إذا انتهت اللعبة
        """
        if len(state.possible_characters) <= 3:
            return None
        
        # حساب الأنتروبي لكل سؤال
        best_question = None
        max_entropy = -1
        
        available_questions = [
            q for q in self.questions 
            if q.id not in [aq.id for aq in state.asked_questions]
        ]
        
        for question in available_questions:
            entropy = self.entropy_calculator.calculate_question_entropy(
                state.possible_characters,
                question
            )
            
            if entropy > max_entropy:
                max_entropy = entropy
                best_question = question
        
        if best_question:
            state.current_question = best_question
            state.asked_questions.append(best_question)
            self.logger.debug(f"تم اختيار سؤال: {best_question.text} (entropy: {max_entropy:.3f})")
        
        return best_question
    
    def process_answer(self, state: GameState, answer: str) -> GameState:
        """
        معالجة إجابة المستخدم وتحديث قائمة الشخصيات المحتملة
        
        Args:
            state: حالة اللعبة الحالية
            answer: إجابة المستخدم (نعم/لا/مش عارف)
            
        Returns:
            حالة اللعبة المحدثة
        """
        if not state.current_question:
            return state
        
        # تسجيل الإجابة
        state.answers[state.current_question.id] = answer
        
        # تصفية الشخصيات حسب الإجابة
        filtered_characters = []
        
        for character in state.possible_characters:
            char_value = character.get_attribute(state.current_question.attribute)
            
            if answer == 'نعم' and char_value == state.current_question.expected_answer:
                filtered_characters.append(character)
            elif answer == 'لا' and char_value != state.current_question.expected_answer:
                filtered_characters.append(character)
            elif answer == 'مش عارف':
                # في حالة مش عارف، نحتفظ بالشخصية
                filtered_characters.append(character)
        
        state.possible_characters = filtered_characters
        state.current_question = None
        
        self.logger.debug(f"بعد التصفية: {len(state.possible_characters)} شخصية متبقية")
        
        return state
    
    def make_guess(self, state: GameState) -> Optional[Character]:
        """
        محاولة تخمين الشخصية
        
        Args:
            state: حالة اللعبة الحالية
            
        Returns:
            الشخصية المتوقعة أو None
        """
        if len(state.possible_characters) == 0:
            return None
        
        # اختيار الشخصية الأكثر احتمالية
        best_character = state.possible_characters[0]
        
        # حساب الثقة في التخمين
        confidence = 1.0 / len(state.possible_characters)
        
        self.logger.info(f"تم التخمين: {best_character.name} (ثقة: {confidence:.2%})")
        
        return best_character
    
    def learn_new_character(self, character_data: Dict):
        """
        إضافة شخصية جديدة إلى قاعدة المعرفة
        
        Args:
            character_data: بيانات الشخصية الجديدة
        """
        new_character = Character.from_dict(character_data)
        
        # التحقق من عدم وجود الشخصية مسبقاً
        if any(c.name == new_character.name for c in self.characters):
            self.logger.warning(f"الشخصية {new_character.name} موجودة مسبقاً")
            return False
        
        self.characters.append(new_character)
        self.data_manager.save_character(new_character)
        
        # إعادة بناء شجرة القرارات
        self.decision_tree.rebuild(self.characters, self.questions)
        
        self.logger.info(f"تم إضافة شخصية جديدة: {new_character.name}")
        return True
    
    def get_statistics(self) -> Dict:
        """
        الحصول على إحصائيات اللعبة
        
        Returns:
            قاموس الإحصائيات
        """
        if self.stats['games_played'] > 0:
            success_rate = (self.stats['successful_guesses'] / 
                          self.stats['games_played'] * 100)
        else:
            success_rate = 0
        
        return {
            **self.stats,
            'total_characters': len(self.characters),
            'total_questions': len(self.questions),
            'success_rate': success_rate
        }
    
    def save_game(self, state: GameState, filename: str):
        """
        حفظ حالة اللعبة
        
        Args:
            state: حالة اللعبة
            filename: اسم الملف
        """
        data = {
            'game_id': state.game_id,
            'possible_characters': [c.to_dict() for c in state.possible_characters],
            'asked_questions': [q.to_dict() for q in state.asked_questions],
            'answers': state.answers,
            'timestamp': datetime.now().isoformat()
        }
        
        save_path = Path("saves") / filename
        save_path.parent.mkdir(exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"تم حفظ اللعبة في {save_path}")
    
    def load_game(self, filename: str) -> Optional[GameState]:
        """
        تحميل حالة لعبة محفوظة
        
        Args:
            filename: اسم الملف
            
        Returns:
            حالة اللعبة المحملة أو None
        """
        load_path = Path("saves") / filename
        
        if not load_path.exists():
            self.logger.error(f"الملف {filename} غير موجود")
            return None
        
        with open(load_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # إعادة بناء الكائنات
        state = GameState(
            game_id=data['game_id'],
            possible_characters=[
                Character.from_dict(c) for c in data['possible_characters']
            ],
            asked_questions=[
                Question.from_dict(q) for q in data['asked_questions']
            ],
            answers=data['answers'],
            current_question=None
        )
        
        self.logger.info(f"تم تحميل اللعبة من {load_path}")
        return state