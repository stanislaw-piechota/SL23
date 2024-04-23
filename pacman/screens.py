"""Module containg screen objects"""

import sys
from time import sleep
from threading import Thread
from abc import ABC, abstractmethod
import pygame
from constants import *
from background import *
from sprites import Player, Enemy, Point
from functions import *


class Screen(ABC):
    """
    Basic class of Screen
    Implementing the concept of Abstract class
    """
    def __init__(self, signals):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.signals = signals
        self.clock = pygame.time.Clock()

    def definite_exit(self):
        """Turning off all the signals"""
        self.signals.running = False
        self.signals.endgame = True
        pygame.quit()
        sys.exit(0)

    @abstractmethod
    def check_events(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def fill_screen(self):
        pass


class EndScreen(Screen):
    """Class with information about win/draw/end"""
    def __init__(self, signals):
        Screen.__init__(self, signals)
        self.points = []
        self.end_texts = []
        self.running = True

    def get_result(self):
        """Determine win/draw or end of round in case of 1 player"""
        if len(self.points) == 1:
            return "end"
        if self.points.count(max(self.points)) >= 2:
            return "draw"
        return "win"

    def update_text(self):
        """Create apropriate messages in case of result"""
        self.end_texts = []
        match self.get_result():
            case "end":
                self.end_texts.append("TIME PASSED")
            case "draw":
                line = "DRAW - "
                for i, points in enumerate(self.points):
                    if points == max(self.points):
                        line += f"Player {i+1} "
                self.end_texts.append(line)
            case "win":
                player_ind = self.points.index(max(self.points))+1
                self.end_texts.append(f"WIN - Player {player_ind}")
        self.end_texts.append("Hit ENTER to play again")

    def render_text(self):
        self.update_text()
        self.texts = []
        self.text_rects = []
        for i, text in enumerate(self.end_texts):
            self.texts.append(FONT.render(text, True, TEXT_COLOR))
            self.text_rects.append(
                self.texts[i].get_rect(centerx=(SCREEN_WIDTH-SCORE_PANEL_WIDTH)//2,
                                       centery=SCREEN_HEIGHT//(len(self.end_texts)+1)*(i+1))
            )

    def check_events(self):
        """Handling events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.definite_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.signals.stage = "intro"
                    self.running = False

    def fill_screen(self):
        """Drawing objects on the screen"""
        self.screen.fill(BACKGROUND_COLOR)
        self.scores.draw_scoreboard()
        for i, text in enumerate(self.texts):
            self.screen.blit(text, self.text_rects[i])
        pygame.display.flip()

    def run(self):
        """
        Neccessary function to run main.py loop
        Main loop of the screen, setting order of actions
        """
        self.running = True
        self.render_text()
        END_MUSIC.play()
        while self.signals.running and self.running:
            self.check_events()
            self.fill_screen()


class IntroScreen(Screen):
    """Welcome screen of the game"""
    def __init__(self, signals):
        Screen.__init__(self, signals)
        self.number_of_players = 0
        # rendering static texts
        self.intro_text = TITLE_FONT.render("PACMAN multiplayer", True, TEXT_COLOR)
        self.intro_text_rect = self.intro_text.get_rect(centerx=SCREEN_WIDTH//2, top=SCREEN_HEIGHT*.05)
        self.get_ready_text = FONT.render("Click button that is shown below to confirm", True, TEXT_COLOR)
        self.get_ready_rect = self.get_ready_text.get_rect(centerx=SCREEN_WIDTH//2, top=SCREEN_HEIGHT*.2)
        self.load_images()
        self.start_text = FONT.render("Hit ENTER to start the game", True, TEXT_COLOR)
        self.start_rect = self.start_text.get_rect(centerx=SCREEN_WIDTH//2, top=SCREEN_HEIGHT*.9)

    def load_images(self):
        self.images, self.images_rects = [], []
        sprite_size = SCREEN_HEIGHT*.2
        margin_left = (SCREEN_WIDTH - sprite_size*7)//2
        for i in range(MIN_NUMBER_OF_PLAYRES, MAX_NUMBER_OF_PLAYERS+1):
            self.images.append(load_sprite_image(i, 0, size=sprite_size, mult=1))
            self.images_rects.append(pygame.Rect(margin_left+(i-1)*sprite_size*2, SCREEN_HEIGHT*.4,
                                                 sprite_size, sprite_size))
        self.reset()

    def reset(self):
        """Change text appearance to normal (white)"""
        self.ready_texts, self.ready_text_rects = [], []
        self.number_of_players = 0
        for i in range(MIN_NUMBER_OF_PLAYRES, MAX_NUMBER_OF_PLAYERS+1):
            self.ready_texts.append(FONT.render(f"PRESS {pygame.key.name(CONTROLS[i-1][0]).upper()}",
                                                True, TEXT_COLOR))
            self.ready_text_rects.append(self.ready_texts[i-1].get_rect(
                centerx=self.images_rects[i-1].centerx, centery=SCREEN_HEIGHT*.65))

    def change_ready_text(self):
        """Change text appearance to ready state - player 'logged into the game' (green)"""
        for i in range(self.number_of_players):
            self.ready_texts[i] = FONT.render("READY!", True, READY_COLOR)
            self.ready_text_rects[i] = self.ready_texts[i-1].get_rect(
                centerx=self.images_rects[i].centerx, centery=SCREEN_HEIGHT*.65)

    def check_events(self):
        """Handling the events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.definite_exit()
            if event.type == pygame.KEYDOWN:
                key, keys = event.key, [keys[0] for keys in CONTROLS]
                # player log in
                if key in keys:
                    player_ind = keys.index(key)
                    if player_ind <= self.number_of_players:
                        self.number_of_players = max(player_ind+1, self.number_of_players)
                        self.change_ready_text()
                        LOGIN_MUSIC.play()
                elif key == pygame.K_RETURN:
                    if MIN_NUMBER_OF_PLAYRES > self.number_of_players or \
                            MAX_NUMBER_OF_PLAYERS < self.number_of_players:
                        return
                    self.signals.stage = "game"
                    self.signals.endgame = False

    def fill_screen(self):
        """Drawing on the screen"""
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.intro_text, self.intro_text_rect)
        self.screen.blit(self.get_ready_text, self.get_ready_rect)
        for i, image in enumerate(self.images):
            self.screen.blit(image, self.images_rects[i])
            self.screen.blit(self.ready_texts[i], self.ready_text_rects[i])
        self.screen.blit(self.start_text, self.start_rect)

        pygame.display.flip()

    def run(self):
        """Reseeting texts and main loop of the screen"""
        self.reset()
        while self.signals.running and self.signals.endgame:
            self.check_events()
            self.fill_screen()
            self.clock.tick(FPS)


class GameScreen(Screen):
    """Main screen containg game mechanics"""
    def __init__(self, number_of_players, signals):
        Screen.__init__(self, signals)

        # object configuration
        self.paused = False
        self.number_of_players = number_of_players
        self.back = Battlefield(self.screen)
        self.scores = Scoreboard(self.number_of_players, self.screen)
        self.setup_points()
        for i in range(1, self.number_of_players+1):
            Player(i, self.back)
            for j in range(min(MAX_PACKMANS_PER_PLAYER-self.number_of_players, FIELD_HEIGHT)):
                enemy = Enemy(self.back)
                configure_enemy(enemy, self.number_of_players, i, j)
        for enemy in Enemy.enemies:
            enemy.choose_direction()
        self.pause_text = TITLE_FONT.render("PAUSED", True, TEXT_COLOR, BACKGROUND_COLOR)
        self.pause_text.set_colorkey(BACKGROUND_COLOR)
        self.pause_rect = self.pause_text.get_rect(centerx=MARGIN_LEFT+(SCREEN_WIDTH-SCORE_PANEL_WIDTH)//2,
                                                   centery=SCREEN_HEIGHT//2)

    def __del__(self):
        # clearing groups when new game will be created
        Player.players.empty()
        Enemy.enemies.empty()
        Point.points.empty()

    def fill_screen(self):
        """Drawing on the screen"""
        if not self.paused:
            self.screen.fill(BACKGROUND_COLOR)
            self.scores.draw_scoreboard()
            self.back.draw_field()
            Point.points.draw(self.back.board)

            # pygame.Group.draw() override not working correctly
            for player in Player.players:
                player.draw()
            for enemy in Enemy.enemies:
                enemy.draw()

            self.screen.blit(self.back.board, (MARGIN_LEFT, MARGIN_TOP))
        else:
            self.screen.blit(self.pause_text, self.pause_rect)
        pygame.display.flip()

    def update_sprites(self):
        if not self.paused:
            Player.players.update()
            Enemy.enemies.update()

    def check_events(self):
        """Handling events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.definite_exit()
            if event.type == pygame.KEYDOWN:
                for player in Player.players:
                    if event.key in player.keys:
                        # automatic choose of direction depending on key
                        player.moving = player.keys.index(event.key)+1
                        player.image = load_sprite_image(player.id, player.moving)
                        player.new = False
                        continue
                if event.key == pygame.K_ESCAPE:
                    # interrupting the course of the game in case of the mistake
                    self.signals.endgame = True
                    self.signals.stage = "intro"
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def _is_normal_kill(self, enemies):
        for enemy in enemies:
            if enemy.active:
                return True
        return False

    def detect_collisions(self):
        """
        Detecting collisions Players-Enemies and Players-Points.
        As method contains all three sprites it is stored here, in more 'outer' scope then sprite class
        """
        collisions = pygame.sprite.groupcollide(Player.players, Enemy.enemies, False, False)
        for player, enemies in collisions.items():
            # player reborn and haven't moved yet
            if player.new:
                continue
            # no active enemies encountered
            if not self._is_normal_kill(enemies):
                break
            # special kill when powerup is active
            if player.powerup:
                enemy_ind = 0
                while not enemies[enemy_ind].active:
                    enemy_ind += 1
                enemy = enemies[enemy_ind]
                enemy.active = False
                enemy.inactive_thread.start()
                self.scores.points[player.id-1] += SPECIAL_POINTS
                player.powerup = False
                break
            # normal kill, without powerup
            self.scores.points[player.id-1] += KILL_POINTS
            self.scores.load_points()
            player.set_beginning_position()
            player.moving = 0
            player.new = True
            player.image = load_sprite_image(player.id, 0)

        # point collisions
        collisions = pygame.sprite.groupcollide(Player.players, Point.points, False, True)
        for player, points in collisions.items():
            if points[0].special:
                player.powerup = True
                POWERUP_MUSIC.play()
            self.scores.points[player.id-1] += DOT_POINT
            self.scores.load_points()
        if len(Point.points) == 0:
            self.setup_points()

    def setup_points(self):
        """Choosing position of powerups and creating instances of normal points"""
        specials = [(randint(2, FIELD_WIDTH-2), randint(2, FIELD_HEIGHT-2))
                    for _ in range(self.number_of_players*POWERUPS_PER_PLAYER)]
        for i in range(FIELD_HEIGHT):
            for j in range(FIELD_WIDTH):
                point_special = (j, i) in specials
                Point(j, i, special=point_special)

    def score_timer(self):
        """Thread timer until the end of the round (prevent freezing)"""
        while (not self.signals.endgame) and self.scores.timer > 0:
            if not self.paused:
                self.scores.update_time()
            sleep(1)
        self.signals.endgame = True
        self.signals.stage = "end"

    def run(self):
        """Main loop of the screen, creating count thread"""

        # assuring that unexpected number of players won't occur
        assert MIN_NUMBER_OF_PLAYRES <= self.number_of_players <= MAX_NUMBER_OF_PLAYERS
        timer_threat = Thread(target=self.score_timer)
        timer_threat.start()

        while not self.signals.endgame:
            self.check_events()
            self.update_sprites()
            self.detect_collisions()
            self.fill_screen()
            self.clock.tick(FPS)
