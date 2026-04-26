# Use Mambaforge as base for efficiency
FROM condaforge/mambaforge:latest

LABEL maintainer="LaBiOmics/UMC Team <fabianomenegidio@umc.br>"
LABEL version="1.0.9"
LABEL description="HumaninFinder: Professional evolutionary discovery tool (Conda-based Container)."

WORKDIR /app

# 1. Copy environment and project files
COPY environment.yml .
COPY . /app

# 2. Create the environment from the official YAML
# We use 'base' or a named env. To keep it simple in Docker, 
# we install into the base environment or activate it.
RUN mamba env update -n base -f environment.yml && \
    mamba clean -afy

# 3. Install the tool as a package
RUN pip install --no-cache-dir .

# 4. PRE-DOWNLOAD MODELS (Bake models into the image)
RUN humanin-finder --setup

# Set entrypoint
ENTRYPOINT ["humanin-finder"]
CMD ["--help"]
