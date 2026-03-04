import asyncio
import random
from typing import Literal
from .base_entity import EntityBase
from app.config import settings


class Animal(EntityBase):
    """
    Domain model representing an Animal entity.

    This model extends EntityBase and defines animal-specific
    attributes and behavior such as aging, hunger progression,
    reproduction checks, and periodic state persistence.

    The `type` field is used as a discriminator for Pydantic
    polymorphic validation.
    """

    type: Literal["Animal"]
    age: float = 0
    breeding_chance: int = 0
    hungry: int = 0

    async def getting_old(self):
        """
        Continuously increase the animal's age.

        On each iteration:
            - Increase age by configured increment.
            - Randomly check if reproduction occurs.
            - Log the updated age.
            - Sleep for configured interval.

        This coroutine runs indefinitely until cancelled.
        """
        try:
            while True:
                self.age += settings.GETTING_OLD

                if random.random() <= self.breeding_chancec/ settings.CHECK_REPRODUCTION:
                    print(settings.REPRODUCTION_MESSAGE % self.ID)

                print(settings.AGE_MESSAGE % (self.ID, str(self.age)))

                await asyncio.sleep(settings.ENTITY_INTERVAL_SECONDS)
        except asyncio.CancelledError or KeyboardInterrupt:
            print(settings.CANCEL)

    async def getting_hungry(self):
        """
        Continuously increase the animal's hunger level.

        On each iteration:
            - Increase hunger up to MAX_HUNGRY.
            - Log the updated hunger value.
            - Sleep for configured interval.

        This coroutine runs indefinitely until cancelled.
        """
        try:
            while True:
                if self.hungry < settings.MAX_HUNGRY:
                    self.hungry += settings.GETTING_HUNGRY

                print(settings.HUNGER_MESSAGE % (self.ID, self.hungry))

                await asyncio.sleep(settings.ENTITY_INTERVAL_SECONDS)

        except asyncio.CancelledError or KeyboardInterrupt:
            print(settings.CANCEL)

    async def persist_state(self, accessor, interval_seconds: int):
        """
        Persist the current in-memory state of the animal to the database.

        Args:
            accessor:
                Data access layer responsible for updating the entity.
            interval_seconds (int):
                Time interval between persistence operations.

        On each iteration:
            - Update age and hunger fields in MongoDB.
            - Log persistence event.
            - Sleep for the specified interval.

        This coroutine runs indefinitely until cancelled.
        """
        try:
            while True:
                await accessor.update_fields(
                    self.ID,
                    {
                        "age": self.age,
                        "hungry": self.hungry
                    }
                )

                print(settings.WRITE_TO_DB_MESSAGE % (self.ID, self.age, self.hungry))

                await asyncio.sleep(interval_seconds)

        except asyncio.CancelledError or KeyboardInterrupt:
            print(settings.CANCEL)

        except Exception as e:
            print(settings.ERROR % e)

    async def process(self, accessor, interval_seconds: int):
        """
        Start the full lifecycle processing for the animal.

        This method runs:
            - Aging process
            - Hunger progression
            - Periodic state persistence

        All tasks are executed concurrently using asyncio.

        Args:
            accessor:
                Data access layer used for persistence.
            interval_seconds (int):
                Interval for database persistence.

        This method blocks until all tasks are cancelled
        or an unhandled exception occurs.
        """
        task_old = asyncio.create_task(self.getting_old())
        task_hungry = asyncio.create_task(self.getting_hungry())
        task_persist = asyncio.create_task(
            self.persist_state(accessor, interval_seconds)
        )

        await asyncio.gather(task_persist, task_old, task_hungry, return_exceptions=False)
