"""
Created by Gestalt on 10/26/21
rbxmx.py

Used for the manipulation of RBXMX objects.

Functions:
    change_script_source(xml_source, new_source) -> str
    get_asset_data(asset_id) -> tuple[bool, str]
"""

import xml.etree.ElementTree as ElementTree
from typing import Union

import requests


def get_asset_data(asset_id: str) -> tuple[bool, str]:
    """Gets the RBXMX data for the specified asset.

    :param asset_id: The asset id in which the program gets the data for.
    :return: The RBXMX data for the given asset id.
    """

    assert asset_id.isdigit(), "The asset id must only include digits!"

    url: str = f"https://assetdelivery.roblox.com/v1/assetId/{asset_id}"

    # Sometimes, the API can fail. This mainly happens whenever the user gives a fake asset.
    try:
        asset_location_fetch_response: requests.Response = requests.get(url)
        asset_location_fetch_json: dict[str] = asset_location_fetch_response.json()
        asset_location: str = asset_location_fetch_json["location"]

        asset_data_fetch_response: requests.Response = requests.get(asset_location)
        asset_data_fetch_text: str = asset_data_fetch_response.text

        return True, asset_data_fetch_text
    except requests.HTTPError:
        print(f"An error occurred while getting the asset data for the id {asset_id}")
        return False, ""


def change_script_source(xml_source: str, new_source: str) -> str:
    """Sets the source text to the given new source.

    :param xml_source: The Roblox asset XML data. Must only include a script.
    :param new_source: The new source text for the script.
    :return: The new asset XML data.
    """

    # We must search through the parsed elements and find the script source.
    try:
        parsed_data: Union[ElementTree.Element, None] = ElementTree.fromstring(xml_source)
    except ElementTree.ParseError:
        parsed_data = None

    assert parsed_data, "Failed to parse asset data. Is the asset in RBXMX format?"

    script_object: ElementTree.Element = parsed_data.find("Item")

    # Just doing some sanity checks.
    assert script_object, "I couldn't find an item in that asset you provided!"

    script_properties: ElementTree.Element = script_object.find("Properties")
    source_property: ElementTree.Element = script_properties.find("ProtectedString[@name='Source']")

    assert source_property is not None, "I couldn't find a source property in your object. Is the asset a script?"

    source_property.text = new_source

    return ElementTree.tostring(parsed_data).decode("utf-8")
