FROM python:3.11-slim

RUN pip install --no-cache-dir \
    jupyter \
    sqlalchemy \
    python-dotenv \
    psycopg2-binary==2.9.9 \
    pandas \
    matplotlib \
    seaborn

EXPOSE 8888
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]