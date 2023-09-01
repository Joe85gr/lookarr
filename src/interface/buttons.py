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
            callback_data="Radarr"
        )

    @staticmethod
    def series_button():
        return InlineKeyboardButton(
            '\U0001F4FA ' + "Series",
            callback_data="Sonarr"
        )

    @staticmethod
    def add_button():
        return InlineKeyboardButton(
            "Add",
            callback_data="GetFolders"
        )

    @staticmethod
    def quality_profile_button(quality_profile: QualityProfile, media_type: str):
        return InlineKeyboardButton(
            f"Quality: {quality_profile.name}",
            callback_data=f"{media_type}Quality: {quality_profile.id}"
        )

    @staticmethod
    def path_button(folder: Folder, media_type: str):
        return InlineKeyboardButton(
            f"Path: {folder.path}, Free: {folder.availableSpace}",
            callback_data=f"{media_type}GetQualityProfiles: {folder.path}"
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
    def season_button(season, selected=None):
        if selected:
            emoji = " 👈"
        else:
            emoji = ""

        return InlineKeyboardButton(
            f"Season {season}{emoji}" if season.isnumeric() else season,
            callback_data=f"SelectSeason: {season}",
        )

    @staticmethod
    def continue_button(text: str, callback_data: str):
        return InlineKeyboardButton(
            text,
            callback_data=callback_data
        )

    @staticmethod
    def delete_button(delete_text: str = "Delete"):
        return InlineKeyboardButton(
            '\U0000274C ' + delete_text,
            callback_data="ConfirmDelete"
        )

    @staticmethod
    def yes_button():
        return InlineKeyboardButton(
            'Yes',
            callback_data="Delete"
        )

    @staticmethod
    def no_button():
        return InlineKeyboardButton(
            'No',
            callback_data="Stop"
        )
