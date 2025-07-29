#!/usr/bin/env python3
"""
Nigerian Content Creation - Visual Content Creator
Creates Instagram-ready images with one-liners on colored backgrounds
"""

import sqlite3
import os
import random
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import logging
from PIL import Image, ImageDraw, ImageFont
import textwrap
import re

logger = logging.getLogger(__name__)

class VisualContentCreator:
    def __init__(self, db_path: str = "content_creation.db", output_dir: str = "generated_images"):
        """Initialize the visual content creator"""
        self.db_path = db_path
        self.output_dir = output_dir
        self.setup_directories()
        self.setup_database()
        self.load_design_templates()
    
    def setup_directories(self):
        """Create output directories for generated images"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "instagram"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "twitter"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "facebook"), exist_ok=True)
    
    def setup_database(self):
        """Setup database table for tracking generated images"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS generated_images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_id INTEGER NOT NULL,
                    image_path TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    background_color TEXT,
                    font_size INTEGER,
                    text_color TEXT,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    posted BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (content_id) REFERENCES generated_content (id)
                )
            ''')
            conn.commit()
    
    def load_design_templates(self):
        """Load design templates and color schemes"""
        # Instagram-optimized color schemes
        self.color_schemes = {
            'naija_humor': [
                '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
                '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
            ],
            'tech_humor': [
                '#2C3E50', '#34495E', '#3498DB', '#2980B9', '#1ABC9C',
                '#16A085', '#27AE60', '#229954', '#F39C12', '#E67E22'
            ],
            'general_humor': [
                '#E74C3C', '#C0392B', '#9B59B6', '#8E44AD', '#3498DB',
                '#2980B9', '#1ABC9C', '#16A085', '#F1C40F', '#F39C12'
            ]
        }
        
        # Platform-specific dimensions
        self.platform_dimensions = {
            'instagram': {
                'square': (1080, 1080),
                'story': (1080, 1920),
                'portrait': (1080, 1350)
            },
            'twitter': {
                'square': (1200, 1200),
                'landscape': (1200, 675)
            },
            'facebook': {
                'square': (1200, 1200),
                'landscape': (1200, 630)
            }
        }
        
        # Text colors for different backgrounds
        self.text_colors = {
            'light': '#000000',  # Black text for light backgrounds
            'dark': '#FFFFFF'    # White text for dark backgrounds
        }
    
    def create_visual_content(self, content_items: List[Dict], platform: str = 'instagram', 
                            format_type: str = 'square') -> List[Dict]:
        """Create visual content for multiple one-liners"""
        generated_images = []
        
        for item in content_items:
            try:
                image_data = self._create_single_image(
                    text=item['one_liner'],
                    humor_type=item['humor_type'],
                    platform=platform,
                    format_type=format_type,
                    content_id=item['id']
                )
                
                if image_data:
                    generated_images.append(image_data)
                    
            except Exception as e:
                logger.error(f"Error creating image for content {item.get('id', 'unknown')}: {str(e)}")
        
        return generated_images
    
    def _create_single_image(self, text: str, humor_type: str, platform: str, 
                           format_type: str, content_id: int) -> Optional[Dict]:
        """Create a single visual image"""
        try:
            # Get dimensions for the platform and format
            dimensions = self.platform_dimensions[platform][format_type]
            width, height = dimensions
            
            # Create image with background
            background_color = self._get_background_color(humor_type)
            img = Image.new('RGB', dimensions, background_color)
            draw = ImageDraw.Draw(img)
            
            # Determine text color based on background brightness
            text_color = self._get_text_color(background_color)
            
            # Calculate optimal font size
            font_size = self._calculate_font_size(text, width, height)
            
            # Load font (fallback to default if custom font not available)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Wrap text to fit image
            wrapped_text = self._wrap_text(text, width, font, draw)
            
            # Calculate text position (center)
            bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # Add some padding and styling
            x += random.randint(-20, 20)  # Slight random positioning
            y += random.randint(-20, 20)
            
            # Draw text with outline for better visibility
            self._draw_text_with_outline(draw, wrapped_text, (x, y), font, text_color)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"content_{content_id}_{timestamp}_{platform}_{format_type}.png"
            filepath = os.path.join(self.output_dir, platform, filename)
            
            # Save image
            img.save(filepath, 'PNG', quality=95)
            
            # Save to database
            self._save_image_record(content_id, filepath, platform, background_color, font_size, text_color)
            
            return {
                'content_id': content_id,
                'image_path': filepath,
                'platform': platform,
                'format_type': format_type,
                'background_color': background_color,
                'text_color': text_color,
                'font_size': font_size
            }
            
        except Exception as e:
            logger.error(f"Error creating single image: {str(e)}")
            return None
    
    def _get_background_color(self, humor_type: str) -> str:
        """Get a random background color based on humor type"""
        colors = self.color_schemes.get(humor_type, self.color_schemes['general_humor'])
        return random.choice(colors)
    
    def _get_text_color(self, background_color: str) -> str:
        """Determine text color based on background brightness"""
        # Convert hex to RGB
        hex_color = background_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Calculate brightness
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        
        # Return dark text for light backgrounds, light text for dark backgrounds
        return self.text_colors['dark'] if brightness < 128 else self.text_colors['light']
    
    def _calculate_font_size(self, text: str, width: int, height: int) -> int:
        """Calculate optimal font size based on text length and image dimensions"""
        base_size = min(width, height) // 15  # Base size
        
        # Adjust based on text length
        if len(text) < 50:
            return base_size
        elif len(text) < 100:
            return int(base_size * 0.8)
        else:
            return int(base_size * 0.6)
    
    def _wrap_text(self, text: str, max_width: int, font: ImageFont.FreeTypeFont, draw: ImageDraw.Draw) -> str:
        """Wrap text to fit within image width"""
        # Estimate characters per line based on font size
        avg_char_width = font.getbbox("W")[2]  # Use 'W' as reference for width
        chars_per_line = max(1, int(max_width * 0.8 / avg_char_width))
        
        # Split text into words
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            
            # Check if line is too long
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width > max_width * 0.8:
                # Remove last word and start new line
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word is too long, force break
                    lines.append(word)
                    current_line = []
        
        # Add remaining words
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def _draw_text_with_outline(self, draw: ImageDraw.Draw, text: str, position: Tuple[int, int], 
                               font: ImageFont.FreeTypeFont, text_color: str):
        """Draw text with outline for better visibility"""
        x, y = position
        
        # Draw outline (black)
        outline_color = '#000000'
        outline_width = 2
        
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:  # Skip the center
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=text_color)
    
    def _save_image_record(self, content_id: int, image_path: str, platform: str, 
                          background_color: str, font_size: int, text_color: str):
        """Save image record to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO generated_images (content_id, image_path, platform, background_color, font_size, text_color)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (content_id, image_path, platform, background_color, font_size, text_color))
            conn.commit()
    
    def get_unprocessed_content(self, limit: int = 10) -> List[Dict]:
        """Get unprocessed content for image creation"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM generated_content 
                WHERE image_created = FALSE AND quality_score > 0.4
                ORDER BY quality_score DESC, created_date DESC
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_content_as_image_created(self, content_id: int):
        """Mark content as having image created"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE generated_content SET image_created = TRUE WHERE id = ?', (content_id,))
            conn.commit()
    
    def get_generated_images(self, limit: int = 20) -> List[Dict]:
        """Get generated images for posting"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT gi.*, gc.one_liner, gc.category, gc.humor_type
                FROM generated_images gi
                JOIN generated_content gc ON gi.content_id = gc.id
                WHERE gi.posted = FALSE
                ORDER BY gi.created_date DESC
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_image_as_posted(self, image_id: int):
        """Mark image as posted"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE generated_images SET posted = TRUE WHERE id = ?', (image_id,))
            conn.commit()
    
    def create_batch_images(self, platform: str = 'instagram', count: int = 10):
        """Create a batch of images for posting"""
        logger.info(f"Creating batch of {count} images for {platform}")
        
        # Get unprocessed content
        content_items = self.get_unprocessed_content(count)
        
        if not content_items:
            logger.info("No unprocessed content found")
            return []
        
        # Create images
        generated_images = self.create_visual_content(content_items, platform)
        
        # Mark content as processed
        for item in content_items:
            self.mark_content_as_image_created(item['id'])
        
        logger.info(f"Successfully created {len(generated_images)} images")
        return generated_images
    
    def create_multi_platform_images(self, content_items: List[Dict]):
        """Create images for multiple platforms"""
        all_images = []
        
        platforms = ['instagram', 'twitter', 'facebook']
        formats = ['square']  # Can add 'story', 'landscape' as needed
        
        for platform in platforms:
            for format_type in formats:
                try:
                    images = self.create_visual_content(content_items, platform, format_type)
                    all_images.extend(images)
                except Exception as e:
                    logger.error(f"Error creating {platform} {format_type} images: {str(e)}")
        
        return all_images

if __name__ == "__main__":
    # Test the visual content creator
    creator = VisualContentCreator()
    
    # Test with sample content
    test_content = [
        {
            'id': 1,
            'one_liner': 'Only in Nigeria: naira devaluation but we still dey manage 😂',
            'humor_type': 'naija_humor'
        },
        {
            'id': 2,
            'one_liner': 'Tech people when AI takes over: *nervous laughter* 😅',
            'humor_type': 'tech_humor'
        }
    ]
    
    # Create test images
    images = creator.create_visual_content(test_content, 'instagram', 'square')
    
    print(f"Created {len(images)} test images:")
    for image in images:
        print(f"- {image['image_path']}")
        print(f"  Platform: {image['platform']}")
        print(f"  Background: {image['background_color']}")
        print() 