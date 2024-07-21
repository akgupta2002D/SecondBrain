import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles


def create_venn_diagram(setA, setB, AnB, U_AuB, labelA='A', labelB='B'):
    # Calculate the universal set size
    U = setA + setB + U_AuB - \
        AnB if isinstance(setA, (int, float)) and isinstance(
            setB, (int, float)) else 'x'

    # Calculate sizes for venn2
    s10 = setA - AnB if isinstance(setA, (int, float)
                                   ) and isinstance(AnB, (int, float)) else 'x'
    s01 = setB - AnB if isinstance(setB, (int, float)
                                   ) and isinstance(AnB, (int, float)) else 'x'
    s11 = AnB

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create the Venn diagram with equal-sized circles
    venn2_subsets = venn2(subsets=(1, 1, 1), set_labels=(labelA, labelB),
                          ax=ax, normalize_to=1, set_colors=('white', 'white'))

    # Add black borders to the circles
    venn2_circles(subsets=(1, 1, 1), ax=ax, linewidth=2,
                  color='black', normalize_to=1)

    # Adjust label positions to top of circles
    for label in venn2_subsets.set_labels:
        label.set_y(label.get_position()[1] + 1.05)

    # Adding subset labels
    venn2_subsets.get_label_by_id('10').set_text(f'{s10}')
    venn2_subsets.get_label_by_id('01').set_text(f'{s01}')
    venn2_subsets.get_label_by_id('11').set_text(f'{s11}')

    # Customize font sizes and weights
    for text in venn2_subsets.subset_labels + venn2_subsets.set_labels:
        text.set_fontsize(14)
        text.set_fontweight('bold')

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
    ax.text(0.90, 0.05, str(U_AuB), fontsize=18, fontweight='bold',
            ha='right', va='bottom', transform=ax.transAxes)
    ax.text(0.98, 1.05, f"U: {U}", fontsize=18, fontweight='bold',
            ha='right', va='bottom', transform=ax.transAxes)

    plt.show()


def main():
    print("Enter values for the Venn diagram. Use 'x' for unknown values.")
    setA = input("Enter size of set A: ")
    setB = input("Enter size of set B: ")
    AnB = input("Enter size of intersection A and B: ")
    U_AuB = input("Enter size of U - (A union B): ")

    # Convert inputs to int if possible, otherwise keep as 'x'
    setA = int(setA) if setA.isdigit() else setA
    setB = int(setB) if setB.isdigit() else setB
    AnB = int(AnB) if AnB.isdigit() else AnB
    U_AuB = int(U_AuB) if U_AuB.isdigit() else U_AuB

    create_venn_diagram(setA, setB, AnB, U_AuB)


if __name__ == "__main__":
    main()
