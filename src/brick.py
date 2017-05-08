import pygame
import cPickle as pickle


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
        if self.gs.player == 2:
            self.gs.dataConn.bricks.append(self)

    def tick(self):
        # check collision with ball
        if self.gs.player == 2:
            alive = 0
            for b in self.gs.dataConn.bricks:
                if b.id == self.id:
                    self.hp = b.hp
                    alive = 1
            if alive == 0:
                self.hp = 0
            self.update()
        elif pygame.sprite.collide_rect(self.gs.ball, self):
            self.hit()
            self.update()

    def hit(self):
        # print "in hit"
        print "updating brick " + str(self.id)
        self.hp -= 1
        b1 = {'brick_id': self.id, 'brick_hp': self.hp}
        b = pickle.dumps(b1)
        self.gs.dataConn.sendData(b)
        # print [str(b2.id) + " = " + str(b2.hp) for b2 in self.gs.bricks]
        print "sent data: ", b1

    def update(self):
        if self.hp <= 0:
            self.gs.bricks.remove(self)
            print "calling kill on brick " + str(self.id)
            self.kill()
        elif self.hp == 1:
            self.image = pygame.image.load(self.img_hit_path)
            self.image = pygame.transform.scale(self.image, (120, 40))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

    def is_dead(self):
        return self.hp
