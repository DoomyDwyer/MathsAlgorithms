# Calculate the trajectory of a projectile fired horizontally from a gun
# Source of mathematics and inspiration taken from Example 1: Predicting the range of a cannonball, 
# Unit 10 Quadratics, Book C, MU123 Discovering Mathematics, The Open University
# Inspiration for the addition of angle θ to formulae for x and x-coordinates from
# https://www.101computing.net/projectile-motion-formula/
# Author of python code: Steve Dwyer

import abc
from math import cos, sin, radians
import matplotlib.pyplot as pyplot
from turtle import Turtle

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

# Define a class of projectiles to paint on the screen
# with a shape and colour and a method for 'stepping' (moving to the next coordinate)
class Projectile(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def step(self):
		pass

# The only projectile we have for Turtle is a black cannonball for now
class TurtleBall(Projectile):
	def __init__(self, turtle, screen):
		# Initialise the Turtle system
		self.turtle = turtle
		self.screen = screen
		self.turtle.pen(fillcolor="black", pencolor="black", pensize=1)
		# Initialise variables to store the latest x and y coordinates, relative to the screen size
		self.height = screen.window_height()
		self.width = screen.window_width()
		self.x_value = None
		self.y_value = None

	# Move to the next coordinate
	def step(self, x, y):
		if x != self.x_value or self.x_value == None or y != self.y_value or self.y_value == None:
			self.turtle.penup()
			self.turtle.goto(x - self.width / 2, y)
			self.turtle.pendown()
			self.turtle.dot()
	
			self.x_value = x
			self.y_value = y

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
	def plot(self, x, y):
		pass

	@abc.abstractmethod
	def finalise(self):
		pass

class TextPlotter(AbstractPlotter):
	# Will display graphs as a collection of coordinates output on the python console
	def plot(self, x, y):
		# Plot the point (x, y) on the graph
		print ('(%f, %f)' % (x, y))

	def finalise(self):
		pass
		
class TurtlePlotter(AbstractPlotter):
	# Will display graphs as a collection of coordinates output on the python console
	def __init__(self, projectile):
		# Create a list of values for the x and y coordinates to be used to plot the graph
		self.turtle = Turtle()
		self.screen = self.turtle.getscreen()
		self.screen.tracer(0, 1)

		# Display the projectile's trajectory in (approximated) real time
		self.projectile = projectile(self.turtle, self.screen)

	def plot(self, x, y):
		# Plot the point (x, y) on the graph
		self.projectile.step(round(x), round(y))

	def finalise(self):
		# The passed y value is less than or equal to zero, 
		# indicating that the cannonball has reached sea level and therefore
		# the algorithm is complete: so plot the graph
		self.turtle.penup()
		self.turtle.goto(self.screen.window_width() / -2, self.screen.window_height() / 2)
		# Allow Turtle to update the screen
		self.screen.update()
		# Clicking on the Turtle graphics window will close it
		self.screen.exitonclick()  
		# Call Tkinter's mainloop function
		self.screen.mainloop()

class PyplotPlotter(AbstractPlotter):
	# Will use the matplotlib.pyplot function to plot a graph with x & y-axes
	def __init__(self):
		# Create a list of values for the x and y coordinates to be used to plot the graph
		self.x_values = []
		self.y_values = []

	def plot(self, x, y):
		# Add the passed x and y values to the internal list variables to use later
		self.x_values.append(x)
		self.y_values.append(y)
		
	def finalise(self):
		# The passed y value is less than or equal to zero, 
		# indicating that the cannonball has reached sea level and therefore
		# the algorithm is complete: so plot the graph
		pyplot.plot(self.x_values, self.y_values)
		pyplot.show

class TrajectoryPlotter():
	def __init__(self, plotter):
		# Use the passed plotting strategy object to plot the parabola of the projectile's trajectory
		self.plotter = plotter

	def calculateTrajectory(self, planet, gun, h, degrees):
		g = planet.g()
		v = gun.muzzleVelocity()
		y = h # Initialise point on y-axis to be identical to our initial height above sea level
		θ = radians(degrees)
		t = 0.0 # Time travelled by the projectile so far (in seconds)
	
		# No account is taken of drag (air resistance) in this model
		# The projectile is fired horizontally
	
		while y > 0.0: # Loop as long as projectile is above sea level
			# Use the linear constant speed equation distance=speed*time to give the point on the x-axis
			# (i.e. the distance travelled horizontally in metres after t seconds)
			x = v * t * cos(θ)
	
			# Use the quadratic free-fall equation to give the point on the y-axis
			# (i.e. the height of the projectile above sea level after having travelled for t seconds)
			#
			# The current height above sea level is the difference between the initial height h and
			# the distance fallen so far
			y = h + v * t * sin(θ) - 0.5 * g * t**2
	
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
plotter = PyplotPlotter() #TurtlePlotter(TurtleBall) 
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
	print ('v = %im/s, h = %im, θ = %i°, t = %fs' % (gun.muzzleVelocity(), height, angle, time))

# Do any tidying up needed by the plotter
plotter.finalise()
