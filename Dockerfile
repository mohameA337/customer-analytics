FROM python:3.11-slim

RUN pip install --default-timeout=100 --no-cache-dir "pandas<2.3" "numpy<2" "matplotlib<3.9" "seaborn" "scikit-learn<1.5" "scipy" "requests"

WORKDIR /app/pipeline/

COPY . /app/pipeline/

CMD ["/bin/bash"]
