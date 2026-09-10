"""Navigation state and services for PiriView Core."""

from dataclasses import dataclass


@dataclass
class SliceNavigationState:
    """Navigation state for a single image series."""

    slice_index: int = 0
    slice_count: int = 0


class NavigationService:
    """Manage slice navigation independently from the user interface."""

    def __init__(self):
        self._state = SliceNavigationState()

    @property
    def state(self) -> SliceNavigationState:
        """Return the current navigation state."""
        return self._state

    def set_series(self, slice_count: int) -> None:
        """Initialize navigation for a newly loaded series."""

        if slice_count < 1:
            raise ValueError("A series must contain at least one slice")

        self._state = SliceNavigationState(
            slice_index=0,
            slice_count=slice_count,
        )

    def set_slice(self, slice_index: int) -> int:
        """Set and return a bounded slice index."""

        if self._state.slice_count < 1:
            raise ValueError("No image series is loaded")

        bounded_index = max(
            0,
            min(slice_index, self._state.slice_count - 1),
        )

        self._state.slice_index = bounded_index
        return bounded_index

    def move_slice(self, steps: int) -> int:
        """Move relative to the current slice and return the new index."""

        return self.set_slice(
            self._state.slice_index + steps
        )
