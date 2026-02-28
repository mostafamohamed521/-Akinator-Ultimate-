"""
كلاس حالة اللعبة - يمثل حالة اللعبة الحالية
"""

from typing import List, Dict, Optional
from .character import Character
from .question import Question

class GameState:
    """
    حالة اللعبة - تحتوي على جميع معلومات اللعبة الجارية
    """
    
    def __init__(self,
                 game_id: str,
                 possible_characters: List[Character],
                 asked_questions: List[Question],
                 answers: Dict[int, str],
                 current_question: Optional[Question] = None):
        """
        تهيئة حالة اللعبة
        
        Args:
            game_id: معرف فريد للعبة
            possible_characters: قائمة الشخصيات المحتملة
            asked_questions: الأسئلة التي تم طرحها
            answers: قاموس الإجابات (رقم السؤال => الإجابة)
            current_question: السؤال الحالي
        """
        self.game_id = game_id
        self.possible_characters = possible_characters
        self.asked_questions = asked_questions
        self.answers = answers
        self.current_question = current_question
    
    def get_answered_questions_count(self) -> int:
        """عدد الأسئلة التي تمت الإجابة عليها"""
        return len(self.asked_questions)
    
    def get_remaining_characters_count(self) -> int:
        """عدد الشخصيات المتبقية"""
        return len(self.possible_characters)
    
    def get_progress_percentage(self, total_characters: int) -> float:
        """نسبة التقدم في اللعبة"""
        if total_characters == 0:
            return 0
        return (1 - len(self.possible_characters) / total_characters) * 100