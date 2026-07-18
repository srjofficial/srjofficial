import sys
from PIL import Image
import html

RAMP = " .`:-=+*cs#%@"

def make_ascii_svg(input_path="source-prepped.png", output_path="avi-ascii.svg"):
    try:
        img = Image.open(input_path).convert("L")
    except Exception as e:
        print(f"Error opening {input_path}: {e}")
        print("Make sure you run prep_photo.py first to generate the prepped image.")
        sys.exit(1)
        
    # Downsample to a character grid (~100x53)
    img = img.resize((100, 53), Image.Resampling.LANCZOS)
    
    # Map pixels to ascii
    pixels = list(img.getdata())
    width, height = img.size
    
    ascii_rows = []
    for y in range(height):
        row = ""
        for x in range(width):
            pixel = pixels[y * width + x]
            # 255 (white) maps to index 0 (space). 0 (black) maps to max index (@).
            idx = int((255 - pixel) / 255 * (len(RAMP) - 1))
            # clamp to valid range just in case
            idx = max(0, min(len(RAMP) - 1, idx))
            row += RAMP[idx]
        ascii_rows.append(row)
        
    # SVG parameters
    font_size = 12
    char_width = 7.2  # Approximate width of a 12px monospace character
    svg_width = int(width * char_width)
    svg_height = int(height * font_size) + 20
    
    svg_lines = []
    # Base SVG tag
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    
    # CSS styling
    svg_lines.append("""
    <style>
        .txt {
            font-family: monospace;
            font-size: 12px;
            fill: #a0a0a0;
            white-space: pre;
        }
        .cursor {
            fill: #a0a0a0;
        }
    </style>
    """)
    
    # Animation settings
    delay_per_row = 0.05
    type_duration = 0.8
    
    # Definitions for clip paths
    svg_lines.append('  <defs>')
    for i in range(height):
        start_time = i * delay_per_row
        svg_lines.append(f'    <clipPath id="clip-{i}">')
        svg_lines.append(f'      <rect x="0" y="{i * font_size}" width="0" height="{font_size + 5}">')
        svg_lines.append(f'        <animate attributeName="width" from="0" to="{svg_width}" begin="{start_time}s" dur="{type_duration}s" fill="freeze" />')
        svg_lines.append(f'      </rect>')
        svg_lines.append(f'    </clipPath>')
    svg_lines.append('  </defs>')
    
    # ASCII text wrapped in groups with clip paths, and cursors
    for i in range(height):
        start_time = i * delay_per_row
        row_text = html.escape(ascii_rows[i])
        y_pos = (i + 1) * font_size
        
        # Wrapped text
        svg_lines.append(f'  <g clip-path="url(#clip-{i})">')
        # xml:space="preserve" ensures leading/trailing spaces aren't stripped
        svg_lines.append(f'    <text x="0" y="{y_pos}" class="txt" xml:space="preserve">{row_text}</text>')
        svg_lines.append(f'  </g>')
        
        # Cursor element
        svg_lines.append(f'  <rect class="cursor" x="0" y="{i * font_size + 2}" width="{char_width}" height="{font_size}">')
        svg_lines.append(f'    <animate attributeName="x" from="0" to="{svg_width}" begin="{start_time}s" dur="{type_duration}s" fill="freeze" />')
        svg_lines.append(f'    <animate attributeName="opacity" values="1;1;0" keyTimes="0;0.99;1" begin="{start_time}s" dur="{type_duration}s" fill="freeze" />')
        svg_lines.append(f'  </rect>')
        
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
        
    print(f"Saved ASCII SVG to {output_path}")

if __name__ == "__main__":
    make_ascii_svg()
