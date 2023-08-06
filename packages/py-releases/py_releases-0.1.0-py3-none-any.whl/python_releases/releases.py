# -*- coding: utf-8 -*-
from .infos import Infos

class Releases:
    def __init__(self) -> None:
        """Get required python versions.
    
        Attributes:
            infos (dict): infos about python versions
                data load from infos.json file
            dev (dict): version and download for the latest python pre-release
            last_stable (dict): version and download link of the last python stable
            all (dict): version and download link for all python releases
                the last item is the dev-version
        """
        self.infos = Infos().data

        self.last_stable = list(self.infos['stables'].items())[-1]
        self.dev = self.infos['dev_release']
        self.all = self._get_all_releases()
    
    def _get_all_releases(self) -> dict:
        all = self.infos['stables']
        all.update(self.dev)
        return all

    def search(self, version) -> str:
        """Search the download link from ´version´.

        Args:
            version (str): version to be searched
        Returns:
            str: Download link corresponding to version
        """
        try:
            return self.infos['stables'][version]
        except Exception:
            print("Version not found")
