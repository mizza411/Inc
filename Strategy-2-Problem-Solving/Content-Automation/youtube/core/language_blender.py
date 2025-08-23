"""
🎭 Enhanced Language Blender - Advanced English-Yoruba Fusion Algorithm
Creates funny, memorable, and viral terms by blending English and Yoruba languages
Advanced architecture with machine learning-inspired scoring and cultural relevance
"""

import random
import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import math

@dataclass
class BlendedTerm:
    """Represents a blended English-Yoruba term with enhanced metadata"""
    english_part: str
    yoruba_part: str
    blended_result: str
    meaning: str
    humor_score: float
    viral_potential: float
    cultural_relevance: float
    context: str
    pronunciation_guide: str
    usage_examples: List[str]
    created_date: datetime

@dataclass
class BlendingPattern:
    """Represents a specific blending pattern with success metrics"""
    pattern_name: str
    pattern_template: str
    success_rate: float
    usage_count: int
    viral_examples: List[str]

class EnhancedLanguageBlender:
    """
    Advanced language blending system for creating viral content
    Combines English and Yoruba using sophisticated algorithms
    """
    
    def __init__(self):
        """Initialize the enhanced language blender with advanced dictionaries and rules"""
        # Enhanced Yoruba word database with cultural context
        self.yoruba_database = {
            # High-impact expressions (viral potential)
            'omo': {
                'meaning': 'child/someone',
                'viral_score': 0.9,
                'cultural_weight': 0.95,
                'pronunciation': 'oh-moh',
                'usage_contexts': ['greeting', 'reaction', 'emphasis']
            },
            'abeg': {
                'meaning': 'please/beg',
                'viral_score': 0.85,
                'cultural_weight': 0.9,
                'pronunciation': 'ah-beg',
                'usage_contexts': ['request', 'politeness', 'emphasis']
            },
            'wahala': {
                'meaning': 'trouble/problems',
                'viral_score': 0.95,
                'cultural_weight': 0.98,
                'pronunciation': 'wah-hah-lah',
                'usage_contexts': ['complaint', 'drama', 'exaggeration']
            },
            'jare': {
                'meaning': 'please/just',
                'viral_score': 0.8,
                'cultural_weight': 0.85,
                'pronunciation': 'jah-ray',
                'usage_contexts': ['request', 'emphasis', 'frustration']
            },
            'sha': {
                'meaning': 'just/only',
                'viral_score': 0.75,
                'cultural_weight': 0.8,
                'pronunciation': 'shah',
                'usage_contexts': ['emphasis', 'simplification', 'dismissal']
            },
            'gan': {
                'meaning': 'really/truly',
                'viral_score': 0.8,
                'cultural_weight': 0.85,
                'pronunciation': 'gahn',
                'usage_contexts': ['emphasis', 'confirmation', 'agreement']
            },
            'o': {
                'meaning': 'yes/okay',
                'viral_score': 0.7,
                'cultural_weight': 0.75,
                'pronunciation': 'oh',
                'usage_contexts': ['agreement', 'acknowledgment', 'response']
            },
            'ko': {
                'meaning': 'no/not',
                'viral_score': 0.7,
                'cultural_weight': 0.75,
                'pronunciation': 'koh',
                'usage_contexts': ['disagreement', 'negation', 'refusal']
            },
            'gbe': {
                'meaning': 'carry/take',
                'viral_score': 0.75,
                'cultural_weight': 0.8,
                'pronunciation': 'gbeh',
                'usage_contexts': ['action', 'movement', 'responsibility']
            },
            'japa': {
                'meaning': 'run away/escape',
                'viral_score': 0.9,
                'cultural_weight': 0.9,
                'pronunciation': 'jah-pah',
                'usage_contexts': ['escape', 'avoidance', 'humor']
            },
            'chop': {
                'meaning': 'eat/enjoy',
                'viral_score': 0.85,
                'cultural_weight': 0.85,
                'pronunciation': 'chop',
                'usage_contexts': ['enjoyment', 'consumption', 'pleasure']
            },
            'waka': {
                'meaning': 'walk/go',
                'viral_score': 0.75,
                'cultural_weight': 0.8,
                'pronunciation': 'wah-kah',
                'usage_contexts': ['movement', 'travel', 'action']
            },
            'dey': {
                'meaning': 'is/are (present tense)',
                'viral_score': 0.8,
                'cultural_weight': 0.85,
                'pronunciation': 'day',
                'usage_contexts': ['present_tense', 'existence', 'state']
            },
            'no': {
                'meaning': 'not/don\'t',
                'viral_score': 0.7,
                'cultural_weight': 0.75,
                'pronunciation': 'noh',
                'usage_contexts': ['negation', 'refusal', 'denial']
            },
            'fit': {
                'meaning': 'can/able to',
                'viral_score': 0.8,
                'cultural_weight': 0.85,
                'pronunciation': 'feet',
                'usage_contexts': ['ability', 'capability', 'permission']
            },
            'sabi': {
                'meaning': 'know/understand',
                'viral_score': 0.85,
                'cultural_weight': 0.9,
                'pronunciation': 'sah-bee',
                'usage_contexts': ['knowledge', 'understanding', 'wisdom']
            }
        }
        
        # Enhanced English word database with viral potential
        self.english_database = {
            # High-viral adjectives
            'fire': {'viral_score': 0.95, 'category': 'adjective', 'trending': True},
            'lit': {'viral_score': 0.9, 'category': 'adjective', 'trending': True},
            'banging': {'viral_score': 0.9, 'category': 'adjective', 'trending': True},
            'sick': {'viral_score': 0.85, 'category': 'adjective', 'trending': True},
            'dope': {'viral_score': 0.85, 'category': 'adjective', 'trending': True},
            'fresh': {'viral_score': 0.8, 'category': 'adjective', 'trending': True},
            'smooth': {'viral_score': 0.75, 'category': 'adjective', 'trending': False},
            'perfect': {'viral_score': 0.8, 'category': 'adjective', 'trending': False},
            'beautiful': {'viral_score': 0.75, 'category': 'adjective', 'trending': False},
            'gorgeous': {'viral_score': 0.75, 'category': 'adjective', 'trending': False},
            'stunning': {'viral_score': 0.8, 'category': 'adjective', 'trending': False},
            'wow': {'viral_score': 0.85, 'category': 'interjection', 'trending': True},
            'incredible': {'viral_score': 0.8, 'category': 'adjective', 'trending': False},
            'unbelievable': {'viral_score': 0.8, 'category': 'adjective', 'trending': False},
            'ridiculous': {'viral_score': 0.85, 'category': 'adjective', 'trending': True},
            'absurd': {'viral_score': 0.8, 'category': 'adjective', 'trending': False},
            'crazy': {'viral_score': 0.9, 'category': 'adjective', 'trending': True},
            'insane': {'viral_score': 0.9, 'category': 'adjective', 'trending': True},
            'wild': {'viral_score': 0.9, 'category': 'adjective', 'trending': True},
            'amazing': {'viral_score': 0.8, 'category': 'adjective', 'trending': False},
            'awesome': {'viral_score': 0.8, 'category': 'adjective', 'trending': False}
        }
        
        # Advanced blending patterns with success metrics
        self.blending_patterns = [
            BlendingPattern(
                "yoruba_english_fusion",
                "{yoruba} {english_adj}",
                0.85,
                150,
                ["omo fire", "abeg lit", "wahala banging"]
            ),
            BlendingPattern(
                "english_yoruba_fusion", 
                "{english_adj} {yoruba}",
                0.8,
                120,
                ["fire omo", "lit abeg", "banging wahala"]
            ),
            BlendingPattern(
                "yoruba_english_noun",
                "{yoruba} {english_noun}",
                0.75,
                90,
                ["omo perfect", "abeg amazing", "wahala incredible"]
            ),
            BlendingPattern(
                "english_yoruba_expression",
                "{english} {yoruba}",
                0.8,
                100,
                ["wow omo", "crazy abeg", "insane wahala"]
            ),
            BlendingPattern(
                "yoruba_emphasis",
                "{yoruba} {yoruba} {english_adj}",
                0.9,
                80,
                ["omo omo fire", "abeg abeg lit", "wahala wahala banging"]
            )
        ]
        
        # Enhanced humor boosters with context awareness
        self.humor_boosters = {
            'general': [
                "Omo, this is {result}!",
                "Abeg, {result} no dey finish!",
                "Wahala no dey finish with {result}!",
                "Jare, {result} is the way!",
                "Sha, {result} is banging!",
                "Gan, {result} is fire!",
                "O, {result} is lit!",
                "Ko, {result} is not it!"
            ],
            'music': [
                "Omo, this song is {result}!",
                "Abeg, {result} is giving me serious vibes!",
                "Wahala no dey finish with this {result}!",
                "Jare, {result} is the soundtrack of my life!"
            ],
            'food': [
                "Omo, this food is {result}!",
                "Abeg, {result} is making me hungry!",
                "Wahala no dey finish with this {result}!",
                "Jare, {result} is the taste of heaven!"
            ],
            'culture': [
                "Omo, this culture is {result}!",
                "Abeg, {result} is representing us well!",
                "Wahala no dey finish with this {result}!",
                "Jare, {result} is the pride of Nigeria!"
            ]
        }
        
        # Cultural relevance multipliers
        self.cultural_multipliers = {
            'music': 1.3,
            'food': 1.2,
            'culture': 1.4,
            'lifestyle': 1.1,
            'technology': 0.9,
            'general': 1.0
        }
    
    def blend_languages(self, context: str = "general", 
                       target_viral_score: float = 0.8) -> BlendedTerm:
        """
        Create a blended English-Yoruba term with advanced scoring
        
        Args:
            context: The context for blending (general, music, food, etc.)
            target_viral_score: Target viral potential score
            
        Returns:
            Enhanced BlendedTerm object
        """
        # Select optimal Yoruba word based on context and viral potential
        yoruba_word, yoruba_data = self._select_optimal_yoruba_word(context, target_viral_score)
        
        # Select optimal English word based on viral potential
        english_word, english_data = self._select_optimal_english_word(target_viral_score)
        
        # Choose best blending pattern
        pattern = self._select_optimal_pattern(yoruba_word, english_word, context)
        
        # Create blended result
        blended_result = self._apply_blending_pattern(pattern, yoruba_word, english_word)
        
        # Calculate advanced scores
        humor_score = self._calculate_enhanced_humor_score(yoruba_word, english_word, context)
        viral_potential = self._calculate_viral_potential(yoruba_word, english_word, context)
        cultural_relevance = self._calculate_cultural_relevance(yoruba_word, context)
        
        # Generate pronunciation guide
        pronunciation_guide = self._generate_pronunciation_guide(yoruba_word, english_word)
        
        # Generate usage examples
        usage_examples = self._generate_usage_examples(blended_result, context)
        
        # Create meaning
        meaning = f"{yoruba_data['meaning']} + {english_word} = {blended_result}"
        
        return BlendedTerm(
            english_part=english_word,
            yoruba_part=yoruba_word,
            blended_result=blended_result,
            meaning=meaning,
            humor_score=humor_score,
            viral_potential=viral_potential,
            cultural_relevance=cultural_relevance,
            context=context,
            pronunciation_guide=pronunciation_guide,
            usage_examples=usage_examples,
            created_date=datetime.now()
        )
    
    def _select_optimal_yoruba_word(self, context: str, target_score: float) -> Tuple[str, Dict]:
        """Select optimal Yoruba word based on context and viral potential"""
        candidates = []
        
        for word, data in self.yoruba_database.items():
            # Calculate context relevance
            context_relevance = 1.0
            if context in data['usage_contexts']:
                context_relevance = 1.3
            
            # Calculate overall score
            overall_score = (data['viral_score'] * 0.6 + 
                           data['cultural_weight'] * 0.4) * context_relevance
            
            if overall_score >= target_score * 0.8:  # Allow some flexibility
                candidates.append((word, data, overall_score))
        
        # Sort by score and select top candidates
        candidates.sort(key=lambda x: x[2], reverse=True)
        
        # Weighted random selection from top candidates
        top_candidates = candidates[:min(3, len(candidates))]
        weights = [c[2] for c in top_candidates]
        
        selected_index = random.choices(range(len(top_candidates)), weights=weights)[0]
        selected_word, selected_data, _ = top_candidates[selected_index]
        
        return selected_word, selected_data
    
    def _select_optimal_english_word(self, target_score: float) -> Tuple[str, Dict]:
        """Select optimal English word based on viral potential"""
        candidates = []
        
        for word, data in self.english_database.items():
            if data['viral_score'] >= target_score * 0.8:
                candidates.append((word, data, data['viral_score']))
        
        # Sort by viral score
        candidates.sort(key=lambda x: x[2], reverse=True)
        
        # Weighted random selection from top candidates
        top_candidates = candidates[:min(3, len(candidates))]
        weights = [c[2] for c in top_candidates]
        
        selected_index = random.choices(range(len(top_candidates)), weights=weights)[0]
        selected_word, selected_data, _ = top_candidates[selected_index]
        
        return selected_word, selected_data
    
    def _select_optimal_pattern(self, yoruba_word: str, english_word: str, context: str) -> BlendingPattern:
        """Select optimal blending pattern based on words and context"""
        # Filter patterns by success rate and context
        suitable_patterns = [p for p in self.blending_patterns if p.success_rate >= 0.75]
        
        # Weight by success rate and usage count
        weights = [p.success_rate * math.log(p.usage_count + 1) for p in suitable_patterns]
        
        selected_pattern = random.choices(suitable_patterns, weights=weights)[0]
        return selected_pattern
    
    def _apply_blending_pattern(self, pattern: BlendingPattern, yoruba_word: str, english_word: str) -> str:
        """Apply the selected blending pattern to create the result"""
        if pattern.pattern_name == "yoruba_emphasis":
            return f"{yoruba_word} {yoruba_word} {english_word}"
        else:
            return f"{yoruba_word} {english_word}"
    
    def _calculate_enhanced_humor_score(self, yoruba_word: str, english_word: str, context: str) -> float:
        """Calculate enhanced humor score using multiple factors"""
        base_score = 0.5
        
        # Yoruba word humor factors
        yoruba_data = self.yoruba_database.get(yoruba_word, {})
        base_score += yoruba_data.get('viral_score', 0.5) * 0.3
        
        # English word humor factors
        english_data = self.english_database.get(english_word, {})
        base_score += english_data.get('viral_score', 0.5) * 0.2
        
        # Context boost
        context_multiplier = self.cultural_multipliers.get(context, 1.0)
        base_score *= context_multiplier
        
        # Word length contrast bonus
        length_diff = abs(len(yoruba_word) - len(english_word))
        if length_diff > 3:
            base_score += 0.1
        
        # Cultural relevance bonus
        if context in yoruba_data.get('usage_contexts', []):
            base_score += 0.15
        
        # Trending bonus
        if english_data.get('trending', False):
            base_score += 0.1
        
        # Random variation
        base_score += random.uniform(-0.05, 0.05)
        
        return max(0.0, min(1.0, base_score))
    
    def _calculate_viral_potential(self, yoruba_word: str, english_word: str, context: str) -> float:
        """Calculate viral potential score"""
        yoruba_data = self.yoruba_database.get(yoruba_word, {})
        english_data = self.english_database.get(english_word, {})
        
        viral_score = (yoruba_data.get('viral_score', 0.5) * 0.6 + 
                      english_data.get('viral_score', 0.5) * 0.4)
        
        # Context multiplier
        context_multiplier = self.cultural_multipliers.get(context, 1.0)
        viral_score *= context_multiplier
        
        return min(1.0, viral_score)
    
    def _calculate_cultural_relevance(self, yoruba_word: str, context: str) -> float:
        """Calculate cultural relevance score"""
        yoruba_data = self.yoruba_database.get(yoruba_word, {})
        base_relevance = yoruba_data.get('cultural_weight', 0.5)
        
        # Context relevance
        if context in yoruba_data.get('usage_contexts', []):
            base_relevance *= 1.2
        
        return min(1.0, base_relevance)
    
    def _generate_pronunciation_guide(self, yoruba_word: str, english_word: str) -> str:
        """Generate pronunciation guide for the blended term"""
        yoruba_data = self.yoruba_database.get(yoruba_word, {})
        yoruba_pronunciation = yoruba_data.get('pronunciation', yoruba_word)
        
        return f"{yoruba_pronunciation} {english_word}"
    
    def _generate_usage_examples(self, blended_term: str, context: str) -> List[str]:
        """Generate usage examples for the blended term"""
        examples = []
        
        if context == "music":
            examples.extend([
                f"This song is {blended_term}!",
                f"I can't stop listening to this {blended_term} music!",
                f"Omo, this beat is {blended_term}!"
            ])
        elif context == "food":
            examples.extend([
                f"This food is {blended_term}!",
                f"I need more of this {blended_term} dish!",
                f"Abeg, this taste is {blended_term}!"
            ])
        else:
            examples.extend([
                f"This is {blended_term}!",
                f"I love how {blended_term} this is!",
                f"Wahala no dey finish with this {blended_term}!"
            ])
        
        return examples[:3]  # Return top 3 examples
    
    def create_humor_boosted_phrase(self, base_term: str, context: str = "general") -> str:
        """Create context-aware humor-boosted phrase"""
        available_boosters = self.humor_boosters.get(context, self.humor_boosters['general'])
        booster = random.choice(available_boosters)
        return booster.format(result=base_term)
    
    def generate_content_batch(self, count: int = 10, context: str = "general", 
                             min_viral_score: float = 0.7) -> List[BlendedTerm]:
        """Generate multiple blended terms with quality filtering"""
        terms = []
        attempts = 0
        max_attempts = count * 3  # Allow some retries for quality
        
        while len(terms) < count and attempts < max_attempts:
            term = self.blend_languages(context, min_viral_score)
            
            # Quality filter - only accept terms with good scores
            if (term.humor_score >= min_viral_score and 
                term.viral_potential >= min_viral_score * 0.8):
                terms.append(term)
            
            attempts += 1
        
        # Sort by combined score (humor + viral + cultural)
        terms.sort(key=lambda x: x.humor_score + x.viral_potential + x.cultural_relevance, 
                  reverse=True)
        
        return terms
    
    def get_context_suggestions(self) -> Dict[str, List[str]]:
        """Get enhanced context suggestions with viral potential"""
        return {
            "music": ["song reactions", "music commentary", "artist analysis", "beat breakdowns"],
            "food": ["restaurant reviews", "cooking tips", "food culture", "taste reactions"],
            "culture": ["traditions", "modern life", "generational differences", "cultural commentary"],
            "technology": ["app reviews", "tech trends", "digital culture", "gadget reactions"],
            "lifestyle": ["daily routines", "life hacks", "personal growth", "lifestyle tips"],
            "entertainment": ["movie reviews", "TV shows", "celebrity news", "entertainment commentary"],
            "general": ["trending topics", "current events", "random thoughts", "viral commentary"]
        }
    
    def export_blending_data(self, export_path: str = "exports") -> str:
        """Export blending data for analysis and optimization"""
        import os
        
        os.makedirs(export_path, exist_ok=True)
        
        export_data = {
            "export_date": datetime.now().isoformat(),
            "yoruba_database": self.yoruba_database,
            "english_database": self.english_database,
            "blending_patterns": [p.__dict__ for p in self.blending_patterns],
            "cultural_multipliers": self.cultural_multipliers,
            "humor_boosters": self.humor_boosters
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_language_blender_data_{timestamp}.json"
        filepath = os.path.join(export_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filepath

# Example usage
if __name__ == "__main__":
    blender = EnhancedLanguageBlender()
    
    # Generate a single enhanced blended term
    print("🎭 Enhanced Language Blending Demo")
    print("=" * 50)
    
    term = blender.blend_languages("music", 0.8)
    print(f"Blended Term: {term.blended_result}")
    print(f"Meaning: {term.meaning}")
    print(f"Humor Score: {term.humor_score:.2f}")
    print(f"Viral Potential: {term.viral_potential:.2f}")
    print(f"Cultural Relevance: {term.cultural_relevance:.2f}")
    print(f"Pronunciation: {term.pronunciation_guide}")
    print(f"Usage Examples: {', '.join(term.usage_examples)}")
    
    # Generate humor-boosted phrase
    phrase = blender.create_humor_boosted_phrase(term.blended_result, "music")
    print(f"\nHumor Phrase: {phrase}")
    
    # Generate content batch
    print(f"\n--- Content Batch (Music Context) ---")
    batch = blender.generate_content_batch(5, "music", 0.8)
    for i, term in enumerate(batch, 1):
        print(f"{i}. {term.blended_result}")
        print(f"   Humor: {term.humor_score:.2f} | Viral: {term.viral_potential:.2f} | Cultural: {term.cultural_relevance:.2f}")
    
    # Export data
    export_path = blender.export_blending_data()
    print(f"\n📁 Blending data exported to: {export_path}")
