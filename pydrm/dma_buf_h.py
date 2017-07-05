from ctypes import *
from .drm_h import _IOW

#struct dma_buf_sync {
#    __u64 flags;
#};

class DmaBufSyncC(Structure):
    _fields_ = [
                ("flags", c_uint64)
               ]

DMA_BUF_SYNC_READ      = (1 << 0)
DMA_BUF_SYNC_WRITE     = (2 << 0)
DMA_BUF_SYNC_RW        = (DMA_BUF_SYNC_READ | DMA_BUF_SYNC_WRITE)
DMA_BUF_SYNC_START     = (0 << 2)
DMA_BUF_SYNC_END       = (1 << 2)
DMA_BUF_SYNC_VALID_FLAGS_MASK = (DMA_BUF_SYNC_RW | DMA_BUF_SYNC_END)

#define DMA_BUF_BASE        'b'
DMA_BUF_BASE = ord('b')
#define DMA_BUF_IOCTL_SYNC  _IOW(DMA_BUF_BASE, 0, struct dma_buf_sync)
DMA_BUF_IOCTL_SYNC = _IOW(DMA_BUF_BASE, 0, DmaBufSyncC)
