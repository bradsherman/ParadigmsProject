import pygame
import sys
import math
from paddle import Paddle
from ball import Ball

class GameSpace:
    def main(self):
        pygame.init()
        self.size = self.width, self.height = (640, 740)
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)

        self.paddle1 = Paddle(self, 1)
        self.paddle2 = Paddle(self, 2)
	self.ball = Ball(self, 45)
        self.clock = pygame.time.Clock()

        while 1:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.paddle1.move(event.key)
                    self.paddle2.move(event.key)
                elif event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            self.paddle1.tick()
            self.paddle2.tick()
	    self.ball.tick()
            self.screen.fill(self.black)
            self.screen.blit(self.paddle1.image, self.paddle1.rect)
            self.screen.blit(self.paddle2.image, self.paddle2.rect)
	    self.screen.blit(self.ball.image, self.ball.rect)

            pygame.display.flip()

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
