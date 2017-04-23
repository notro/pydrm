from .base import DrmObject

def fourcc_code(a, b, c, d):
    return (ord(a) | (ord(b) << 8) | (ord(c) << 16) | (ord(d) << 24))

DRM_FORMAT_BIG_ENDIAN   = (1<<31)

DRM_FORMAT_C8           = fourcc_code('C', '8', ' ', ' ') # [7:0] C
DRM_FORMAT_R8           = fourcc_code('R', '8', ' ', ' ') # [7:0] R
DRM_FORMAT_R16          = fourcc_code('R', '1', '6', ' ') # [15:0] R little endian
DRM_FORMAT_RG88         = fourcc_code('R', 'G', '8', '8') # [15:0] R:G 8:8 little endian
DRM_FORMAT_GR88         = fourcc_code('G', 'R', '8', '8') # [15:0] G:R 8:8 little endian
DRM_FORMAT_RG1616       = fourcc_code('R', 'G', '3', '2') # [31:0] R:G 16:16 little endian
DRM_FORMAT_GR1616       = fourcc_code('G', 'R', '3', '2') # [31:0] G:R 16:16 little endian
DRM_FORMAT_RGB332       = fourcc_code('R', 'G', 'B', '8') # [7:0] R:G:B 3:3:2
DRM_FORMAT_BGR233       = fourcc_code('B', 'G', 'R', '8') # [7:0] B:G:R 2:3:3
DRM_FORMAT_XRGB4444     = fourcc_code('X', 'R', '1', '2') # [15:0] x:R:G:B 4:4:4:4 little endian
DRM_FORMAT_XBGR4444     = fourcc_code('X', 'B', '1', '2') # [15:0] x:B:G:R 4:4:4:4 little endian
DRM_FORMAT_RGBX4444     = fourcc_code('R', 'X', '1', '2') # [15:0] R:G:B:x 4:4:4:4 little endian
DRM_FORMAT_BGRX4444     = fourcc_code('B', 'X', '1', '2') # [15:0] B:G:R:x 4:4:4:4 little endian
DRM_FORMAT_ARGB4444     = fourcc_code('A', 'R', '1', '2') # [15:0] A:R:G:B 4:4:4:4 little endian
DRM_FORMAT_ABGR4444     = fourcc_code('A', 'B', '1', '2') # [15:0] A:B:G:R 4:4:4:4 little endian
DRM_FORMAT_RGBA4444     = fourcc_code('R', 'A', '1', '2') # [15:0] R:G:B:A 4:4:4:4 little endian
DRM_FORMAT_BGRA4444     = fourcc_code('B', 'A', '1', '2') # [15:0] B:G:R:A 4:4:4:4 little endian
DRM_FORMAT_XRGB1555     = fourcc_code('X', 'R', '1', '5') # [15:0] x:R:G:B 1:5:5:5 little endian
DRM_FORMAT_XBGR1555     = fourcc_code('X', 'B', '1', '5') # [15:0] x:B:G:R 1:5:5:5 little endian
DRM_FORMAT_RGBX5551     = fourcc_code('R', 'X', '1', '5') # [15:0] R:G:B:x 5:5:5:1 little endian
DRM_FORMAT_BGRX5551     = fourcc_code('B', 'X', '1', '5') # [15:0] B:G:R:x 5:5:5:1 little endian
DRM_FORMAT_ARGB1555     = fourcc_code('A', 'R', '1', '5') # [15:0] A:R:G:B 1:5:5:5 little endian
DRM_FORMAT_ABGR1555     = fourcc_code('A', 'B', '1', '5') # [15:0] A:B:G:R 1:5:5:5 little endian
DRM_FORMAT_RGBA5551     = fourcc_code('R', 'A', '1', '5') # [15:0] R:G:B:A 5:5:5:1 little endian
DRM_FORMAT_BGRA5551     = fourcc_code('B', 'A', '1', '5') # [15:0] B:G:R:A 5:5:5:1 little endian
DRM_FORMAT_RGB565       = fourcc_code('R', 'G', '1', '6') # [15:0] R:G:B 5:6:5 little endian
DRM_FORMAT_BGR565       = fourcc_code('B', 'G', '1', '6') # [15:0] B:G:R 5:6:5 little endian
DRM_FORMAT_RGB888       = fourcc_code('R', 'G', '2', '4') # [23:0] R:G:B little endian
DRM_FORMAT_BGR888       = fourcc_code('B', 'G', '2', '4') # [23:0] B:G:R little endian
DRM_FORMAT_XRGB8888     = fourcc_code('X', 'R', '2', '4') # [31:0] x:R:G:B 8:8:8:8 little endian
DRM_FORMAT_XBGR8888     = fourcc_code('X', 'B', '2', '4') # [31:0] x:B:G:R 8:8:8:8 little endian
DRM_FORMAT_RGBX8888     = fourcc_code('R', 'X', '2', '4') # [31:0] R:G:B:x 8:8:8:8 little endian
DRM_FORMAT_BGRX8888     = fourcc_code('B', 'X', '2', '4') # [31:0] B:G:R:x 8:8:8:8 little endian
DRM_FORMAT_ARGB8888     = fourcc_code('A', 'R', '2', '4') # [31:0] A:R:G:B 8:8:8:8 little endian
DRM_FORMAT_ABGR8888     = fourcc_code('A', 'B', '2', '4') # [31:0] A:B:G:R 8:8:8:8 little endian
DRM_FORMAT_RGBA8888     = fourcc_code('R', 'A', '2', '4') # [31:0] R:G:B:A 8:8:8:8 little endian
DRM_FORMAT_BGRA8888     = fourcc_code('B', 'A', '2', '4') # [31:0] B:G:R:A 8:8:8:8 little endian
DRM_FORMAT_XRGB2101010  = fourcc_code('X', 'R', '3', '0') # [31:0] x:R:G:B 2:10:10:10 little endian
DRM_FORMAT_XBGR2101010  = fourcc_code('X', 'B', '3', '0') # [31:0] x:B:G:R 2:10:10:10 little endian
DRM_FORMAT_RGBX1010102  = fourcc_code('R', 'X', '3', '0') # [31:0] R:G:B:x 10:10:10:2 little endian
DRM_FORMAT_BGRX1010102  = fourcc_code('B', 'X', '3', '0') # [31:0] B:G:R:x 10:10:10:2 little endian
DRM_FORMAT_ARGB2101010  = fourcc_code('A', 'R', '3', '0') # [31:0] A:R:G:B 2:10:10:10 little endian
DRM_FORMAT_ABGR2101010  = fourcc_code('A', 'B', '3', '0') # [31:0] A:B:G:R 2:10:10:10 little endian
DRM_FORMAT_RGBA1010102  = fourcc_code('R', 'A', '3', '0') # [31:0] R:G:B:A 10:10:10:2 little endian
DRM_FORMAT_BGRA1010102  = fourcc_code('B', 'A', '3', '0') # [31:0] B:G:R:A 10:10:10:2 little endian
DRM_FORMAT_YUYV         = fourcc_code('Y', 'U', 'Y', 'V') # [31:0] Cr0:Y1:Cb0:Y0 8:8:8:8 little endian
DRM_FORMAT_YVYU         = fourcc_code('Y', 'V', 'Y', 'U') # [31:0] Cb0:Y1:Cr0:Y0 8:8:8:8 little endian
DRM_FORMAT_UYVY         = fourcc_code('U', 'Y', 'V', 'Y') # [31:0] Y1:Cr0:Y0:Cb0 8:8:8:8 little endian
DRM_FORMAT_VYUY         = fourcc_code('V', 'Y', 'U', 'Y') # [31:0] Y1:Cb0:Y0:Cr0 8:8:8:8 little endian
DRM_FORMAT_AYUV         = fourcc_code('A', 'Y', 'U', 'V') # [31:0] A:Y:Cb:Cr 8:8:8:8 little endian
DRM_FORMAT_NV12         = fourcc_code('N', 'V', '1', '2') # 2x2 subsampled Cr:Cb plane
DRM_FORMAT_NV21         = fourcc_code('N', 'V', '2', '1') # 2x2 subsampled Cb:Cr plane
DRM_FORMAT_NV16         = fourcc_code('N', 'V', '1', '6') # 2x1 subsampled Cr:Cb plane
DRM_FORMAT_NV61         = fourcc_code('N', 'V', '6', '1') # 2x1 subsampled Cb:Cr plane
DRM_FORMAT_NV24         = fourcc_code('N', 'V', '2', '4') # non-subsampled Cr:Cb plane
DRM_FORMAT_NV42         = fourcc_code('N', 'V', '4', '2') # non-subsampled Cb:Cr plane
DRM_FORMAT_YUV410       = fourcc_code('Y', 'U', 'V', '9') # 4x4 subsampled Cb (1) and Cr (2) planes
DRM_FORMAT_YVU410       = fourcc_code('Y', 'V', 'U', '9') # 4x4 subsampled Cr (1) and Cb (2) planes
DRM_FORMAT_YUV411       = fourcc_code('Y', 'U', '1', '1') # 4x1 subsampled Cb (1) and Cr (2) planes
DRM_FORMAT_YVU411       = fourcc_code('Y', 'V', '1', '1') # 4x1 subsampled Cr (1) and Cb (2) planes
DRM_FORMAT_YUV420       = fourcc_code('Y', 'U', '1', '2') # 2x2 subsampled Cb (1) and Cr (2) planes
DRM_FORMAT_YVU420       = fourcc_code('Y', 'V', '1', '2') # 2x2 subsampled Cr (1) and Cb (2) planes
DRM_FORMAT_YUV422       = fourcc_code('Y', 'U', '1', '6') # 2x1 subsampled Cb (1) and Cr (2) planes
DRM_FORMAT_YVU422       = fourcc_code('Y', 'V', '1', '6') # 2x1 subsampled Cr (1) and Cb (2) planes
DRM_FORMAT_YUV444       = fourcc_code('Y', 'U', '2', '4') # non-subsampled Cb (1) and Cr (2) planes
DRM_FORMAT_YVU444       = fourcc_code('Y', 'V', '2', '4') # non-subsampled Cr (1) and Cb (2) planes

# format, depth, num_planes, cpp, hsub, vsub
drm_formats = {
        DRM_FORMAT_C8              : [ 8,  1, [ 1, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGB332          : [ 8,  1, [ 1, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGR233          : [ 8,  1, [ 1, 0, 0 ], 1, 1 ],
        DRM_FORMAT_XRGB4444        : [ 0,  1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_XBGR4444        : [ 0,  1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGBX4444        : [ 0,  1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGRX4444        : [ 0,  1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_ARGB4444        : [ 0,  1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_ABGR4444        : [ 0,  1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGBA4444        : [ 0,  1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGRA4444        : [ 0,  1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_XRGB1555        : [ 15, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_XBGR1555        : [ 15, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGBX5551        : [ 15, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGRX5551        : [ 15, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_ARGB1555        : [ 15, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_ABGR1555        : [ 15, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGBA5551        : [ 15, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGRA5551        : [ 15, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGB565          : [ 16, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGR565          : [ 16, 1, [ 2, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGB888          : [ 24, 1, [ 3, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGR888          : [ 24, 1, [ 3, 0, 0 ], 1, 1 ],
        DRM_FORMAT_XRGB8888        : [ 24, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_XBGR8888        : [ 24, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGBX8888        : [ 24, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGRX8888        : [ 24, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_XRGB2101010     : [ 30, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_XBGR2101010     : [ 30, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGBX1010102     : [ 30, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGRX1010102     : [ 30, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_ARGB2101010     : [ 30, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_ABGR2101010     : [ 30, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGBA1010102     : [ 30, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGRA1010102     : [ 30, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_ARGB8888        : [ 32, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_ABGR8888        : [ 32, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_RGBA8888        : [ 32, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_BGRA8888        : [ 32, 1, [ 4, 0, 0 ], 1, 1 ],
        DRM_FORMAT_YUV410          : [ 0,  3, [ 1, 1, 1 ], 4, 4 ],
        DRM_FORMAT_YVU410          : [ 0,  3, [ 1, 1, 1 ], 4, 4 ],
        DRM_FORMAT_YUV411          : [ 0,  3, [ 1, 1, 1 ], 4, 1 ],
        DRM_FORMAT_YVU411          : [ 0,  3, [ 1, 1, 1 ], 4, 1 ],
        DRM_FORMAT_YUV420          : [ 0,  3, [ 1, 1, 1 ], 2, 2 ],
        DRM_FORMAT_YVU420          : [ 0,  3, [ 1, 1, 1 ], 2, 2 ],
        DRM_FORMAT_YUV422          : [ 0,  3, [ 1, 1, 1 ], 2, 1 ],
        DRM_FORMAT_YVU422          : [ 0,  3, [ 1, 1, 1 ], 2, 1 ],
        DRM_FORMAT_YUV444          : [ 0,  3, [ 1, 1, 1 ], 1, 1 ],
        DRM_FORMAT_YVU444          : [ 0,  3, [ 1, 1, 1 ], 1, 1 ],
        DRM_FORMAT_NV12            : [ 0,  2, [ 1, 2, 0 ], 2, 2 ],
        DRM_FORMAT_NV21            : [ 0,  2, [ 1, 2, 0 ], 2, 2 ],
        DRM_FORMAT_NV16            : [ 0,  2, [ 1, 2, 0 ], 2, 1 ],
        DRM_FORMAT_NV61            : [ 0,  2, [ 1, 2, 0 ], 2, 1 ],
        DRM_FORMAT_NV24            : [ 0,  2, [ 1, 2, 0 ], 1, 1 ],
        DRM_FORMAT_NV42            : [ 0,  2, [ 1, 2, 0 ], 1, 1 ],
        DRM_FORMAT_YUYV            : [ 0,  1, [ 2, 0, 0 ], 2, 1 ],
        DRM_FORMAT_YVYU            : [ 0,  1, [ 2, 0, 0 ], 2, 1 ],
        DRM_FORMAT_UYVY            : [ 0,  1, [ 2, 0, 0 ], 2, 1 ],
        DRM_FORMAT_VYUY            : [ 0,  1, [ 2, 0, 0 ], 2, 1 ],
        DRM_FORMAT_AYUV            : [ 0,  1, [ 4, 0, 0 ], 1, 1 ],
}

class DrmFormat(DrmObject):
    def __init__(self, fourcc):
        if isinstance(fourcc, int):
            self.fourcc = fourcc
            self.name = DrmFormat.fourcc_to_str(fourcc)
        else:
            self.name = str(fourcc)
            self.fourcc = DrmFormat.str_to_fourcc(self.name)

        if self.fourcc in drm_formats.keys():
            f = drm_formats[self.fourcc]
            self.depth = f[0]
            self.planes = f[1]
            self.cpp = f[2]
            self.hsub = f[3]
            self.vsub = f[4]
        else:
            raise NotImplementedError(self.name)

    def __eq__(self, other):
        return self.fourcc == other.fourcc

    @classmethod
    def fourcc_to_str(cls, fourcc):
        s = ""
        for i in range(4):
            s += "%s" % chr((fourcc >> (i*8)) & 0xff)
        return s

    @classmethod
    def str_to_fourcc(cls, str):
        try:
            return fourcc_code(str[0], str[1], str[2], str[3])
        except:
            raise ValueError("invalid fourcc string")
