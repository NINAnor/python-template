FROM rust:1.74-slim-bookworm AS base


FROM base as builder
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    musl-tools
ENV ARC="x86_64-unknown-linux-musl"
RUN rustup target add "${ARC}"
ARG MDBOOK_VERSION=0.4.36
RUN cargo install mdbook --version "${MDBOOK_VERSION}" --target "${ARC}"


FROM base as dev
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    musl-tools libssl-dev pkg-config
RUN cargo install mdbook-kroki-preprocessor
COPY --from=builder /usr/local/cargo/bin/mdbook /usr/local/bin/mdbook
WORKDIR /book
ENTRYPOINT [ "/usr/local/bin/mdbook" ]


FROM dev as build
ARG KROKI_ENDPOINT="https://kroki.io/"
ENV MDBOOK_PREPROCESSOR__KROKI_PREPROCESSOR__ENDPOINT="${KROKI_ENDPOINT}"
COPY src src
COPY theme theme
COPY book.toml .
RUN mdbook build


FROM nginx as prod
COPY --from=build /book/book/ /var/www/
COPY default.conf.template /etc/nginx/templates/
