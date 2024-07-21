from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles

# Variables to control the display
setA = 50  # Size of set A
setB = 60  # Size of set B
AnB = 20   # Size of intersection A and B
U_AUB = 10  # Size of U - (A union B)
U = (setA + setB + U_AUB) - AnB     # Size of universal set
labelA = 'A'  # Label for set A
labelB = 'B'  # Label for set B

# Calculate sizes for venn2
s10 = setA - AnB  # In A but not in B
s01 = setB - AnB  # In B but not in A
s11 = AnB         # In both A and B

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
    label.set_y(label.get_position()[1] + 1.05)  # Move labels up

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
ax.set_axis_on()  # Turn on the axis
ax.set_xticks([])  # Remove x-axis ticks
ax.set_yticks([])  # Remove y-axis ticks

# Add annotations
ax.text(0.90, 0.05, str(U_AUB), fontsize=18, fontweight='bold',
        ha='right', va='bottom', transform=ax.transAxes)
ax.text(0.98, 1.05, "U: " + str(U), fontsize=18, fontweight='bold',
        ha='right', va='bottom', transform=ax.transAxes)

# Display the plot
plt.show()
