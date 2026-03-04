import asyncio

from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.models.tree import Tree
from app.services.lifecycle.tree_config import TreeConfig


class TreeLifecycleService:
    """
    This service is responsible for managing the full asynchronous lifecycle of Animal entities.
    """
    def __init__(
        self,
        accessor: EntityMongoAccessor,
        config: TreeConfig
    ):
        """
        Initialize the service with required dependencies

        Args:
            accessor: EntityMongoAccessor instance for DB persistence.
            config: AnimalConfig instance defining lifecycle behavior.
        """
        self.accessor = accessor
        self.config = config
        self._tasks: dict[str, asyncio.Task] = {}

    async def run(self, tree: Tree):
        """
        Run aging, hunger, and persistence tasks concurrently.

        Args:
            tree: Tree domain entity
        """
        try:
            while True:
                tree.grow(self.config.height_increment)

                await self.accessor.update_fields(
                    tree.ID,
                    {
                        "height": tree.height
                    }
                )
                await asyncio.sleep(self.config.interval)

        except asyncio.CancelledError:
            raise
