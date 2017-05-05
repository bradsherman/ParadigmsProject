import pygame
import sys
import math

class Ball(pygame.sprite.Sprite):
    def __init__(self, gs, angle):
	self.image = pygame.image.load('./data/yellow_ball.png')
	self.image = pygame.transform.scale(self.image, (self.image.get_rect().width / 2, self.image.get_rect().height / 2))
	self.rect = self.image.get_rect()
	self.gs = gs
	self.rect.center = self.gs.screen.get_rect().center

	self.speed = 2 
	self.angle = angle
	self.speed_x = self.speed * math.cos(angle)
	self.speed_y = self.speed * math.sin(angle)

    def tick(self):
	# Check for collision with wall
	if self.rect.left < 0 or self.rect.right > self.gs.width:
	    self.speed_x = -self.speed_x
	if self.rect.top < 0 or self.rect.bottom > self.gs.height:
	    self.speed_y = -self.speed_y
	
	# Check for collision with paddles
	if self.rect.colliderect(self.gs.paddle1) or self.rect.colliderect(self.gs.paddle2):
	    self.speed_y = -self.speed_y

	self.rect = self.rect.move(self.speed_x, self.speed_y)	
