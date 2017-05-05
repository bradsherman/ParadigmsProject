import pygame
import sys
from paddle import Paddle
from ball import Ball
from brick import Brick


class GameSpace:
    def main(self):
        pygame.init()
        pygame.key.set_repeat(1, 50)
        self.size = self.width, self.height = (655, 740)
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)

        self.paddle1 = Paddle(self, 1)
        self.paddle2 = Paddle(self, 2)
	self.ball = Ball(self, 45)
        self.bricks = []
        self.draw_bricks()
        self.clock = pygame.time.Clock()

        while 1:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.paddle1.move(event.key)
                    self.paddle2.move(event.key)
                elif event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

            self.paddle1.tick()
            self.paddle2.tick()
	    self.ball.tick()
            [b.tick() for b in self.bricks]

            self.screen.fill(self.black)
            self.screen.blit(self.paddle1.image, self.paddle1.rect)
            self.screen.blit(self.paddle2.image, self.paddle2.rect)
	    self.screen.blit(self.ball.image, self.ball.rect)

            [self.screen.blit(b.image, b.rect) for b in self.bricks]

            pygame.display.flip()

    def draw_bricks(self):
        for i in range(65, self.width - 65, self.width/5):
            for j in [25, 75]:
                self.bricks.append(Brick(self, i, j))
            for k in [self.height - 25, self.height - 75]:
                self.bricks.append(Brick(self, i, k))


if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
