# AWSPy
Utility tools for running Python services in AWS. Note: This package isn't designed to replace
services such as [Boto3](https://github.com/boto/boto3) - the Python AWS SDK.

# Features
## Fargate Backed ECS
- Tooling to extract container metadata, stats, and task information
- [Fargate Readme](https://github.com/ScholarPack/awspy/blob/main/awspy/ecs/README.MD)

# Installation

Install using Pip:

```bash
pip install awspy
```

# Usage

Import the service, then run commands:

```python
from awspy.ecs import Fargate

Fargate().get_container_metadata_v4()
```

Each service is initialised in a common way. You can pass configuration options during
initialisation (and if no options are provided then all options revert to their defaults):

```python
from awspy.ecs import Fargate

Fargate(raise_errors=False, logger=my_logger)
```

The options available for all services are:

|Option|Type|Description|Default|
|------|----|-----------|-------|
|raise_errors|Boolean|Should exceptions bubble up?|True|
|logger|Python logger|A Python logger instance to log information and errors to.|Python logger (`logging.getLogger(__name__)`)|

# Useful Links

AWSPy:

- [PyPi](https://pypi.org/project/awspy/)
- [GitHub](https://github.com/ScholarPack/awspy)
- [Releases](https://github.com/ScholarPack/awspy/releases)

Useful Python AWS Packages

- [Localstack](https://localstack.cloud/)
- [Moto](https://github.com/spulec/moto)
- [Boto3](https://github.com/boto/boto3)
