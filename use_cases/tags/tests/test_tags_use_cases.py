from unittest.mock import MagicMock

import pytest

from entities.entities import Tag
from use_cases.tags.exceptions import ExistingTagException, MissingTagException
from use_cases.tags.tags import TagsUseCases

mock_name = "My Mom"
mock_color = "#FF0000"
mock_slug = "my_mom"


class TagServiceProtocolMock:
    # this a detail (database) implementation that is not important here
    def create(self, name: str, color: str | None = None) -> Tag:
        ...

    def update(self, name: str, new_tag: Tag) -> Tag:  # type: ignore
        ...

    def delete(self, name: str) -> None:
        ...

    def get_all(self) -> list[Tag]:  # type: ignore
        ...

    def get_tag(self, tag_name: str) -> Tag:  # type: ignore
        ...


new_name = "My Son"
mock = TagServiceProtocolMock()


def test_create_tag_use_case():
    mock.create = MagicMock(return_value=Tag(mock_name, mock_color))
    tags_use_cases = TagsUseCases(mock)
    tag = tags_use_cases.create_tag(mock_name, mock_color)
    assert tag.name == mock_name
    assert tag.color == mock_color


def test_create_existing_tag_use_case():
    mock.create = MagicMock(side_effect=ExistingTagException)
    tags_use_cases = TagsUseCases(mock)
    with pytest.raises(ExistingTagException) as ex:
        tags_use_cases.create_tag(mock_name, mock_color)
        assert str(ex) == ExistingTagException.msg


def test_update_tag_name_use_case():
    mock.get_tag = MagicMock(return_value=Tag(mock_name, mock_color))
    mock.update = MagicMock(return_value=Tag(new_name, mock_color))
    tags_use_cases = TagsUseCases(mock)
    tag = tags_use_cases.update_tag_name(mock_name, new_name)
    assert tag.name == new_name
    assert tag.color == mock_color


def test_update_tag_name_to_existing_tag_use_case():
    mock.get_tag = MagicMock(return_value=Tag(new_name, mock_color))
    mock.update = MagicMock(side_effect=ExistingTagException)
    tags_use_cases = TagsUseCases(mock)
    with pytest.raises(ExistingTagException) as ex:
        tags_use_cases.update_tag_name(new_name, mock_name)
        assert str(ex) == ExistingTagException.msg


def test_update_tag_name_to_non_existing_tag_use_case():
    mock.get_tag = MagicMock(return_value=Tag(mock_name, mock_color))
    mock.update = MagicMock(side_effect=MissingTagException)
    tags_use_cases = TagsUseCases(mock)
    with pytest.raises(MissingTagException) as ex:
        tags_use_cases.update_tag_name(new_name, mock_name)
        assert str(ex) == MissingTagException.msg


def test_update_tag_color_use_case():
    new_color = "#FFFFFF"
    mock.get_tag = MagicMock(return_value=Tag(mock_name, mock_color))
    mock.update = MagicMock(return_value=Tag(mock_name, new_color))
    tags_use_cases = TagsUseCases(mock)
    tag = tags_use_cases.update_tag_color(mock_name, new_color)
    assert tag.color == new_color


def test_update_tag_color_to_non_existing_tag_use_case():
    new_color = "#FFFFFF"
    mock.get_tag = MagicMock(side_effect=MissingTagException)
    tags_use_cases = TagsUseCases(mock)
    with pytest.raises(MissingTagException) as ex:
        tags_use_cases.update_tag_color(mock_name, new_color)
        assert str(ex) == MissingTagException.msg


def test_delete_tag_use_case():
    mock.get_all = MagicMock(return_value=[])
    mock.delete = MagicMock(return_value=[])
    tags_use_cases = TagsUseCases(mock)
    tags_use_cases.delete_tag(mock_name)
    assert len(tags_use_cases.get_all_tags()) == 0


def test_get_all_tags_use_case():
    expected_return = [Tag(mock_name, mock_color)]
    mock.get_all = MagicMock(return_value=expected_return)
    tags_use_cases = TagsUseCases(mock)
    assert tags_use_cases.get_all_tags() == expected_return


def test_delete_non_existing_tag_use_case():
    mock.delete = MagicMock(side_effect=MissingTagException)
    tags_use_cases = TagsUseCases(mock)
    with pytest.raises(MissingTagException) as ex:
        tags_use_cases.delete_tag(mock_name)
        assert str(ex) == MissingTagException.msg
