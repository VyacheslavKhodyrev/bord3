from django.apps import AppConfig


class PosterBoardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "poster_board"

    def ready(self):
        from . import signals
