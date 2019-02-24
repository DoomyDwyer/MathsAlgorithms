# Calculate the trajectory of a projectile fired horizontally from a gun
# Source of mathematics and inspiration taken from Example 1: Predicting the range of a cannonball, 
# Unit 10 Quadratics, Book C, MU123 Discovering Mathematics, The Open University
# Author of python code: Steve Dwyer

from time import sleep

def plotPoint(x, y):
	# Plot the point (x, y) on the graph
	print ('(%f, %f)' % (x, y))
	# or: rounded to the nearest integer to get discrete coordinates to use in a graphics system
	#print ('(%i, %i)' % (round(x), round(y)))

	# Display the projectile's trajectory in real time
	sleep(0.0005)

def calculateTrajectory(h, v):
	y = h # Initialise point on y-axis to be identical to our initial height above sea level
	g = 9.81 # The constant g, i.e. acceleration due to gravity (in metres per second squared)
	t = 0.0 # Time travelled by the projectile so far (in seconds)

	# No account is taken of drag (air resistance) in this model
	# The projectile is fired horizontally

	while y > 0.0: # Loop as long as projectile is above sea level
		# Use the linear constant speed equation distance=speed*time to give the point on the x-axis
		# (i.e. the distance travelled horizontally in metres after t seconds)
		x = v * t

		# Use the quadratic free-fall equation to give the point on the y-axis
		# (i.e. the height of the projectile above sea level after having travelled for t seconds)
		#
		# The current height above sea level is the difference between the initial height h and
		# the distance fallen so far
		y = h - (0.5 * g * t**2)

		# Plot the points using the rendering method of choice
		plotPoint(x, y)

		# Increment time travelled so far by 1 ms (millisecond)
		t = t + 0.001
	# End while

	# Splash! Your projectile has hit sea level (assuming nothing else got in the way ;-)
	return t

# Initialise our variables and call the Calculate Trajectory function
# Use floats, not integers, for all calculations
h = 10.0 # Initial height above sea level (in metres)
v = 300.0 # Muzzle velocity of gun (in m/s)
t = calculateTrajectory(h, v)
# Just out of interest: the time take to reach sea level -
# This was returned by the calculateTrajectory() function
print ('t = %fs' % t)
