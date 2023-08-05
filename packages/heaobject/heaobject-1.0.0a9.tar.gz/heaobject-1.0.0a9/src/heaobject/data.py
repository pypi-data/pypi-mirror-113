from heaobject import root
from abc import ABC
from typing import List, Optional
from copy import deepcopy


class MimeTypeTransform(root.AbstractMemberObject):
    def __init__(self):
        super().__init__()
        self.__mime_type = None
    
    @property
    def mime_type(self) -> Optional[str]:
        return self.__mime_type
    
    @property
    def mime_type(self, mime_type: Optional[str]) -> None:
        self.__mime_type = str(mime_type) if mime_type is not None else None


class DataObject(root.AbstractDesktopObject, ABC):

    def __init__(self):
        super().__init__()
    
    @property
    def mime_type(self) -> str:
        pass
    
    @property
    def mime_type_transforms(self) -> List[MimeTypeTransform]:
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
