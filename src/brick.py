import pygame

class Brick(pygame.sprite.Sprite):
    def __init__(self, gs, x, y, i):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.x = x
        self.y = y
        self.id = i
        self.img_path = './data/brick.png'
        self.img_hit_path = './data/brick_hit.png'
        self.image = pygame.image.load(self.img_path)
        # original 146 x 69
        self.image = pygame.transform.scale(self.image, (120, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.image_orig = self.image
        self.rect_orig = self.rect
        self.hp = 2

    def tick(self):
        # Check for collision with ball
        if self.gs.player == 1:
            if pygame.sprite.collide_rect(self.gs.ball, self):
                self.hit()
                self.update()
                # Force update to client's bricks
                self.gs.send_brick_update()
        else:
            self.update()

    def hit(self):
        self.hp -= 1

    def update(self):
        if self.hp <= 0:
            self.gs.bricks.remove(self)
            self.kill()
        elif self.hp == 1:
            self.image = pygame.image.load(self.img_hit_path)
            self.image = pygame.transform.scale(self.image, (120, 40))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

    def is_dead(self):
        return self.hp
