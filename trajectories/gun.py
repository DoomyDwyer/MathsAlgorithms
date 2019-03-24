# Calculate the trajectory of a projectile fired from a gun
#
# Source of mathematics and inspiration taken from Example 1: Predicting the range of a cannonball,
# Unit 10 Quadratics, Book C, MU123 Discovering Mathematics, The Open University
#
# Inspiration for the addition of angle θ to formulae for x and x-coordinates from
# https://www.101computing.net/projectile-motion-formula/
#
# Ballistic properties of .303 round from
# https://en.wikipedia.org/wiki/.303_British
#
# Author of python code: Steve Dwyer

import abc
from math import cos, sin, radians
from matplotlib import pyplot
from turtle import Turtle, Vec2D

# Define a class of planets with their respective values of the constant g,
# i.e. acceleration due to gravity (in metres per second squared)
# g on earth is approx 9.81, on mars 3.728 and on the surface of the moon 1.62
class Planet(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def g(self):
		pass

class Earth(Planet):
	def g(self):
		return 9.81

class Mars(Planet):
	def g(self):
		return 3.728

class Luna(Planet):
	def g(self):
		return 1.62

# A class of guns with their respective muzzle velocities
class Gun(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def muzzleVelocity(self):
		pass

# A shipborne cannon
class Cannon(Gun):
	def __init__(self):
		# Use floats, not integers, for all calculations
		self.v = 300.0 # Muzzle velocity of gun (in m/s)

	def muzzleVelocity(self):
		return self.v

# A Lee Enfield rifle with Mark VII .303 ammunition
class LeeEnfield303MarkVII(Gun):
	def __init__(self):
		# Use floats, not integers, for all calculations
		self.v = 744.0 # Muzzle velocity of gun (in m/s)

	def muzzleVelocity(self):
		return self.v

class AbstractPlotter(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def init(self):
		pass

	@abc.abstractmethod
	def plot(self, x, y):
		pass

	@abc.abstractmethod
	def finalise(self):
		pass

# Define a class of projectiles to paint on the screen
# with a shape and colour and a method for 'stepping' (moving to the next coordinate)
class Projectile(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def step(self):
		pass

# The only projectile we have for Turtle is a black cannonball for now
class TurtleBall(Projectile, Turtle):
	def __init__(self, window_width, window_height):
		# Set scale factor accordingly to display all the trajectories on the screen
		# (Using a planet with a low G and a gun with a high muzzle velocity will require the
		# scale factor to be increased significantly)
		self.scalefactor = 10

		# Initialise the Turtle object
		Turtle.__init__(self, shape="circle")
		# Hide the turtle as soon as possible, otherwise you get ugly flashes at the centre of the screen
		self.hideturtle()

		# Give the cannonball its form
		self.penup()
		self.color("black")
		self.pencolor("red")
		self.resizemode("user")
		self.shapesize(8 / self.scalefactor)
		# Having y offset as zero pushes the start & end of a trajectory off the bottom of the screen,
		# so elevate it slightly (10 pixels seems to work)
		y_offset = 10
		self.setposition(-window_width // 2, -window_height // 2 + y_offset)
		# All points will be plotted relative to this position
		self.starting_position = self.position()
		# Now make the cannonball visible
		self.showturtle()
		self.pendown()

	# Move to the next coordinate
	def step(self, x, y):
		# Use the Turtle Vector addition functionality to move the cannonball
		self.setposition(self.starting_position + Vec2D(x // self.scalefactor, y // self.scalefactor))

class TurtlePlotter(AbstractPlotter):
	# Will display graphs as a collection of coordinates output on the python console
	def __init__(self, projectile_class):
		# Initialise the Turtle system
		turtle = Turtle()
		turtle.reset()
		# Get rid of the ugly arrow at the centre of the screen
		turtle.hideturtle()
		self.screen = turtle.getscreen()
		# Maximise the screen, with a bit of space around so you move or resize it
		self.screen.setup(width = 0.9, height = 0.9, startx = 10, starty = 10)
		# Get the current graphics window width & height
		self.window_width = self.screen.window_width()
		self.window_height = self.screen.window_height()
		# Display the projectile's trajectory in (virtual) real time
		self.screen.tracer(1000, 1)
		# The class and an instance variable for the projectile
		self.projectile_class = projectile_class
		self.projectile = None

	def init(self):
		# Instantiate a new projectile object from the class passed into the Constructor
		self.projectile = self.projectile_class(self.window_width, self.window_height)

	def plot(self, x, y):
		# Tell the projectile to move to point (x, y) on the graph.
		# Use integer division to always pass in whole numbers
		self.projectile.step(x // 1, y // 1)

	def finalise(self):
		# Make sure the last point is plotted by updating the screen
		self.screen.update()
		# Call Tkinter's mainloop function
		self.screen.mainloop()

class PyplotPlotter(AbstractPlotter):
	# Will use the matplotlib.pyplot function to plot a graph with x & y-axes
	def __init__(self):
		# Create a list of values for the x and y coordinates to be used to plot the graph
		self.x_values = []
		self.y_values = []

	def init(self):
		pass

	def plot(self, x, y):
		# Add the passed x and y values to the internal list variables to use later
		self.x_values.append(x)
		self.y_values.append(y)

	def finalise(self):
		# the algorithm is complete: so plot the graph
		pyplot.plot(self.x_values, self.y_values)
		pyplot.show

class TextPlotter(AbstractPlotter):
	# Will display graphs as a collection of coordinates output on the python console
	def init(self):
		pass

	def plot(self, x, y):
		# Plot the point (x, y) on the graph
		print ('(%f, %f)' % (x, y))

	def finalise(self):
		pass

class TrajectoryPlotter():
	def __init__(self, plotter):
		# Use the passed plotting strategy object to plot the parabola of the projectile's trajectory
		self.plotter = plotter

	def calculateTrajectory(self, planet, gun, h, degrees):
		g = planet.g()
		v = gun.muzzleVelocity()
		y = h # Initialise point on y-axis to be identical to our initial height above sea level
		t = 0.0 # Time travelled by the projectile so far (in seconds)

		# cos() and sin() expect their argument to be passed in radians, not degrees
		θ = radians(degrees)
		# Perform the cos() and sin() operations outside the loop, as these are relatively expensive
		# operations and the values won't change throughout the trajectory anyway
		cos_θ = cos(θ)
		sin_θ = sin(θ)

		self.plotter.init()

		while y > 0.0: # Loop as long as projectile is above sea level
			# Use the linear constant speed equation displacement = velocity * time to give the point on the x-axis
			# (i.e. the distance travelled horizontally in metres after t seconds)
			# No account is taken of drag (air resistance) in this model
			x = v * t * cos_θ

			# Use the quadratic free-fall equation to give the point on the y-axis
			# (i.e. the height of the projectile above sea level after having travelled for t seconds)
			#
			# The current height above sea level is the difference between the initial height h and
			# the distance fallen so far
			y = h + v * t * sin_θ - 0.5 * g * t**2

			# Plot the points using the rendering method of choice:
			# invoke the plot() method on the plotting strategy object
			self.plotter.plot(x, y)

			# Increment time travelled so far by 1 ms (millisecond)
			t = t + 0.001
		# End while

		# Splash! Your projectile has hit sea level (assuming nothing else got in the way ;-)
		return t

# Instantiate the Plotter class we want to use -
# We'll pass this to the TrajectoryPlotter's constructor so we can change the plotting behaviour
# at compile time, without having to alter the code of the method containing the actual maths
plotter = TurtlePlotter(TurtleBall)
# Instantiate the trajectoryPlotter object, with the chosen plotting strategy object passed to the constructor
trajectoryPlotter = TrajectoryPlotter(plotter)
# We'll use g for our calculation for the planet of our choice
planet = Earth()
# Use the shipborne cannon as our weapon of choice
gun = Cannon()
# Determine height above sea level for the gun and the angle at which the projectile is fired
# Use floats, not integers, for all calculations
height = 10.0

for angle in [0.0, 15.0, 30.0, 45.0, 60.0, 75.0]:
	# Call the method to calculate the trajectory
	time = trajectoryPlotter.calculateTrajectory(planet, gun, height, angle)
	# Just out of interest: the time take to reach sea level -
	# This was returned by the calculateTrajectory() method
	print ('v = %im/s, h = %im, angle = %i°, t = %fs' % (gun.muzzleVelocity(), height, angle, time))

# Do any tidying up needed by the plotter
plotter.finalise()
