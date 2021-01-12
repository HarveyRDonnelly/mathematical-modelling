# Copyright Harvey Donnelly 2021
# www.donl.io 
# 'ln(1-x) Maclaurin Series Approximations'

from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation
import matplotlib.pyplot as plot
import numpy as np
import seaborn as sns
import math
from math import pi

# Plot Variables
plotTitle = 'ln(1-x) Maclaurin Series Approximations'
initalCoefficient = [0]
animationFileName = 'lnApproximations.gif'

# Constants
minimumDegree = 0
maximimumDegree = 50
initDegree = 7

rcStyle = {
    'axes.facecolor':'k',
    'figure.facecolor':'k',
    'axes.edgecolor':'w',
    'xtick.color':'w',
    'ytick.color':'w',
    'axes.labelcolor': 'w',
    'grid.color': 'grey'
}

# Coefficient Function
def lnMaclaurinSeriesCoefficients(degree):
    coefficients = initalCoefficient

    for i in range(degree - 1):
        coefficients = coefficients + [((-1)*(math.factorial(i))) / math.factorial(i+1)]

    return np.array(list(reversed(coefficients)))

# Animation Functions
def animate(i):
    global approximationPolynomial, approximationPlot

    if (slider.val != i):
        slider.set_val(val=i)

    approximationPolynomial = np.poly1d(lnMaclaurinSeriesCoefficients(i))
    approximationPlot.remove()
    approximationPlot, = plot.plot(x, approximationPolynomial(x), 'r')
    figure.canvas.draw()
    return approximationPlot,

def playAnimation(self):
    anim = animation.FuncAnimation(figure, animate, frames=np.arange(minimumDegree, (maximimumDegree + 1), 1), interval=25, blit=True, repeat=False)
    plot.show()

def saveAnimation(self):
    anim = animation.FuncAnimation(figure, animate, frames=np.arange(minimumDegree, (maximimumDegree + 1), 1), interval=25, blit=True, repeat=False)
    anim.save(animationFileName, fps=5)

# Plot Rendering Function
def update(a):
    global approximationPolynomial, approximationPlot

    if (slider.val != a):
        slider.set_val(val=a)
    
    approximationPolynomial = np.poly1d(lnMaclaurinSeriesCoefficients(a))
    approximationPlot.remove()
    approximationPlot, = plot.plot(x, approximationPolynomial(x), 'r')
    figure.canvas.draw_idle()

# SNS Theme Setup
sns.set_theme(context='paper', style='darkgrid', palette='deep', font='Century Gothic', font_scale=1, color_codes=True, rc=rcStyle)

# Figure Setuo
figure = plot.figure(figsize=(8,6))
x = np.linspace(-12*pi, 12*pi, 500)

approximationPolynomial = np.poly1d(lnMaclaurinSeriesCoefficients(initDegree))

# Axes Setup
plotAxes = plot.axes([0.1, 0.30, 0.8, 0.6])
sliderAxes = plot.axes([0.1, 0.175, 0.8, 0.05])
playAnimationButtonAxes = plot.axes([0.58, 0.05, 0.15, 0.05])
saveAnimationButtonAxes = plot.axes([0.75, 0.05, 0.15, 0.05])

# Plot Setup
plot.axes(plotAxes)
plot.title(plotTitle, weight='bold').set(color='w', fontsize='18')
plot.xlim(-12*pi, 12*pi)
plot.ylim(-4, 4)

# ln(1 - x) and Approximation Plot Setup
lnPlot, = plot.plot(x, np.log(1 - x), 'khaki')
approximationPlot, = plot.plot(x, approximationPolynomial(x), 'r')

# Slider Setup
slider = Slider(sliderAxes, label='Degree', valmin=minimumDegree, valmax=maximimumDegree, valinit=initDegree, color='c', valstep=1)
sliderTicks = np.arange(minimumDegree, maximimumDegree, 2)
sliderAxes.xaxis.set_visible(True)
sliderAxes.set_xticks(sliderTicks)
slider.label.set(color='w', weight='bold')
slider.valtext.set(color='w', weight='bold')

# Play Animation Button Setup
playAnimationButton = Button(playAnimationButtonAxes, 'Play Animation', color='k', hovercolor='cadetblue')
playAnimationButton.label.set(color='w', weight='bold')
playAnimationButton.on_clicked(playAnimation)

# Save Animation Button Setup
saveAnimationButton = Button(saveAnimationButtonAxes, 'Save Animation', color='k', hovercolor='cadetblue')
saveAnimationButton.label.set(color='w', weight='bold')
saveAnimationButton.on_clicked(saveAnimation)

# Slider Listener
slider.on_changed(update)

# Display Plot
plot.show()