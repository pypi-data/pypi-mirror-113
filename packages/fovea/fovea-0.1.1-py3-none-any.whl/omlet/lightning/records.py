import os
import sys
import omlet.utils as U
from pytorch_lightning.callbacks import Callback
from . import omlet_logger


class SourceCodeBackup(Callback):
    DEFAULT_INCLUDE_PATTERNS = ("*.py", "*.sh", "*.yaml", "*.yml", "*.md")

    def __init__(self, source_dir=".", sub_dir="code", include_patterns=None):
        """
        Args:
            tag_var_map: maps a tensorboard tag to the tracked variable
        """
        self.exp_dir = None  # will be populated by OmletTrainer
        self.sub_dir = sub_dir
        self.source_dir = self._get_code_path(source_dir)
        assert os.path.exists(
            self.source_dir
        ), 'source code dir "{}" does not exist'.format(self.source_dir)
        assert os.path.isdir(
            self.source_dir
        ), f'source code dir "{self.source_dir}" is not a directory'
        self._source_dir_last_part = U.last_part_in_path(self.source_dir)
        self._backup_dir = None
        if not include_patterns:
            include_patterns = self.DEFAULT_INCLUDE_PATTERNS
        self.include_patterns = include_patterns

    @property
    def backup_dir(self):
        """
        {exp_dir}/code/{your_repo_name}
        """
        if self._backup_dir is not None:
            return self._backup_dir

        assert self.exp_dir, "please use this callback with OmletTrainer"
        desired_path = U.f_join(self.exp_dir, self.sub_dir, self._source_dir_last_part)
        self._backup_dir = U.next_available_file_name(desired_path)
        if self._backup_dir != desired_path:
            omlet_logger.warning(
                f'Source code backup dir "{U.last_part_in_path(desired_path)}/" already exists, saving instead to "{U.last_part_in_path(self._backup_dir)}/"'
            )
        return self._backup_dir

    def _get_code_path(self, path):
        "handles both abspath and relative path"
        path = os.path.expanduser(path)
        if os.path.isabs(path):
            return path
        else:
            # relative to the launch script
            path = os.path.join(U.script_dir(), path)
            return os.path.abspath(path)

    def on_init_start(self, trainer):
        U.f_mkdir(self.backup_dir)
        U.f_copytree(
            self.source_dir,
            self.backup_dir,
            include=self.include_patterns,
            exist_ok=True,
        )
        omlet_logger.info(
            f"Backed up source code {self.source_dir} to {self.backup_dir}"
        )


class CsvRecord(Callback):
    # TODO
    pass
