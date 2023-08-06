import logging
from omlet.utils.logging_utils import omlet_logger

# ================= Patch up PL lightning ================
import pytorch_lightning
import omlet.utils.misc_utils

pytorch_lightning.core.memory.get_human_readable_count = lambda num: omlet.utils.misc_utils.get_human_readable_count(
    num, precision=2
)

# ======================================
from .core import ExtendedModule, STAGES
from .trainer import *
from .callbacks import *
from .checkpoint import ExtendedCheckpoint
from .multi_optimizer import MultiOptimizerModule
