from __future__ import annotations

from pathlib import Path

import pygame


class SoundManager:
    def __init__(self) -> None:
        self._initialized = False
        self._mixer_available = False
        self.music: pygame.mixer.Music | None = None
        self.shoot_sound: pygame.mixer.Sound | None = None

    def initialize(self) -> None:
        if self._initialized:
            return
        try:
            import pygame.mixer
            pygame.mixer.init()
            self._mixer_available = True
            self._load_sounds()
        except Exception:
            pass
        self._initialized = True

    def _load_sounds(self) -> None:
        base_path = Path(__file__).parent.parent

        music_path = base_path / "sounds/background_music.mp3"
        if music_path.exists():
            try:
                pygame.mixer.music.load(str(music_path))
                self.music = pygame.mixer.music
            except pygame.error:
                pass

        shoot_path = base_path / "sounds/bullet_fire.wav.mp3"
        if shoot_path.exists():
            try:
                self.shoot_sound = pygame.mixer.Sound(str(shoot_path))
            except pygame.error:
                pass

    def play_music(self, loops: int = -1) -> None:
        if self.music:
            try:
                self.music.play(loops=loops)
            except pygame.error:
                pass

    def stop_music(self) -> None:
        if self.music:
            try:
                self.music.stop()
            except pygame.error:
                pass

    def play_shoot(self) -> None:
        if self.shoot_sound:
            try:
                self.shoot_sound.play()
            except pygame.error:
                pass


_sound_manager: SoundManager | None = None


def get_sound_manager() -> SoundManager:
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
        _sound_manager.initialize()
    return _sound_manager
