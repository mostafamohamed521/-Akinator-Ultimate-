"""
حساب الأنتروبي لاختيار أفضل الأسئلة
"""

import math
from typing import List, Dict, Any
from collections import Counter
from ..models.character import Character
from ..models.question import Question

class EntropyCalculator:
    """
    حساب الأنتروبي (مقياس عدم اليقين) للأسئلة
    لاختيار السؤال الذي يقسم مجموعة الشخصيات بأفضل طريقة
    """
    
    def calculate_entropy(self, characters: List[Character]) -> float:
        """
        حساب الأنتروبي لمجموعة من الشخصيات
        
        Args:
            characters: قائمة الشخصيات
            
        Returns:
            قيمة الأنتروبي (كلما زادت، زاد عدم اليقين)
        """
        if not characters:
            return 0
        
        # حساب توزيع الفئات
        categories = [c.category for c in characters]
        category_counts = Counter(categories)
        
        entropy = 0
        total = len(characters)
        
        for count in category_counts.values():
            probability = count / total
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    def calculate_question_entropy(self, 
                                   characters: List[Character], 
                                   question: Question) -> float:
        """
        حساب الأنتروبي المتوقع بعد طرح سؤال معين
        
        Args:
            characters: قائمة الشخصيات الحالية
            question: السؤال المراد تقييمه
            
        Returns:
            الأنتروبي المتوقع (كلما زاد، كان السؤال أفضل)
        """
        if not characters:
            return 0
        
        # توزيع الإجابات المحتملة
        answer_distribution = self._get_answer_distribution(characters, question)
        
        # حساب الأنتروبي المرجح
        weighted_entropy = 0
        total = len(characters)
        
        for answer, count in answer_distribution.items():
            if count == 0:
                continue
            
            probability = count / total
            # الأنتروبي بعد هذا الفرع
            branch_entropy = self._calculate_branch_entropy(
                characters, question, answer
            )
            weighted_entropy += probability * branch_entropy
        
        return weighted_entropy
    
    def _get_answer_distribution(self, 
                                 characters: List[Character], 
                                 question: Question) -> Dict[str, int]:
        """
        حساب توزيع الإجابات المحتملة لسؤال معين
        
        Returns:
            قاموس يربط كل إجابة بعدد الشخصيات
        """
        distribution = {
            'نعم': 0,
            'لا': 0,
            'مش عارف': 0
        }
        
        for character in characters:
            char_value = character.get_attribute(question.attribute)
            
            if char_value == question.expected_answer:
                distribution['نعم'] += 1
            elif char_value is not None:
                distribution['لا'] += 1
            else:
                distribution['مش عارف'] += 1
        
        return distribution
    
    def _calculate_branch_entropy(self,
                                   characters: List[Character],
                                   question: Question,
                                   answer: str) -> float:
        """
        حساب الأنتروبي لفرع معين من السؤال
        """
        # تصفية الشخصيات حسب الإجابة
        filtered = []
        
        for character in characters:
            char_value = character.get_attribute(question.attribute)
            
            if answer == 'نعم' and char_value == question.expected_answer:
                filtered.append(character)
            elif answer == 'لا' and char_value != question.expected_answer:
                filtered.append(character)
            elif answer == 'مش عارف':
                filtered.append(character)
        
        return self.calculate_entropy(filtered)
    
    def calculate_information_gain(self,
                                   characters: List[Character],
                                   question: Question) -> float:
        """
        حساب كسب المعلومات من سؤال معين
        
        Args:
            characters: قائمة الشخصيات
            question: السؤال
            
        Returns:
            كسب المعلومات (الفرق بين الأنتروبي الحالي والمتوقع)
        """
        current_entropy = self.calculate_entropy(characters)
        expected_entropy = self.calculate_question_entropy(characters, question)
        
        return current_entropy - expected_entropy
    
    def find_best_question(self,
                          characters: List[Character],
                          questions: List[Question],
                          asked_questions: List[Question] = None) -> Question:
        """
        إيجاد أفضل سؤال لطرحه
        
        Args:
            characters: قائمة الشخصيات المتبقية
            questions: جميع الأسئلة المتاحة
            asked_questions: الأسئلة التي سبق طرحها
            
        Returns:
            أفضل سؤال
        """
        asked_ids = [q.id for q in (asked_questions or [])]
        available_questions = [q for q in questions if q.id not in asked_ids]
        
        if not available_questions:
            return None
        
        best_question = None
        max_gain = -1
        
        for question in available_questions:
            gain = self.calculate_information_gain(characters, question)
            if gain > max_gain:
                max_gain = gain
                best_question = question
        
        return best_question