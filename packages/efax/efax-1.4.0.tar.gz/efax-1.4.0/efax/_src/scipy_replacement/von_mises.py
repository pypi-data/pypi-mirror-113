from typing import Optional

import numpy as np
from scipy import stats as ss
from tjax import RealArray

from .shaped_distribution import ShapedDistribution

__all__ = ['ScipyVonMises']


class ScipyVonMises(ShapedDistribution):
    """
    This class allows distributions having a non-empty shape.
    """
    def __init__(self, kappa: RealArray, loc: Optional[RealArray] = None):
        if loc is None:
            loc = np.zeros_like(kappa)
        shape = np.broadcast(kappa, loc).shape
        rvs_shape = ()
        dtype = np.result_type(kappa.dtype, loc.dtype)  # type: ignore
        kappa = np.broadcast_to(kappa, shape).astype(dtype)  # type: ignore
        loc: RealArray = np.broadcast_to(loc, shape).astype(dtype)  # type: ignore
        objects = np.empty(shape, dtype=np.object_)
        for i in np.ndindex(*shape):
            objects[i] = ss.vonmises(kappa[i], loc[i])
        super().__init__(shape, rvs_shape, dtype, objects)
