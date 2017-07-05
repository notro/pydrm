import ctypes
import fcntl
import mmap

from .base import DrmObject
from .drm_h import DRM_RDWR, DRM_CLOEXEC, DrmPrimeHandleC, DRM_IOCTL_PRIME_HANDLE_TO_FD, DRM_IOCTL_PRIME_FD_TO_HANDLE
from .drm_h import DRM_IOCTL_MODE_CREATE_DUMB, DRM_IOCTL_MODE_MAP_DUMB, DRM_IOCTL_MODE_DESTROY_DUMB
from .drm_mode_h import DrmModeCreateDumbC, DrmModeMapDumbC, DrmModeDestroyDumbC
from .dma_buf_h import DMA_BUF_SYNC_START, DMA_BUF_SYNC_END, DmaBufSyncC, DMA_BUF_IOCTL_SYNC

class DrmBuffer(DrmObject):
    def __init__(self, drm, format_, width, height):
        self._drm = drm
        self.format = format_
        self.width = width
        self.height = height
        self.handles=[ 0, 0, 0 ]
        self.pitches=[ 0, 0, 0 ]
        self.offsets=[ 0, 0, 0 ]
        self.map = None
        self.fd = None

    def mmap(self):
        if self.fd is None:
            raise ValueError("fd is not set")
        self.map = mmap.mmap(self.fd, self.len, offset=self.offsets[0])
        return self.map

    def munmap(self):
        if self.map:
            self.map.close()
            self.map = None

    def _sync(self, flags):
        if self.fd is None:
            raise ValueError("fd is not set")
        arg = DmaBufSyncC()
        arg.flags = flags
        fcntl.ioctl(self.fd, DMA_BUF_IOCTL_SYNC, arg)

    def sync_start(self):
        self._sync(DMA_BUF_SYNC_START)

    def sync_end(self):
        self._sync(DMA_BUF_SYNC_END)

    def prime_export(self, flags=DRM_CLOEXEC | DRM_RDWR):
        arg = DrmPrimeHandleC()
        arg.handle = self.id
        arg.flags = flags
        fcntl.ioctl(self._drm.fd, DRM_IOCTL_PRIME_HANDLE_TO_FD, arg)
        return arg.fd

    @classmethod
    def prime_import(cls, drm, fd, format_, width, height):
        arg = DrmPrimeHandleC()
        arg.fd = fd
        fcntl.ioctl(drm.fd, DRM_IOCTL_PRIME_FD_TO_HANDLE, arg)

        self = cls(drm, format_, width, height)
        self._arg = arg
        self.fd = fd
        self.id = int(arg.handle)
        self.pitch = self.format.cpp[0] * width
        self.len = height * self.pitch

        self.handles[0] = self.id
        self.pitches[0] = self.pitch
        self.offsets[0] = 0

        if self.format.planes > 1:
            raise NotImplementedError("support for format %s is not implemented yet\n" % self.format.name)

        return self


class DrmDumbBuffer(DrmBuffer):
    def __init__(self, drm, format_, width, height):
        super(DrmDumbBuffer, self).__init__(drm, format_, width, height)

        arg = DrmModeCreateDumbC()
        arg.bpp = self.format.cpp[0] * 8;
        arg.width = self.width;
        arg.height = self.height;

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_CREATE_DUMB, arg)

        #self.handle = arg.handle
        self.id = int(arg.handle)
        self.len = int(arg.size)
        self.pitch = int(arg.pitch)
        self._arg = arg

        self.handles[0] = self.id
        self.pitches[0] = self.pitch
        self.offsets[0] = 0

        if self.format.planes > 1:
            raise NotImplementedError("support for format %s is not implemented yet\n" % self.format.name)

    def destroy(self):
        self.munmap()
        arg = DrmModeDestroyDumbC()
        arg.handle = self.id
        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_DESTROY_DUMB, arg)

#                ("handle", c_uint32),
#                ("pad", c_uint32),
#                ("offset", c_uint64),

    def mmap(self):
        arg = DrmModeMapDumbC()
        arg.handle = self.id
        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_MAP_DUMB, arg)
        self.map = mmap.mmap(self._drm.fd.fileno(), self.len, offset=arg.offset)
        return self.map

    def munmap(self):
        if self.map:
            self.map.close()
            self.map = None


