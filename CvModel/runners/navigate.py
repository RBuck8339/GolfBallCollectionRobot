from gpiozero import Motor
import time
import math 


class Navigate():
	def __init__(self):
		# Left side of robot (tentative pins)
		self.front_left = Motor(forward=17, backward=27, pwm=12) # IN1, IN2, ENA
		self.back_left  = Motor(forward=22, backward=23, pwm=13) # IN3, IN4, ENB

		# Right side of robot (tentative pins)
		self.front_right = Motor(forward=5,  backward=6,  pwm=18) # IN1, IN2, ENA
		self.back_right  = Motor(forward=20, backward=21, pwm=19) # IN3, IN4, ENB


	def set_speeds(self, left, right):
        	# Left Motors
        	if left >= 0:
            		self.front_left.forward(left); self.back_left.forward(left)
        	else:
            		self.front_left.backward(abs(left)); self.back_left.backward(abs(left))
        	
		# Right Motors
       		if right >= 0:
            		self.front_right.forward(right); self.back_right.forward(right)
        	else:
            		self.front_right.backward(abs(right)); self.back_right.backward(abs(right))	

	
	def stop(self):
        	self.front_left.stop()
		self.back_left.stop()
        	self.front_right.stop()
		self.back_right.stop()

	def move(self, x_loc, z_loc): 
		""" Move to coordinates specified in meters

		
		params:
			x_loc (float): x_location (forward) of desired location relative to base frame
			z_loc (float): z_location (right and left) of desired location relative to base frame
		"""

		# -angle means ball is on right
		angle_offset = math.degrees(math.atan(z_loc, x_loc))
		

		curr_dist = x_loc
	
		turn_speed = 0.5
		turn_time = abs(angle_offset) * 0.01

		# Turn to robot
		if angle_offset > 0:
			self.set_speeds(turn_speed, -turn_speed)
		else:
			self.set_speeds(-turn_speed, turn_speed)
		time.sleep(turn_time)
		self.stop() 
		# Reset ^^^ 

		# Move forward until we turn (giving some clearance)
		dist_to_ball = math.sqrt(x_loc**2 + z_loc**2)
		dist_to_move = dist_to_ball - 0.4  # Giving some clearance to swing 
		if dist_to_move > 0:
			drive_time = dist_to_move / 0.25
			self.set_speeds(0.5, 0.5)
			self.sleep(drive_time)
			self.stop()

		# Spin 180 degrees so we can back into the ball
		print("Pivoting")
		self.set_speeds(0.6, -0.6)
		self.sleep(1.0)  # Needs calibration for turning
		self.stop()

		self.stop()
		# Back into the ball (5 seconds should be long enough)

		# Backing up
		reverse_dist = clearance_amt + 0.25  # Tune
		reverse_time = reverse_dist / 0.2 
		self.set_speeds(-0.4, -0.4)
		time.sleep(reverse_time)
		self.stop()
		
		print("Attempt at grabbing ball complete")
