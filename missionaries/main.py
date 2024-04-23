import algorithm as alg
import pygame
from constants import *
from random import choice
from sys import exit


class Controller():
    """
    Class holding and controlling positions of all objects displayed on the screen
    And control all events of the game.

    It's main purpose is to share screen, and event bools i.e. raft_animation
    """
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.game_running = False
        self.initialise_game()
        self.animated_figure = None
        self.raft_animation = False

    def rand_not_colliding_rect(self, side):
        """
        Rand a position on adequate side of the river which isn't occupied by other figure
        """
        width, height = CANNIBAL.get_width(), MISSIONARY.get_height()
        if side == "<":
            xs = [i*width for i in range(LEFT_WIDTH//width)]
            ys = [SCREEN_HEIGHT-LEFT_HEIGHT+i*height for i in range(LEFT_HEIGHT//height)]
        else:
            xs = [SCREEN_WIDTH-RIGHT_WIDTH+i*width for i in range(RIGHT_WIDTH//width)]
            ys = [SCREEN_HEIGHT-RIGHT_HEIGHT+i*height for i in range(RIGHT_HEIGHT//height)]
        # missionary is higher than cannibal
        # cannibal is wider than missionary
        new_rect = pygame.Rect(choice(xs), choice(ys), CANNIBAL.get_width(), MISSIONARY.get_height())
        while new_rect.collidelist([x["rect"] for x in self.cannibals+self.missionaries]) >= 0:
            new_rect.topleft = (choice(xs), choice(ys))
        return new_rect

    def update_hint(self):
        """
        Update counter of moves, check the current minimum according to new path
        and render new text with the resulting value
        """
        self.moves_count += 1
        currrent_min_moves = min([len(x) for x in alg.find_path(self.position, [self.position], alg.winning)])-1
        self.moves_render = FONT.render(HINT_TEXT.format(currrent_min_moves), True, TEXT_COLOR)

    def initialise_game(self):
        """
        Create / reset neccessary basic attributes of the game
        """
        self.position = alg.starting
        self.win = None
        self.cannibals, self.missionaries = [], []
        for _ in range(CHARACTERS_NUMBER):
            self.cannibals.append({
                "rect": self.rand_not_colliding_rect(STARTING_SIDE),
                "type": "c",
                "side": STARTING_SIDE,
                "state": "edge"
            })
            self.missionaries.append({
                "rect": self.rand_not_colliding_rect(STARTING_SIDE),
                "type": "m",
                "side": STARTING_SIDE,
                "state": "edge"
            })
        self.raft_rect = RAFT.get_rect(topleft=self.get_raft_position())
        self.raft_count = 0
        self.raft_crew = []
        self.minimum_moves = min([len(x) for x in alg.find_path(self.position, [self.position], alg.winning)])-1
        self.moves_count = -1
        self.update_hint()

    def update_screen(self):
        """
        Display objects according to current phase of the game
        """
        self.screen.blit(BACKGROUND, BACKGROUND.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        if self.game_running:
            if self.raft_animation:
                self.animate_raft()
            if self.animated_figure:
                self.transfer_figure()
            for i in range(CHARACTERS_NUMBER):
                self.screen.blit(CANNIBAL, self.cannibals[i]["rect"])
                self.screen.blit(MISSIONARY, self.missionaries[i]["rect"])
            self.screen.blit(RAFT, self.raft_rect)
            self.screen.blit(self.moves_render, self.moves_render.get_rect(center=(SCREEN_WIDTH//2, 50)))
        else:
            # game not started
            if not isinstance(self.win, bool):
                self.screen.blit(STARTING_TEXT, STARTING_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
            else:
                # game won
                if self.win:
                    self.screen.blit(WIN_TEXT, WIN_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
                # game lost
                else:
                    self.screen.blit(LOSING_TEXT, LOSING_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
                self.screen.blit(self.moves_render, self.moves_render.get_rect(center=(SCREEN_WIDTH//2, 50)))
        pygame.display.flip()

    def calculate_direction(self):
        """
        Get current position of the raft and its side
        And calculate the direction of movement of the raft
        """
        sign = alg.split_position(self.position)[2]
        if sign == "<":
            self.side_index = 0
        else:
            self.side_index = 1
        self.opposite_index = 1-self.side_index
        self.direction = self.opposite_index - self.side_index

    def animate_raft(self):
        """
        Animate raft and objects on it aka raft crew
        """
        # when the expression reaches 0 it means the raft came to the right place
        if self.direction * (RAFT_POSITIONS[self.opposite_index][0]-self.raft_rect.x) > 0:
            self.raft_rect.x += self.direction * RAFT_SPEED
            for figure in self.raft_crew:
                figure["rect"].x += self.direction * RAFT_SPEED
        else:
            # raft on the other side
            # stop animation and update position
            self.raft_rect.x = RAFT_POSITIONS[self.opposite_index][0]
            self.raft_animation = False
            # as raft reached other side it can be considered as move completion
            self.update_position()

    def get_raft_position(self):
        """
        Get raft destination position according to side
        """
        sign = alg.split_position(self.position)[2]

        if sign == "<":
            return RAFT_POSITIONS[0]
        return RAFT_POSITIONS[1]

    def calculate_velocity(self):
        """
        Calculate new position of each figure after changing place
        And the speed it needs to maintain to reach the position in
        certain number of frames (ANIMATION_STEPS)
        """
        # calculate position when figure is reqiestered as raft crew
        if self.animated_figure["state"] == "raft":
            new_left, new_bottom = self.rand_not_colliding_rect(alg.split_position(self.position)[2]).bottomleft
        else:
            crew_xs = [x["rect"].left for x in self.raft_crew]
            # take first empty place on the raft
            for i in range(RAFT_CAPACITY):
                new_left = self.raft_rect.left + i * CANNIBAL.get_width()
                if new_left not in crew_xs:
                    break
            new_bottom = self.raft_rect.bottom
        # derivates of velocities
        self.dx = (new_left-self.animated_figure["rect"].left)/ANIMATION_STEPS
        self.dy = (new_bottom-self.animated_figure["rect"].bottom)/ANIMATION_STEPS
        self.animation_step = 0
        # dx and dy are often < 1 and wouldn't be registered when assigned to rect
        # so 3rd variable of float type is used to store actual position
        self.animated_figure_x, self.animated_figure_y = self.animated_figure["rect"].bottomleft

    def transfer_figure(self):
        """
        Function to animate each figure
        """
        # limit of slots on the raft
        if self.raft_count >= RAFT_CAPACITY and\
                self.animated_figure not in self.raft_crew:
            self.animated_figure = None
            return
        # animation came to an end
        if self.animation_step == ANIMATION_STEPS:
            # figure switches from side to raft
            if self.animated_figure["state"] == "edge":
                self.animated_figure["state"] = "raft"
                self.raft_crew.append(self.animated_figure)
                self.raft_count += 1
            # antagonistic case
            else:
                self.animated_figure["state"] = "edge"
                self.raft_crew.remove(self.animated_figure)
                self.raft_count -= 1
            self.animated_figure = None
            return

        self.animated_figure_x += self.dx
        self.animated_figure_y += self.dy
        self.animated_figure["rect"].bottomleft = (self.animated_figure_x, self.animated_figure_y)
        self.animation_step += 1

    def update_position(self):
        """
        Updates position after move is completed, checks for victory or lose
        and takes care of updating hint text
        """
        raft_crew_types = [x["type"] for x in self.raft_crew]
        raft_string = ''.join(sorted(raft_crew_types))
        self.position = alg.get_resulting_position(self.position, raft_string)
        new_sign = alg.split_position(self.position)[2]
        for figure in self.raft_crew:
            figure["side"] = new_sign
        if self.position == alg.winning:
            self.win = True
            self.game_running = False
            self.moves_count += 1
            self.moves_render = FONT.render(FINAL_TEXT.format(self.moves_count, self.minimum_moves), True, TEXT_COLOR)
            return
        elif self.position in alg.losing:
            self.win = False
            self.game_running = False
            self.moves_count += 1
            self.moves_render = FONT.render(FINAL_TEXT.format(self.moves_count, self.minimum_moves), True, TEXT_COLOR)
            return
        self.update_hint()

    def check_events(self):
        """
        Checks for input of the player and reacts adequately
        Because of all the animations it doesn't call functions but sets event variables
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if not self.game_running:
                    self.game_running = True
                    self.initialise_game()
            # 2nd and 3rd condition are disabling few animations onging at one moment
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.raft_animation and not self.animated_figure:
                # player not allowed to control game when its not started
                if not self.game_running:
                    return
                if self.raft_rect.collidepoint(event.pos) and self.raft_count >= 1:
                    self.raft_animation = True
                    self.calculate_direction()

                    continue
                for figure in self.cannibals+self.missionaries:
                    if figure["rect"].collidepoint(event.pos) and\
                        alg.split_position(self.position)[2] == figure["side"] and\
                            not self.animated_figure:
                        self.animated_figure = figure
                        self.calculate_velocity()


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Missionaries and cannibals")
    clock = pygame.time.Clock()
    music = pygame.mixer.Sound(SOUND_PATH)
    controller = Controller(screen)

    music.play(loops=-1)
    while True:
        controller.check_events()
        controller.update_screen()
        clock.tick(FPS)


if __name__ == "__main__":
    run_game()
