"""
✅ Content Validation System
Ensures YouTube videos meet high-effort content requirements for monetization
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ValidationResult:
    """Result of content validation"""
    is_valid: bool
    score: float  # 0.0 to 1.0
    issues: List[str]
    recommendations: List[str]
    validation_date: datetime

@dataclass
class ContentMetrics:
    """Content quality metrics"""
    word_count: int
    estimated_duration: float
    language_blend_count: int
    trending_term_count: int
    content_sections: int
    research_depth_score: float
    originality_score: float
    engagement_potential: float

class HighEffortContentValidator:
    """
    Validates content meets YouTube's high-effort requirements for monetization
    """
    
    def __init__(self):
        """Initialize the content validator"""
        self.logger = logging.getLogger(__name__)
        
        # YouTube monetization requirements
        self.min_duration_minutes = 8.0
        self.min_word_count = 1200  # ~150 words per minute
        self.min_content_sections = 5
        self.min_language_blends = 2
        self.min_trending_terms = 1
        
        # Quality thresholds
        self.min_research_score = 0.7
        self.min_originality_score = 0.8
        self.min_engagement_score = 0.7
        
        # Content complexity indicators
        self.complexity_keywords = [
            "research", "analysis", "study", "investigation", "examination",
            "exploration", "breakdown", "explanation", "interpretation",
            "comparison", "evaluation", "assessment", "review", "critique"
        ]
        
        self.engagement_indicators = [
            "you won't believe", "this is insane", "breaking down",
            "deep dive", "exclusive", "revealed", "shocking",
            "amazing", "incredible", "unbelievable", "mind-blowing"
        ]
    
    def validate_video_script(self, script_data: Dict) -> ValidationResult:
        """
        Validate a video script meets high-effort requirements
        
        Args:
            script_data: Script data dictionary
            
        Returns:
            ValidationResult with validation details
        """
        try:
            self.logger.info("Starting video script validation...")
            
            # Extract content metrics
            metrics = self._calculate_content_metrics(script_data)
            
            # Perform validation checks
            issues = []
            recommendations = []
            score = 0.0
            
            # Check 1: Duration requirement
            if metrics.estimated_duration < self.min_duration_minutes:
                issues.append(f"Video duration ({metrics.estimated_duration:.1f} min) below minimum ({self.min_duration_minutes} min)")
                recommendations.append("Expand content with additional sections or detailed explanations")
                score += 0.1
            else:
                score += 0.2
            
            # Check 2: Word count requirement
            if metrics.word_count < self.min_word_count:
                issues.append(f"Word count ({metrics.word_count}) below minimum ({self.min_word_count})")
                recommendations.append("Add more detailed content and explanations")
                score += 0.1
            else:
                score += 0.2
            
            # Check 3: Content structure
            if metrics.content_sections < self.min_content_sections:
                issues.append(f"Content sections ({metrics.content_sections}) below minimum ({self.min_content_sections})")
                recommendations.append("Break content into more logical sections")
                score += 0.1
            else:
                score += 0.2
            
            # Check 4: Language blending integration
            if metrics.language_blend_count < self.min_language_blends:
                issues.append(f"Language blends ({metrics.language_blend_count}) below minimum ({self.min_language_blends})")
                recommendations.append("Integrate more English-Yoruba language blending")
                score += 0.1
            else:
                score += 0.2
            
            # Check 5: Trending terms integration
            if metrics.trending_term_count < self.min_trending_terms:
                issues.append(f"Trending terms ({metrics.trending_term_count}) below minimum ({self.min_trending_terms})")
                recommendations.append("Include more trending topics and viral terms")
                score += 0.1
            else:
                score += 0.2
            
            # Check 6: Research depth
            if metrics.research_depth_score < self.min_research_score:
                issues.append(f"Research depth score ({metrics.research_depth_score:.2f}) below minimum ({self.min_research_score})")
                recommendations.append("Add more research-based content and citations")
                score += 0.1
            else:
                score += 0.2
            
            # Check 7: Originality
            if metrics.originality_score < self.min_originality_score:
                issues.append(f"Originality score ({metrics.originality_score:.2f}) below minimum ({self.min_originality_score})")
                recommendations.append("Increase unique language blending and cultural perspective")
                score += 0.1
            else:
                score += 0.2
            
            # Check 8: Engagement potential
            if metrics.engagement_potential < self.min_engagement_score:
                issues.append(f"Engagement potential ({metrics.engagement_potential:.2f}) below minimum ({self.min_engagement_score})")
                recommendations.append("Add more engaging hooks and call-to-actions")
                score += 0.1
            else:
                score += 0.2
            
            # Determine if content is valid
            is_valid = score >= 0.8 and len(issues) <= 2
            
            # Generate additional recommendations if needed
            if not is_valid:
                recommendations.extend(self._generate_improvement_suggestions(metrics))
            
            validation_result = ValidationResult(
                is_valid=is_valid,
                score=score,
                issues=issues,
                recommendations=recommendations,
                validation_date=datetime.now()
            )
            
            self.logger.info(f"Validation completed. Score: {score:.2f}, Valid: {is_valid}")
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Error in script validation: {e}")
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=[f"Validation error: {str(e)}"],
                recommendations=["Fix validation system error"],
                validation_date=datetime.now()
            )
    
    def _calculate_content_metrics(self, script_data: Dict) -> ContentMetrics:
        """Calculate content quality metrics"""
        try:
            # Extract text content
            content_parts = [
                script_data.get('hook', ''),
                script_data.get('introduction', ''),
                script_data.get('main_content', []),
                script_data.get('transitions', []),
                script_data.get('conclusion', ''),
                script_data.get('call_to_action', '')
            ]
            
            # Flatten main content if it's a list
            if isinstance(content_parts[2], list):
                content_parts[2] = ' '.join(content_parts[2])
            
            # Calculate word count
            full_text = ' '.join(str(part) for part in content_parts)
            word_count = len(full_text.split())
            
            # Estimate duration (150 words per minute)
            estimated_duration = word_count / 150.0
            
            # Count content sections
            content_sections = len([part for part in content_parts if part and len(str(part).strip()) > 10])
            
            # Count language blends and trending terms
            language_blend_count = len(script_data.get('language_blends', []))
            trending_term_count = len(script_data.get('trending_terms', []))
            
            # Calculate research depth score
            research_score = self._calculate_research_depth(full_text)
            
            # Calculate originality score
            originality_score = self._calculate_originality_score(script_data)
            
            # Calculate engagement potential
            engagement_score = self._calculate_engagement_potential(full_text)
            
            return ContentMetrics(
                word_count=word_count,
                estimated_duration=estimated_duration,
                language_blend_count=language_blend_count,
                trending_term_count=trending_term_count,
                content_sections=content_sections,
                research_depth_score=research_score,
                originality_score=originality_score,
                engagement_potential=engagement_score
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {e}")
            return ContentMetrics(
                word_count=0, estimated_duration=0.0, language_blend_count=0,
                trending_term_count=0, content_sections=0, research_depth_score=0.0,
                originality_score=0.0, engagement_potential=0.0
            )
    
    def _calculate_research_depth(self, text: str) -> float:
        """Calculate research depth score based on content complexity"""
        try:
            text_lower = text.lower()
            
            # Count complexity keywords
            complexity_count = sum(1 for keyword in self.complexity_keywords if keyword in text_lower)
            
            # Count numbers and statistics (indicators of research)
            number_count = len(re.findall(r'\d+', text))
            
            # Count citations or references
            citation_indicators = len(re.findall(r'according to|study shows|research|source|reference', text_lower))
            
            # Calculate score (0.0 to 1.0)
            score = min(1.0, (complexity_count * 0.2 + number_count * 0.01 + citation_indicators * 0.1))
            
            return score
            
        except Exception as e:
            self.logger.error(f"Error calculating research depth: {e}")
            return 0.0
    
    def _calculate_originality_score(self, script_data: Dict) -> float:
        """Calculate originality score based on unique elements"""
        try:
            score = 0.0
            
            # Language blending uniqueness
            language_blends = script_data.get('language_blends', [])
            if language_blends:
                score += 0.4  # High originality from language blending
            
            # Cultural perspective
            cultural_indicators = ['yoruba', 'nigerian', 'african', 'culture', 'tradition']
            script_text = str(script_data).lower()
            cultural_count = sum(1 for indicator in cultural_indicators if indicator in script_text)
            score += min(0.3, cultural_count * 0.1)
            
            # Unique content structure
            if script_data.get('hook') and script_data.get('call_to_action'):
                score += 0.2
            
            # Trending terms integration
            if script_data.get('trending_terms'):
                score += 0.1
            
            return min(1.0, score)
            
        except Exception as e:
            self.logger.error(f"Error calculating originality: {e}")
            return 0.0
    
    def _calculate_engagement_potential(self, text: str) -> float:
        """Calculate engagement potential score"""
        try:
            text_lower = text.lower()
            
            # Count engagement indicators
            engagement_count = sum(1 for indicator in self.engagement_indicators if indicator in text_lower)
            
            # Count questions (engagement drivers)
            question_count = text.count('?')
            
            # Count exclamations (emotional engagement)
            exclamation_count = text.count('!')
            
            # Calculate score
            score = min(1.0, (engagement_count * 0.2 + question_count * 0.05 + exclamation_count * 0.03))
            
            return score
            
        except Exception as e:
            self.logger.error(f"Error calculating engagement: {e}")
            return 0.0
    
    def _generate_improvement_suggestions(self, metrics: ContentMetrics) -> List[str]:
        """Generate specific improvement suggestions based on metrics"""
        suggestions = []
        
        if metrics.estimated_duration < self.min_duration_minutes:
            suggestions.append("Add 2-3 more content sections to reach 8+ minutes")
        
        if metrics.word_count < self.min_word_count:
            suggestions.append("Expand each section with more detailed explanations")
        
        if metrics.language_blend_count < self.min_language_blends:
            suggestions.append("Integrate more English-Yoruba language blending throughout the script")
        
        if metrics.research_depth_score < self.min_research_score:
            suggestions.append("Include more statistics, studies, and research-backed information")
        
        if metrics.originality_score < self.min_originality_score:
            suggestions.append("Add more unique cultural perspectives and language fusion")
        
        if metrics.engagement_potential < self.min_engagement_score:
            suggestions.append("Include more hooks, questions, and engaging call-to-actions")
        
        return suggestions
    
    def validate_batch_content(self, scripts: List[Dict]) -> List[ValidationResult]:
        """Validate multiple scripts in batch"""
        results = []
        
        for i, script in enumerate(scripts):
            self.logger.info(f"Validating script {i+1}/{len(scripts)}")
            result = self.validate_video_script(script)
            results.append(result)
        
        return results
    
    def get_validation_summary(self, results: List[ValidationResult]) -> Dict:
        """Generate summary of batch validation results"""
        if not results:
            return {"error": "No validation results to summarize"}
        
        valid_count = sum(1 for r in results if r.is_valid)
        total_count = len(results)
        avg_score = sum(r.score for r in results) / total_count
        
        # Collect all issues and recommendations
        all_issues = []
        all_recommendations = []
        
        for result in results:
            all_issues.extend(result.issues)
            all_recommendations.extend(result.recommendations)
        
        # Count most common issues
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        return {
            "total_scripts": total_count,
            "valid_scripts": valid_count,
            "validation_rate": f"{(valid_count/total_count)*100:.1f}%",
            "average_score": f"{avg_score:.2f}",
            "most_common_issues": sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "total_recommendations": len(all_recommendations),
            "validation_date": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    # Initialize validator
    validator = HighEffortContentValidator()
    
    # Sample script data for testing
    sample_script = {
        "hook": "You won't believe what's happening with trending music!",
        "introduction": "Today we're diving deep into the latest viral songs and breaking down why they're so popular.",
        "main_content": [
            "First, let's analyze the beat structure and why it's so catchy.",
            "Next, we'll look at the lyrics and cultural significance.",
            "Finally, we'll explore how this fits into current music trends."
        ],
        "transitions": ["Now let's move on to", "This brings us to"],
        "conclusion": "The future of music is here, and it's absolutely incredible!",
        "call_to_action": "Don't forget to like, subscribe, and share this video!",
        "language_blends": ["omo", "abeg", "jare"],
        "trending_terms": ["viral", "trending", "fire"]
    }
    
    # Validate the script
    print("🔍 Validating sample script...")
    result = validator.validate_video_script(sample_script)
    
    print(f"\n📊 Validation Results:")
    print(f"Valid: {'✅' if result.is_valid else '❌'}")
    print(f"Score: {result.score:.2f}/1.0")
    
    if result.issues:
        print(f"\n❌ Issues Found:")
        for issue in result.issues:
            print(f"  • {issue}")
    
    if result.recommendations:
        print(f"\n💡 Recommendations:")
        for rec in result.recommendations:
            print(f"  • {rec}")
    
    print(f"\n📅 Validated: {result.validation_date}")
