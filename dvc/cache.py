import os

from dvc.config import Config


class Cache(object):
    CACHE_DIR = 'cache'

    def __init__(self, project):
        from dvc.remote import Remote

        self.project = project

        config = project.config._config[Config.SECTION_CACHE]
        local = config.get(Config.SECTION_CACHE_LOCAL)

        if local:
            name = Config.SECTION_REMOTE_FMT.format(local)
            sect = project.config._config[name]
        else:
            default_cache_dir = os.path.join(project.dvc_dir, self.CACHE_DIR)
            cache_dir = config.get(Config.SECTION_CACHE_DIR, default_cache_dir)
            cache_type = config.get(Config.SECTION_CACHE_TYPE)
            protected = config.get(Config.SECTION_CACHE_PROTECTED)

            sect = {
                Config.PRIVATE_CWD: config.get(Config.PRIVATE_CWD,
                                               project.dvc_dir),
                Config.SECTION_REMOTE_URL: cache_dir,
                Config.SECTION_CACHE_TYPE: cache_type,
                Config.SECTION_CACHE_PROTECTED: protected
            }

        self.local = Remote(project, sect)

        self.s3 = self._get_remote(config, Config.SECTION_CACHE_S3)
        self.gs = self._get_remote(config, Config.SECTION_CACHE_GS)
        self.ssh = self._get_remote(config, Config.SECTION_CACHE_SSH)
        self.hdfs = self._get_remote(config, Config.SECTION_CACHE_HDFS)
        self.azure = self._get_remote(config, Config.SECTION_CACHE_AZURE)

    def _get_remote(self, config, name):
        from dvc.remote import Remote

        remote = config.get(name, None)
        if not remote:
            return None

        name = Config.SECTION_REMOTE_FMT.format(remote)
        sect = self.project.config._config[name]
        return Remote(self.project, sect)
