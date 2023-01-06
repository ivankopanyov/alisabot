"""Класс Result отображает результат операции."""


class Result:
    """Отобразить результат операции."""

    def __init__(self, success, value, error):
        """Отобразить результат операции."""
        self.success = success
        self.error = error
        self.value = value

    def __str__(self):
        """Неформальное строковое представление результата."""
        if self.success:
            return "[Success]"
        else:
            return f"[Failure] {self.error}"

    def __repr__(self):
        """Официальное строковое представление результата."""
        if self.success:
            return f"<Result success={self.success}>"
        else:
            return f'<Result success={self.success}, message="{self.error}">'

    @property
    def failure(self):
        """Флаг для отображения, выполнилась ли операция неудачно."""
        return not self.success

    def on_success(self, func, *args, **kwargs):
        """Передать результат успешной операции (если есть) в следующую функцию."""
        if self.failure:
            return self
        if self.value:
            return func(self.value, *args, **kwargs)
        return func(*args, **kwargs)

    def on_failure(self, func, *args, **kwargs):
        """Передать сообщение об ошибке из неудачной операции в следующую функцию."""
        if self.success:
            return self.value if self.value else None
        if self.error:
            return func(self.error, *args, **kwargs)
        return func(*args, **kwargs)

    def on_both(self, func, *args, **kwargs):
        """Передать результат (успешный/неудачный) в следующую функцию."""
        if self.value:
            return func(self.value, *args, **kwargs)
        return func(*args, **kwargs)

    @staticmethod
    def Fail(error_message):
        """Создать объект Result object для неудачной операции."""
        return Result(False, value=None, error=error_message)

    @staticmethod
    def Ok(value=None):
        """Создать объект Result для успешной операции."""
        return Result(True, value=value, error=None)

    @staticmethod
    def Combine(results):
        """Вернуть объект Result на основе результата списка объектов Results."""
        if all(result.success for result in results):
            return Result.Ok()
        errors = [result.error for result in results if result.failure]
        return Result.Fail("\n".join(errors))
