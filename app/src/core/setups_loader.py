import json
import os
from typing import Dict, List, Tuple

from configs import Paths, Settings
from core import Setup


class SetupsLoader:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.load_setups(settings)
        self.setups = self.setups_from_dict(self.setups_dict)

    def load_setups(self, settings: Settings) -> None:
        sample_setup = {
            "Sample Setup": [
                "echo \"Welcome to Setuppy!\"",
                "echo \"We hope you enjoy.\"",
                "echo \"More versions coming in the future...\""
            ]
        }

        if not settings.first_time:            
            try:
                with open(self.settings.to_dict().get("DefaultSetupsFile", Paths.SETUPS_JSON_FILE), "r") as setups_file:
                    content = setups_file.read()
                    
                    self.file_content = content
                    self.setups_dict = json.loads(content)
                    return
                
            except FileNotFoundError:
                self.settings.loading_errors.append(
                    "Setups file not found.\n" \
                    "Check the existance of the file setted in the settings."
                )

            except json.JSONDecodeError as e:
                self.settings.loading_errors.append(
                    "An error ocurred while parsing the JSON setups file.\n" \
                    "Please fix it.\n" +
                    e.__str__()
                )
                
            except Exception as e:
                self.settings.loading_errors.append("Unexpected error while trying to read setups file:\n" + e.__str__())
        
        self.file_content = json.dumps(sample_setup)
        self.setups_dict = sample_setup
        self.save_setups()

    def save_setups(self) -> None:
        folder = os.path.dirname(Paths.SETUPS_JSON_FILE)
        os.makedirs(folder, exist_ok=True)
        
        with open(self.settings.to_dict().get("DefaultSetupsFile", Paths.SETUPS_JSON_FILE), "w") as setups_file:
            setups_file.write(json.dumps(self.setups_dict, indent=4))
            self.update_setups()
            

    def setups_from_dict(self, setups_dict: Dict) -> List[Setup]:
        return [
            Setup(setup_name, setup_steps)
            for setup_name, setup_steps
            in setups_dict.items()
        ]
    
    def update_setups(self) -> None:
        self.setups = self.setups_from_dict(self.setups_dict)

    def delete_setup(self, setup: Setup) -> None:
        self.setups_dict.pop(setup.name)
        self.setups.remove(setup)
        self.save_setups()