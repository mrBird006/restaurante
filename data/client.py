from typing import List, Dict, Optional

class PlateDataClient:
    def get_all_plates(self) -> List[Dict]:
        raise NotImplementedError

    def get_plate_by_slug(self, slug: str) -> Optional[Dict]:
        raise NotImplementedError

    def add_like(self, slug: str, email: str) -> None:
        raise NotImplementedError

    def add_dislike(self, slug: str, email: str) -> None:
        raise NotImplementedError

    def remove_reaction(self, slug: str, email: str) -> None:
        raise NotImplementedError

    def add_comment(self, slug: str, name: str, comment: str) -> None:
        raise NotImplementedError
