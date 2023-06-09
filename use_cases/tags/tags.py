from typing import Protocol

from entities.entities import Tag


class TagsRepository(Protocol):
    def create(self, name: str, color: str | None = None) -> Tag:
        ...

    def update(self, name: str, tag: Tag) -> Tag:
        ...

    def delete(self, name: str) -> None:
        ...

    def get_all(self) -> list[Tag]:
        ...

    def get_tag(self, name: str) -> Tag:
        ...


class TagsUseCases:
    def __init__(self, tag_service: TagsRepository):
        self.tag_service = tag_service

    def create_tag(self, name, color) -> Tag:
        """It creates a new tag with the given name and color

        :returns: Tag
        :raises: ExistingTagException
        """
        return self.tag_service.create(name, color)

    def update_tag_name(self, current_name: str, new_name: str) -> Tag:
        """
        It updates the name of the tag with the given new name

        :param current_name
        :param new_name
        :return: Tag
        :raises: ExistingTagException, MissingTagException
        """
        tag = self.tag_service.get_tag(current_name)
        new_tag = Tag(new_name, tag.color)
        return self.tag_service.update(current_name, new_tag)

    def update_tag_color(self, current_name: str, new_color: str) -> Tag:
        """
        It updates the color of the tag with the given new color
        :param current_name:
        :param new_color:
        :return: Tag
        :raises: ExistingTagException, MissingTagException
        """
        tag = self.tag_service.get_tag(current_name)
        new_tag = Tag(tag.name, new_color)
        return self.tag_service.update(current_name, new_tag)

    def delete_tag(self, label) -> None:
        """
        It deletes the tag with the given label
        :param label:
        :return: None
        :raises: MissingTagException
        """
        self.tag_service.delete(label)

    def get_all_tags(self) -> list[Tag]:
        """
        It returns all the tags
        :return: list[Tag] or []
        """
        return self.tag_service.get_all()
