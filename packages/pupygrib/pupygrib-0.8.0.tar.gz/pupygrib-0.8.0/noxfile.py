"""Nox configuration for pupygrib."""

import glob
import os
import sys

import nox
from nox.command import CommandFailed

nox.options.sessions = [
    "format",
    "imports",
    "lint",
    "manifest",
    "typing",
    "doctest",
    "unittest",
    "coverage",
]

python_sources = ["noxfile.py", "src/pupygrib", "setup.py", "tests"]
numpy_versions = {
    (3, 7): [
        "1.15.4",
        "1.16.6",
        "1.17.5",
        "1.18.5",
        "1.19.5",
        "1.20.3",
        "1.21.0",
    ],
    (3, 8): [
        "1.17.5",
        "1.18.5",
        "1.19.5",
        "1.20.3",
        "1.21.0",
    ],
    (3, 9): [
        "1.19.5",
        "1.20.3",
        "1.21.0",
    ],
}
latest_numpy_version = numpy_versions[sys.version_info[:2]][-1]


@nox.session
def requirements(session: nox.Session) -> None:
    """Compile all requirement files"""
    session.install("pip-tools")

    def pipcompile(outputfile: str, *inputfiles: str) -> None:
        session.run(
            "pip-compile",
            "--quiet",
            "--allow-unsafe",
            "--output-file",
            outputfile,
            *inputfiles,
            *session.posargs,
            env={"CUSTOM_COMPILE_COMMAND": "nox -s requirements"},
        )

    pipcompile("requirements/test.txt", "requirements/test.in")
    pipcompile("requirements/typing.txt", "requirements/typing.in")
    pipcompile("requirements/dev.txt", "requirements/dev.in")
    pipcompile("requirements/ci.txt", "requirements/ci.in")


@nox.session
def format(session: nox.Session) -> None:
    """Check the source code format with Black"""
    session.install("black ~= 21.6b0")
    session.run("black", "--check", "--quiet", *python_sources)


@nox.session
def imports(session: nox.Session) -> None:
    """Check the source code imports with isort"""
    session.install("isort ~= 5.9.2")
    session.run("isort", "--check", *python_sources)


@nox.session
def lint(session: nox.Session) -> None:
    """Check the source code with flake8"""
    session.install("flake8 ~= 3.9.2")
    session.run("flake8", *python_sources)


@nox.session
def manifest(session: nox.Session) -> None:
    """Check that the MANIFEST.in is up-to-date"""
    session.install("check-manifest ~= 0.46")
    session.run("check-manifest")


@nox.session
def typing(session: nox.Session) -> None:
    """Run a static type check with mypy"""
    session.install("-r", "requirements/typing.txt")
    session.install(f"numpy ~= {latest_numpy_version}")
    session.install("-e", ".")
    if sys.version_info < (3, 8):
        session.run("mypy", "--allow-untyped-calls", *python_sources)
    else:
        session.run("mypy", *python_sources)


@nox.session
def doctest(session: nox.Session) -> None:
    """Check the code examples in the documentation"""
    session.install("-r", "requirements/test.txt")
    session.install(f"numpy ~= {latest_numpy_version}")
    session.install("-e", ".")
    session.run("pytest", "--doctest-glob=*.md", *glob.glob("*.md"))


@nox.session
def coverage(session: nox.Session) -> None:
    """Check unit test coverage"""
    session.install("-r", "requirements/test.txt")
    session.install(f"numpy ~= {latest_numpy_version}")
    session.install("-e", ".")
    session.run("pytest", "--cov=pupygrib", "tests", *session.posargs)


def get_junit_prefix(numpy: str) -> str:
    pyversion = f"py{sys.version_info.major}{sys.version_info.minor}"
    npversion = f"np{''.join(numpy.split('.')[:2])}"
    return f"tests_{pyversion}_{npversion}"


@nox.session
@nox.parametrize("numpy", numpy_versions[sys.version_info[:2]])
def unittest(session: nox.Session, numpy: str) -> None:
    """Run the unit tests"""
    session.install("-r", "requirements/test.txt")
    try:
        session.install("--only-binary", "numpy", f"numpy ~= {numpy}")
    except CommandFailed:
        session.skip("No numpy wheel for this python version")
    if "CI" in os.environ:
        session.install("--find-links", "dist", "--no-deps", "--pre", "pupygrib")
        junitprefix = get_junit_prefix(numpy)
        ciargs = ["--junit-xml", f"{junitprefix}.xml", "--junit-prefix", junitprefix]
    else:
        session.install("-e", ".")
        ciargs = []
    session.run("pytest", "tests", *ciargs, *session.posargs)
