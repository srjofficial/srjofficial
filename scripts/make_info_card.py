import os

def generate_neofetch_svg(output_path="info-card.svg"):
    # Check if we should render a static (frozen) frame without animations
    is_static = os.environ.get("STATIC") == "1"
    
    # Neofetch data
    title = "saroj@srjofficial"
    separator = "-" * len(title)
    
    # The requested key/value rows. You can edit these values!
    data = [
        ("Now", "Building a dynamic automated GitHub profile"),
        ("Prev", "Exploring new libraries and frameworks"),
        ("Stack", "Python, SVG, Open Source Magic"),
        ("Highlights", "Creating self-typing terminal SVGs")
    ]
    
    # SVG Dimensions
    width = 450
    height = 200
    font_size = 14
    line_height = 22
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    # CSS styling tailored to look like a terminal UI (GitHub Dark theme inspired)
    svg_lines.append("""
    <style>
        .text {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 14px;
        }
        .title { fill: #58a6ff; font-weight: bold; }
        .sep { fill: #8b949e; }
        .key { fill: #7ee787; font-weight: bold; }
        .val { fill: #c9d1d9; }
    </style>
    """)
    
    y_pos = 30
    delay = 0.0
    delay_step = 0.15
    anim_dur = "0.5s"
    
    def get_group_tag(delay_sec):
        if is_static:
            return '  <g>'
        else:
            return (f'  <g opacity="0">\n'
                    f'    <animate attributeName="opacity" values="0;1" begin="{delay_sec}s" dur="{anim_dur}" fill="freeze" />\n'
                    f'    <animateTransform attributeName="transform" type="translate" values="-15 0; 0 0" begin="{delay_sec}s" dur="{anim_dur}" fill="freeze" />')
            
    # Draw Title
    svg_lines.append(get_group_tag(delay))
    svg_lines.append(f'    <text x="20" y="{y_pos}" class="text title">{title}</text>')
    svg_lines.append('  </g>')
    y_pos += line_height
    delay += delay_step
    
    # Draw Separator
    svg_lines.append(get_group_tag(delay))
    svg_lines.append(f'    <text x="20" y="{y_pos}" class="text sep">{separator}</text>')
    svg_lines.append('  </g>')
    y_pos += line_height
    delay += delay_step
    
    # Draw Rows
    for key, val in data:
        svg_lines.append(get_group_tag(delay))
        svg_lines.append(f'    <text x="20" y="{y_pos}" class="text key">{key}</text>')
        # Align the values nicely to the right of the keys
        svg_lines.append(f'    <text x="130" y="{y_pos}" class="text val">{val}</text>')
        svg_lines.append('  </g>')
        
        y_pos += line_height
        delay += delay_step
        
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
        
    print(f"Saved neofetch info card to {output_path} (STATIC={is_static})")

if __name__ == "__main__":
    generate_neofetch_svg()
