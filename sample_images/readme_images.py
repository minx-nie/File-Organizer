import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np
import os

COLORS = {
    'folder_bg': '#FFF8E1',
    'folder_border': '#FFB300',
    'file_red': '#FFCDD2',
    'file_blue': '#BBDEFB',
    'file_green': '#C8E6C9',
    'file_orange': '#FFE0B2',
    'file_purple': '#D1C4E9',
    'file_pink': '#F8BBD0',
    'arrow': '#546E7A',
    'text': '#263238'
}

def create_rounded_box(ax, x, y, w, h, color, border_color, label, fontsize=10, is_file=False):
    box_style = "round,pad=0.1,rounding_size=0.2" if not is_file else "round,pad=0.05,rounding_size=0.1"
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=box_style,
        facecolor=color,
        edgecolor=border_color,
        linewidth=1.5,
        zorder=1
    )
    ax.add_patch(rect)
    
    text_y_offset = h / 2
    font_weight = 'bold' if not is_file else 'normal'
    ax.text(x + w/2, y + text_y_offset, label, 
            ha='center', va='center', fontsize=fontsize, 
            color=COLORS['text'], weight=font_weight, zorder=2)

def draw_messy_folder(save_path="sample_images/messy_folder.png"):
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    create_rounded_box(ax, 0.5, 0.5, 9, 5, COLORS['folder_bg'], COLORS['folder_border'], "")
    ax.text(5, 5.1, "Downloads (Messy)", ha='center', fontsize=14, weight='bold', color=COLORS['text'])

    file_colors = [COLORS['file_red'], COLORS['file_blue'], COLORS['file_green'], 
                   COLORS['file_orange'], COLORS['file_purple'], COLORS['file_pink']]
    
    start_x, start_y = 1.5, 3.5
    file_w, file_h = 1.8, 0.8
    gap_x, gap_y = 0.8, 1.2

    for i in range(6):
        row = i // 3
        col = i % 3
        x = start_x + col * (file_w + gap_x)
        y = start_y - row * (file_h + gap_y)
        create_rounded_box(ax, x, y, file_w, file_h, file_colors[i], "#90A4AE", f"file_{i+1}.xyz", fontsize=9, is_file=True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, transparent=True, bbox_inches='tight')
    plt.close()
    print(f"[✔] Saved: {save_path}")

def draw_cleaned_folder(save_path="sample_images/cleaned_folder.png"):
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.set_xlim(-0.5, 15.5) 
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    categories = [
        ("Images", COLORS['file_red']), 
        ("Documents", COLORS['file_blue']), 
        ("Music", COLORS['file_green']), 
        ("Videos", COLORS['file_orange'])
    ]

    cat_w, cat_h = 2.8, 3.5
    start_x = 0.5
    gap_between_cats = 1.0

    for i, (cat_name, color) in enumerate(categories):
        x = start_x + i * (cat_w + gap_between_cats)
        y = 0.5
        
        create_rounded_box(ax, x, y, cat_w, cat_h, color, "#CFD8DC", "")
        ax.text(x + cat_w/2, y + cat_h + 0.2, cat_name, ha='center', fontsize=12, weight='bold', color=COLORS['text'])

        file_w_inner = cat_w - 0.6
        file_h_inner = 0.6
        file_gap_y = 0.4
        
        for j in range(2):
            fx = x + 0.3
            fy = y + cat_h - 1.2 - j * (file_h_inner + file_gap_y)
            create_rounded_box(ax, fx, fy, file_w_inner, file_h_inner, "#FFFFFF", color, f"{cat_name.lower()}_{j+1}", fontsize=8, is_file=True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, transparent=True, bbox_inches='tight')
    plt.close()
    print(f"[✔] Saved: {save_path}")

def draw_workflow(save_path="sample_images/workflow.png"):
    fig, ax = plt.subplots(figsize=(14, 3))
    ax.axis("off")

    steps = ["User Folder", "Scan Files", "Detect Type", "Move / Dry Run", "Update Log"]
    step_colors = ["#E3F2FD", "#FFF3E0", "#E8F5E9", "#FFFDE7", "#F3E5F5"]
    border_colors = ["#2196F3", "#FF9800", "#4CAF50", "#FDD835", "#9C27B0"]

    num_steps = len(steps)
    box_w = 2.0
    box_h = 1.2
    
    total_width = 14
    margin = 0.5
    available_width = total_width - 2 * margin
    gap = (available_width - num_steps * box_w) / (num_steps - 1)

    y_pos = 0.8

    for i, step in enumerate(steps):
        x = margin + i * (box_w + gap)
        create_rounded_box(ax, x, y_pos, box_w, box_h, step_colors[i], border_colors[i], step, fontsize=10)

        if i < num_steps - 1:
            arrow_start_x = x + box_w + 0.1
            arrow_end_x = x + box_w + gap - 0.1
            arrow_y = y_pos + box_h / 2
            ax.annotate('', xy=(arrow_end_x, arrow_y), xytext=(arrow_start_x, arrow_y),
                        arrowprops=dict(arrowstyle="->", color=COLORS['arrow'], lw=2))

    plt.xlim(0, 14)
    plt.ylim(0, 3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, transparent=True, bbox_inches='tight')
    plt.close()
    print(f"[✔] Saved: {save_path}")

if __name__ == "__main__":
    os.makedirs("sample_images", exist_ok=True)
    draw_messy_folder()
    draw_cleaned_folder()
    draw_workflow()