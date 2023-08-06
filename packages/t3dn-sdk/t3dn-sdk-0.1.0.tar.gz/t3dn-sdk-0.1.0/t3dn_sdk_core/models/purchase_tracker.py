class PurchaseTrackerModel(object):
    '''The main model used for storing purchase tracker information.'''

    def __init__(
        self,
        token=None,
        url=None,
        detect_title=None,
        apply_size=None,
    ):
        self.token = token
        self.url = url
        self.detect_title = detect_title
        self.apply_size = apply_size

    @classmethod
    def from_dict(cls, data):
        return cls(
            token=data.get('token'),
            url=data.get('url'),
            detect_title=data.get('detectTitle'),
            apply_size=(
                data.get('applySize').get('width'),
                data.get('applySize').get('height'),
            ),
        )

    def to_dict(self):
        return {
            'token': self.token,
            'url': self.url,
            'detectTitle': self.detect_title,
            'applySize': {
                'width': self.apply_size[0],
                'height': self.apply_size[1],
            },
        }


class PurchaseTrackerFileModel(object):
    '''The main model used for storing purchase tracker file information.'''

    def __init__(self, filename=None, url=None):
        self.filename = filename
        self.url = url

    @classmethod
    def from_dict(cls, data):
        return cls(
            filename=data.get('filename'),
            url=data.get('url'),
        )

    def to_dict(self):
        return {
            'filename': self.filename,
            'url': self.url,
        }


class PurchaseTrackerMappingModel(object):
    '''Model that defines how a downloaded file should be installed.'''

    def __init__(self, folder=None, clear_subdirs=None):
        self.folder = folder
        self.clear_subdirs = clear_subdirs

    @classmethod
    def from_dict(cls, data):
        return cls(
            folder=data.get('folder'),
            clear_subdirs=data.get('clear_subdirs'),
        )

    def to_dict(self):
        return {
            'folder': self.folder,
            'clear_subdirs': self.clear_subdirs,
        }
