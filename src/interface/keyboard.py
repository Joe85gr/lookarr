from src.infrastructure.folder import Folder
from src.infrastructure.quality_profiles import QualityProfile
from src.interface.buttons import Buttons


class Keyboard:
    def __init__(self):
        self._buttons = Buttons()

    def folders(self, folders: list[Folder]):
        return [[self._buttons.path_button(folder)] for folder in folders] + [[self._buttons.stop_button()]]

    def search(self):
        keyboard = [
            [self._buttons.series_button(), self._buttons.movie_button()],
            [self._buttons.stop_button()],
        ]

        return keyboard

    def quality_profiles(self, profiles:  list[QualityProfile]):

        return [[self._buttons.quality_profile_button(profile)] for profile in profiles] \
             + [[self._buttons.stop_button()]]

    def delete(self):
        keyboard = [
            [self._buttons.yes_button()],
            [self._buttons.no_button()]
        ]

        return keyboard

    def medias(self, is_in_library: bool, has_file: bool, results_count: int, current_position: int) -> list:
        if not is_in_library:
            keyboard = [[self._buttons.add_button()]]
        elif has_file:
            keyboard = [[self._buttons.delete_button()]]
        else:
            keyboard = [[self._buttons.delete_button("Cancel Download")]]

        if results_count > 1 and results_count > current_position == 0:  # show next
            keyboard.append([self._buttons.next_button()])
        elif results_count - 1 == current_position:  # show previous
            keyboard.append([self._buttons.previous_button()])
        else:
            keyboard.append([self._buttons.previous_button(), self._buttons.next_button()])

        keyboard.append([self._buttons.stop_button()])

        return keyboard
