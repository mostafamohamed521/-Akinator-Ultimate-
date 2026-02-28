"""
كلاس الشخصية - يمثل شخصية في قاعدة المعرفة
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class Character:
    """
    كلاس الشخصية - يحتوي على جميع بيانات وصفات الشخصية
    """
    
    def __init__(self, 
                 id: int,
                 name: str,
                 category: str,
                 attributes: Dict[str, Any],
                 aliases: List[str] = None,
                 birth_year: Optional[int] = None,
                 death_year: Optional[int] = None,
                 nationality: Optional[str] = None,
                 bio: Optional[str] = None,
                 image_url: Optional[str] = None,
                 tags: List[str] = None):
        """
        تهيئة شخصية جديدة
        
        Args:
            id: معرف فريد
            name: اسم الشخصية
            category: التصنيف الرئيسي
            attributes: قاموس الصفات
            aliases: أسماء بديلة
            birth_year: سنة الميلاد
            death_year: سنة الوفاة
            nationality: الجنسية
            bio: سيرة مختصرة
            image_url: رابط صورة
            tags: علامات تصنيف إضافية
        """
        self.id = id
        self.name = name
        self.category = category
        self.attributes = attributes
        self.aliases = aliases or []
        self.birth_year = birth_year
        self.death_year = death_year
        self.nationality = nationality
        self.bio = bio
        self.image_url = image_url
        self.tags = tags or []
        
        # إضافة صفات مشتقة
        self._derive_attributes()
    
    def _derive_attributes(self):
        """اشتقاق صفات إضافية من البيانات الموجودة"""
        # إضافة صفة الحياة
        if self.birth_year and self.death_year:
            self.attributes['is_alive'] = False
        elif self.birth_year and not self.death_year:
            self.attributes['is_alive'] = True
        
        # إضافة صفة العصر
        if self.birth_year:
            if self.birth_year < 500:
                self.attributes['era'] = 'قديم'
            elif self.birth_year < 1500:
                self.attributes['era'] = 'وسطي'
            elif self.birth_year < 1900:
                self.attributes['era'] = 'حديث'
            else:
                self.attributes['era'] = 'معاصر'
    
    def get_attribute(self, attribute_name: str) -> Any:
        """
        الحصول على قيمة صفة معينة
        
        Args:
            attribute_name: اسم الصفة
            
        Returns:
            قيمة الصفة أو None إذا لم توجد
        """
        # البحث في الصفات المباشرة
        if attribute_name in self.attributes:
            return self.attributes[attribute_name]
        
        # البحث في الصفات المشتقة
        derived_attrs = {
            'age': self.get_age(),
            'century': self.get_century(),
            'name_length': len(self.name),
            'has_aliases': len(self.aliases) > 0
        }
        
        return derived_attrs.get(attribute_name)
    
    def get_age(self) -> Optional[int]:
        """حساب العمر التقريبي للشخصية"""
        if self.birth_year:
            if self.death_year:
                return self.death_year - self.birth_year
            else:
                return datetime.now().year - self.birth_year
        return None
    
    def get_century(self) -> Optional[str]:
        """الحصول على القرن الذي عاشت فيه الشخصية"""
        if self.birth_year:
            century = ((self.birth_year - 1) // 100) + 1
            return f"{century}th"
        return None
    
    def matches_attributes(self, criteria: Dict[str, Any]) -> bool:
        """
        التحقق مما إذا كانت الشخصية تطابق معايير معينة
        
        Args:
            criteria: قاموس المعايير (الصفة: القيمة المطلوبة)
            
        Returns:
            True إذا تطابقت جميع المعايير
        """
        for attr, value in criteria.items():
            if self.get_attribute(attr) != value:
                return False
        return True
    
    def similarity_score(self, other: 'Character') -> float:
        """
        حساب درجة التشابه مع شخصية أخرى
        
        Args:
            other: شخصية أخرى
            
        Returns:
            درجة التشابه (0-1)
        """
        common_attrs = 0
        total_attrs = 0
        
        for attr, value in self.attributes.items():
            if attr in other.attributes:
                total_attrs += 1
                if value == other.attributes[attr]:
                    common_attrs += 1
        
        if total_attrs == 0:
            return 0
        
        return common_attrs / total_attrs
    
    def to_dict(self) -> Dict:
        """تحويل الشخصية إلى قاموس للتخزين"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'attributes': self.attributes,
            'aliases': self.aliases,
            'birth_year': self.birth_year,
            'death_year': self.death_year,
            'nationality': self.nationality,
            'bio': self.bio,
            'image_url': self.image_url,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Character':
        """إنشاء شخصية من قاموس"""
        return cls(
            id=data['id'],
            name=data['name'],
            category=data['category'],
            attributes=data['attributes'],
            aliases=data.get('aliases', []),
            birth_year=data.get('birth_year'),
            death_year=data.get('death_year'),
            nationality=data.get('nationality'),
            bio=data.get('bio'),
            image_url=data.get('image_url'),
            tags=data.get('tags', [])
        )
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category})"
    
    def __repr__(self) -> str:
        return f"Character(id={self.id}, name='{self.name}')"