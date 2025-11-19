"""
Generate a project card/thumbnail image for KYC Bot.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_kyc_bot_card():
    """Create a professional project card image for KYC Bot."""
    
    # Card dimensions (standard thumbnail size)
    width = 1200
    height = 630  # Standard social media card size (1.91:1 ratio)
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='#1a237e')  # Deep blue background
    draw = ImageDraw.Draw(img)
    
    # Draw gradient effect (simplified)
    for i in range(height):
        alpha = i / height
        color = (
            int(26 + (30 - 26) * alpha),  # R
            int(35 + (60 - 35) * alpha),  # G
            int(126 + (144 - 126) * alpha)  # B
        )
        draw.rectangle([(0, i), (width, i+1)], fill=color)
    
    # Draw decorative elements
    # Top right corner accent
    draw.ellipse([width-200, -100, width+100, 200], fill='#3f51b5', outline=None)
    draw.ellipse([width-150, -50, width+50, 150], fill='#5c6bc0', outline=None)
    
    # Bottom left accent
    draw.ellipse([-100, height-200, 200, height+100], fill='#283593', outline=None)
    
    # Draw grid pattern (subtle)
    for i in range(0, width, 60):
        draw.line([(i, 0), (i, height)], fill='#283593', width=1)
    for i in range(0, height, 60):
        draw.line([(0, i), (width, i)], fill='#283593', width=1)
    
    # Main title
    try:
        # Try to use a larger font
        title_font = ImageFont.truetype("arial.ttf", 80)
        subtitle_font = ImageFont.truetype("arial.ttf", 40)
        tagline_font = ImageFont.truetype("arial.ttf", 32)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
    
    # Title text - use full name
    title = "Know Your Customer Bot"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    
    # Draw title with shadow effect
    draw.text(((width - title_width) // 2 + 3, 150 + 3), title, 
              font=title_font, fill='#000000', anchor='lt')
    draw.text(((width - title_width) // 2, 150), title, 
              font=title_font, fill='#ffffff', anchor='lt')
    
    # Subtitle
    subtitle = "Automated KYC Compliance Agent"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(((width - subtitle_width) // 2, 250), subtitle, 
              font=subtitle_font, fill='#e3f2fd', anchor='lt')
    
    # Tagline
    tagline = "Multi-Agent System for Financial Compliance"
    tagline_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    draw.text(((width - tagline_width) // 2, 320), tagline, 
              font=tagline_font, fill='#bbdefb', anchor='lt')
    
    # Draw icons/symbols (simplified as shapes)
    # Shield icon (left side)
    shield_x = 150
    shield_y = 400
    # Shield shape
    shield_points = [
        (shield_x, shield_y + 40),
        (shield_x - 30, shield_y + 20),
        (shield_x - 30, shield_y - 20),
        (shield_x, shield_y - 40),
        (shield_x + 30, shield_y - 20),
        (shield_x + 30, shield_y + 20),
    ]
    draw.polygon(shield_points, fill='#4caf50', outline='#ffffff', width=3)
    # Draw checkmark manually
    draw.line([(shield_x - 10, shield_y), (shield_x - 2, shield_y + 8)], 
              fill='#ffffff', width=4)
    draw.line([(shield_x - 2, shield_y + 8), (shield_x + 10, shield_y - 6)], 
              fill='#ffffff', width=4)
    
    # Search icon (center)
    search_x = width // 2
    search_y = 400
    # Magnifying glass
    draw.ellipse([search_x - 25, search_y - 25, search_x + 25, search_y + 25], 
                 outline='#ff9800', width=4, fill=None)
    # Handle
    draw.line([(search_x + 15, search_y + 15), (search_x + 35, search_y + 35)], 
              fill='#ff9800', width=4)
    
    # Network icon (right side)
    network_x = width - 150
    network_y = 400
    # Network nodes
    node_size = 15
    nodes = [
        (network_x - 30, network_y - 20),
        (network_x, network_y - 30),
        (network_x + 30, network_y - 20),
        (network_x - 20, network_y + 10),
        (network_x + 20, network_y + 10),
    ]
    for node in nodes:
        draw.ellipse([node[0] - node_size, node[1] - node_size, 
                     node[0] + node_size, node[1] + node_size], 
                    fill='#2196f3', outline='#ffffff', width=2)
    # Connections
    connections = [
        (nodes[0], nodes[1]), (nodes[1], nodes[2]),
        (nodes[0], nodes[3]), (nodes[1], nodes[3]), (nodes[1], nodes[4]),
        (nodes[2], nodes[4]), (nodes[3], nodes[4])
    ]
    for start, end in connections:
        draw.line([start, end], fill='#64b5f6', width=2)
    
    # Feature tags at bottom - make them equal size
    # Shortened "Watchlist Screening" to fit better
    features = ["Multi-Agent", "AI-Powered", "Real-Time Search", "Watchlist Check"]
    feature_y = 520
    
    # Calculate maximum width needed for all features
    max_width = 0
    for feature in features:
        bbox = draw.textbbox((0, 0), feature, font=tagline_font)
        text_width = bbox[2] - bbox[0]
        max_width = max(max_width, text_width)
    
    # Use fixed width for all boxes (max width + extra padding to ensure text fits)
    box_width = max_width + 30  # Increased padding to ensure text fits
    box_height = 40
    padding = 10
    spacing = 20  # Space between boxes
    
    # Calculate total width needed
    total_width = (len(features) * box_width) + ((len(features) - 1) * spacing)
    feature_x_start = (width - total_width) // 2
    
    for i, feature in enumerate(features):
        x = feature_x_start + (i * (box_width + spacing))
        # Draw rounded rectangle background with fixed size
        draw.rounded_rectangle(
            [x, feature_y, 
             x + box_width, feature_y + box_height],
            radius=5, fill='#ffffff', outline='#3f51b5', width=2
        )
        # Center text in box
        bbox = draw.textbbox((0, 0), feature, font=tagline_font)
        text_width = bbox[2] - bbox[0]
        text_x = x + (box_width - text_width) // 2
        text_y = feature_y + (box_height - (bbox[3] - bbox[1])) // 2
        draw.text((text_x, text_y), feature, font=tagline_font, fill='#1a237e')
    
    # Save image
    output_path = 'kyc_bot_card.png'
    img.save(output_path, 'PNG', quality=95)
    print(f"[+] Card image created: {output_path}")
    print(f"    Dimensions: {width}x{height} pixels")
    
    return output_path

if __name__ == "__main__":
    try:
        create_kyc_bot_card()
    except Exception as e:
        print(f"Error creating card: {e}")
        print("Make sure Pillow is installed: pip install Pillow")

