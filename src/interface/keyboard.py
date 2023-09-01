from src.infrastructure.folder import Folder
from src.infrastructure.quality_profiles import QualityProfile
from src.interface.buttons import Buttons


class Keyboard:
    @staticmethod
    def folders(folders: list[Folder], media_type: str):
        return [[Buttons.path_button(folder, media_type)] for folder in folders] + [[Buttons.stop_button()]]

    @staticmethod
    def search():
        keyboard = [
            [Buttons.series_button(), Buttons.movie_button()],
            [Buttons.stop_button()],
        ]

        return keyboard

    @staticmethod
    def quality_profiles(profiles:  list[QualityProfile], media_type: str):

        return [[Buttons.quality_profile_button(profile, media_type)] for profile in profiles] \
             + [[Buttons.stop_button()]]

    @staticmethod
    def delete():
        keyboard = [
            [Buttons.yes_button()],
            [Buttons.no_button()]
        ]

        return keyboard

    @staticmethod
    def seasons(seasons: list):
        keyboard = []
        at_least_one_selected = False
        all_selected = True
        for value in seasons:
            if value["selected"]:
                at_least_one_selected = True
            else:
                all_selected = False
            keyboard.append([Buttons.season_button(str(value["seasonNumber"]), value["selected"])])

        if at_least_one_selected:
            keyboard.append([Buttons.continue_button("Continue", "AddSeries")])

        keyboard.append([Buttons.stop_button()])

        if len(seasons) > 1:
            first_button_text = "Unselect" if all_selected else "All"
            keyboard.insert(0, [Buttons.season_button(first_button_text)])

        return keyboard

    @staticmethod
    def medias(is_in_library: bool, has_file: bool | None, results_count: int, current_position: int) -> list:
        if not is_in_library:
            keyboard = [[Buttons.add_button()]]
        elif has_file is None or has_file:
            keyboard = [[Buttons.delete_button()]]
        else:
            keyboard = [[Buttons.delete_button("Cancel")]]

        if results_count > 1 and results_count > current_position == 0:  # show next
            keyboard.append([Buttons.next_button()])
        elif results_count - 1 == current_position:  # show previous
            keyboard.append([Buttons.previous_button()])
        else:
            keyboard.append([Buttons.previous_button(), Buttons.next_button()])

        keyboard.append([Buttons.stop_button()])

        return keyboard
