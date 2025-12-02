import pygame
import os

from src.config import *

pygame.mixer.init()
# Nhạc nền
pygame.mixer.music.load(os.path.join(ASSETS_SOUND_DIR, "nhacnen.mp3"))

# Sounds effect
def _load_sound():
    sounds = {}
    sounds['click'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, "click_dapan.wav"))
    sounds['no'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, "no.mp3"))
    sounds['yes'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, "yes.mp3"))

    return sounds