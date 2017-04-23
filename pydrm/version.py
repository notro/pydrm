from ctypes import *
import fcntl

from .base import DrmObject
from .drm_h import DrmVersionC, DRM_IOCTL_VERSION

class DrmVersion(DrmObject):
    def __init__(self, drm):
        self._drm = drm
        arg = DrmVersionC()
        arg.name = create_string_buffer(256)
        arg.name_len = 255
        arg.date = create_string_buffer(256)
        arg.date_len = 255
        arg.desc = create_string_buffer(256)
        arg.desc_len = 255

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_VERSION, arg)

        self._arg = arg
        self.major = int(arg.major)
        self.minor = int(arg.minor)
        self.patchlevel = int(arg.patchlevel)
        self.name = str(arg.name[:arg.name_len])
        self.date = str(arg.date[:arg.date_len])
        self.desc = str(arg.desc[:arg.desc_len])
