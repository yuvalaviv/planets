import asyncio

from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.models.animal import Animal
from app.services.lifecycle.animal_config import AnimalConfig


class AnimalLifecycleService:
    def __init__(
        self,
        accessor: EntityMongoAccessor,
        config: AnimalConfig
    ):
        self.accessor = accessor
        self.config = config
        self._tasks: dict[str, asyncio.Task] = {}

    async def start(self, animal: Animal):
        task = asyncio.create_task(self._run(animal))
        self._tasks[animal.ID] = task

    async def stop(self, animal_id: str):
        task = self._tasks.get(animal_id)
        if task:
            task.cancel()
            await task
            del self._tasks[animal_id]

    async def _run(self, animal: Animal):
        try:
            while True:
                animal.grow(self.config.age_increment)
                animal.increase_hunger(
                    self.config.hunger_increment,
                    self.config.max_hunger
                )

                await self.accessor.update_fields(
                    animal.ID,
                    {
                        "age": animal.age,
                        "hungry": animal.hungry,
                    }
                )
                await asyncio.sleep(self.config.interval)

        except asyncio.CancelledError:
            raise

    async def supervise(self, animal: Animal):
        while True:
            try:
                await self._run(animal)
            except Exception:
                raise
