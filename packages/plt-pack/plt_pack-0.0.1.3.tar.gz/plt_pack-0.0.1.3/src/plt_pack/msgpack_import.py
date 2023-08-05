import msgpack
import msgpack_numpy

msgpack_numpy.patch()

__all__ = ['msgpack']
