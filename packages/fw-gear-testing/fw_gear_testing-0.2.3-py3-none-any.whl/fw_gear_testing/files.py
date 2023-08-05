"""Testing fixtures for creating/mocking certain files."""
import io
import logging

log = logging.getLogger(__name__)

try:
    import pydicom
    from fw_file import dicom
except (ImportError, ModuleNotFoundError):
    pass
import pytest


def merge_dcmdict(custom: dict, default: dict) -> dict:
    """Merge a custom dict onto some defaults."""
    custom = custom or {}
    merged = {}
    for key, value in default.items():
        merged[key] = value
    for key, value in custom.items():
        if value is UNSET:
            merged.pop(key)
        else:
            merged[key] = value
    return merged


def apply_dcmdict(dataset: pydicom.Dataset, dcmdict: dict) -> None:
    """Add dataelements to a dataset from the given dcmdict."""
    # pylint: disable=invalid-name
    try:
        dcmdict = dcmdict or {}
        for key, value in dcmdict.items():
            if isinstance(value, (list, tuple)) and len(value) == 2:
                VR_dict = pydicom.datadict.dictionary_VR(key)
                VR, value = value
                if VR == VR_dict:
                    dataset.add_new(key, VR, value)
                else:
                    try:
                        dataset.add_new(key, VR_dict, value)
                    except:
                        log.error(
                            f"Could not add key {key}, VR {VR_dict}, value {value}"
                        )
            else:
                VR = pydicom.datadict.dictionary_VR(key)
                dataset.add_new(key, VR, value)
    except NameError:
        log.error("Need pydicom to use this fixture.")
        return None


# sentinel value for merge() to skip default_dcmdict keys
UNSET = object()


default_dcmdict = dict(
    SOPClassUID="1.2.840.10008.5.1.4.1.1.4",  # MR Image Storage
    SOPInstanceUID="1.2.3",
    PatientID="test",
    StudyInstanceUID="1",
    SeriesInstanceUID="1.2",
)


@pytest.fixture
def default_dcmdict_fixture():
    """default dataset dict used in create_dcm."""
    return default_dcmdict


def create_ds(**dcmdict) -> pydicom.Dataset:
    dataset = pydicom.Dataset()
    apply_dcmdict(dataset, dcmdict)
    return dataset


@pytest.fixture
def create_ds_fixture():
    """Create and return a dataset from a dcmdict."""
    return create_ds


def create_dcm(file=None, preamble=None, file_meta=None, **dcmdict):
    try:
        dcmdict = merge_dcmdict(dcmdict, default_dcmdict)
        dataset = pydicom.FileDataset(file, create_ds(**dcmdict))
        dataset.preamble = preamble or b"\x00" * 128
        dataset.file_meta = pydicom.dataset.FileMetaDataset()
        apply_dcmdict(dataset.file_meta, file_meta)
        file = file or io.BytesIO()
        pydicom.dcmwrite(file, dataset, write_like_original=bool(file_meta))
        if isinstance(file, io.BytesIO):
            file.seek(0)
        return dicom.DICOM(file)
    except NameError:
        log.error("Need pydicom and fw-file to use this fixture.")
        return None


@pytest.fixture
def create_dcm_fixture():  # pylint: disable=redefined-outer-name
    """Create a dataset and return it loaded as an fw_file.dicom.DICOM."""

    return create_dcm
