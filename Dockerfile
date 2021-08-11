FROM szabogtamas/jupy_rocker

RUN sudo apt-get update -y && \
    sudo apt-get install -y libxt-dev && \
    sudo apt-get install -y libx11-dev && \
    sudo apt-get install -y libcairo2-dev && \
    sudo apt-get install -y libxml2-dev && \
    sudo apt-get install -y libbz2-dev && \
    sudo apt-get install -y liblzma-dev

RUN pip3 install jupytext && \
    pip3 install numpy && \
    pip3 install pandas && \
    pip3 install matplotlib && \
    pip3 install seaborn && \
    pip3 install scipy && \
    pip3 install scikit-learn && \
    pip3 install umap-learn

ADD ./scripts /usr/local/dev_scripts
ADD ./notebooks /usr/local/notebooks
ADD ./example_data /usr/local/example_data

RUN install2.r --error \
    --deps TRUE \
    devtools \
    rlang \
    optparse \
    docstring \
    plotly \
    heatmaply \
    openxlsx \
    umap \
    tsne

RUN chmod a+rwx -R /home/rstudio
ADD ./configs/rstudio-prefs.json /home/rstudio/.config/rstudio/rstudio-prefs.json