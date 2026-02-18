from ghosttrace.core import GhostTrace

class GhostWriter(GhostTrace):
    def _save_ghost_json(self):
        import json
        from pathlib import Path

        ghost_file = Path(self.output_dir) / ".ghost.json"
        data = {}
        if ghost_file.exists():
            with open(ghost_file, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

        data["phantom_branches"] = [
            branch for branch in self._phantom_branches
        ]

        with open(ghost_file, "w") as f:
            json.dump(data, f, indent=2)
