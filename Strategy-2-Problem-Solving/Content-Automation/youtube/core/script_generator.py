"""
📝 Script Generator - Automated Video Script Creation
Generates engaging video scripts for faceless videos with language blending
"""

import random
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VideoScript:
    """Represents a complete video script"""
    title: str
    hook: str
    introduction: str
    main_content: List[str]
    transitions: List[str]
    conclusion: str
    call_to_action: str
    estimated_duration: int  # in minutes
    target_length: int  # target words for 8+ minute video
    language_blends: List[str]
    trending_terms: List[str]
    generated_date: datetime

class ScriptGenerator:
    """
    Generates automated video scripts for faceless videos
    Ensures high-effort content that meets YouTube monetization requirements
    """
    
    def __init__(self):
        """Initialize the script generator with templates and patterns"""
        self.hook_templates = [
            "Omo, you won't believe what I just discovered about {topic}!",
            "Abeg, {topic} is giving me serious wahala right now!",
            "Jare, let me tell you something about {topic} that will blow your mind!",
            "Sha, {topic} is the most {adjective} thing I've seen this week!",
            "Gan, {topic} is making waves and I need to break it down for you!",
            "O, {topic} is trending and I have some thoughts that will make you laugh!",
            "Ko, {topic} is not what you think it is! Let me explain why!"
        ]
        
        self.introduction_templates = [
            "Welcome back to the channel! Today we're diving deep into {topic}.",
            "If you're new here, make sure to subscribe because we're about to explore {topic}.",
            "Before we get into {topic}, hit that like button if you're excited about this!",
            "Today's video is all about {topic}, and trust me, you don't want to miss this!",
            "I've been researching {topic} for days, and what I found will surprise you!"
        ]
        
        self.transition_templates = [
            "Now, let's talk about something even more interesting...",
            "But wait, there's more to this story...",
            "Here's where it gets really {adjective}...",
            "Omo, you think that's all? Abeg, there's more!",
            "Jare, let me take this to another level...",
            "Sha, this is just the beginning...",
            "Gan, this is where the real {topic} begins!"
        ]
        
        self.conclusion_templates = [
            "So there you have it! {topic} is definitely {adjective}.",
            "Omo, {topic} is more complex than we thought, right?",
            "Abeg, what do you think about {topic}? Let me know in the comments!",
            "Jare, {topic} is giving us a lot to think about!",
            "Sha, that's my take on {topic}. What's yours?"
        ]
        
        self.call_to_action_templates = [
            "If you enjoyed this video, make sure to like, subscribe, and hit that notification bell!",
            "Don't forget to share this video with your friends who love {topic}!",
            "Comment below with your thoughts on {topic}! I love reading your opinions!",
            "Follow me on social media for more {topic} content and daily updates!",
            "Thanks for watching! See you in the next video where we'll explore even more {topic}!"
        ]
        
        # Content expansion phrases for 8+ minute videos
        self.expansion_phrases = [
            "Let me break this down even further...",
            "Here's another angle to consider...",
            "What makes this even more interesting is...",
            "Let me give you some examples...",
            "Here's why this matters...",
            "Let me explain this in detail...",
            "This connects to something bigger...",
            "Let me share a personal story about this...",
            "Here's what I learned from researching this...",
            "This reminds me of something else..."
        ]
    
    def generate_script(
        self,
        topic: str,
        context: str = "general",
        target_minutes: int = 8,
        extra_trending_terms: Optional[List[str]] = None,
    ) -> VideoScript:
        """
        Generate a complete video script for a given topic

        Args:
            topic: Main topic of the video
            context: Context (music, food, culture, etc.)
            target_minutes: Target video length in minutes
            extra_trending_terms: Optional terms from trending topic analysis

        Returns:
            Complete VideoScript object
        """
        # Calculate target word count (average speaking rate: 150 words per minute)
        target_words = target_minutes * 150
        
        # Generate script components
        hook = self._generate_hook(topic)
        introduction = self._generate_introduction(topic)
        main_content = self._generate_main_content(topic, context, target_words)
        transitions = self._generate_transitions(len(main_content), topic)
        conclusion = self._generate_conclusion(topic)
        call_to_action = self._generate_call_to_action(topic)
        
        # Extract language blends and trending terms
        language_blends = self._extract_language_blends(main_content)
        trending_terms = self._extract_trending_terms(main_content)
        if extra_trending_terms:
            merged = list(dict.fromkeys(trending_terms + extra_trending_terms))
            trending_terms = merged[:12]

        # Calculate estimated duration
        total_words = len(' '.join([hook, introduction] + main_content + 
                                 transitions + [conclusion, call_to_action]).split())
        estimated_duration = max(target_minutes, total_words // 150)
        
        return VideoScript(
            title=self._generate_title(topic),
            hook=hook,
            introduction=introduction,
            main_content=main_content,
            transitions=transitions,
            conclusion=conclusion,
            call_to_action=call_to_action,
            estimated_duration=estimated_duration,
            target_length=target_words,
            language_blends=language_blends,
            trending_terms=trending_terms,
            generated_date=datetime.now()
        )
    
    def _generate_hook(self, topic: str) -> str:
        """Generate an engaging hook for the video"""
        template = random.choice(self.hook_templates)
        adjectives = ["crazy", "insane", "amazing", "wild", "incredible", "unbelievable"]
        adjective = random.choice(adjectives)
        
        return template.format(topic=topic, adjective=adjective)
    
    def _generate_introduction(self, topic: str) -> str:
        """Generate video introduction"""
        template = random.choice(self.introduction_templates)
        return template.format(topic=topic)
    
    def _generate_main_content(self, topic: str, context: str, target_words: int) -> List[str]:
        """Generate main content sections to meet target word count"""
        content_sections = []
        current_words = 0
        
        # Core content topics based on context
        core_topics = self._get_core_topics(topic, context)
        
        for i, core_topic in enumerate(core_topics):
            if current_words >= target_words * 0.8:  # Leave room for intro/conclusion
                break
                
            # Generate content for this topic
            section = self._generate_content_section(core_topic, context)
            content_sections.append(section)
            
            # Add expansion phrases to meet word count
            if current_words < target_words * 0.6:
                expansion = self._add_expansion_content(section, topic)
                content_sections.append(expansion)
            
            current_words += len(section.split()) + len(expansion.split())
        
        return content_sections
    
    def _get_core_topics(self, topic: str, context: str) -> List[str]:
        """Get core topics to cover based on context"""
        if context == "music":
            return [
                f"History of {topic}",
                f"Why {topic} is trending",
                f"Cultural impact of {topic}",
                f"Language blending opportunities in {topic}",
                f"Future of {topic}"
            ]
        elif context == "food":
            return [
                f"Origin of {topic}",
                f"Cultural significance of {topic}",
                f"Modern variations of {topic}",
                f"Personal experiences with {topic}",
                f"Recommendations for {topic}"
            ]
        else:
            return [
                f"What is {topic}?",
                f"Why {topic} matters",
                f"Different perspectives on {topic}",
                f"Impact of {topic}",
                f"Future implications of {topic}"
            ]
    
    def _generate_content_section(self, core_topic: str, context: str) -> str:
        """Generate content for a specific topic"""
        base_content = f"Let's talk about {core_topic}. "
        
        # Add context-specific content
        if context == "music":
            base_content += f"This is where things get really interesting because music has a way of bringing people together. "
            base_content += f"When I think about {core_topic}, I can't help but notice how it connects to our daily lives. "
        elif context == "food":
            base_content += f"Food is such a universal language, and {core_topic} is no exception. "
            base_content += f"Every culture has its own take on this, and that's what makes it so fascinating. "
        else:
            base_content += f"This topic is more complex than it seems at first glance. "
            base_content += f"There are so many layers to explore, and each one reveals something new. "
        
        return base_content
    
    def _add_expansion_content(self, base_section: str, topic: str) -> str:
        """Add expansion content to meet word count requirements"""
        expansion = random.choice(self.expansion_phrases)
        
        # Add specific details
        details = [
            f"Let me give you some real examples of how {topic} affects our daily lives.",
            f"This connects to something bigger that we all experience.",
            f"Here's what I learned from researching this topic in depth.",
            f"This reminds me of other trends we've seen in the past.",
            f"Let me break down why this matters to you personally."
        ]
        
        detail = random.choice(details)
        return f"{expansion} {detail}"
    
    def _generate_transitions(self, content_count: int, topic: str) -> List[str]:
        """Generate transitions between content sections"""
        transitions = []
        adjectives = ["interesting", "fascinating", "amazing", "incredible", "wild"]
        
        for i in range(content_count - 1):
            template = random.choice(self.transition_templates)
            adjective = random.choice(adjectives)
            transition = template.format(adjective=adjective, topic=topic)
            transitions.append(transition)
        
        return transitions
    
    def _generate_conclusion(self, topic: str) -> str:
        """Generate video conclusion"""
        template = random.choice(self.conclusion_templates)
        adjectives = ["fascinating", "complex", "interesting", "amazing", "incredible"]
        adjective = random.choice(adjectives)
        
        return template.format(topic=topic, adjective=adjective)
    
    def _generate_call_to_action(self, topic: str) -> str:
        """Generate call to action"""
        template = random.choice(self.call_to_action_templates)
        return template.format(topic=topic)
    
    def _generate_title(self, topic: str) -> str:
        """Generate engaging video title"""
        title_templates = [
            "Omo, {topic} is Giving Me Serious Wahala!",
            "Abeg, Let Me Tell You About {topic}!",
            "Jare, {topic} is More Than You Think!",
            "Sha, {topic} is Trending and Here's Why!",
            "Gan, {topic} Will Blow Your Mind!",
            "O, {topic} is the Future!",
            "Ko, {topic} is Not What You Expect!"
        ]
        
        template = random.choice(title_templates)
        return template.format(topic=topic)
    
    def _extract_language_blends(self, content: List[str]) -> List[str]:
        """Extract language blending opportunities from content"""
        blends = []
        yoruba_words = ['omo', 'abeg', 'wahala', 'jare', 'sha', 'gan', 'o', 'ko']
        
        for section in content:
            words = section.lower().split()
            for word in words:
                if word in yoruba_words:
                    blends.append(word)
        
        return list(set(blends))  # Remove duplicates
    
    def _extract_trending_terms(self, content: List[str]) -> List[str]:
        """Extract potential trending terms from content"""
        trending_words = ['trending', 'viral', 'popular', 'hot', 'fire', 'lit', 'banging']
        terms = []
        
        for section in content:
            words = section.lower().split()
            for word in words:
                if word in trending_words:
                    terms.append(word)
        
        return list(set(terms))  # Remove duplicates
    
    def format_script_for_video(self, script: VideoScript) -> str:
        """Format script for easy reading during video creation"""
        formatted = f"🎥 VIDEO SCRIPT: {script.title}\n"
        formatted += f"📅 Generated: {script.generated_date.strftime('%Y-%m-%d %H:%M')}\n"
        formatted += f"⏱️ Target Duration: {script.estimated_duration} minutes\n"
        formatted += f"📝 Target Words: {script.target_length}\n\n"
        
        formatted += f"🎯 HOOK:\n{script.hook}\n\n"
        
        formatted += f"👋 INTRODUCTION:\n{script.introduction}\n\n"
        
        formatted += "📚 MAIN CONTENT:\n"
        for i, section in enumerate(script.main_content, 1):
            formatted += f"{i}. {section}\n"
            if i < len(script.transitions):
                formatted += f"   → {script.transitions[i-1]}\n"
            formatted += "\n"
        
        formatted += f"🎬 CONCLUSION:\n{script.conclusion}\n\n"
        
        formatted += f"📢 CALL TO ACTION:\n{script.call_to_action}\n\n"
        
        formatted += f"🔥 LANGUAGE BLENDS: {', '.join(script.language_blends)}\n"
        formatted += f"📈 TRENDING TERMS: {', '.join(script.trending_terms)}\n"
        
        return formatted

# Example usage
if __name__ == "__main__":
    generator = ScriptGenerator()
    
    # Generate a script for a music topic
    print("🎬 Generating video script...")
    script = generator.generate_script("Olivia Rodrigo's new song", "music", 8)
    
    # Format and display the script
    formatted_script = generator.format_script_for_video(script)
    print(formatted_script)
    
    print(f"\n📊 Script Statistics:")
    print(f"Title: {script.title}")
    print(f"Estimated Duration: {script.estimated_duration} minutes")
    print(f"Content Sections: {len(script.main_content)}")
    print(f"Language Blends: {len(script.language_blends)}")
    print(f"Trending Terms: {len(script.trending_terms)}")
