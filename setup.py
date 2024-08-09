"""
setup.py

unstructured-cpu - pre-processing tools for unstructured data without GPU dependencies

Copyright 2022 Unstructured Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import List, Optional, Union
from setuptools import find_packages, setup
from unstructured.__version__ import __version__

def load_requirements(file_list: Optional[Union[str, List[str]]] = None) -> List[str]:
    if file_list is None:
        file_list = ["requirements/base.in"]
    if isinstance(file_list, str):
        file_list = [file_list]
    requirements: List[str] = []
    for file in file_list:
        with open(file, encoding="utf-8") as f:
            requirements.extend(f.readlines())
    requirements = [
        req.strip() for req in requirements
        if req.strip() and not req.startswith("#") and not req.startswith("-")
    ]
    return requirements

# Load all requirements
all_requirements = load_requirements([
    "requirements/base.in",
    "requirements/extra-csv.in",
    "requirements/extra-docx.in",
    "requirements/extra-epub.in",
    "requirements/extra-pdf-image.in",
    "requirements/extra-markdown.in",
    "requirements/extra-msg.in",
    "requirements/extra-odt.in",
    "requirements/extra-pandoc.in",
    "requirements/extra-pptx.in",
    "requirements/extra-xlsx.in",
    "requirements/huggingface.in",
    "requirements/extra-paddleocr.in",
])

# Remove duplicates while preserving order
all_requirements = list(dict.fromkeys(all_requirements))

setup(
    name="unstructured-cpu",
    version=__version__,
    description="No more headache on cuda for unstructured data processing",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Sigrid Jin",
    author_email="requirements.jinhyung@gmail.com",
    url="https://github.com/Unstructured-IO/unstructured",
    packages=find_packages(),
    install_requires=all_requirements,
    entry_points={
        "console_scripts": ["unstructured-ingest=unstructured.ingest.main:main"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9.0,<3.13",
    license="Apache-2.0",
    keywords="NLP PDF HTML CV XML parsing preprocessing",
    package_data={"unstructured": ["nlp/*.txt", "py.typed"]},
)