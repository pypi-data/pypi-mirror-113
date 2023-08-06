# -*- coding: utf-8 -*-
"""handler with infos."""

import json
import os

from datetime import datetime

from .scrapper import update_releases

class Infos:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    def __init__(self, update=True) -> None:
        """Load the json file.
    
        Args:
            update (bool, opptinally): update the json file before loading data, if True.
        Attributes:
            data (dict): json loaded
        """
        self.data = self._load_json();
        if update:
            self.update(delay=0)
    
    def _load_json(self) -> dict:
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)

        file = open('{}/releases_infos/infos.json'.format(dir))
        json_data = json.load(file)
        file.close()

        return json_data
    
    def update(self, delay=3) -> None:
        """Update Json file and data attribute.
        
        Args:
            delay (int): indicates the minimum days for updating the json
                the value is compared with the last update date
        """
        now = datetime.now().date()
        last_update_date = datetime.strptime(
            self.data['last_update']['date'],
            '%Y-%m-%d'
        ).date()

        diff = now - last_update_date
        if diff.days >= delay:
            has_changed = False

            dev_version = list(self.data['dev_release'].keys())[0]
            last_stable = self.data['last_update']['stable_version']

            new_infos = update_releases(dev_version, last_stable)
            new_dev = new_infos['new_dev']
            new_stables = new_infos['new_stables']

            if new_dev:
                has_changed = True
                self.data['dev_release'] = new_dev
            
            if new_stables:
                has_changed = True

                #update stable version if exists new stable
                stable_version = list(new_infos['new_stables'].keys())
                stable_version = (
                    stable_version[0] if stable_version else last_stable
                )

                new_last_update = {
                    "date": now.strftime('%Y-%m-%d'),
                    "stable_version": stable_version
                }

                new_stables.update(self.data['stables'])
                new_stables = dict(sorted(
                    new_stables.items(),
                    key=lambda item: item[0]
                ))
                
                self.data['last_update'] = new_last_update
                self.data['stables'] = new_stables
            
            if has_changed:
                path = os.path.realpath(__file__)
                dir = os.path.dirname(path)
                file = '{}/releases_infos/infos.json'.format(dir)

                with open(file, 'w') as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=4)
