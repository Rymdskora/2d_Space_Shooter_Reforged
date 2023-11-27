import pygame


# I handle all the game's events, I operate in the GLOBAL NAMESPACE.
class EventHandler:
    events = []

    @classmethod
    def checkEventQueue(cls, returned):
        for event in EventHandler.events:
            if returned == 'quit':
                if event.type == pygame.QUIT:
                    return True
            elif returned == 'clicked':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return True
