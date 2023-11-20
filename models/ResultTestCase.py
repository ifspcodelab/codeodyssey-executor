import uuid

class ResultTestCase:
    def __init__(self, test_name, success, info,  time, result_id):
        self._id = uuid.uuid4()
        self._test_name = test_name
        self._success = success
        self._info = info
        self._time = time
        self._result_id = result_id

    @property
    def id(self):
        return self._id

    @property
    def test_name(self):
        return self._test_name

    @property
    def success(self):
        return self._success

    @property
    def info(self):
        return self._info

    @property
    def time(self):
        return self._time

    @property
    def result_id(self):
        return self._result_id

    @test_name.setter
    def test_name(self, value):
        self._test_name = value

    @success.setter
    def success(self, value):
        self._success = value

    @info.setter
    def info(self, value):
        self._info = value

    @time.setter
    def time(self, value):
        self._time = value

    @result_id.setter
    def result_id(self, value):
        self._result_id= value

    def __str__(self):
        return f"ResultTestCase(id={str(self._id)}, test_name={self._test_name}, success={self._success}, info={self._info}, time={self._time}, result_id={str(self._result_id)})"
    
    def asdict(self):
        return {'id': str(self._id), 'test_name': self._test_name, 'success': self._success, 'info': self._info, 'time': self._time, 'result_id': str(self.result_id)}