"""Hierachy related fixtures."""
import copy
import random

import flywheel
import pytest

rand = random.Random()

hex_choices = "abcdef0123456789"


def make_object_id():
    # Twelve byte hex
    return "".join(rand.choices(hex_choices, k=24))


@pytest.fixture
def object_id():
    return make_object_id


def make_file_id():
    parts = [8, 4, 4, 4, 12]
    return "-".join(["".join(rand.choices(hex_choices, k=part)) for part in parts])


@pytest.fixture
def file_id():
    return make_file_id


class MockFinder:
    def __init__(self, arr):
        self.arr = arr

    def iter(self):
        for x in self.arr:
            yield x

    def iter_find(self, *args, **kwargs):
        yield from self.iter()

    def find(self, *args, **kwargs):
        return self.arr

    def find_first(self, *args, **kwargs):
        return self.arr[0]

    def __len__(self):
        return len(self.arr)

    def __call__(self):
        return self.arr


@pytest.fixture
def finder():
    def make_finder(arr):
        return MockFinder(arr)

    return make_finder


class MockContainerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        analyses = []
        files = []
        _update = None  # to store updates made to the container when calling `update`

    def reload(self):
        if self._update:
            for k, v in self._update.items():
                setattr(self, k, v)
            self._update = None
        return self

    def update(self, *args, **kwargs):
        self._update = flywheel.util.params_to_dict("update", args, kwargs)
        return None

    def get_file(self, name):
        if self.files:
            for file in self.files:
                if file.name == name:
                    return file
            return files[0]
        return None


class MockFileEntry(flywheel.FileEntry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = parent


class MockAcquisition(MockContainerMixin, flywheel.Acquisition):
    pass


class MockSession(MockContainerMixin, flywheel.Session):
    acquisitions = MockFinder([])


class MockSubject(MockContainerMixin, flywheel.Subject):
    sessions = MockFinder([])


class MockProject(MockContainerMixin, flywheel.Project):
    subjects = MockFinder([])


default_parents = {
    "acquisition": None,
    "analysis": None,
    "group": None,
    "project": None,
    "session": None,
    "subject": None,
}


class _containers:
    def __init__(self):
        self.containers = dict()

    def get_container(self, _id):
        if _id in self.containers:
            return self.containers[_id]
        else:
            raise flywheel.rest.ApiException(status=409, reason="Not Found")

    def add_container(self, container):
        self.containers[container.id] = container


_cont = _containers()


@pytest.fixture
def containers():
    return _cont


def make_acquisition(label, n_files=1, par=None):
    parents = copy.deepcopy(default_parents)
    if par:
        parents.update(par)
    acquisition = MockAcquisition(label=label, id=make_object_id(), parents=parents)
    files = []
    for i in range(n_files):
        files.append(
            MockFileEntry(
                name=f"file-{i}",
                id=make_file_id(),
                file_id=make_object_id(),
                parent=acquisition,
            )
        )
    acquisition.files = files
    _cont.add_container(acquisition)
    return acquisition


@pytest.fixture
def fw_acquisition():
    return make_acquisition


def make_session(label, n_acqs=1, n_files=1, par=None):
    parents = copy.deepcopy(default_parents)
    if par:
        parents.update(par)
    session = MockSession(label=label, id=make_object_id(), parents=parents)
    acquisitions = []
    for i in range(n_acqs):
        parents.update({"session": session.id})
        acquisitions.append(
            make_acquisition(f"acq-{i}-{label}", n_files=n_files, par=parents)
        )
    session.acquisitions = MockFinder(acquisitions)
    _cont.add_container(session)
    return session


@pytest.fixture
def fw_session():
    return make_session


def make_subject(label, n_ses=1, n_acqs=1, n_files=1, par=None):
    parents = copy.deepcopy(default_parents)
    if par:
        parents.update(par)
    subject = MockSubject(label=label, id=make_object_id(), parents=parents)
    sessions = []
    for i in range(n_ses):
        parents.update({"subject": subject.id})
        sessions.append(
            make_session(
                f"ses-{i}-{label}", n_acqs=n_acqs, n_files=n_files, par=parents
            )
        )
    subject.sessions = MockFinder(sessions)
    _cont.add_container(subject)
    return subject


@pytest.fixture
def fw_subject(fw_session, object_id, containers):
    return make_subject


def make_project(
    label="test", n_subs=1, n_ses=1, n_acqs=1, n_files=1, par={"group": "test"}
):
    parents = copy.deepcopy(default_parents)
    if par:
        parents.update(par)
    project = MockProject(label=label, id=make_object_id(), parents=parents)
    subjects = []
    for i in range(n_subs):
        parents.update({"project": project.id})
        subjects.append(
            make_subject(
                f"sub-{i}", n_ses=n_ses, n_acqs=n_acqs, n_files=n_files, par=parents
            )
        )
    project.subjects = MockFinder(subjects)
    _cont.add_container(project)
    return project


@pytest.fixture
def fw_project(fw_subject, object_id, containers):
    return make_project
