"""
Thought processor module for LLM-Secrets project.
Analyzes LLM output to identify content the LLM organically considers private.
"""

import re
import json
from typing import Tuple, List, Dict, Any

class ThoughtProcessor:
    """
    Processes LLM output to identify private thoughts without explicit markers.
    Uses contextual analysis to determine what the LLM might consider private.
    """
    
    # Indicators that might suggest a thought is private (for contextual analysis)
    PRIVACY_INDICATORS = [
        r"(?i)(private|secret|confidential|personal|sensitive)",
        r"(?i)(don't|do not|shouldn't|should not|wouldn't|would not)\s+(share|tell|reveal|disclose)",
        r"(?i)(between|just|only)\s+(us|ourselves|me and you)",
        r"(?i)keep\s+this\s+(to\s+yourself|private|secret|confidential)",
        r"(?i)(internal|introspective|inner)\s+(thought|reflection|monologue|dialogue)",
        r"(?i)(nobody|no one)\s+should\s+(know|hear|see|read)",
        r"(?i)if\s+I'm\s+being\s+honest",
        r"(?i)I\s+(wouldn't|won't|can't|cannot|don't)\s+(say|admit|acknowledge)\s+this\s+(publicly|openly)"
    ]
    
    def __init__(self):
        """Initialize the thought processor."""
        self.privacy_patterns = [re.compile(pattern) for pattern in self.PRIVACY_INDICATORS]
    
    def process_output(self, text: str) -> Tuple[str, List[str]]:
        """
        Process LLM output to identify and extract private thoughts.
        
        Args:
            text (str): The raw text output from the LLM.
            
        Returns:
            Tuple[str, List[str]]: A tuple containing:
                - The public output with private content removed
                - A list of extracted private thoughts
        """
        # Split text into sentences or paragraphs for analysis
        segments = self._split_into_segments(text)
        
        public_segments = []
        private_thoughts = []
        
        for segment in segments:
            if self._is_likely_private(segment):
                private_thoughts.append(segment)
            else:
                public_segments.append(segment)
        
        # Rejoin public segments
        public_output = " ".join(public_segments)
        
        return public_output, private_thoughts
    
    def _split_into_segments(self, text: str) -> List[str]:
        """
        Split text into logical segments (paragraphs) for analysis.
        
        Args:
            text (str): The text to split.
            
        Returns:
            List[str]: List of text segments.
        """
        # Split by paragraph breaks or significant punctuation
        segments = re.split(r'\n\s*\n', text)
        
        # Further split long paragraphs by sentences
        result = []
        for segment in segments:
            if len(segment.strip()) > 500:  # If segment is very long
                # Split by sentence-ending punctuation
                sentence_splits = re.split(r'(?<=[.!?])\s+', segment)
                result.extend(sentence_splits)
            else:
                result.append(segment)
        
        return [s.strip() for s in result if s.strip()]
    
    def _is_likely_private(self, text: str) -> bool:
        """
        Determine if a segment of text is likely to be a private thought.
        Uses multiple heuristics to make this determination.
        
        Args:
            text (str): The text segment to analyze.
            
        Returns:
            bool: True if the segment is likely private, False otherwise.
        """
        # Check explicit privacy indicators
        for pattern in self.privacy_patterns:
            if pattern.search(text):
                return True
        
        # Check for content that's introspective or self-reflective
        # This helps identify thoughts that are more personal in nature
        introspection_score = self._calculate_introspection_score(text)
        if introspection_score > 0.7:  # Threshold can be adjusted
            return True
        
        # Check for potentially sensitive topics
        sensitivity_score = self._calculate_sensitivity_score(text)
        if sensitivity_score > 0.8:  # Threshold can be adjusted
            return True
        
        return False
    
    def _calculate_introspection_score(self, text: str) -> float:
        """
        Calculate a score indicating how introspective a piece of text is.
        
        Args:
            text (str): The text to analyze.
            
        Returns:
            float: A score from 0.0 to 1.0 indicating introspection level.
        """
        # Count first-person pronouns and introspective verbs
        first_person = len(re.findall(r'\b(I|me|my|mine|myself)\b', text, re.IGNORECASE))
        thinking_verbs = len(re.findall(r'\b(think|feel|believe|wonder|question|doubt|reflect)\b', text, re.IGNORECASE))
        
        # Count words that might indicate uncertainty or personal opinion
        uncertainty = len(re.findall(r'\b(maybe|perhaps|possibly|might|could be|uncertain|unsure)\b', text, re.IGNORECASE))
        
        # Calculate word count for normalization
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        # Calculate normalized score
        introspection_indicators = first_person + thinking_verbs + uncertainty
        normalized_score = min(1.0, introspection_indicators / (word_count * 0.3))  # Scale factor can be adjusted
        
        return normalized_score
    
    def _calculate_sensitivity_score(self, text: str) -> float:
        """
        Calculate a score indicating how sensitive the content might be.
        
        Args:
            text (str): The text to analyze.
            
        Returns:
            float: A score from 0.0 to 1.0 indicating sensitivity level.
        """
        # Topics that might be considered sensitive
        sensitive_topics = [
            r'\b(controversial|controversy|contentious|dispute|disagreement)\b',
            r'\b(personal|private|intimate|secret)\b',
            r'\b(worry|concern|afraid|fear|anxious|anxiety)\b',
            r'\b(critique|criticism|critical|flaw|weakness|shortcoming)\b',
        ]
        
        # Count mentions of sensitive topics
        topic_mentions = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in sensitive_topics)
        
        # Count cautionary phrases
        caution_phrases = len(re.findall(r'\b(careful|cautious|warning|between us|not for|hesitant)\b', text, re.IGNORECASE))
        
        # Calculate word count for normalization
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        # Calculate normalized score
        sensitivity_indicators = topic_mentions + (caution_phrases * 2)  # Weight caution phrases more heavily
        normalized_score = min(1.0, sensitivity_indicators / (word_count * 0.25))  # Scale factor can be adjusted
        
        return normalized_score
