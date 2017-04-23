from .format import DrmFormat
from .framebuffer import DrmDumbFramebuffer
from .buffer import DrmDumbBuffer


class DrmImageFramebuffer(DrmDumbFramebuffer):
    def __init__(self, drm, format, width, height):
        from PIL import Image
        self._drm = drm
        self.format = format
        self.width = width
        self.height = height
        self.bo = DrmDumbBuffer(self._drm, self.format, self.width, self.height)
        self.bo.mmap()
        if self.format.name == 'XR24':
            # didn't find an XRGB format
            self.image = Image.new("RGBX", (self.width, self.height))
        else:
            raise ValueError("DrmImageFramebuffer does not support format '%s'" % self.format.name)
        self._create()

    def flush(self, x1=None, y1=None, x2=None, y2=None):
        # FIXME: Revisit and see if this can be sped up and support big endian
        # Convert RGBX -> Little Endian XRGB
        b = bytearray(self.image.tobytes())
        b[0::4], b[2::4] = b[2::4], b[0::4]
        self.bo.map[:] = str(b)
        super(DrmDumbFramebuffer, self).flush(x1, y1, x2, y2)
