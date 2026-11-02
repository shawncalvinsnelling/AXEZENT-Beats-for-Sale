# AXEZENT self-hosted beat player. Python standard library only.
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 AXEZENT_PREVIEW_DIR=/private
WORKDIR /srv/axezent
COPY index.html .
COPY assets ./assets
COPY data ./data
COPY server ./server
USER 65532:65532
EXPOSE 8080
CMD ["python", "server/axezent_site.py", "--host", "0.0.0.0", "--port", "8080"]
