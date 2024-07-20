from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles

# Sample sets
set1 = {'dogs', 'cats'}
set2 = {'cats', 'parrots'}

# Create figure and axes
fig, ax = plt.subplots(figsize=(8, 6))

# Create the Venn diagram with smaller circles
venn2_subsets = venn2([set1, set2], set_labels=(
    'A', 'B'), ax=ax, normalize_to=0.7, set_colors=('white', 'white'))  # Reduce size to 70%

# Add black borders to the circles
venn2_circles([set1, set2], ax=ax, linewidth=2,
              color='black', normalize_to=0.7)

# Adjust label positions to top of circles
for label in venn2_subsets.set_labels:
    label.set_y(label.get_position()[1] + 0.90)  # Move labels up

# Adding subset labels
venn2_subsets.get_label_by_id('10').set_text('250-x')
venn2_subsets.get_label_by_id('01').set_text('200-x')
venn2_subsets.get_label_by_id('11').set_text('x')

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
ax.text(0.90, 0.05, "25", fontsize=18, fontweight='bold',
        ha='right', va='bottom', transform=ax.transAxes)
ax.text(0.98, 0.92, "U", fontsize=18, fontweight='bold',
        ha='right', va='bottom', transform=ax.transAxes)

# Display the plot
plt.show()
