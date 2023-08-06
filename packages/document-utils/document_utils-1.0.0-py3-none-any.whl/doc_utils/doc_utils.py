from .read_utils import DocReadUtils
from .write_utils import DocWriteUtils

class DocUtils(DocReadUtils, DocWriteUtils):
    """Class for all document utilities. 
    Primarily should be used as a mixin for future functions
    but can be a standalone.
    """
