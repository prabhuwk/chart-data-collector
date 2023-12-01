FROM python:3.11.6-slim-bookworm

COPY . /app/
RUN useradd -m trader && chown -R trader:trader /app/
USER trader
WORKDIR /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
CMD ["bash"]
