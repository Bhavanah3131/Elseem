import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def showgraph(name,x,y):
    # Sample data
    #months = ['nov','aug']
    #values = [x,y]

    # Define colors for each bar
    # colors = ['red','orange']

    # Create a bar plot with different colors for each bar
    #plt.bar(months, values)

    # Add labels and title
    plt.xlabel('months')
    plt.ylabel('Values')
    plt.title(name)

    # Display the graph
    plt.show()
def show_piechart(high,low,equal,new):
    if high is None:
        high = 0
    # Example data
    mylabels = ['Gain', 'Reduced', 'Stable', 'Recent']
    sizes = [high, low, equal, new]  # Proportions of the pie
    colors = ['green', 'red', 'grey', 'blue']  # Colors for each slice
    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=mylabels,
        colors=colors,
        wedgeprops={'width': 0.4},  # Controls the width of the donut
        startangle=90  # Rotates the chart for better visibility
    )

    # Display the donut chart
    ax.set_aspect('equal')  # Ensures the chart is a circle
    plt.title('Donut Chart Example')
    plt.show()

def show_line(nameofissuer,prev, new):
    months = ['august','november']
    values = [prev, new]

    # Create a simple line graph
    plt.figure(figsize=(8, 5))
    plt.plot(months, values, marker='o', color='blue', linestyle='-', label='Sample Data')

    # Add labels and title
    plt.title(nameofissuer, fontsize=16)
    plt.xlabel('Months', fontsize=12)
    plt.ylabel('Values', fontsize=12)

    # Add grid and legend
    plt.grid(alpha=0.5)
    plt.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()

def show_bar(Categories, values):
    Categories = ['Gain', 'Reduced', 'Stable', 'Recent']
   # sizes = [high, low, equal, new]  # Proportions of the pie
    Values=[high, low, equal, new]
    colors = ['green', 'red', 'grey', 'blue']


# Creating the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(Categories, values, color=colors)
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Simple Bar Graph Example')

    plt.show()

if __name__ == '__main__':
    # chart()
    # showgraph('bh',25,40)
    # import matplotlib.pyplot as plt
    show_piechart(30, 20, 50,20)  # Data to p
    
    #Categories=['high', 'low', 'equal', 'new']
    #values=[30, 20, 50,20]
    #show_bar(Categories, values)

    # Plot
    

