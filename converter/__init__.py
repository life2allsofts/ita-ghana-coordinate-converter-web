# Choose converter based on environment
import os

if os.environ.get('VERCEL'):
    from .pure_python_converter import GhanaPurePythonConverter as GhanaWebConverter
else:
    try:
        from .ghana_converter import GhanaWebConverter
    except ImportError:
        from .pure_python_converter import GhanaPurePythonConverter as GhanaWebConverter