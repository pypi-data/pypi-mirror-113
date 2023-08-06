from typing import Generic

from simple_cqrs.helpers.typing import T


class DomainEventSerializer(Generic[T]):
    def serialize(self, event: T) -> str:
        raise NotImplementedError

    def deserialize(self, serialized_event: str, manifest) -> T:
        raise NotImplementedError
