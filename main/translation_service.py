import openai
from django.conf import settings
from django.core.cache import cache
import json


class TranslationService:
    """Service for translating CV content using OpenAI API."""
    
    # Language mapping for the required languages plus additional popular languages
    LANGUAGES = {
        # Original 17 required languages
        'cornish': 'Cornish',
        'manx': 'Manx', 
        'breton': 'Breton',
        'inuktitut': 'Inuktitut',
        'kalaallisut': 'Kalaallisut',
        'romani': 'Romani',
        'occitan': 'Occitan',
        'ladino': 'Ladino',
        'northern_sami': 'Northern Sami',
        'upper_sorbian': 'Upper Sorbian',
        'kashubian': 'Kashubian',
        'zazaki': 'Zazaki',
        'chuvash': 'Chuvash',
        'livonian': 'Livonian',
        'tsakonian': 'Tsakonian',
        'saramaccan': 'Saramaccan',
        'bislama': 'Bislama',
        'french': 'French',
        'german': 'German',
        'spanish': 'Spanish',
        'portuguese_brazil': 'Portuguese (Brazil)',
        'italian': 'Italian',
        'japanese': 'Japanese',
        'chinese_simplified': 'Chinese (Simplified)',
        'ukrainian': 'Ukrainian',
        'korean': 'Korean',
        'turkish': 'Turkish'
    }
    
    def __init__(self):
        """Initialize the translation service."""
        self.client = None
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip():
            try:
                self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def get_available_languages(self):
        """Get list of available languages for translation."""
        return self.LANGUAGES
    
    def get_languages_by_category(self):
        """Get languages organized by category."""
        required_languages = {
            'cornish': 'Cornish',
            'manx': 'Manx', 
            'breton': 'Breton',
            'inuktitut': 'Inuktitut',
            'kalaallisut': 'Kalaallisut',
            'romani': 'Romani',
            'occitan': 'Occitan',
            'ladino': 'Ladino',
            'northern_sami': 'Northern Sami',
            'upper_sorbian': 'Upper Sorbian',
            'kashubian': 'Kashubian',
            'zazaki': 'Zazaki',
            'chuvash': 'Chuvash',
            'livonian': 'Livonian',
            'tsakonian': 'Tsakonian',
            'saramaccan': 'Saramaccan',
            'bislama': 'Bislama',
        }
        
        popular_languages = {
            'french': 'French',
            'german': 'German',
            'spanish': 'Spanish',
            'portuguese_brazil': 'Portuguese (Brazil)',
            'italian': 'Italian',
            'japanese': 'Japanese',
            'chinese_simplified': 'Chinese (Simplified)',
            'ukrainian': 'Ukrainian',
            'korean': 'Korean',
            'turkish': 'Turkish'
        }
        
        return {
            'required': required_languages,
            'popular': popular_languages,
            'all': self.LANGUAGES
        }
    
    def translate_cv_content(self, cv, target_language):
        """
        Translate CV content to the specified language.
        
        Args:
            cv: CV model instance
            target_language: Target language code
            
        Returns:
            dict: Translated CV content
        """
        if not self.client:
            return {
                'error': 'OpenAI API key not configured. Please set OPENAI_API_KEY in settings.',
                'translated': False
            }
        
        if not settings.OPENAI_API_KEY or not settings.OPENAI_API_KEY.strip():
            return {
                'error': 'OpenAI API key is not set. Please configure OPENAI_API_KEY in your environment.',
                'translated': False
            }
        
        if target_language not in self.LANGUAGES:
            return {
                'error': f'Language {target_language} not supported',
                'translated': False
            }
        
        # Create cache key for this translation
        cache_key = f'cv_translation_{cv.id}_{target_language}'
        
        # Check if translation is cached
        cached_translation = cache.get(cache_key)
        if cached_translation:
            return cached_translation
        
        try:
            # Prepare CV content for translation
            cv_content = self._prepare_cv_content(cv)
            
            # Create translation prompt
            prompt = self._create_translation_prompt(cv_content, target_language)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator. Translate the CV content accurately while maintaining the professional tone and structure."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            # Parse the response
            translated_content = response.choices[0].message.content
            
            # Parse the JSON response
            try:
                result = json.loads(translated_content)
                result['translated'] = True
                result['language'] = self.LANGUAGES[target_language]
                result['original_language'] = 'English'
                
                # Cache the translation for 1 hour
                cache.set(cache_key, result, 3600)
                
                return result
                
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw text
                return {
                    'error': 'Failed to parse translation response',
                    'raw_response': translated_content,
                    'translated': False
                }
                
        except Exception as e:
            return {
                'error': f'Translation failed: {str(e)}',
                'translated': False
            }
    
    def _prepare_cv_content(self, cv):
        """Prepare CV content for translation."""
        return {
            'name': f"{cv.firstname} {cv.lastname}",
            'bio': cv.bio,
            'skills': cv.skills,
            'projects': cv.projects,
            'contacts': cv.contacts
        }
    
    def _create_translation_prompt(self, cv_content, target_language):
        """Create the translation prompt for OpenAI."""
        language_name = self.LANGUAGES[target_language]
        
        return f"""
Please translate the following CV content into {language_name}. 
Return the result as a JSON object with the following structure:

{{
    "name": "translated name",
    "bio": "translated bio",
    "skills": "translated skills",
    "projects": "translated projects", 
    "contacts": "translated contacts"
}}

CV Content to translate:
Name: {cv_content['name']}
Bio: {cv_content['bio']}
Skills: {cv_content['skills']}
Projects: {cv_content['projects']}
Contacts: {cv_content['contacts']}

Please ensure the translation maintains the professional tone and structure of the original CV.
""" 