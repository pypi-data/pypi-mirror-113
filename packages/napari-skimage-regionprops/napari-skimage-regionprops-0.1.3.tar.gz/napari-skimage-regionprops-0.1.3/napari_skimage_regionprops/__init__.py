try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.1.3"




from ._regionprops import napari_experimental_provide_function
