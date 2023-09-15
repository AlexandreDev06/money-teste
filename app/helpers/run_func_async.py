import asyncio


def run_func_async():
    def wraper(func):
        def run(self, *args, **kwargs):
            return asyncio.run(func(self, *args, **kwargs))

        return run

    return wraper
