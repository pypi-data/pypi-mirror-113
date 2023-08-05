"""
This module contains HEA objects supporting items that are openable in the HEA desktop, called data objects (DataObject
below). HEA uses internet MIME types to provide additional information about the type of data in a DataObject. You can
read more about MIME types at https://www.iana.org/assignments/media-types/media-types.xhtml and
https://en.wikipedia.org/wiki/Media_type.

HEA defines the following custom MIME types that are intended only for internal use by the different parts of HEA:

application/x.folder: HEA folders (heaobject.folder.Folder)
application/x.item: HEA items (heaobject.folder.Item)
"""

from heaobject import root
from abc import ABC
from typing import List, Optional
from copy import deepcopy


class MimeTypeTransform(root.AbstractMemberObject):
    """
    Represents a MIME type that a desktop object supports when opened.
    """
    def __init__(self):
        """
        Constructor. Sets the mime_type property to None.
        """
        super().__init__()
        self.__mime_type = None

    @property
    def mime_type(self) -> Optional[str]:
        """
        The MIME type. When added to a data object, this attribute should not be None.
        """
        return self.__mime_type

    @property
    def mime_type(self, mime_type: Optional[str]) -> None:
        self.__mime_type = str(mime_type) if mime_type is not None else None


class DataObject(root.AbstractDesktopObject, ABC):
    """
    Interface for data objects, which are objects that are openable in the HEA desktop. The main difference between
    openable and other objects is the addition of two properties: a MIME type property, and a property containing a
    list of the MIME types that the object supports providing when it is opened.
    """

    @property
    def mime_type(self) -> str:
        """
        The object's MIME type. Note that HEA uses '*/x.*' for all HEA-specific private
        MIME types that only need to be understood by the different parts of HEA, such as 'application/x.folder' for
        folders.
        """
        pass

    @property
    def mime_type_transforms(self) -> List[MimeTypeTransform]:
        """
        The media types that this object supports when it is opened. Normally, this list includes the object's MIME
        type, but it may include additional MIME types that the microservice for this object type supports returning.
        Web service calls to open this object type should include one or more of these MIME types in the Accept header.
        This attribute cannot be null. The empty list means "any MIME type".
        """
        pass



class DataFile(DataObject):

    DEFAULT_MIME_TYPE = 'text/plain'

    def __init__(self):
        super().__init__()
        self.__mime_type = DataFile.DEFAULT_MIME_TYPE
        self.__mime_type_tranforms = []

    @property
    def mime_type(self) -> str:
        return self.__mime_type

    @mime_type.setter
    def mime_type(self, mime_type: str) -> None:
        if mime_type is None:
            self.__mime_type = DataFile.DEFAULT_MIME_TYPE
        else:
            self.__mime_type = str(mime_type)

    @property
    def mime_type_transforms(self) -> List[MimeTypeTransform]:
        return deepcopy(self.__mime_type_tranforms)

    @mime_type_transforms.setter
    def mime_type_transforms(self, mime_type_transforms: List[MimeTypeTransform]) -> None:
        if mime_type_transforms is None:
            self.__mime_type_tranforms = []
        else:
            if not all(isinstance(m, MimeTypeTransform) for m in mime_type_transforms):
                raise KeyError("mime_type_transforms can only contain MimeTypeTransform objects")
            self.__mime_type_tranforms = deepcopy(list(mime_type_transforms) if isinstance(mime_type_transforms, list) else mime_type_transforms)


class DataInDatabase(DataObject):

    def __init__(self):
        super().__init__()

    @property
    def mime_type(self) -> str:
        return 'application/x.data-in-database'

    @property
    def mime_type_transforms(self) -> List[MimeTypeTransform]:
        m = MimeTypeTransform()
        m.mime_type = 'application/x.data-in-database'
        return [m]
