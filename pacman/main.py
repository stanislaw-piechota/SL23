"""Main module of the game"""
import pygame
from screens import GameScreen, IntroScreen, EndScreen
from constants import BACKGROUND_MUSIC


class Signals():
    """
    Class used for storing signals synchornising work of threads and screen
    Implementation of client-server architecture.
    """
    def __init__(self):
        self.running = True
        self.stage = "intro"
        self.endgame = True
        self.background_channel = pygame.mixer.Channel(1)


if __name__ == "__main__":
    # initalization of objects except game_screen
    pygame.init()
    signals = Signals()
    intro_screen = IntroScreen(signals)
    game_screen = None
    end_screen = EndScreen(signals)
    signals.background_channel.play(BACKGROUND_MUSIC, -1)

    while signals.running:
        match signals.stage:
            case "game":
                del game_screen  # memory saving
                # New GameScreen instance is created due to possible new number of players
                game_screen = GameScreen(intro_screen.number_of_players, signals)
            case "end":
                end_screen.points = game_screen.scores.points
                end_screen.scores = game_screen.scores

        # automatic switch of screens depending on stage
        locals().get(f"{signals.stage}_screen").run()
