from coh2_stats.match.match_statistics import MatchStatistics
from coh2_stats.query.coh2_io import Coh2IO
from coh2_stats.utils.serialization import PickleSerialization

class MatchCollection(PickleSerialization):
    def __init__(self, collection_name: str, matches = []) -> str:
        self.matches = matches
        self.collection_name = collection_name
        super().__init__("match_collection", collection_name)

    def save_to_csv(self):
        io = Coh2IO("output", "csv")
        data = '\n'.join([str(match) for match in self.matches])
        io.write_str(data, self.collection_name)

    def add(self, match):
        self.matches.append(match)

    def add_list(self, matches):
        self.matches.extend(matches)

    def filter_by_playercard_collection(self, playercard_ollection):
        predicate = lambda match: match.detail.is_qualified(playercard_ollection)
        self.filter(predicate)
        return self

    def filter(self, predicate):
        result = []
        for match in self.matches:
            if predicate(match):
                result.append(match)
        self.matches = result
        return self

    def __repr__(self) -> str:
        return f"{self.collection_name}:, totally {len(self.matches)}" 


