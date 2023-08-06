# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3priorityqueue",
    packages=["k3priorityqueue"],
    version="0.1.2",
    license='MIT',
    description='priorityQueue is a queue with priority support',
    long_description="# k3priorityqueue\n\n[![Action-CI](https://github.com/pykit3/k3priorityqueue/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3priorityqueue/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3priorityqueue.svg?branch=master)](https://travis-ci.com/pykit3/k3priorityqueue)\n[![Documentation Status](https://readthedocs.org/projects/k3priorityqueue/badge/?version=stable)](https://k3priorityqueue.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3priorityqueue)](https://pypi.org/project/k3priorityqueue)\n\npriorityQueue is a queue with priority support\n\nk3priorityqueue is a component of [pykit3] project: a python3 toolkit set.\n\n\nPriorityQueue is a queue with priority support:\n\nThe numbers of items it pops from each producer matches exactly the ratio of their priority:\nIf the priorities of 3 producer A, B and C are 1, 3 and 7, and it runs long\nenough, it is expected that the number of items popped from A, B and C are\n1:3:7.\n\nimport k3priorityqueue\n\nproducers = (\n    # id, priority, iterable\n    (1, 1, [1] * 10),\n    (2, 2, [2] * 10),\n    (3, 3, [3] * 10),\n)\npq = k3priorityqueue.PriorityQueue()\nfor pid, prio, itr in producers:\n    pq.add_producer(pid, prio, itr)\n\ncount = {}\nfor _ in range(12):\n    val = pq.get()\n    count[val] = count.get(val, 0) + 1\n    print(val)\n\nprint('respect priority ratio: counts:', repr(count))\n\nwhile True:\n    try:\n        val = pq.get()\n    except k3priorityqueue.Empty as e:\n        break\n    count[val] = count.get(val, 0) + 1\n    print(val)\n\nprint('consumed all: counts:', repr(count))\n\n\n\n\n# Install\n\n```\npip install k3priorityqueue\n```\n\n# Synopsis\n\n```python\n\nimport k3priorityqueue\n\nproducers = (\n    # id, priority, iterable\n    (1, 1, [1] * 10),\n    (2, 2, [2] * 10),\n    (3, 3, [3] * 10),\n)\npq = k3priorityqueue.PriorityQueue()\nfor pid, prio, itr in producers:\n    pq.add_producer(pid, prio, itr)\n\ncount = {}\nfor _ in range(12):\n    val = pq.get()\n    count[val] = count.get(val, 0) + 1\n    print(val)\n\nprint('respect priority ratio: counts:', repr(count))\n\nwhile True:\n    try:\n        val = pq.get()\n    except k3priorityqueue.Empty as e:\n        break\n    count[val] = count.get(val, 0) + 1\n    print(val)\n\nprint('consumed all: counts:', repr(count))\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3",
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3priorityqueue',
    keywords=['python', 'priorityqueue'],
    python_requires='>=3.0',

    install_requires=['k3ut>=0.1.15,<0.2', 'k3heap>=0.1.5,<0.2', 'k3thread>=0.1.0,<0.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
