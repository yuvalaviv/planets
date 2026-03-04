import asyncio
import random
from typing import Literal
from datetime import datetime
from .base_entity import EntityBase


class Animal(EntityBase):
    type: Literal["Animal"]
    age: float = 0
    breeding_chance: int = 0
    hungry: int = 0
    _persist_interval: int = 10  # seconds between DB updates

    async def getting_old(self):
        """Increase age and possibly trigger reproduction"""
        while True:
            self.age += 0.1
            if random.randint(0, 100) <= self.breeding_chance:
                print(f"Animal {self.ID} reproduced!")
            print(f"Animal {self.ID} age: {self.age:.1f}")
            await asyncio.sleep(3)

    async def getting_hungry(self):
        """Increase hunger over time"""
        while True:
            self.hungry += 1
            print(f"Animal {self.ID} hunger: {self.hungry}")
            await asyncio.sleep(5)

    async def persist_state(self, accessor):
        """Persist the current state to MongoDB every _persist_interval seconds"""
        while True:
            print("a")
            await accessor.update_fields(self.ID, {
                "age": self.age,
            })
            print(f"[DB] Animal {self.ID} persisted: age={self.age:.1f}, hungry={self.hungry}")
            await asyncio.sleep(self._persist_interval)

    async def process(self, accessor):
        """Run all tasks concurrently"""
        # Schedule tasks concurrently
        task_old = asyncio.create_task(self.getting_old())
        task_hungry = asyncio.create_task(self.getting_hungry())
        task_persist = asyncio.create_task(self.persist_state(accessor))

        # Await them all (they run indefinitely)
        await asyncio.gather(*self._tasks)