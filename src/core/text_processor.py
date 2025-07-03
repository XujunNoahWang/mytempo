"""
Text processing and Markdown parsing for MyTempo application.
"""

import re
from typing import List, Tuple, Dict, Any
from ..utils.constants import CHINESE_FONT, ENGLISH_FONT


class TextProcessor:
    """Handles text processing and Markdown parsing"""
    
    @staticmethod
    def is_chinese_char(char: str) -> bool:
        """Check if character is Chinese.
        
        Args:
            char: Character to check
            
        Returns:
            True if character is Chinese
        """
        return '\u4e00' <= char <= '\u9fff'
    
    @staticmethod
    def get_font_tag(char: str, base_tag: str = '') -> str:
        """Get appropriate font tag for character.
        
        Args:
            char: Character to get font for
            base_tag: Base tag to append to
            
        Returns:
            Font tag string
        """
        prefix = 'zh' if TextProcessor.is_chinese_char(char) else 'en'
        return f'{prefix}_{base_tag}' if base_tag else prefix
    
    @staticmethod
    def process_heading(line: str, level: int) -> List[Tuple[str, str]]:
        """Process heading line.
        
        Args:
            line: Line content
            level: Heading level (1-6)
            
        Returns:
            List of (character, tag) tuples
        """
        # Remove heading markers
        marker_length = level + 1  # # for level 1, ## for level 2, etc.
        title_text = line[marker_length:].strip()
        
        result = []
        for char in title_text:
            tag = TextProcessor.get_font_tag(char, f'h{level}')
            result.append((char, tag))
        result.append(('\n', ''))
        
        return result
    
    @staticmethod
    def process_horizontal_line() -> List[Tuple[str, str]]:
        """Process horizontal line.
        
        Returns:
            List of (character, tag) tuples
        """
        return [('─' * 10, 'horizontal_line'), ('\n', '')]
    
    @staticmethod
    def process_quote(line: str) -> List[Tuple[str, str]]:
        """Process quoted text.
        
        Args:
            line: Line content
            
        Returns:
            List of (character, tag) tuples
        """
        quote_text = line[2:].strip()  # Remove > and spaces
        result = []
        
        # Add quote indicator
        result.append((' ' * 5 + '│ ', 'horizontal_line'))
        
        # Process text format inside quote
        formatted_chars = TextProcessor._process_text_format(quote_text, ['quote'])
        result.extend(formatted_chars)
        result.append(('\n', ''))
        
        return result
    
    @staticmethod
    def _process_text_format(text: str, base_tags: List[str] = None) -> List[Tuple[str, str]]:
        """Process text formatting from inside to outside.
        
        Args:
            text: Text to process
            base_tags: Base tags to apply
            
        Returns:
            List of (character, tag) tuples
        """
        if base_tags is None:
            base_tags = []
        
        def apply_format(text: str, tags: List[str]) -> List[Tuple[str, str]]:
            """Apply format to text."""
            result = []
            for char in text:
                char_tags = []
                if TextProcessor.is_chinese_char(char):
                    base = 'zh'
                else:
                    base = 'en'
                
                # Process tag combination
                all_tags = tags + base_tags
                if all_tags:
                    tag_combination = '_'.join(sorted(all_tags))
                    char_tags.append(f'{base}_{tag_combination}')
                else:
                    char_tags.append(base)
                
                result.append((char, char_tags[0]))
            return result
        
        def process_formats(text: str, current_tags: List[str]) -> List[Tuple[str, str]]:
            """Process text format recursively."""
            # Try to match different formats
            bold_match = re.search(r'\*\*(.*?)\*\*', text)
            highlight_match = re.search(r'==(.*?)==', text)
            italic_match = re.search(r'[*_](.*?)[*_]', text)
            
            if not any([bold_match, highlight_match, italic_match]):
                # If no format mark is found, output text directly
                return apply_format(text, current_tags)
            
            # Select the first found format mark
            matches = []
            if bold_match:
                matches.append(('bold', bold_match))
            if highlight_match:
                matches.append(('highlight', highlight_match))
            if italic_match:
                matches.append(('italic', italic_match))
            
            # Sort by start position
            matches.sort(key=lambda x: x[1].start())
            format_type, match = matches[0]
            
            result = []
            
            # Process text before format mark
            if match.start() > 0:
                result.extend(apply_format(text[:match.start()], current_tags))
            
            # Process text with format
            inner_text = match.group(1)
            result.extend(process_formats(inner_text, current_tags + [format_type]))
            
            # Process text after format mark
            if match.end() < len(text):
                result.extend(process_formats(text[match.end():], current_tags))
            
            return result
        
        return process_formats(text, [])
    
    @staticmethod
    def process_normal_line(line: str) -> List[Tuple[str, str]]:
        """Process normal text line.
        
        Args:
            line: Line content
            
        Returns:
            List of (character, tag) tuples
        """
        if not line:
            return [('\n', '')]
        
        result = TextProcessor._process_text_format(line)
        result.append(('\n', ''))
        return result
    
    @staticmethod
    def parse_markdown(content: str) -> List[Tuple[str, str]]:
        """Parse Markdown content into formatted characters.
        
        Args:
            content: Raw Markdown content
            
        Returns:
            List of (character, tag) tuples
        """
        lines = content.split('\n')
        result = []
        
        for line in lines:
            if line.startswith('# '):
                result.extend(TextProcessor.process_heading(line, 1))
            elif line.startswith('## '):
                result.extend(TextProcessor.process_heading(line, 2))
            elif line.startswith('### '):
                result.extend(TextProcessor.process_heading(line, 3))
            elif line.startswith('#### '):
                result.extend(TextProcessor.process_heading(line, 4))
            elif line.startswith('##### '):
                result.extend(TextProcessor.process_heading(line, 5))
            elif line.startswith('###### '):
                result.extend(TextProcessor.process_heading(line, 6))
            elif line == '---':
                result.extend(TextProcessor.process_horizontal_line())
            elif line.startswith('> '):
                result.extend(TextProcessor.process_quote(line))
            else:
                result.extend(TextProcessor.process_normal_line(line))
        
        return result 