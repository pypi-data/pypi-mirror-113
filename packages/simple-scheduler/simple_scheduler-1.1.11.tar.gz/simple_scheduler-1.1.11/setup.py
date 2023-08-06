"""
    reference: https://pythonhosted.org/an_example_pypi_project/setuptools.html
"""

import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
print(HERE)
README = (HERE / "README.md").read_text()
setup(
    name="simple_scheduler",
    version="1.1.11",
    description="Easily schedule multiple events and recurring tasks (simultaneously in background).",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Vernal-Inertia/simple_scheduler",
    author="Vernal Inertia",
    author_email="tanveer2407@gmail.com",
    license="MIT",
    keywords='python, schedule, simple, scheduler, jobs, tasks, easy',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha"
    ],
    packages=["simple_scheduler"],
    include_package_data=True,
    install_requires=["multiprocess","pytz"],
    python_requires='>=3',
    project_urls={
        'Examples':'https://github.com/Vernal-Inertia/simple_scheduler/tree/main/examples',
        'Issues': 'https://github.com/Vernal-Inertia/simple_scheduler/issues',
        'Documentation': 'https://github.com/Vernal-Inertia/simple_scheduler/blob/main/README.md',
        'Source': 'https://github.com/Vernal-Inertia/simple_scheduler'}
)
