"""Tests for agents/actions.py — Action types."""

from __future__ import annotations

import numpy as np

from agents.actions import (
    ActionSpace,
    ActionType,
    ModifyCell,
    ModifyRegion,
    Wait,
)
from world.cell import CellState


class TestActionType:
    def test_all_types(self) -> None:
        assert hasattr(ActionType, "MODIFY_CELL")
        assert hasattr(ActionType, "MODIFY_REGION")
        assert hasattr(ActionType, "SIGNAL")
        assert hasattr(ActionType, "WAIT")


class TestModifyCell:
    def test_set_alive(self, small_world) -> None:
        action = ModifyCell(1, 1, alive=True, agent_id="a1")
        action.apply(small_world, None)
        assert small_world.get(1, 1) == CellState.ALIVE

    def test_set_dead(self, small_world) -> None:
        from world.cell import CellState

        small_world.set(1, 1, CellState.ALIVE)
        action = ModifyCell(1, 1, alive=False, agent_id="a1")
        action.apply(small_world, None)
        assert small_world.get(1, 1) == CellState.DEAD

    def test_action_type(self) -> None:
        action = ModifyCell(0, 0, alive=True)
        assert action.action_type == ActionType.MODIFY_CELL

    def test_repr(self) -> None:
        action = ModifyCell(1, 2, alive=True, agent_id="a1")
        assert "ModifyCell" in repr(action)


class TestModifyRegion:
    def test_fill_rectangle(self, small_world) -> None:
        action = ModifyRegion(1, 1, 3, 3, agent_id="a1")
        action.apply(small_world, None)
        for y in range(1, 4):
            for x in range(1, 4):
                assert small_world.get(x, y) == CellState.ALIVE

    def test_with_pattern(self, small_world) -> None:
        pattern = np.array([[1, 0], [0, 1]], dtype=np.uint8)
        action = ModifyRegion(0, 0, 1, 1, pattern=pattern, agent_id="a1")
        action.apply(small_world, None)
        assert small_world.get(0, 0) == CellState.ALIVE
        assert small_world.get(1, 0) == CellState.DEAD
        assert small_world.get(0, 1) == CellState.DEAD
        assert small_world.get(1, 1) == CellState.ALIVE

    def test_skips_out_of_bounds(self, small_world) -> None:
        action = ModifyRegion(3, 3, 10, 10, agent_id="a1")
        action.apply(small_world, None)
        assert small_world.get(4, 4) == CellState.ALIVE


class TestWait:
    def test_does_nothing(self, small_world) -> None:
        from world.cell import CellState

        small_world.set(2, 2, CellState.ALIVE)
        action = Wait(agent_id="a1")
        action.apply(small_world, None)
        assert small_world.get(2, 2) == CellState.ALIVE

    def test_action_type(self) -> None:
        action = Wait()
        assert action.action_type == ActionType.WAIT


class TestActionSpace:
    def test_create_modify_cell(self) -> None:
        space = ActionSpace()
        action = space.create_modify_cell(1, 2, alive=True, agent_id="a1")
        assert isinstance(action, ModifyCell)
        assert action.x == 1
        assert action.y == 2

    def test_create_wait(self) -> None:
        space = ActionSpace()
        action = space.create_wait(agent_id="a1")
        assert isinstance(action, Wait)

    def test_is_enabled(self) -> None:
        space = ActionSpace()
        assert space.is_enabled(ActionType.MODIFY_CELL)
        assert space.is_enabled(ActionType.WAIT)

    def test_disabled_action(self) -> None:
        space = ActionSpace(enabled_types=[ActionType.WAIT])
        assert not space.is_enabled(ActionType.MODIFY_CELL)
        assert space.is_enabled(ActionType.WAIT)
