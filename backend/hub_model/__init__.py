from .rmbg_model import ImageSegmentation   
from .migan import MiganInpainting

segmentation = ImageSegmentation()
migan = MiganInpainting()

__all__ = ["ImageSegmentation", "segmentation", "MiganInpainting", "migan"]
