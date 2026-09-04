"""Basic DICOM loading utilities for PiriView Core."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable

import pydicom
from pydicom.dataset import Dataset
from pydicom.errors import InvalidDicomError


def _slice_sort_key(dataset: Dataset) -> tuple[float, int]:
    """Return a stable sort key for slices in a DICOM series."""
    position = getattr(dataset, "ImagePositionPatient", None)
    if position is not None and len(position) >= 3:
        try:
            return float(position[2]), int(getattr(dataset, "InstanceNumber", 0))
        except (TypeError, ValueError):
            pass

    try:
        instance_number = int(getattr(dataset, "InstanceNumber", 0))
    except (TypeError, ValueError):
        instance_number = 0

    return float(instance_number), instance_number


def load_dicom_file(path: str | Path) -> Dataset:
    """Load one DICOM file and return its pydicom dataset."""
    return pydicom.dcmread(str(Path(path)))


def load_dicom_series(folder: str | Path) -> dict[str, list[Dataset]]:
    """Load DICOM files from a folder and group them by SeriesInstanceUID.

    Non-DICOM files are skipped. Files are searched recursively so nested
    study folders are supported. Each returned series is sorted using slice
    position when available, with InstanceNumber as a fallback.
    """
    root = Path(folder)
    if not root.exists():
        raise FileNotFoundError(f"DICOM folder does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Expected a folder, got: {root}")

    grouped: defaultdict[str, list[Dataset]] = defaultdict(list)

    for file_path in _iter_files(root):
        try:
            dataset = pydicom.dcmread(str(file_path), stop_before_pixels=False)
        except (InvalidDicomError, OSError, PermissionError):
            continue

        series_uid = getattr(dataset, "SeriesInstanceUID", None)
        if not series_uid:
            continue

        grouped[str(series_uid)].append(dataset)

    return {
        series_uid: sorted(datasets, key=_slice_sort_key)
        for series_uid, datasets in grouped.items()
    }


def _iter_files(folder: Path) -> Iterable[Path]:
    """Yield all files below a folder recursively."""
    for path in folder.rglob("*"):
        if path.is_file():
            yield path
