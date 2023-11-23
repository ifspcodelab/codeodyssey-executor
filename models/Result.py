import uuid

class Result:
    def __init__(self, name, time, error, resolution_id):
        self._id = uuid.uuid4()
        self._name = name
        self._time = time
        self._error = error
        self._resolution_id = resolution_id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def time(self):
        return self._time

    @property
    def error(self):
        return self._error
    
    @property
    def resolution_id(self):
        return self._resolution_id

    @name.setter
    def name(self, value):
        self._name = value

    @time.setter
    def time(self, value):
        self._time = value

    @error.setter
    def error(self, value):
        self._error = value

    @resolution_id.setter
    def resolution_id(self, value):
        self._resolution_id = value

    def __str__(self):
        return f"Result(id={str(self._id)}, name={self._name}, time={self._time}, error={self._error}, resolution_id={self._resolution_id})"
    
    def asdict(self):
        return {'id': str(self._id), 'name': self._name, 'time': self._time, 'error':self._error, 'resolution_id': self._resolution_id}