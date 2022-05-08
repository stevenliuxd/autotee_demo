class ErrorCategory():
    name: str
    status_code: int
    message: str = "Unknown error"
class ErrorCategoryInvalidDate(ErrorCategory):
    name: str = "BAD REQUEST"
    status_code: int = 400
    message: str 
class ErrorCategoryUnknown(ErrorCategory):
    name: str = "INTERNAL SERVER ERROR"
    status_code: int = 500
    message: str
class ErrorCategoryDateTooFar(ErrorCategory):
    name: str = "BAD REQUEST"
    status_code: int = 400
    message: str
class ErrorCategoryInvalidTeeTime(ErrorCategory):
    name: str = "BAD REQUEST"
    status_code: int = 400
    message: str 
class ErrorCategoryInvalidCourse(ErrorCategory):
    name: str = "BAD REQUEST"
    status_code: int = 400
    message: str 

####################################################################################
class TeeException(Exception):
    def __init__(self, category: str, message: str, status_code: int):
        self.category = category
        self.status_code = status_code
        self.message = message
class UnknownException(TeeException):
    def __init__(self, message: str = ErrorCategoryUnknown.message):
        super().__init__(
            category=ErrorCategoryUnknown.name,
            status_code=ErrorCategoryUnknown.status_code,
            message=message, 
        )
class InvalidDateException(TeeException):
    def __init__(self, message: str = ErrorCategoryInvalidDate.message):
        super().__init__(
            category=ErrorCategoryInvalidDate.name,
            status_code=ErrorCategoryInvalidDate.status_code,
            message=message, 
        )
class DateTooFarException(TeeException):
    def __init__(self, message: str = ErrorCategoryDateTooFar.message):
        super().__init__(
            category=ErrorCategoryDateTooFar.name,
            status_code=ErrorCategoryDateTooFar.status_code,
            message=message, 
        )
class TeeTimeException(TeeException):
    def __init__(self, message: str = ErrorCategoryInvalidTeeTime.message):
        super().__init__(
            category=ErrorCategoryInvalidTeeTime.name,
            status_code=ErrorCategoryInvalidTeeTime.status_code,
            message=message, 
        )
class CourseException(TeeException):
    def __init__(self, message: str = ErrorCategoryInvalidCourse.message):
        super().__init__(
            category=ErrorCategoryInvalidCourse.name,
            status_code=ErrorCategoryInvalidCourse.status_code,
            message=message, 
        )