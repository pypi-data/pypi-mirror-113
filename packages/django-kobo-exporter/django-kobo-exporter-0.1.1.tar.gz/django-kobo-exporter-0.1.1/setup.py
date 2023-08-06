from setuptools import find_packages, setup

setup(
    name="django-kobo-exporter",
    version="0.1.1",
    description="prometheus exporter for kobo hub",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/release-engineering/django-kobo-exporter",
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=["django", "prometheus-client", "kobo"],
    python_requires=">2.6",
    project_urls={
        "Changelog": "https://github.com/release-engineering/django-kobo-exporter/blob/master/CHANGELOG.md",
    },
)
