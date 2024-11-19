# Use Python 3.12 base image
FROM python:3.12

# Set Python to unbuffered mode
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app/

# Install uv
# Reference: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.4.29 /uv /bin/uv

# Place executables in the environment at the front of the path
# Reference: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
# Reference: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Reference: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Copy configuration files
COPY ./pyproject.toml ./uv.lock ./README.md /app/

# Install dependencies
# Reference: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Set the Python path
ENV PYTHONPATH=/app

# Copy application code
COPY ./app /app/app

# COPY environment variables
COPY .env /app

# Sync the project dependencies
# Reference: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Expose port 8080
EXPOSE 8080  

# Start FastAPI with uvicorn and set to use 4 workers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
