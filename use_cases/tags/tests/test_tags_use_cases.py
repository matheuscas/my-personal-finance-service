from typing import Optional

import pytest
from slugify import slugify

from entities.entities import Tag
from use_cases.tags.tags import (
    ExistingTagException,
    MissingTagException,
    TagsUseCases,
)

mock_name = "My Mom"
mock_color = "#FF0000"
mock_slug = "my_mom"

database: list[Tag] = []


@pytest.fixture(autouse=True)
def clean_database():
    global database
    database = []
    yield


class TagServiceProtocolMock:
    # this a detail (database) implementation that is not important here
    def create(self, name: str, color: Optional[str] = None) -> Tag:
        for tag in database:
            if slugify(tag.name, separator="_") == mock_slug:
                raise ExistingTagException
        return Tag(name, color)

    def update(self, name: str, new_tag: Tag) -> Tag:
        try:
            searched_tag = [
                tag
                for tag in database
                if slugify(tag.name, separator="_")
                == slugify(name, separator="_")
            ][0]
            if searched_tag.name == new_tag.name:
                # it wants to update only the color
                return Tag(searched_tag.name, new_tag.color)
        except IndexError as e:
            raise MissingTagException from e

        if [
            tag
            for tag in database
            if slugify(tag.name, separator="_")
            == slugify(new_tag.name, separator="_")
        ]:
            raise ExistingTagException
        return Tag(new_tag.name, new_tag.color)

    def delete(self, name: str) -> None:
        global database
        if not database:
            raise MissingTagException
        database = [tag for tag in database if tag.name != name]

    def get_all(self) -> list[Tag]:
        return database

    def get_tag(self, tag_name: str) -> Tag:  # type: ignore
        if database:
            for tag in database:
                if tag.name == tag_name:
                    return tag
        raise MissingTagException


def test_create_tag_use_case():
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    tag = tags_use_cases.create_tag(mock_name, mock_color)
    assert tag.name == mock_name
    assert tag.color == mock_color


def test_create_existing_tag_use_case():
    database.append(Tag(mock_name, mock_color))
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    with pytest.raises(ExistingTagException) as ex:
        tags_use_cases.create_tag(mock_name, mock_color)
        assert str(ex) == ExistingTagException.msg


def test_update_tag_name_use_case():
    database.append(Tag(mock_name, mock_color))
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    new_label = "My Son"
    tag = tags_use_cases.update_tag_name(mock_name, new_label)
    assert tag.name == new_label
    assert tag.color == mock_color


def test_update_tag_name_to_existing_tag_use_case():
    new_label = "My Son"
    database.append(Tag(mock_name, mock_color))
    database.append(Tag(new_label, mock_color))
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    with pytest.raises(ExistingTagException) as ex:
        tags_use_cases.update_tag_name(new_label, mock_name)
        assert str(ex) == ExistingTagException.msg


def test_update_tag_name_to_non_existing_tag_use_case():
    new_label = "My Son"
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    with pytest.raises(MissingTagException) as ex:
        tags_use_cases.update_tag_name(new_label, mock_name)
        assert str(ex) == MissingTagException.msg


def test_delete_tag_use_case():
    database.append(Tag(mock_name, mock_color))
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    tags_use_cases.delete_tag(mock_name)
    assert len(database) == 0


def test_delete_non_existing_tag_use_case():
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    with pytest.raises(MissingTagException) as ex:
        tags_use_cases.delete_tag(mock_name)
        assert str(ex) == MissingTagException.msg


def test_get_all_tags_use_case():
    database.append(Tag(mock_name, mock_color))
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    assert tags_use_cases.get_all_tags() == [Tag(mock_name, mock_color)]


def test_update_tag_color_use_case():
    database.append(Tag(mock_name, mock_color))
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    new_color = "#FFFFFF"
    tag = tags_use_cases.update_tag_color(mock_name, new_color)
    assert tag.color == new_color


def test_update_tag_color_to_non_existing_tag_use_case():
    new_color = "#FFFFFF"
    tags_use_cases = TagsUseCases(TagServiceProtocolMock())
    with pytest.raises(MissingTagException) as ex:
        tags_use_cases.update_tag_color(mock_name, new_color)
        assert str(ex) == MissingTagException.msg
