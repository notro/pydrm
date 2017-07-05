from .format import DrmFormat
from .framebuffer import DrmFramebuffer
from .buffer import DrmDumbBuffer


class DrmImageFramebuffer(DrmFramebuffer):
    def __init__(self, drm=None, format_=None, width=None, height=None, bo=None):
        if drm and format_ and width and height and bo is None:
            bo = DrmDumbBuffer(drm, format_, width, height)
        elif (drm or format_ or width or height) and bo is None:
            raise TypeError()
        super(DrmImageFramebuffer, self).__init__(bo)
        self._setup()

    def _setup(self):
        from PIL import Image
        self.bo.mmap()
        if self.format.name == 'XR24':
            # didn't find an XRGB format
            self.image = Image.new("RGBX", (self.width, self.height))
        else:
            raise ValueError("DrmImageFramebuffer does not support format '%s'" % self.format.name)

    def flush(self, x1=None, y1=None, x2=None, y2=None):
        # FIXME: Revisit and see if this can be sped up and support big endian
        # Convert RGBX -> Little Endian XRGB
        b = bytearray(self.image.tobytes())
        b[0::4], b[2::4] = b[2::4], b[0::4]
        self.bo.map[:] = str(b)
        super(DrmImageFramebuffer, self).flush(x1, y1, x2, y2)
