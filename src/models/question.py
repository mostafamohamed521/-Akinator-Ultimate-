"""
كلاس السؤال - يمثل سؤالاً في اللعبة
"""

from typing import Dict, Any, Optional

class Question:
    """
    كلاس السؤال - يحتوي على بيانات السؤال وكيفية تقييمه
    """
    
    def __init__(self, 
                 id: int,
                 text: str,
                 attribute: str,
                 expected_answer: Any,
                 category: str = "basic",
                 difficulty: int = 1):
        """
        تهيئة سؤال جديد
        
        Args:
            id: معرف فريد للسؤال
            text: نص السؤال
            attribute: الصفة التي يختبرها السؤال
            expected_answer: القيمة المتوقعة للإجابة "نعم"
            category: تصنيف السؤال (basic, profession, etc.)
            difficulty: صعوبة السؤال (1-5)
        """
        self.id = id
        self.text = text
        self.attribute = attribute
        self.expected_answer = expected_answer
        self.category = category
        self.difficulty = difficulty
    
    def evaluate(self, character_value: Any) -> str:
        """
        تقييم إجابة شخصية معينة على هذا السؤال
        
        Args:
            character_value: قيمة الصفة في الشخصية
            
        Returns:
            "نعم" أو "لا" أو "مش عارف"
        """
        if character_value is None:
            return "مش عارف"
        elif character_value == self.expected_answer:
            return "نعم"
        else:
            return "لا"
    
    def to_dict(self) -> Dict:
        """تحويل السؤال إلى قاموس للتخزين"""
        return {
            'id': self.id,
            'text': self.text,
            'attribute': self.attribute,
            'expected_answer': self.expected_answer,
            'category': self.category,
            'difficulty': self.difficulty
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Question':
        """إنشاء سؤال من قاموس"""
        return cls(
            id=data['id'],
            text=data['text'],
            attribute=data['attribute'],
            expected_answer=data['expected_answer'],
            category=data.get('category', 'basic'),
            difficulty=data.get('difficulty', 1)
        )
    
    def __str__(self) -> str:
        return f"[{self.id}] {self.text}"
    
    def __repr__(self) -> str:
        return f"Question(id={self.id}, text='{self.text[:20]}...')"