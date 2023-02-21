import sys
import random
import pygame
import time

class game:
    def __init__(self):

        self.ecran=pygame.display.set_mode((700, 450))

        self.score = 0
        self.score_list = self.charger_scores()

        pygame.display.set_caption('snake')
        self.game_on=True


        self.position_x = 34*10
        self.position_y = 22*10
        self.direction_x = 0
        self.direction_y = 0
        self.body = 10
        self.fruit = 10

        self.fruit_pos_x = random.randint(0,68-1)*10+10
        self.fruit_pos_y = random.randint(0,43-1)*10+10
        print(self.fruit_pos_y, self.fruit_pos_x)

        self.pos_snake = []
        self.size_snake = 1

        self.start_screen = True
        self.scoreboard = False

        self.image = pygame.image.load('snake.jfif')
        self.title = pygame.transform.scale(self.image,(200,100))


        super().__init__()
        self.TBU = 0.05
        self.last_update: float = 0

        self.game_over = False


    def main_fonction(self):

        while self.start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.scoreboard:
                            self.scoreboard=False
                        else:
                            self.scoreboard=True
                        self.score_list = self.charger_scores()
                    if event.key == pygame.K_RETURN:
                        self.start_screen = False
                        self.scoreboard = False

                self.ecran.fill((0,0,0))

                self.ecran.blit(self.title,(270,50,100,50))
                self.msg('petite','Snake',(340,270,100,50),(255,255,255))
                self.msg('petite','Le carré vert est votre serpent et le rouge est une pomme.' ,(190,200,200,5),(240,240,240))
                self.msg('petite', 'Déplacez le serpent autour de l écran et mangez autant de pommes que vous pouvez ', (100, 220, 200, 5), (240, 240, 240))
                self.msg('petite','jusqu à ce que l écran soit plein du corps du serpent.',(205,240,200,5),(240,240,240))
                self.msg('moyenne', 'Appuyez sur ENTRER pour commencer', (180, 400, 200, 5), (255,0,0))
                self.msg('petite', 'Pressez Echap pour ouvrir le tableau des scores', (20, 20, 200, 5), (255, 84, 84))

                if self.scoreboard:
                    self.afficher_scores()

                pygame.display.flip()

        while self.game_on:
            if self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.scoreboard:
                                self.scoreboard = False
                            else:
                                self.scoreboard = True
                            self.score_list = self.charger_scores()
                        if event.key == pygame.K_RETURN:
                            self.game_over = False
                            self.scoreboard = False
                            self.position_x = 34 * 10
                            self.position_y = 22 * 10
                            self.direction_x = 0
                            self.direction_y = 0
                            self.body = 10
                            self.fruit = 10

                            self.fruit_pos_x = random.randint(0, 68 - 1) * 10 + 10
                            self.fruit_pos_y = random.randint(0, 43 - 1) * 10 + 10
                            print(self.fruit_pos_y, self.fruit_pos_x)

                            self.pos_snake = []
                            self.size_snake = 1
                            self.score = 0

                self.affichage()

                self.farlands()
                self.msg('grande',"GAME OVER",(270,220,200,5),(0,0,250))
                self.msg('petite','Pressez Entrée pour relancer la partie',(240,120,200,5),(250,0,0))
                self.msg('petite', 'Pressez Echap pour ouvrir le tableau des scores', (20, 20, 200, 5), (255, 84, 84))
                if self.scoreboard:
                    self.afficher_scores()

                pygame.display.flip()
            else:
                if time.time() > self.last_update + self.TBU:
                    self.last_update = time.time()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()

                        if event.type == pygame.KEYDOWN:

                            if event.key == pygame.K_RIGHT:
                                self.direction_x = 10
                                self.direction_y = 0

                            if event.key == pygame.K_LEFT:
                                self.direction_x = -10
                                self.direction_y = 0

                            if event.key == pygame.K_DOWN:
                                self.direction_x = 0
                                self.direction_y = 10

                            if event.key == pygame.K_UP:
                                self.direction_x = 0
                                self.direction_y = -10


                    self.moove()

                    if self.fruit_pos_y == self.position_y and self.fruit_pos_x == self.position_x:
                        self.score += 1

                        self.fruit_pos_x = random.randint(0,68-1)*10+10
                        self.fruit_pos_y = random.randint(0,43-1)*10+10

                        self.size_snake += 1

                    head = []
                    head.append(self.position_x)
                    head.append(self.position_y)

                    self.pos_snake.append(head)

                    if len(self.pos_snake)>self.size_snake:
                        self.pos_snake.pop(0)

                    if self.position_x <= 0 or self.position_x >= 690 or self.position_y <= 0 or self.position_y >= 440:
                        self.game_over = True
                        self.save_scores()


                    self.affichage()

                    self.action(head)

                    self.farlands()

                    pygame.display.flip()

    def save_scores(self):
        file = open("scores.txt", "a")
        file.write("\n"+str(self.score))
        file.close()

    def afficher_scores(self):
        self.ecran.fill((0, 0, 0))
        self.msg("grande", "Vos scores", (290, 50, 200, 5), (255, 84, 84))
        self.msg('moyenne', 'Appuyez sur ENTRER pour commencer', (180, 400, 200, 5), (255, 0, 0))
        self.msg('petite', 'Pressez Echap pour fermer le tableau des scores', (20, 20, 200, 5), (255, 84, 84))
        for i in range(len(self.score_list)):
            self.msg("moyenne", str(self.score_list[i]), (310, 120+(i*38), 200, 5), (255, 84, 84))

    def charger_scores(self):
        scores = [self.score]
        try:
            with open("scores.txt", "r") as file:
                scores = file.read().splitlines()
        except Exception as e:
            print(e)
        return scores

    def farlands(self):
        pygame.draw.rect(self.ecran, (0,0,0),(0,0,700,450),10)

    def moove(self):
        self.position_x += self.direction_x
        self.position_y += self.direction_y


    def affichage(self):
        self.ecran.fill((219, 219, 219))


        pygame.draw.rect(self.ecran, (0, 250, 0), (self.position_x, self.position_y, self.body, self.body))
        pygame.draw.rect(self.ecran, (255, 0, 0), (self.fruit_pos_x, self.fruit_pos_y, self.fruit, self.fruit))

        self.snake()
        self.msg('petite', 'Score : '+str(self.score), (620, 20, 200, 5), (255, 84, 84))

    def snake(self):
        for parts in self.pos_snake:
            pygame.draw.rect(self.ecran, (0, 255, 0), (parts[0], parts[1], self.body, self.body))


    def action(self,head):
        for parts in self.pos_snake[:-1]:
            if head == parts:
                self.game_over = True
                file = open("test.txt", "a")
                file.write(str(self.score)+"\n")
                file.close()


    def msg(self,font,message,message_rectangle,couleur):
        if font == 'petite':
            font = pygame.font.SysFont('Lato',20,False)
        elif font == 'moyenne':
            font = pygame.font.SysFont('Lato',30,False)
        elif font == 'grande':
            font = pygame.font.SysFont('Lato',40,True)

        message = font.render(message,True,couleur)
        self.ecran.blit(message,message_rectangle)


if __name__ == '__main__':
    pygame.init()
    game().main_fonction()
    pygame.quit()
