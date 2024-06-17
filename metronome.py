import threading
import time
import pygame

class Metronome:
    def __init__(self, bpm=60, beats_per_measure=4, sound_file=None, command=None):
        self.__bpm = bpm
        self.__beats_per_measure = beats_per_measure
        self.__sound_file = sound_file
        self.__interval = 60.0 / bpm
        self.__is_running = False
        self.__thread = None
        self.__command = command
        
        pygame.mixer.init()
        pygame.init()

        if self.__sound_file:
            self.tick_sound = pygame.mixer.Sound(self.__sound_file)

    def start(self):
        if not self.__is_running:
            self.__is_running = True
            self.__thread = threading.Thread(target=self._metronome_thread)
            self.__thread.start()

    def stop(self):
        self.__is_running = False
        if self.__thread:
            self.__thread.join(timeout = 1)

    def _metronome_thread(self):
        while self.__is_running:
            if self.__sound_file:
                self.tick_sound.play()
            if self.__command:
                self.__command()
            time.sleep(self.__interval)

    def set_bpm(self, bpm):
        self.__bpm = bpm
        self.__interval = 60.0 / self.__bpm

    def set_beats_per_measure(self, beats_per_measure):
        self.__beats_per_measure = beats_per_measure