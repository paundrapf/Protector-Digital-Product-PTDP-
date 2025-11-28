#!/usr/bin/env python3
"""Convert SVG icons to ICO format for Windows applications."""

import cairosvg
from PIL import Image
import io
import os

def svg_to_ico(svg_path, ico_path, sizes=[16, 32, 48, 64, 128, 256]):
    """Convert SVG to ICO with multiple sizes."""
    
    # Read SVG
    with open(svg_path, 'rb') as f:
        svg_data = f.read()
    
    # Create images at different sizes
    images = []
    for size in sizes:
        # Convert SVG to PNG at specific size
        png_data = cairosvg.svg2png(
            bytestring=svg_data,
            output_width=size,
            output_height=size
        )
        
        # Open as PIL Image
        img = Image.open(io.BytesIO(png_data))
        img = img.convert('RGBA')
        images.append(img)
    
    # Save as ICO
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    
    print(f"Created: {ico_path}")

def main():
    # Directory setup
    base_dir = "/workspaces/Protector-Digital-Product-PTDP-"
    icons_dir = os.path.join(base_dir, "assets", "icons")
    
    # Convert each icon
    icons = [
        ("creator_icon.svg", "creator_icon.ico"),
        ("viewer_icon.svg", "viewer_icon.ico"),
        ("installer_icon.svg", "installer_icon.ico"),
    ]
    
    for svg_name, ico_name in icons:
        svg_path = os.path.join(icons_dir, svg_name)
        ico_path = os.path.join(icons_dir, ico_name)
        
        if os.path.exists(svg_path):
            svg_to_ico(svg_path, ico_path)
        else:
            print(f"Warning: {svg_path} not found")
    
    print("\nAll icons converted successfully!")

if __name__ == "__main__":
    main()
