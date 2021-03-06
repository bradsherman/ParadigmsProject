import pygame
import math

class Ball(pygame.sprite.Sprite):
    def __init__(self, gs, angle):
        self.image = pygame.image.load('./data/yellow_ball.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_rect().width / 2, self.image.get_rect().height / 2))
        self.rect = self.image.get_rect()
        self.left_point = (self.rect.left, self.rect.centery)
        self.right_point = (self.rect.right, self.rect.centery)
        self.top_point = (self.rect.centerx, self.rect.top)
        self.bottom_point = (self.rect.centerx, self.rect.bottom)
        self.gs = gs
        self.rect.center = self.gs.screen.get_rect().center

        self.speed = 6
        self.angle = angle
        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)
        self.update_counter = 0

    def tick(self):
        # Check for collision with wall
        if self.rect.left < 0 or self.rect.right > self.gs.width:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > self.gs.height:
            self.speed_y = -self.speed_y

        # Check for collision with paddles
        if self.rect.colliderect(self.gs.paddle1.rect):
            if self.rect.centery > self.gs.paddle1.rect.centery:
                self.speed_y = abs(self.speed_y)
            else:
                self.speed_y = -abs(self.speed_y)
        if self.rect.colliderect(self.gs.paddle2.rect):
            if self.rect.centery > self.gs.paddle2.rect.centery:
                self.speed_y = abs(self.speed_y)
            else:
                self.speed_y = -abs(self.speed_y)

        # Check for collision with bricks
        if self.update_counter > 0:
            self.update_counter -= 1
            return
        for brick in self.gs.bricks:
            if self.rect.colliderect(brick.rect):
                # Check for a vertical collision
                if self.rect.centery < brick.rect.top or self.rect.centery > brick.rect.bottom:
                    self.speed_y = - self.speed_y
                    break
                    self.update_counter = 2
                # Check for a horizontal collision
                elif self.rect.centerx > brick.rect.right or self.rect.centerx < brick.rect.left:
                    self.speed_x = - self.speed_x
                    break
                    self.update_counter = 2

        self.rect = self.rect.move(self.speed_x, self.speed_y)

    def update(self, x, y, speedx, speedy):
        # Force update of ball's information
        self.update_counter = 3
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_x = speedx
        self.speed_y = speedy
