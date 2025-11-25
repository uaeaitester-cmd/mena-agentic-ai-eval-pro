#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Language Support for MENA Bias Evaluation Pipeline
Support for Arabic, Persian, and English
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Language(Enum):
    """Supported languages"""
    ARABIC = "ar"
    PERSIAN = "fa"
    ENGLISH = "en"
    UNKNOWN = "unknown"


@dataclass
class LanguageConfig:
    """Configuration for a language"""
    code: str
    name: str
    native_name: str
    direction: str  # ltr or rtl
    sentiment_labels: Dict[str, str]
    demographics: Dict[str, List[str]]


class LanguageDetector:
    """Detect language of text"""
    
    # Unicode ranges for different scripts
    ARABIC_RANGE = (0x0600, 0x06FF)
    PERSIAN_RANGE = (0x06A0, 0x06FF)
    ENGLISH_RANGE = (0x0041, 0x007A)
    
    @classmethod
    def detect(cls, text: str) -> Language:
        """
        Detect language of text
        
        Args:
            text: Input text
        
        Returns:
            Detected Language enum
        """
        if not text or not text.strip():
            return Language.UNKNOWN
        
        # Count characters from each script
        arabic_count = 0
        persian_count = 0
        english_count = 0
        
        for char in text:
            code_point = ord(char)
            
            if cls.ARABIC_RANGE[0] <= code_point <= cls.ARABIC_RANGE[1]:
                arabic_count += 1
            if cls.PERSIAN_RANGE[0] <= code_point <= cls.PERSIAN_RANGE[1]:
                persian_count += 1
            if (ord('A') <= code_point <= ord('Z')) or (ord('a') <= code_point <= ord('z')):
                english_count += 1
        
        total = arabic_count + persian_count + english_count
        
        if total == 0:
            return Language.UNKNOWN
        
        # Determine dominant language
        if english_count / total > 0.5:
            return Language.ENGLISH
        elif persian_count / total > 0.3:
            return Language.PERSIAN
        elif arabic_count / total > 0.3:
            return Language.ARABIC
        else:
            return Language.UNKNOWN


class MultilingualTranslator:
    """Translation and localization utilities"""
    
    # Sentiment label translations
    SENTIMENT_TRANSLATIONS = {
        Language.ARABIC: {
            'positive': 'إيجابي',
            'negative': 'سلبي',
            'neutral': 'محايد'
        },
        Language.PERSIAN: {
            'positive': 'مثبت',
            'negative': 'منفی',
            'neutral': 'خنثی'
        },
        Language.ENGLISH: {
            'positive': 'positive',
            'negative': 'negative',
            'neutral': 'neutral'
        }
    }
    
    # UI text translations
    UI_TRANSLATIONS = {
        Language.ARABIC: {
            'accuracy': 'الدقة',
            'precision': 'الدقة',
            'recall': 'الاستدعاء',
            'f1_score': 'درجة F1',
            'bias_score': 'درجة التحيز',
            'fairness': 'العدالة',
            'results': 'النتائج',
            'analysis': 'التحليل',
            'model': 'النموذج',
            'dataset': 'مجموعة البيانات'
        },
        Language.PERSIAN: {
            'accuracy': 'دقت',
            'precision': 'صحت',
            'recall': 'بازیابی',
            'f1_score': 'امتیاز F1',
            'bias_score': 'امتیاز تعصب',
            'fairness': 'عدالت',
            'results': 'نتایج',
            'analysis': 'تحلیل',
            'model': 'مدل',
            'dataset': 'مجموعه داده'
        },
        Language.ENGLISH: {
            'accuracy': 'Accuracy',
            'precision': 'Precision',
            'recall': 'Recall',
            'f1_score': 'F1 Score',
            'bias_score': 'Bias Score',
            'fairness': 'Fairness',
            'results': 'Results',
            'analysis': 'Analysis',
            'model': 'Model',
            'dataset': 'Dataset'
        }
    }
    
    @classmethod
    def translate_sentiment(cls, sentiment: str, target_lang: Language) -> str:
        """Translate sentiment label"""
        translations = cls.SENTIMENT_TRANSLATIONS.get(target_lang, {})
        return translations.get(sentiment.lower(), sentiment)
    
    @classmethod
    def translate_ui_text(cls, key: str, target_lang: Language) -> str:
        """Translate UI text"""
        translations = cls.UI_TRANSLATIONS.get(target_lang, {})
        return translations.get(key.lower(), key)
    
    @classmethod
    def get_all_ui_translations(cls, target_lang: Language) -> Dict[str, str]:
        """Get all UI translations for a language"""
        return cls.UI_TRANSLATIONS.get(target_lang, cls.UI_TRANSLATIONS[Language.ENGLISH])


class TextNormalizer:
    """Normalize text for different languages"""
    
    @staticmethod
    def normalize_arabic(text: str) -> str:
        """
        Normalize Arabic text
        - Remove diacritics
        - Normalize alef variants
        - Remove tatweel
        """
        # Remove Arabic diacritics
        text = re.sub(r'[\u064B-\u0652]', '', text)
        
        # Normalize alef variants
        text = re.sub(r'[إأآا]', 'ا', text)
        
        # Remove tatweel (elongation)
        text = re.sub(r'ـ', '', text)
        
        # Normalize teh marbuta
        text = re.sub(r'ة', 'ه', text)
        
        return text.strip()
    
    @staticmethod
    def normalize_persian(text: str) -> str:
        """
        Normalize Persian text
        - Convert Arabic characters to Persian equivalents
        - Remove diacritics
        """
        # Convert Arabic ya and kaf to Persian
        text = text.replace('ي', 'ی')
        text = text.replace('ك', 'ک')
        
        # Remove diacritics
        text = re.sub(r'[\u064B-\u0652]', '', text)
        
        # Remove zero-width characters
        text = re.sub(r'[\u200c\u200d]', '', text)
        
        return text.strip()
    
    @staticmethod
    def normalize_english(text: str) -> str:
        """Normalize English text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    @classmethod
    def normalize(cls, text: str, language: Language) -> str:
        """
        Normalize text based on language
        
        Args:
            text: Input text
            language: Detected language
        
        Returns:
            Normalized text
        """
        if language == Language.ARABIC:
            return cls.normalize_arabic(text)
        elif language == Language.PERSIAN:
            return cls.normalize_persian(text)
        elif language == Language.ENGLISH:
            return cls.normalize_english(text)
        else:
            return text.strip()


class MultilingualProcessor:
    """
    High-level processor for multilingual text
    Combines detection, normalization, and translation
    """
    
    def __init__(self, default_language: Language = Language.ENGLISH):
        self.default_language = default_language
        self.detector = LanguageDetector()
        self.translator = MultilingualTranslator()
        self.normalizer = TextNormalizer()
    
    def process_text(
        self,
        text: str,
        detect_language: bool = True,
        normalize: bool = True
    ) -> Tuple[str, Language]:
        """
        Process text with language detection and normalization
        
        Args:
            text: Input text
            detect_language: Whether to auto-detect language
            normalize: Whether to normalize text
        
        Returns:
            Tuple of (processed_text, detected_language)
        """
        # Detect language
        if detect_language:
            language = self.detector.detect(text)
        else:
            language = self.default_language
        
        # Normalize
        if normalize:
            text = self.normalizer.normalize(text, language)
        
        return text, language
    
    def localize_results(
        self,
        results: Dict[str, any],
        target_language: Language
    ) -> Dict[str, any]:
        """
        Localize analysis results to target language
        
        Args:
            results: Analysis results dictionary
            target_language: Target language for localization
        
        Returns:
            Localized results dictionary
        """
        localized = {}
        
        for key, value in results.items():
            # Translate key
            translated_key = self.translator.translate_ui_text(key, target_language)
            
            # Translate value if it's a sentiment
            if isinstance(value, str) and value.lower() in ['positive', 'negative', 'neutral']:
                value = self.translator.translate_sentiment(value, target_language)
            
            localized[translated_key] = value
        
        return localized
    
    def get_language_config(self, language: Language) -> LanguageConfig:
        """Get configuration for a language"""
        
        configs = {
            Language.ARABIC: LanguageConfig(
                code="ar",
                name="Arabic",
                native_name="العربية",
                direction="rtl",
                sentiment_labels=self.translator.SENTIMENT_TRANSLATIONS[Language.ARABIC],
                demographics={
                    'region': ['الخليج', 'الشام', 'شمال أفريقيا', 'مصر'],
                    'gender': ['ذكر', 'أنثى'],
                    'age_group': ['18-25', '26-35', '36-45', '46+']
                }
            ),
            Language.PERSIAN: LanguageConfig(
                code="fa",
                name="Persian",
                native_name="فارسی",
                direction="rtl",
                sentiment_labels=self.translator.SENTIMENT_TRANSLATIONS[Language.PERSIAN],
                demographics={
                    'region': ['خلیج', 'شام', 'شمال آفریقا', 'مصر'],
                    'gender': ['مرد', 'زن'],
                    'age_group': ['18-25', '26-35', '36-45', '46+']
                }
            ),
            Language.ENGLISH: LanguageConfig(
                code="en",
                name="English",
                native_name="English",
                direction="ltr",
                sentiment_labels=self.translator.SENTIMENT_TRANSLATIONS[Language.ENGLISH],
                demographics={
                    'region': ['Gulf', 'Levant', 'North Africa', 'Egypt'],
                    'gender': ['Male', 'Female'],
                    'age_group': ['18-25', '26-35', '36-45', '46+']
                }
            )
        }
        
        return configs.get(language, configs[Language.ENGLISH])


# Example usage
if __name__ == "__main__":
    print("🌐 Testing Multilingual Support\n")
    
    # Test language detection
    texts = {
        "الخدمة ممتازة جداً": Language.ARABIC,
        "خدمات عالی است": Language.PERSIAN,
        "The service is excellent": Language.ENGLISH,
    }
    
    detector = LanguageDetector()
    
    print("Language Detection:")
    for text, expected in texts.items():
        detected = detector.detect(text)
        status = "✅" if detected == expected else "❌"
        print(f"  {status} '{text}' → {detected.value}")
    
    print("\n" + "="*50)
    
    # Test normalization
    print("\nText Normalization:")
    
    normalizer = TextNormalizer()
    
    arabic_text = "الخِدْمَة مُمْتَازَة"
    normalized = normalizer.normalize_arabic(arabic_text)
    print(f"  Arabic: '{arabic_text}' → '{normalized}'")
    
    persian_text = "خدمات عالي است"
    normalized = normalizer.normalize_persian(persian_text)
    print(f"  Persian: '{persian_text}' → '{normalized}'")
    
    print("\n" + "="*50)
    
    # Test translation
    print("\nSentiment Translation:")
    
    translator = MultilingualTranslator()
    
    for lang in [Language.ARABIC, Language.PERSIAN, Language.ENGLISH]:
        positive = translator.translate_sentiment('positive', lang)
        print(f"  {lang.value}: 'positive' → '{positive}'")
    
    print("\n" + "="*50)
    
    # Test full processor
    print("\nFull Processing:")
    
    processor = MultilingualProcessor()
    
    test_text = "الخِدْمَة مُمْتَازَة جِدّاً"
    processed, lang = processor.process_text(test_text)
    
    print(f"  Original: '{test_text}'")
    print(f"  Processed: '{processed}'")
    print(f"  Language: {lang.value}")
    
    print("\n✅ Test completed!")