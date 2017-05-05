import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(self, gs, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.image = pygame.image.load('./data/brick.png')
        # original 146 x 69
        self.image = pygame.transform.scale(self.image, (120, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image_orig = self.image
        self.rect_orig = self.rect
        self.hp = 2

    def tick(self):
        pass

    def hit(self):
        self.hp -= 1
        if self.hp == 0:
            print "brick dead!!!"

    def is_dead(self):
        return self.hp
