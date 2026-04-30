from gpiozero import Motor
import time
import math


class Navigate():
	def __init__(self):
		# Left side of robot (tentative pins)
		self.left_side = Motor(forward=17, backward=27)  # IN1, IN2, ENA
		self.right_side = Motor(forward=22, backward=23)  # IN3, IN4, ENB


	def set_speeds(self, left, right):
		# Speeds are legacy, but kept just in case we want to use ENA and ENB
		# Left Motors
		if left >= 0:
			self.left_side.forward()  # Optionally pass in speed
		else:
			self.left_side.backward()

		# Right Motors
		if right >= 0:
			self.right_side.forward()
		else:
			self.right_side.backward()


	def stop(self):
		self.left_side.stop()
		self.right_side.stop()


	def move(self, x_loc, z_loc):
		""" Move to coordinates specified in meters


		params:
			x_loc (float): x_location (forward) of desired location relative to base frame
			z_loc (float): z_location (right and left) of desired location relative to base frame
		"""

		# -angle means ball is on right
		angle_offset = math.degrees(math.atan2(z_loc, x_loc))

		curr_dist = x_loc
		turn_speed = 0.5
		turn_time = abs(angle_offset) / 90.0  # Needs calibration: seconds per 90 degrees at turn_speed=0.5

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
		clearance_amt = 0.4
		dist_to_move = dist_to_ball - clearance_amt  # Giving some clearance to swing
		if dist_to_move > 0:
			drive_time = dist_to_move / 0.5
			self.set_speeds(0.5, 0.5)
			time.sleep(drive_time)
			self.stop()

		# Spin 180 degrees so we can back into the ball
		print("Pivoting")
		self.set_speeds(0.6, -0.6)  # Legacy speeds
		time.sleep(1.0)  # Needs calibration for turning
		self.stop()

		# Back into the ball (5 seconds should be long enough)
		# Backing up
		reverse_dist = clearance_amt + 0.25  # Tune
		reverse_time = reverse_dist / 0.2
		self.set_speeds(-0.4, -0.4)
		time.sleep(reverse_time)
		self.stop()

		print("Attempt at grabbing ball complete")
