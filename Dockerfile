FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SRC_DIR /usr/bin/src/webapp/src
ENV VIRTUAL_ENV=${SRC_DIR}/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Transfer files
COPY src/modules/* ${SRC_DIR}/modules/
COPY src/tests/* ${SRC_DIR}/tests/
COPY src/pyproject.toml ${SRC_DIR}/pyproject.toml
COPY src/setup.cfg ${SRC_DIR}/setup.cfg
COPY src/requirements-staging.txt ${SRC_DIR}/requirements.txt

# Set environment
WORKDIR ${SRC_DIR}
RUN python3 -m venv $VIRTUAL_ENV

# Install dependencies:
RUN pip install -r requirements.txt

# Tests
WORKDIR ${SRC_DIR}
RUN python3 -m unittest
RUN pytest

# RUN
CMD ["uvicorn", "endpoints:app", "--app-dir=/usr/bin/src/webapp/src/modules", "--reload", "--host", "0.0.0.0", "--port", "80"]