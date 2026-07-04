# this file is *not* meant to cover or endorse the use of nox or pytest or
# testing in general,
#
#  It's meant to show the use of:
#
#  - check-manifest
#     confirm items checked into vcs are in your sdist
#  - readme_renderer (when using a reStructuredText README)
#     confirms your long_description will render correctly on PyPI.
#
#  and also to help confirm pull requests to this project.

import nox
import os

nox.options.sessions = ["lint"]

# Define the minimal nox version required to run
nox.needs_version = ">= 2024.3.2"


@nox.session
def lint(session):
    session.install("flake8")
    session.run(
        "flake8", "--exclude", ".nox,*.egg,build,data",
        "--select", "E,W,F", "."
    )


@nox.session
def build_and_check_dists(session):
    session.install("build", "check-manifest >= 0.42", "twine")

    session.run("check-manifest", "--ignore", "jsonata/**,noxfile.py,tests/**")
    session.run("python", "-m", "build")
    session.run("python", "-m", "twine", "check", "dist/*")


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"])
def tests(session):
    session.install("pytest")
    session.install("pytest-asyncio")
    build_and_check_dists(session)

    generated_files = os.listdir("dist/")
    generated_sdist = os.path.join("dist/", generated_files[1])

    session.install(generated_sdist)

    session.run("python", "tests/generate.py")
    session.run("py.test", "tests/", *session.posargs)


# Exercises the optional pluggable regex_engine hook against Google's RE2
# (tests/re2_engine_test.py). Kept as its own session so the main `tests`
# session -- and the package itself -- stay free of a google-re2 dependency;
# this one opts in explicitly.
@nox.session
def test_re2(session):
    session.install("pytest")
    session.install("google-re2")
    build_and_check_dists(session)

    generated_files = os.listdir("dist/")
    sdists = sorted(f for f in generated_files if f.endswith(".tar.gz"))
    if not sdists:
        session.error("No sdist (.tar.gz) found in dist/")
    generated_sdist = os.path.join("dist/", sdists[0])

    session.install(generated_sdist)

    session.run("py.test", "tests/re2_engine_test.py", *session.posargs)
