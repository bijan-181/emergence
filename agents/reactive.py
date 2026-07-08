"""ReactiveAgent — rule-based agent that diffs world against target."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from agents.actions import ActionSpace, Wait
from agents.base import Agent, AgentType
from agents.perception import LocalPerception, Perception, TargetPerception

if TYPE_CHECKING:
    from agents.actions import Action
    from world.world import World


class ReactiveAgent(Agent):
    """A simple rule-based agent that moves cells toward the target pattern.

    Strategy:
      1. Perceive a local neighborhood and the target.
      2. Compute a diff map: cells that differ from the target.
      3. Pick the closest mismatch to the agent's center.
      4. Return a ModifyCell action for that cell.

    Parameters:
        agent_id: Unique identifier.
        position: World coordinate the agent is anchored to.
        local_radius: Half-size of the local perception window.
        target: Target pattern as a binary matrix (or None).
        target_offset: (x, y) offset where the target is placed.
    """

    def __init__(
        self,
        agent_id: str = "reactive-0",
        position: tuple[int, int] = (100, 100),
        local_radius: int = 50,
        target: np.ndarray | None = None,
        target_offset: tuple[int, int] = (0, 0),
    ) -> None:
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.REACTIVE,
            position=position,
        )
        self._radius = local_radius
        self._target = target
        self._target_offset = target_offset
        self._action_space = ActionSpace()

    def set_target(
        self, target: np.ndarray | None, offset: tuple[int, int] = (0, 0)
    ) -> None:
        self._target = target
        self._target_offset = offset

    def perceive(
        self, world: World, target: np.ndarray | None
    ) -> Perception:
        local_ch = LocalPerception(self._radius)
        t = target if target is not None else self._target
        target_ch = TargetPerception(t)
        return Perception(
            local=local_ch.observe(world, self.position),
            target=target_ch.observe(world, self.position),
            generation=world.generation,
        )

    def decide(self, perception: Perception) -> Action:
        if perception.target is None or not perception.target.is_loaded:
            return self._action_space.create_wait(self.agent_id)

        if perception.local is None:
            return self._action_space.create_wait(self.agent_id)

        mismatch = self._find_closest_mismatch(
            perception.local, perception.target
        )
        if mismatch is None:
            return self._action_space.create_wait(self.agent_id)

        wx, wy = mismatch
        return self._action_space.create_modify_cell(
            wx, wy, alive=True, agent_id=self.agent_id
        )

    def _find_closest_mismatch(
        self, local: "LocalView", target: "TargetView"
    ) -> tuple[int, int] | None:
        """Find the world-coordinate cell closest to center with a mismatch.

        Returns None if no mismatches exist.
        """
        local_cells = local.cells
        offset_x, offset_y = local.offset
        tw = target.pattern.shape[1]
        th = target.pattern.shape[0]
        r = local.radius

        best: tuple[int, int] | None = None
        best_dist = float("inf")

        for ly in range(local_cells.shape[0]):
            for lx in range(local_cells.shape[1]):
                wx = (offset_x + lx) % (r * 2 + 2)
                wy = (offset_y + ly) % (r * 2 + 2)

                tx = wx - self._target_offset[0]
                ty = wy - self._target_offset[1]
                if tx < 0 or ty < 0 or tx >= tw or ty >= th:
                    continue

                target_val = target.pattern[ty, tx]
                local_val = local_cells[ly, lx]
                if target_val == local_val:
                    continue

                dist = abs(lx - r) + abs(ly - r)
                if dist < best_dist:
                    best_dist = dist
                    best = (wx, wy)

        return best

    def __repr__(self) -> str:
        return (
            f"ReactiveAgent(id={self.agent_id!r}, "
            f"pos={self.position}, radius={self._radius})"
        )
