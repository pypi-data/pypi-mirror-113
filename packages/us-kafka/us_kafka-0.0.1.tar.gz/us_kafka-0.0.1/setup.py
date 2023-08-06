from setuptools import setup, find_packages


def get_version():
    with open('version') as version_file:
        return version_file.read().strip()


def get_requirements():
    with open('requirements.txt') as requirement_file:
        return [package.strip() for package in requirement_file if package.strip()]


setup(
    name="us_kafka",
    version=get_version(),
    author="Ukuspeed",
    author_email="info@ukuspeed.gmail.com",
    description="Wrapper around confluent-kafka for ukuspeed services",
    url="https://github.com/ukuspeed/us-kafka",
    packages=find_packages(exclude='us-kafka'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=get_requirements()
)
