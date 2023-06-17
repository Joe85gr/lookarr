from telegram import InlineKeyboardButton

from src.infrastructure.folder import Folder
from src.infrastructure.quality_profiles import QualityProfile


class Buttons:
    @staticmethod
    def stop_button():
        return InlineKeyboardButton(
            '\U0001F6D1',
            callback_data="Stop"
        )

    @staticmethod
    def movie_button():
        return InlineKeyboardButton(
            '\U0001F3AC ' + "Movie",
            callback_data="Movie"
        )

    @staticmethod
    def series_button():
        return InlineKeyboardButton(
            '\U0001F4FA ' + "Series",
            callback_data="Series"
        )

    @staticmethod
    def new_search_button():
        return InlineKeyboardButton(
            '\U0001F50D ' + "NewSearch",
            callback_data="New"
        )

    @staticmethod
    def add_button():
        return InlineKeyboardButton(
            "Add",
            callback_data="Add"
        )

    @staticmethod
    def next_button():
        return InlineKeyboardButton(
            "Next result" + ' \U000023ED',
            callback_data="Next"
        )

    @staticmethod
    def previous_button():
        return InlineKeyboardButton(
            '\U000023EE ' + "Previous result",
            callback_data="Previous"
        )

    @staticmethod
    def path_button(folder: Folder):
        return InlineKeyboardButton(
            f"Path: {folder.path}, Free: {folder.availableSpace}",
            callback_data=f"Path: {folder.path}"
        )

    @staticmethod
    def quality_profile_button(quality_profile: QualityProfile):
        return InlineKeyboardButton(
            f"Quality: {quality_profile.name}",
            callback_data=f"Quality: {quality_profile.id}"
        )

    @staticmethod
    def season_button(season):
        return InlineKeyboardButton(
            f"Season {season}",
            callback_data=f"Season: {season}"
        )

    @staticmethod
    def delete_button():
        return InlineKeyboardButton(
            '\U0000274C ' + "Delete",
            callback_data="Delete"
        )
