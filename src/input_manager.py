"""
Created by Gestalt on 10/26/21
input_manager.py

Handles the users input.

Functions:
    prompt_overwrite_asset()
"""

from requests import Response

from src import change_script_source, Uploader, get_asset_data


def start_input_loop():
    cookie: str = input("Hello! Please begin by stating your cookie. ")
    uploader = Uploader(cookie)

    while True:
        user_input: str = input("Please input a command. ")

        if user_input in input_events:
            input_events[user_input](uploader)
        else:
            print("That is not a valid command. Please run help to view a list of commands.")


def _help(_: Uploader):
    print(
        "Commands:\n\nhelp\n\tDisplays all of the accessible commands.\n\noverwriteasset\n\tDisplays a prompt to overwrite an assets source.\n\npublishasset\n\tDisplays a prompt to upload a new asset.\n")


def _prompt_upload(uploader: Uploader):
    # First, we ask for the users information.
    user_new_source: str = input("Please input the new source. ")
    user_asset_name: str = input("What is the name of this new asset? ")
    user_asset_description: str = input("What is the description? ")
    user_asset_copylocked: bool = str.lower(input("Should the asset be copylocked? (yes or no) ")) == "yes" or False
    user_asset_group_id: str = input("If the asset should be uploaded under a group, please send the id here, else,"
                                     "leave it blank. ")

    # Store the received information to be sent with the request.
    asset_information: dict[str] = {
        "name": user_asset_name,
        "description": user_asset_description,
        "copylocked": user_asset_copylocked,
        "groupId": user_asset_group_id
    }

    # Lastly, we must convert the old script source to the new one.
    with open("ScriptTemplate.rbxmx") as file:
        new_source: str = change_script_source(file.read(), user_new_source)

        file.close()

    update_response: Response = uploader.upload_asset(new_source, asset_information)

    # Making sure that the request was valid.
    assert update_response.status_code == 200, "The request was not valid. Please check your arguments."

    print("Successfully updated!")


def _prompt_overwrite_asset(uploader: Uploader):
    # First, we ask for the users information.
    asset_id: str = input("Please input the asset that you would like to update. ")
    user_new_source: str = input("Please input the new source. ")

    # Get the data on our asset.
    _, asset_data = get_asset_data(asset_id)

    # Lastly, we must convert the old script source to the new one.
    new_source: str = change_script_source(asset_data, user_new_source)
    update_response: Response = uploader.overwrite_asset(asset_id, new_source)

    # Making sure that the request was valid.
    assert update_response.status_code == 200, "The request was not valid. Please check your arguments."

    print("Successfully updated!")


input_events: dict[str] = {
    "help": _help,
    "overwriteasset": _prompt_overwrite_asset,
    "uploadasset": _prompt_upload
}
