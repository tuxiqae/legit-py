# build stage
FROM python:3.10 AS builder

# install PDM
RUN pip install -U --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY src/ /project/src

# install dependencies and project into the local packages directory
WORKDIR /project
RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable


# run stage
FROM python:3.10

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.10/lib /project/pkgs
COPY --from=builder /project/src /project/src

# set command/entrypoint, adapt to fit your needs
CMD ["python", "-m", "project.src.main"]
