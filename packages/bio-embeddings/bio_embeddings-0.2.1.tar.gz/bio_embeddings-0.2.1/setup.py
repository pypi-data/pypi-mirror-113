# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bio_embeddings',
 'bio_embeddings.align',
 'bio_embeddings.embed',
 'bio_embeddings.extract',
 'bio_embeddings.extract.annotations',
 'bio_embeddings.extract.basic',
 'bio_embeddings.extract.light_attention',
 'bio_embeddings.mutagenesis',
 'bio_embeddings.project',
 'bio_embeddings.utilities',
 'bio_embeddings.utilities.filemanagers',
 'bio_embeddings.visualize']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'atomicwrites>=1.4.0,<2.0.0',
 'biopython>=1.76,<2.0',
 'gensim>=3.8.2,<4.0.0',
 'h5py>=3.2.1,<4.0.0',
 'humanize>=3.2.0,<4.0.0',
 'importlib_metadata>=1.7.0,<2.0.0',
 'lock>=2018.3.25,<2019.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.3,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'plotly>=4.6.0,<5.0.0',
 'python-slugify>=4.0.1,<5.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'scikit-learn>=0.24.0,<0.25.0',
 'scipy>=1.4.1,<2.0.0',
 'torch>=1.8.0,<=1.10.0',
 'tqdm>=4.45.0,<5.0.0',
 'umap-learn>=0.5.1,<0.6.0']

extras_require = \
{'all': ['bio-embeddings-cpcprot==0.0.1',
         'bio-embeddings-tape-proteins==0.5',
         'bio-embeddings-plus==0.1.1',
         'bio-embeddings-bepler==0.0.1',
         'bio-embeddings-allennlp==0.9.2',
         'bio-embeddings-deepblast==0.1.0',
         'transformers>=4.5.0,<5.0.0',
         'jax-unirep>=1.0.0,<2.0.0',
         'fair-esm==0.3.1'],
 'bepler': ['bio-embeddings-bepler==0.0.1'],
 'cpcprot': ['bio-embeddings-cpcprot==0.0.1',
             'bio-embeddings-tape-proteins==0.5'],
 'deepblast': ['bio-embeddings-deepblast==0.1.0', 'fsspec==0.8.5'],
 'esm': ['fair-esm==0.3.1'],
 'plus': ['bio-embeddings-plus==0.1.1'],
 'seqvec': ['bio-embeddings-allennlp==0.9.2'],
 'transformers': ['transformers>=4.5.0,<5.0.0'],
 'unirep': ['jax-unirep>=1.0.0,<2.0.0', 'jaxlib==0.1.57'],
 'webserver': ['pymongo>=3.11.2,<4.0.0',
               'sentry-sdk[flask]>=1.0.0,<2.0.0',
               'flask>=1.0.0,<2.0.0']}

entry_points = \
{'console_scripts': ['bio_embeddings = bio_embeddings.utilities.cli:main']}

setup_kwargs = {
    'name': 'bio-embeddings',
    'version': '0.2.1',
    'description': 'A pipeline for protein embedding generation and visualization',
    'long_description': '<p align="center">\n  <a href="https://chat.bioembeddings.com/">\n    <img src="https://chat.bioembeddings.com/api/v1/shield.svg?type=online&name=chat&icon=false" />\n  </a>\n</p>\n\n# Bio Embeddings\nResources to learn about bio_embeddings:\n\n- Quickly predict protein structure and function from sequence via embeddings: [embed.protein.properties](https://embed.protein.properties).\n- Read the current documentation: [docs.bioembeddings.com](https://docs.bioembeddings.com).\n- Chat with us: [chat.bioembeddings.com](https://chat.bioembeddings.com).\n- We presented the bio_embeddings pipeline as a talk at ISMB 2020 & LMRL 2020. You can [find the talk on YouTube](https://www.youtube.com/watch?v=NucUA0QiOe0&feature=youtu.be), [the poster on F1000](https://f1000research.com/posters/9-876), and our [Current Protocol Manuscript](https://doi.org/10.1002/cpz1.113).\n- Check out the [`examples`](examples) of pipeline configurations a and [`notebooks`](notebooks).\n\nProject aims:\n\n  - Facilitate the use of language model based biological sequence representations for transfer-learning by providing a single, consistent interface and close-to-zero-friction\n  - Reproducible workflows\n  - Depth of representation (different models from different labs trained on different dataset for different purposes)\n  - Extensive examples, handle complexity for users (e.g. CUDA OOM abstraction) and well documented warnings and error messages.\n\nThe project includes:\n\n- General purpose python embedders based on open models trained on biological sequence representations (SeqVec, ProtTrans, UniRep,...)\n- A pipeline which:\n  - embeds sequences into matrix-representations (per-amino-acid) or vector-representations (per-sequence) that can be used to train learning models or for analytical purposes\n  - projects per-sequence embedidngs into lower dimensional representations using UMAP or t-SNE (for lightwieght data handling and visualizations)\n  - visualizes low dimensional sets of per-sequence embeddings onto 2D and 3D interactive plots (with and without annotations)\n  - extracts annotations from per-sequence and per-amino-acid embeddings using supervised (when available) and unsupervised approaches (e.g. by network analysis)\n- A webserver that wraps the pipeline into a distributed API for scalable and consistent workfolws\n\n## Installation\n\nYou can install `bio_embeddings` via pip or use it via docker.\n\n### Pip\n\nInstall the pipeline like so:\n\n```bash\npip install bio-embeddings[all]\n```\n\nTo install the unstable version, please install the pipeline like so:\n\n```bash\npip install -U "bio-embeddings[all] @ git+https://github.com/sacdallago/bio_embeddings.git"\n```\n\n### Docker\n\nWe provide a docker image at `ghcr.io/bioembeddings/bio_embeddings`. Simple usage example:\n\n```shell_script\ndocker run --rm --gpus all \\\n    -v "$(pwd)/examples/docker":/mnt \\\n    -v bio_embeddings_weights_cache:/root/.cache/bio_embeddings \\\n    -u $(id -u ${USER}):$(id -g ${USER}) \\\n    ghcr.io/bioembeddings/bio_embeddings:v0.1.6 /mnt/config.yml\n```\n\nSee the [`docker`](examples/docker) example in the [`examples`](examples) folder for instructions. You can also use `ghcr.io/bioembeddings/bio_embeddings:latest` which is built from the latest commit.\n\n### Installation notes\n\n`bio_embeddings` was developed for unix machines with GPU capabilities and [CUDA](https://developer.nvidia.com/cuda-zone) installed. If your setup diverges from this, you may encounter some inconsistencies (e.g. speed is significantly affected by the absence of a GPU and CUDA). For Windows users, we strongly recommend the use of [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10).\n\n\n## What model is right for you?\n\nEach models has its strengths and weaknesses (speed, specificity, memory footprint...). There isn\'t a "one-fits-all" and we encourage you to at least try two different models when attempting a new exploratory project.\n\nThe models `prottrans_bert_bfd`, `prottrans_albert_bfd`, `seqvec` and `prottrans_xlnet_uniref100` were all trained with the goal of systematic predictions. From this pool, we believe the optimal model to be `prottrans_bert_bfd`, followed by `seqvec`, which has been established for longer and uses a different principle (LSTM vs Transformer).\n\n## Usage and examples\n\nWe highly recommend you to check out the [`examples`](examples) folder for pipeline examples, and the [`notebooks`](notebooks) folder for post-processing pipeline runs and general purpose use of the embedders.\n\nAfter having installed the package, you can:\n\n1. Use the pipeline like:\n\n    ```bash\n    bio_embeddings config.yml\n    ```\n\n    [A blueprint of the configuration file](examples/parameters_blueprint.yml), and an example setup can be found in the [`examples`](examples) directory of this repository.\n\n1. Use the general purpose embedder objects via python, e.g.:\n\n    ```python\n    from bio_embeddings.embed import SeqVecEmbedder\n\n    embedder = SeqVecEmbedder()\n\n    embedding = embedder.embed("SEQVENCE")\n    ```\n\n    More examples can be found in the [`notebooks`](notebooks) folder of this repository.\n    \n## Cite\n\nIf you use `bio_embeddings` for your research, we would appreciate it if you could cite the following paper:\n\n> Dallago, C., Schütze, K., Heinzinger, M., Olenyi, T., Littmann, M., Lu, A. X., Yang, K. K., Min, S., Yoon, S., Morton, J. T., & Rost, B. (2021). Learned embeddings from deep learning to visualize and predict protein sets. Current Protocols, 1, e113. doi: [10.1002/cpz1.113](https://doi.org/10.1002/cpz1.113)\n\n\nThe corresponding bibtex:\n```\n@article{https://doi.org/10.1002/cpz1.113,\nauthor = {Dallago, Christian and Schütze, Konstantin and Heinzinger, Michael and Olenyi, Tobias and Littmann, Maria and Lu, Amy X. and Yang, Kevin K. and Min, Seonwoo and Yoon, Sungroh and Morton, James T. and Rost, Burkhard},\ntitle = {Learned Embeddings from Deep Learning to Visualize and Predict Protein Sets},\njournal = {Current Protocols},\nvolume = {1},\nnumber = {5},\npages = {e113},\nkeywords = {deep learning embeddings, machine learning, protein annotation pipeline, protein representations, protein visualization},\ndoi = {https://doi.org/10.1002/cpz1.113},\nurl = {https://currentprotocols.onlinelibrary.wiley.com/doi/abs/10.1002/cpz1.113},\neprint = {https://currentprotocols.onlinelibrary.wiley.com/doi/pdf/10.1002/cpz1.113},\nyear = {2021}\n}\n\nAdditionally, we invite you to cite the work from others that was collected in `bio_embeddings` (see section _"Tools by category"_ below). We are working on an enhanced user guide which will include proper references to all citable work collected in `bio_embeddings`.\n\n```\n\n## Contributors\n\n- Christian Dallago (lead)\n- Konstantin Schütze\n- Tobias Olenyi\n- Michael Heinzinger\n\n## Non-exhaustive list of tools available (see following section for more details):\n\n- Fastext\n- Glove\n- Word2Vec\n- SeqVec (https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3220-8)\n  - SeqVecSec and SeqVecLoc for secondary structure and subcellularlocalization prediction\n- ProtTrans (ProtBert, ProtAlbert, ProtT5) (https://doi.org/10.1101/2020.07.12.199554)\n  - ProtBertSec and ProtBertLoc for secondary structure and subcellular localization prediction\n- UniRep (https://www.nature.com/articles/s41592-019-0598-1)\n- ESM/ESM1b (https://www.biorxiv.org/content/10.1101/622803v3)\n- PLUS (https://github.com/mswzeus/PLUS/)\n- CPCProt (https://www.biorxiv.org/content/10.1101/2020.09.04.283929v1.full.pdf)\n- PB-Tucker (https://www.biorxiv.org/content/10.1101/2021.01.21.427551v1)\n- GoPredSim (https://www.nature.com/articles/s41598-020-80786-0)\n- DeepBlast (https://www.biorxiv.org/content/10.1101/2020.11.03.365932v1)\n\n## Datasets \n\n- `prottrans_t5_xl_u50` residue and sequence embeddings of the Human proteome at full precision + secondary structure predictions + sub-cellular localisation predictions: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5047020.svg)](https://doi.org/10.5281/zenodo.5047020)\n\n----\n\n## Tools by category\n\n\n<details>\n<summary>Pipeline</summary>\n<br>\n\n- align:\n  - DeepBlast (https://www.biorxiv.org/content/10.1101/2020.11.03.365932v1)\n- embed:\n  - ProtTrans BERT trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n  - SeqVec (https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3220-8)\n  - ProtTrans ALBERT trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n  - ProtTrans XLNet trained on UniRef100 (https://doi.org/10.1101/2020.07.12.199554)\n  - ProtTrans T5 trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n  - ProtTrans T5 trained on BFD and fine-tuned on UniRef50 (in-house)\n  - UniRep (https://www.nature.com/articles/s41592-019-0598-1)\n  - ESM/ESM1b (https://www.biorxiv.org/content/10.1101/622803v3)\n  - PLUS (https://github.com/mswzeus/PLUS/)\n  - CPCProt (https://www.biorxiv.org/content/10.1101/2020.09.04.283929v1.full.pdf)\n- project:\n  - t-SNE\n  - UMAP\n  - PB-Tucker (https://www.biorxiv.org/content/10.1101/2021.01.21.427551v1)\n- visualize:\n  - 2D/3D sequence embedding space\n- extract:\n  - supervised:\n    - SeqVec: DSSP3, DSSP8, disorder, subcellular location and membrane boundness as in https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3220-8\n    - ProtBertSec and ProtBertLoc as reported in https://doi.org/10.1101/2020.07.12.199554\n  - unsupervised:\n    - via sequence-level (reduced_embeddings), pairwise distance (euclidean like [goPredSim](https://github.com/Rostlab/goPredSim), more options available, e.g. cosine)\n</details>\n\n<details>\n<summary>General purpose embedders</summary>\n<br>\n\n- ProtTrans BERT trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n- SeqVec (https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3220-8)\n- ProtTrans ALBERT trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n- ProtTrans XLNet trained on UniRef100 (https://doi.org/10.1101/2020.07.12.199554)\n- ProtTrans T5 trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n- ProtTrans T5 trained on BFD + fine-tuned on UniRef50 (https://doi.org/10.1101/2020.07.12.199554)\n- Fastext\n- Glove\n- Word2Vec\n- UniRep (https://www.nature.com/articles/s41592-019-0598-1)\n- ESM/ESM1b (https://www.biorxiv.org/content/10.1101/622803v3)\n- PLUS (https://github.com/mswzeus/PLUS/)\n- CPCProt (https://www.biorxiv.org/content/10.1101/2020.09.04.283929v1.full.pdf)\n</details>\n',
    'author': 'Christian Dallago',
    'author_email': 'christian.dallago@tum.de',
    'maintainer': 'Rostlab',
    'maintainer_email': 'admin@rostlab.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
