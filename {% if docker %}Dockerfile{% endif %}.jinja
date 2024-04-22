FROM debian:12.5 as base
RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install --no-install-recommends -yq python3 python3-pip git python3-venv python3-dev

WORKDIR /app
RUN python3 -m venv .venv
ENV PYTHONPATH=/app/.venv/lib
ENV PATH=/app/.venv/bin:$PATH
COPY ./pyproject.toml .
RUN pip install -e .


FROM base
COPY src src
COPY entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]
