# InteractionSimulator
Simulator for the INTERACTION dataset

## Installation

### Dependencies

Install requirements with pip

```
pip install -r requirements.txt
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### Dataset

The INTERACTION dataset contains a two folders which should be copied into a folder called ``./datasets``: 
  - the contents of ``recorded_trackfiles`` should be copied to ``./datasets/trackfiles``
  - the contents of ``maps`` should be copied to ``./datasets/maps``

### Tests

``python tests/test_idm_graph.py`` should generate a 300-timeframe-long simulation video, `idm_graph.mp4`, with an IDM policy and ClosestObstacle graph.

If issues with ffmpeg and using Conda to manage environment, can resolve with ``conda install -c conda-forge ffmpeg``
