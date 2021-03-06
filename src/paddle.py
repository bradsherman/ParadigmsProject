import pygame
import cPickle as pickle


class Paddle(pygame.sprite.Sprite):
    def __init__(self, gs, player_num):
        pygame.sprite.Sprite.__init__(self)
        self.player_num = player_num
        if player_num == 1:
            self.image = pygame.image.load('./data/player1.png')
            self.image = pygame.transform.scale(self.image, (115, 23))
            self.rect = self.image.get_rect()
            self.rect.center = (320, 200)
        else:
            self.image = pygame.image.load('./data/player2.png')
            self.image = pygame.transform.scale(self.image, (115, 23))
            self.rect = self.image.get_rect()
            self.rect.center = (320, 540)

        self.image_orig = self.image
        self.rect_orig = self.rect
        self.speed = 0

        self.gs = gs

    def tick(self):
	# Keep paddle on screen
        self.rect.clamp_ip(self.gs.screen.get_rect())

    def update(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, key):
        inc = 15 # distance by which paddle moves
        if self.player_num == 1:
            if key == pygame.K_RIGHT:
                self.rect = self.rect.move(inc, 0)
            elif key == pygame.K_LEFT:
                self.rect = self.rect.move(-inc, 0)
        else:
            if key == pygame.K_d:
                self.rect = self.rect.move(inc, 0)
            elif key == pygame.K_a:
                self.rect = self.rect.move(-inc, 0)

	# Update other player on position
	if self.player_num == 1:
	    pos = {'paddle1x': self.rect.centerx, 'paddle1y': self.rect.centery}
	    pos = pickle.dumps(pos)
	    self.gs.dataConn.sendData(pos)
	else:
	    pos = {'paddle2x': self.rect.centerx, 'paddle2y': self.rect.centery}
	    pos = pickle.dumps(pos)
	    self.gs.dataConn.sendData(pos)
	    
