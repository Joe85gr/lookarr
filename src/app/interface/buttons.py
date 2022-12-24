from telegram import InlineKeyboardButton


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
            callback_data="Next result"
        )

    @staticmethod
    def previous_button(

    ):
        return InlineKeyboardButton(
            '\U000023EE ' + "Previous result",
            callback_data="Previous result"
        )

    @staticmethod
    def path_button(path, free):
        return InlineKeyboardButton(
            f"Path: {path['path']}, Free: {free}",
            callback_data=f"Path: {path['path']}"
        )

    @staticmethod
    def quality_profile_button(quality_profile):
        return InlineKeyboardButton(
            f"Quality: {quality_profile['name']}",
            callback_data=f"Quality profile: {quality_profile['id']}"
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
            '\U00002795 ' + "Delete",
            callback_data="Delete"
        )
