import uuid

class Result:
    def __init__(self, name, time, error, activity_id):
        self._id = uuid.uuid4()
        self._name = name
        self._time = time
        self._error = error
        self._activity_id = activity_id

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
    def activity_id(self):
        return self._activity_id

    @name.setter
    def name(self, value):
        self._name = value

    @time.setter
    def time(self, value):
        self._time = value

    @error.setter
    def error(self, value):
        self._error = value

    @activity_id.setter
    def activity_id(self, value):
        self._activity_id = value

    def __str__(self):
        return f"Result(id={str(self._id)}, name={self._name}, time={self._time}, error={self._error}, activity_id={self._activity_id})"
    
    def asdict(self):
        return {'id': str(self._id), 'name': self._name, 'time': self._time, 'error':self._error, 'activity_id': self._activity_id}