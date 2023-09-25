import asyncio


def run_func_async():
    """Wraps a function with asyncio.run() to run it in an async context.

    Args:
        func (callable): The function to be wrapped.

    Returns:
        callable: The wrapped function
    """

    def wraper(func):
        """Returns: callable: The wrapped function."""

        def run(self, *args, **kwargs):
            return asyncio.run(func(self, *args, **kwargs))

        return run

    return wraper
