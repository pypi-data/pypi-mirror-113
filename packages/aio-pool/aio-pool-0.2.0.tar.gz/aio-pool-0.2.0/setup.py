# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_pool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aio-pool',
    'version': '0.2.0',
    'description': "Extending Python's process pool to support async functions.",
    'long_description': '# aio-pool\nExtending Python\'s `multiporcessing.Pool` to support coroutine functions.  \nCan be useful for when using a server with very high bandwidth or doing both very large IO and CPU tasks at the same time.   \n\nAll methods of `multiprocessing.Pool` are supported.    \nAll paramters for multiprocessing.Pool are supported.  \n\n## examples:\nSetting concurrency limit. This means each process can run with up to 8 concurrent tasks at a time. \n```python\nimport asyncio\nfrom aio_pool import AioPool\n\n\nasync def powlong(a):\n  await asyncio.sleep(1)\n  return a**2\n\nif __name__ == \'__main__\':\n  with AioPool(processes=2, concurrency_limit=8) as pool:\n    results = pool.map(powlong, [i for i in range(16)])  # Should take 2 seconds (2*8).\n    print(results) \n\n```\n\nAsync initliazers are also suppported.\n\n```python\nimport asyncio\nfrom aio_pool import AioPool\n\nasync def start(message):\n  await asyncio.sleep(1)\n  print(message)\n\nasync def powlong(a):\n  await asyncio.sleep(1)\n  return a**2\n\nif __name__ == \'__main__\':\n  with AioPool(processes=2, \n               concurrency_limit=8, \n               initializer=start,\n               init_args=("Started with AioPool", )) as pool:\n    results = pool.map(powlong, [i for i in range(16)])  # Should take 2 seconds (2*8).\n    print(results) \n    \n```\n\nBy default, AioPool also set up a default executor for any non-async tasks.  \nThe size can be determined by `threadpool_size` arguemnt, which defaults to 1.   \nNone default event loops(`uvloop` for example) are supported as well, using the `loop_initializer` argument.  \nAlso, non-async functions are supported by default, as the AioPool worker identify if the function is async or not.  \nIf the function is not async, it runs inside the threadpool, to allow the requested concurrency.   \nThis means that order of execution is not guaranteed, even if the function is not async.  \nHowever, the order of results is guaranteed through the pool API (map, starmap, apply, etc...).  \n\n```python\nfrom aio_pool import AioPool\nimport uvloop\n\nwith AioPool(loop_initializer=uvloop.new_event_loop, threadpool_size=4) pool:\n  pool.map(print, [i for i in range(8)])\n```\n \n\n\n',
    'author': 'Itay Azolay',
    'author_email': 'itayazolay@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Itayazolay/aio-pool',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
