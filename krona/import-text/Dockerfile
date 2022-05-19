FROM conda/miniconda3
RUN conda update -n base -c defaults conda
WORKDIR /batchx
RUN conda install -c bioconda krona
RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential python3 python3-pandas && apt-get autoremove
RUN apt-get install -y curl && apt-get autoremove
RUN /usr/local/bin/ktUpdateTaxonomy.sh
COPY import-text.py .
RUN chmod -R 777 /batchx/import-text.py
ENTRYPOINT /batchx/import-text.py
LABEL io.batchx.manifest=09
COPY manifest /batchx/manifest/
