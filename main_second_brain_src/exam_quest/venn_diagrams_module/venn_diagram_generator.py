import sys
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles
import matplotlib.font_manager as fm
import os


def create_venn_diagram(setA, setB, AnB, U_AuB, labelA='A', labelB='B', filename='venn_diagram'):
    # Set up Nepali font
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(
        script_dir, 'NotoSansDevanagari-VariableFont_wdth,wght.ttf')
    nepali_font = fm.FontProperties(fname=font_path, weight='bold')

    # Calculate the universal set size
    if all(isinstance(x, (int, float)) for x in [setA, setB, AnB, U_AuB]):
        U = setA + setB + U_AuB - AnB
    else:
        U = 'x'

    # Calculate sizes for venn2
    s10 = setA - AnB if isinstance(setA, (int, float)
                                   ) and isinstance(AnB, (int, float)) else 'x'
    s01 = setB - AnB if isinstance(setB, (int, float)
                                   ) and isinstance(AnB, (int, float)) else 'x'
    s11 = AnB

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(12, 10))  # Increased figure size

    # Create the Venn diagram with equal-sized circles
    venn2_subsets = venn2(subsets=(1, 1, 1), set_labels=(labelA, labelB),
                          ax=ax, normalize_to=1, set_colors=('white', 'white'))

    # Add black borders to the circles
    venn2_circles(subsets=(1, 1, 1), ax=ax, linewidth=2,
                  color='black', normalize_to=1)

    # Adjust label positions and style
    for label in venn2_subsets.set_labels:
        label.set_y(label.get_position()[1] + 1.05)
        label.set_fontproperties(nepali_font)
        label.set_fontsize(24)  # Increased font size for set labels

    # Adding and styling subset labels
    for label_id in ['10', '01', '11']:
        label = venn2_subsets.get_label_by_id(label_id)
        if label:
            label.set_text(f'{locals()[f"s{label_id}"]}')
            label.set_fontproperties(nepali_font)
            label.set_fontsize(20)  # Increased font size for subset labels

    # Get current axis limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Expand axis limits to maintain original border
    expansion_factor = 1.2
    ax.set_xlim(xlim[0] * expansion_factor, xlim[1] * expansion_factor)
    ax.set_ylim(ylim[0] * expansion_factor, ylim[1] * expansion_factor)

    # Add a box around the Venn diagram
    ax.set_axis_on()
    ax.set_xticks([])
    ax.set_yticks([])

    # Add annotations
    ax.text(0.90, 0.05, str(U_AuB), fontsize=22, fontweight='bold',
            ha='right', va='bottom', transform=ax.transAxes, fontproperties=nepali_font)
    ax.text(0.98, 1.05, f"U: {U}", fontsize=22, fontweight='bold',
            ha='right', va='bottom', transform=ax.transAxes, fontproperties=nepali_font)

    # Save the figure with higher DPI for better quality
    plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
    plt.close()


def main():
    if len(sys.argv) == 8:
        # If command-line arguments are provided, use them
        setA, setB, AnB, U_AuB, labelA, labelB, filename = sys.argv[1:]
        setA = int(setA) if setA.isdigit() else 'x'
        setB = int(setB) if setB.isdigit() else 'x'
        AnB = int(AnB) if AnB.isdigit() else 'x'
        U_AuB = int(U_AuB) if U_AuB.isdigit() else 'x'
    else:
        # Otherwise, use interactive input
        print("Enter values for the Venn diagram. Use 'x' for unknown values.")
        setA = input("Enter size of set A: ")
        setB = input("Enter size of set B: ")
        AnB = input("Enter size of intersection A and B: ")
        U_AuB = input("Enter size of U - (A union B): ")
        labelA = input("Enter label for set A: ")
        labelB = input("Enter label for set B: ")
        filename = input(
            "Enter filename to save the image (without extension): ")

        # Convert inputs to int if possible, otherwise keep as 'x'
        setA = int(setA) if setA.isdigit() else 'x'
        setB = int(setB) if setB.isdigit() else 'x'
        AnB = int(AnB) if AnB.isdigit() else 'x'
        U_AuB = int(U_AuB) if U_AuB.isdigit() else 'x'

    create_venn_diagram(setA, setB, AnB, U_AuB, labelA, labelB, filename)
    print(f"Venn diagram saved as {filename}.png")


if __name__ == "__main__":
    main()
