"""
Created by Gestalt on 10/26/21
upload.py

Utilizes the Roblox api to overwrite assets.

See for Response object.
https://2.python-requests.org/en/master/user/advanced/#request-and-response-objects

Classes:
    Uploader

Functions:
    upload_asset(asset_data, asset_information) -> Response (see above)
    overwrite_asset(asset_id, asset_data) -> Response (see above)
"""

from requests import Response

from sessions import post_with_cross_reference


class Uploader:
    def __init__(self, roblox_cookie: str):
        self.cookie: str = roblox_cookie

    def upload_asset(self, asset_data: str, asset_information: dict[str]) -> Response:
        """Uploads a new Roblox asset to the marketplace.

        :param asset_data: The source for the new asset.
        :param asset_information: The properties that will apply to the new asset.
        :return: Response Object
        """

        # Check if the user provided all of the correct arguments.
        assert asset_information["name"], "You must provide a name inside of the asset information!"

        # Set our default arguments.
        asset_information.setdefault("description", "")
        asset_information.setdefault("group_id", "")
        asset_information.setdefault("copylocked", "true")

        url: str = f"https://data.roblox.com/Data/Upload.ashx?json=1&assetid=0&type=Model&genreTypeId=1" \
                   f"&name={asset_information['name']}" \
                   f"&description={asset_information['description']}" \
                   f"&ispublic={asset_information['copylocked']}" \
                   f"&allowComments=false" \
                   f"&groupId={asset_information['group_id']}"

        return post_with_cross_reference(self.cookie, url=url, data=asset_data)

    def overwrite_asset(self, asset_id: str, asset_data: str) -> Response:
        """Overwrites the specified asset with the new given source.

        :param asset_id: The asset that will be overwritten.
        :param asset_data: The new data that the asset will hold. (in rbxmx format)
        :return: Response Object
        """

        url: str = f"https://data.roblox.com/Data/Upload.ashx?type=Model&assetid={asset_id}&type=Model&genreTypeId=1"

        return post_with_cross_reference(self.cookie, url=url, data=asset_data)
