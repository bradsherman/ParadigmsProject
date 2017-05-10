import pygame
import sys
from paddle import Paddle
from ball import Ball
from brick import Brick
from twisted.internet.task import LoopingCall
import cPickle as pickle

class GameSpace:
    def __init__(self, DataConnection, player):
        self.dataConn = DataConnection
        self.player = player
        self.other = 1 if self.player == 2 else 2
        self.num_players = 1
        self.update_counter = 0
        self.game_over = 0
        self.winner = 0
        self.quitter = 0
        self.init_screen()
        self.init_title()

    def run(self):
        self.show_title()
        self.init_game()

        # initialize some variables differently based on which player
        if self.player == 1:
            self.dataConn.paddlex = self.paddle2.rect.centerx
            self.dataConn.paddley = self.paddle2.rect.centery
            lc = LoopingCall(self.loop)
            lc.start(1 / 60)
        elif self.player == 2:
            self.dataConn.paddlex = self.paddle1.rect.centerx
            self.dataConn.paddley = self.paddle1.rect.centery
            lc = LoopingCall(self.loop)
            lc.start(1 / 60)

    def init_screen(self):
        # initialize the screen for gameplay
        pygame.init()
        pygame.key.set_repeat(1, 50)
        self.size = self.width, self.height = (655, 740)
        self.black = 0, 0, 0
        self.white = 255, 255, 255
        self.screen = pygame.display.set_mode(self.size)

    def loop(self):
        # show waiting screen if we don't have both players
        if self.num_players < 2:
            # we still want to quit even if we are waiting
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.exit()
                elif event.type == pygame.QUIT:
                    self.exit()
            self.screen.fill(self.black)
            self.screen.blit(self.waiting, (((self.width - self.waiting.get_width()) / 2), ((self.height - self.waiting.get_height()) / 2)))
            pygame.display.flip()
            return

        if self.game_over:
            # if game is over, display a winner or who quit
            self.show_exit()

        if self.winner:
            self.show_winner()

        self.clock.tick(60)
        if self.player == 1:
            self.update_counter += 1
            if self.update_counter == 30:
                self.send_ball_update()
            elif self.update_counter == 60:
                self.send_brick_update()
            elif self.update_counter == 90:
                self.send_paddle1_update()
            elif self.update_counter == 120:
                self.send_paddle2_update()
                self.update_counter = 0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if self.player == 1:
                    self.paddle1.move(event.key)
                elif self.player == 2:
                    self.paddle2.move(event.key)
            elif event.type == pygame.QUIT:
                self.exit()

        self.paddle1.tick()
        self.paddle2.tick()
        [b.tick() for b in self.bricks]
        self.ball.tick()
        self.check_winner()

        self.screen.fill(self.black)
        self.screen.blit(self.paddle1.image, self.paddle1.rect)
        self.screen.blit(self.paddle2.image, self.paddle2.rect)
        self.screen.blit(self.ball.image, self.ball.rect)

        [self.screen.blit(b.image, b.rect) for b in self.bricks]

        pygame.display.flip()

    def send_brick_update(self):
        b = {'bricks': {}}
        for brick in self.bricks:
            b['bricks'][brick.id] = brick.hp
        b1 = pickle.dumps(b)
        self.dataConn.sendData(b1)

    def send_paddle1_update(self):
        p1x = self.paddle1.rect.centerx
        p1y = self.paddle1.rect.centery
        paddle1 = {'paddle1x': p1x, 'paddle1y': p1y}
        p = pickle.dumps(paddle1)
        self.dataConn.sendData(p)

    def send_paddle2_update(self):
        p2x = self.paddle2.rect.centerx
        p2y = self.paddle2.rect.centery
        paddle1 = {'paddle2x': p2x, 'paddle2y': p2y}
        p = pickle.dumps(paddle1)
        self.dataConn.sendData(p)

    def send_ball_update(self):
        b = {'ball': {}}
        b['ball']['ballx'] = self.ball.rect.centerx
        b['ball']['bally'] = self.ball.rect.centery
        b['ball']['ballspeedx'] = self.ball.speed_x
        b['ball']['ballspeedy'] = self.ball.speed_y
        b1 = pickle.dumps(b)
        self.dataConn.sendData(b1)

    def show_title(self):
        while self.title_screen:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    req = {'player' + str(self.player): 'ready'}
                    self.dataConn.transport.write(pickle.dumps(req))
                    self.title_screen = 0
                    continue
                elif event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

            self.screen.fill(self.black)
            self.screen.blit(self.title, ((self.width - self.title.get_width()) / 2, (self.height - self.title.get_height()) / 2))
            self.screen.blit(self.authors, (((self.width - self.authors.get_width()) / 2), (self.height / 2) + self.title.get_height()))
            self.screen.blit(self.start, (((self.width - self.start.get_width()) / 2), (self.height / 2) + self.title.get_height() + self.authors.get_height()))
            self.screen.blit(self.quit, (((self.width - self.quit.get_width()) / 2), (self.height / 2) + self.title.get_height() + self.start.get_height() + self.authors.get_height()))
            self.screen.blit(self.player_label, (((self.width - self.player_label.get_width()) / 2), (self.height / 2) + self.title.get_height() + self.start.get_height() + self.authors.get_height() + self.quit.get_height()))
            pygame.display.flip()

    def show_exit(self):
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.quit_game()
                elif event.type == pygame.QUIT:
                    self.quit_game()

            self.screen.fill(self.black)
            self.screen.blit(self.quit_text, ((self.width - self.quit_text.get_width()) / 2, (self.height - self.quit_text.get_height()) / 2))
            pygame.display.flip()

    def show_winner(self):
        while self.winner:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.quit_game()
                    # pygame.display.quit()
                    # sys.exit()
                elif event.type == pygame.QUIT:
                    self.quit_game()
                    # pygame.display.quit()
                    # sys.exit()

            self.screen.fill(self.black)
            self.screen.blit(self.win_text, ((self.width - self.win_text.get_width()) / 2, (self.height - self.win_text.get_height()) / 2))
            pygame.display.flip()

    def init_title(self):
        self.title_screen = 1
        self.font = "monospace"
        self.title_font = pygame.font.SysFont(self.font, 60)
        self.title = self.title_font.render("Brick Breaker", 1, self.white)
        self.author_font = pygame.font.SysFont(self.font, 25)
        self.authors = self.author_font.render("Brad Sherman and Ben Dalgarn", 1, self.white)
        self.start_font = pygame.font.SysFont(self.font, 20)
        self.start = self.start_font.render("Press 's' to start connecting", 1, self.white)
        self.quit = self.start_font.render("Press 'q' to quit anytime", 1, self.white)
        self.player_label = self.author_font.render("You are player " + str(self.player), 1, self.white)
        self.waiting = self.author_font.render("Waiting for player " + str(self.other), 1, self.white)

    def init_game(self):
        self.paddle1 = Paddle(self, 1)
        self.paddle2 = Paddle(self, 2)
        self.ball = Ball(self, 45)
        self.dataConn.ballx = self.ball.rect.centerx
        self.dataConn.bally = self.ball.rect.centery
        self.bricks = []
        self.draw_bricks()
        self.clock = pygame.time.Clock()

    def draw_bricks(self):
        h = 0
        for j in [25, 75]:
            for i in range(65, self.width - 65, self.width / 5):
                self.bricks.append(Brick(self, i, j, h))
                h += 1
        for k in [self.height - 25, self.height - 75]:
            for i in range(65, self.width - 65, self.width / 5):
                self.bricks.append(Brick(self, i, k, h))
                h += 1

    def check_winner(self):
        p1 = True
        p2 = True
        for b in self.bricks:
            if b.id >= 0 and b.id <= 9:
                p2 = False
            if b.id >= 10 and b.id <= 19:
                p1 = False
        if p1:
            self.winner = 1
        if p2:
            self.winner = 2

        if self.winner:
            self.win_text = self.author_font.render(str(self.winner) + " won the game", 1, self.white)
            w = {'winner': str(self.other)}
            win = pickle.dumps(w)
            self.dataConn.sendData(win)
            self.dataConn.shutdown_other()

    def add_player(self):
        self.num_players = 2

    def exit(self):
        self.game_over = 1
        self.quitter = self.player
        self.quit_text = self.author_font.render("Player " + str(self.quitter) + " quit the game", 1, self.white)
        self.dataConn.shutdown_other()

    def other_exit(self):
        self.game_over = 1
        self.quitter = self.other
        self.quit_text = self.author_font.render("Player " + str(self.quitter) + " quit the game", 1, self.white)

    def quit_game(self):
        self.dataConn.shutdown_other()
        pygame.display.quit()
        sys.exit()

if __name__ == '__main__':
    gs = GameSpace(None, 1)
    gs.run()
