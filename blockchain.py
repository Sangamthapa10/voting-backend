import hashlib
import json
from datetime import datetime


class Block:
    def __init__(self, index, data, previous_hash="0"):
        self.index = index
        self.timestamp = datetime.utcnow().isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }


class VoteBlockchain:
    """
    Simple SHA256 hash chain stored in the DB via VoteBlock model.
    Each vote becomes an immutable block linked to the previous one.
    """

    @staticmethod
    def get_last_block():
        from elections.models import VoteBlock
        last = VoteBlock.objects.order_by('-index').first()
        return last

    @staticmethod
    def add_vote_block(vote_data: dict) -> dict:
        """
        Creates a new block for a vote and saves it to the DB.
        Returns the saved block dict.
        """
        from elections.models import VoteBlock

        last = VoteBlockchain.get_last_block()

        if last:
            previous_hash = last.hash
            index = last.index + 1
        else:
            previous_hash = "0"
            index = 0

        block = Block(index=index, data=vote_data, previous_hash=previous_hash)

        VoteBlock.objects.create(
            index=block.index,
            timestamp=block.timestamp,
            data=json.dumps(block.data),
            previous_hash=block.previous_hash,
            hash=block.hash,
        )

        return block.to_dict()

    @staticmethod
    def is_chain_valid() -> bool:
        """Verify the integrity of the entire vote chain."""
        from elections.models import VoteBlock

        blocks = list(VoteBlock.objects.order_by('index'))
        if not blocks:
            return True

        for i, block in enumerate(blocks):
            # Recalculate hash
            block_string = json.dumps({
                "index": block.index,
                "timestamp": block.timestamp,
                "data": json.loads(block.data),
                "previous_hash": block.previous_hash,
            }, sort_keys=True)
            expected_hash = hashlib.sha256(block_string.encode()).hexdigest()

            if block.hash != expected_hash:
                return False

            if i > 0 and block.previous_hash != blocks[i - 1].hash:
                return False

        return True
