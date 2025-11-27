try:
    # Try to import the pyproj version first
    from .ghana_converter import GhanaWebConverter
except ImportError:
    # Fall back to pure Python version
    from .pure_python_converter import GhanaPurePythonConverter as GhanaWebConverter

from .coordinate_utils import dms_to_decimal, decimal_to_dms

__all__ = ['GhanaWebConverter', 'dms_to_decimal', 'decimal_to_dms']