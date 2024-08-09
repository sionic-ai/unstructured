"""
setup.py

unstructured - pre-processing tools for unstructured data

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
        req for req in requirements if not req.startswith("#") and not req.startswith("-")
    ]
    return requirements

def load_all_requirements():
    all_files = [
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
        "requirements/extra-paddleocr.in",
        "requirements/huggingface.in",
        "requirements/ingest/airtable.in",
        "requirements/ingest/astra.in",
        "requirements/ingest/azure.in",
        "requirements/ingest/azure-cognitive-search.in",
        "requirements/ingest/biomed.in",
        "requirements/ingest/box.in",
        "requirements/ingest/chroma.in",
        "requirements/ingest/clarifai.in",
        "requirements/ingest/confluence.in",
        "requirements/ingest/delta-table.in",
        "requirements/ingest/discord.in",
        "requirements/ingest/dropbox.in",
        "requirements/ingest/elasticsearch.in",
        "requirements/ingest/gcs.in",
        "requirements/ingest/github.in",
        "requirements/ingest/gitlab.in",
        "requirements/ingest/google-drive.in",
        "requirements/ingest/hubspot.in",
        "requirements/ingest/jira.in",
        "requirements/ingest/kafka.in",
        "requirements/ingest/mongodb.in",
        "requirements/ingest/notion.in",
        "requirements/ingest/onedrive.in",
        "requirements/ingest/opensearch.in",
        "requirements/ingest/outlook.in",
        "requirements/ingest/pinecone.in",
        "requirements/ingest/postgres.in",
        "requirements/ingest/qdrant.in",
        "requirements/ingest/reddit.in",
        "requirements/ingest/s3.in",
        "requirements/ingest/sharepoint.in",
        "requirements/ingest/salesforce.in",
        "requirements/ingest/sftp.in",
        "requirements/ingest/slack.in",
        "requirements/ingest/wikipedia.in",
        "requirements/ingest/weaviate.in",
        "requirements/ingest/embed-huggingface.in",
        "requirements/ingest/embed-octoai.in",
        "requirements/ingest/embed-vertexai.in",
        "requirements/ingest/embed-voyageai.in",
        "requirements/ingest/embed-openai.in",
        "requirements/ingest/embed-aws-bedrock.in",
        "requirements/ingest/databricks-volumes.in",
    ]
    return load_requirements(all_files)


setup(
    name="unstructured-cpu",
    description="A library that prepares raw documents for downstream ML tasks.",
    long_description=open("README.md", encoding="utf-8").read(),  # noqa: SIM115
    long_description_content_type="text/markdown",
    keywords="NLP PDF HTML CV XML parsing preprocessing",
    url="https://github.com/Unstructured-IO/unstructured",
    python_requires=">=3.9.0,<3.13",
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
    author="Unstructured Technologies",
    author_email="devops@unstructuredai.io",
    license="Apache-2.0",
    packages=find_packages(),
    version=__version__,
    entry_points={
        "console_scripts": ["unstructured-ingest=unstructured.ingest.main:main"],
    },
    install_requires=load_all_requirements(),
    package_dir={"unstructured": "unstructured"},
    package_data={"unstructured": ["nlp/*.txt", "py.typed"]},
)
