# pylint:skip-file
"""
Wrapper for the functionality for various installation and project setup commands
see:
    `python setup.py help`
for more details
"""
from setuptools import setup, find_packages

setup(name="autoreduce_qp",
      version="22.0.0.dev3",
      description="ISIS Autoreduction queue processor",
      author="ISIS Autoreduction Team",
      url="https://github.com/ISISScientificComputing/autoreduce/",
      install_requires=[
          "autoreduce_utils==22.0.0.dev3", "autoreduce_db==22.0.0.dev5", "Django==3.2.4", "fire==0.4.0",
          "plotly==4.14.3", "stomp.py==6.1.0"
      ],
      packages=find_packages(),
      entry_points={"console_scripts": ["autoreduce-qp-start = autoreduce_qp.queue_processor.queue_listener:main"]},
      classifiers=[
          "Programming Language :: Python :: 3 :: Only",
      ])
