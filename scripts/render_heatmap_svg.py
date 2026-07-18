import json
import datetime
import os

# GitHub-ish green ramp: none -> brightest
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap(input_json="data/contributions.json", output_svg="contrib-heatmap.svg"):
    try:
        with open(input_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"{input_json} not found! Run fetch_contributions.py first.")
        return
        
    days = data["days"]
    stats = data["stats"]
    
    # Grid settings
    cell_size = 10
    cell_spacing = 3
    cell_total = cell_size + cell_spacing
    
    # Group days into weeks (columns)
    columns = []
    current_col = []
    
    for d in days:
        dt = datetime.datetime.strptime(d["date"], "%Y-%m-%d")
        
        # GitHub's heatmap starts on Sunday (weekday() == 6 in Python)
        day_of_week = (dt.weekday() + 1) % 7
        
        # If it's the very first column and doesn't start on a Sunday, pad the top
        if not columns and not current_col and day_of_week != 0:
            for _ in range(day_of_week):
                current_col.append(None)
                
        current_col.append(d)
        
        # Once a column hits 7 days (Sun-Sat), move to the next column
        if len(current_col) == 7:
            columns.append(current_col)
            current_col = []
            
    # Pad the last column if it ends early
    if current_col:
        while len(current_col) < 7:
            current_col.append(None)
        columns.append(current_col)
        
    # Calculate SVG dimensions
    svg_width = len(columns) * cell_total + 40
    svg_height = 7 * cell_total + 60
    
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    
    # CSS: Diagonal slide-down keyframes
    lines.append("""
    <style>
        .text { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
            font-size: 11px; 
            fill: #8b949e; 
        }
        .cell { 
            animation: slideDown 0.6s ease-out forwards; 
            opacity: 0; 
        }
        @keyframes slideDown {
            0% { opacity: 0; transform: translateY(-10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
    """)
    
    grid_x_offset = 20
    grid_y_offset = 20
    
    # Draw the rounded boxes
    for col_idx, col in enumerate(columns):
        x = grid_x_offset + col_idx * cell_total
        # Stagger the animation across columns for the slide-down effect
        delay = col_idx * 0.02 
        
        for row_idx, day in enumerate(col):
            if day is None:
                continue
                
            y = grid_y_offset + row_idx * cell_total
            
            # Map level to palette (clamping up to max palette length)
            level = min(len(PALETTE) - 1, day["level"])
            color = PALETTE[level]
            
            # Add slightly staggered delay per row to create a diagonal effect
            diag_delay = delay + (row_idx * 0.015)
            
            lines.append(f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" class="cell" style="animation-delay: {diag_delay:.3f}s;" />')
            
    # Draw Stats Footer and Legend
    legend_y = grid_y_offset + 7 * cell_total + 15
    
    # Stats string
    total = stats["total_last_year"]
    lines.append(f'  <text x="{grid_x_offset}" y="{legend_y + 9}" class="text">{total:,} contributions in the last year</text>')
    
    # Legend
    legend_x = svg_width - 150
    lines.append(f'  <text x="{legend_x}" y="{legend_y + 9}" class="text">Less</text>')
    
    for i, color in enumerate(PALETTE):
        lx = legend_x + 35 + i * cell_total
        lines.append(f'  <rect x="{lx}" y="{legend_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" />')
        
    lines.append(f'  <text x="{legend_x + 35 + len(PALETTE)*cell_total + 5}" y="{legend_y + 9}" class="text">More</text>')
    
    lines.append('</svg>')
    
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"Saved animated heatmap SVG to {output_svg}")

if __name__ == "__main__":
    render_heatmap()
