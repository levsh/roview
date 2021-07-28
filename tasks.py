from invoke import task


@task
def run_linter(c):
    cmd = "pipenv run flake8 --filename=roview.py --count --show-source --statistics"
    c.run(cmd)


@task
def run_tests(c):
    cmd = "pipenv run coverage run --source roview -m pytest tests.py && pipenv run coverage report -m"
    c.run(cmd)
