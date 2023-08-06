from setuptools import find_packages, setup

setup(
    name="django-kobo-exporter",
    version="0.1.0",
    description="prometheus exporter for kobo hub",
    url="https://github.com/release-engineering/django-kobo-exporter",
    license="GPLv3",
    packages=find_packages(exclude=["tests"]),
    install_requires=["django", "prometheus-client", "kobo"],
    python_requires=">2.6",
)
