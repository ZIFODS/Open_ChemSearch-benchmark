![image](https://github.com/ZIFODS/Open_ChemSearch-benchmark/assets/122999957/8648f74f-d1f8-4a37-a508-0cbc54571a8b)


# Chemsearch Benchmark
Benchmark of chemsearch running on a cluster.

## Setup

This project is designed to be run as a docker container within the same Kubernetes cluster as the benchmarked chemsearch application.
Use the [Docker file](Dockerfile) to build an image, then push it to the AWS Elastic Container Registry (ECR).
Edit the Kubernetes [manifest file](/k8s/pod.yaml) to reference the stored image:

    ```
    spec:
        containers:
            ...
            image: "XXXXXXXXXX.amazonaws.com/chemsearch-benchmark:latest"
    ```

The stored image can then be used to create a container.

Before creating a container, the AWS Elastic Kubernetes Service (EKS) cluster must be setup as specified in the chemsearch [README](https://github.com/ZIFODS/chemsearch).
Add a new node group to the cluster with 1 node.
This node does not need GPU resources, and should not have other chemsearch pods running on it.
The AWS EC2 instance type m6i.8xlarge is a good option.

The Kubernetes [manifest file](/k8s/pod.yaml) can then be used to deploy the benchmark container to the cluster.
I recommend connecting to the running container using Visual Studio Code with the Kubernetes extension.

Check everything is setup correctly through running the test suite:

```
python -m pytest tests
```

## Usage

With the environment setup complete, it will be possible to run the [benchmark script](/src/chemsearch/scripts/benchmark.py).
It tests all chemsearch applications in the cluster by submitting queries asynchronously to their IP addresses, then aggregating the responses.

**Command Line**

```
benchmark -q path/to/read/queries.smi -l path/to/write/logs.log -n chemsearch.default.svc.cluster.local 
```

| Flag | Type | Description | Required? | Allowed Values | Example Value | Default Value |
| --- | --- | --- | --- | --- | --- | --- |
| -q / --queries | str | SMI file to read query molecules from. | Yes | | path/to/read/molecules.parquet | |
| -l / --log-file | str | File to write logs. | Yes | | path/to/write/logs.log | |
| -n / --dns-name | str | DNS name of service for cluster. | Yes | | chemsearch.default.svc.cluster.local | |
| -f / --format | str | Format of query strings. | No | smarts/ smiles | | smiles |
| -p / --port | int | Port used by containers in cluster. | No | | | 5000 |
| --seed | int | Seed for shuffling queries and runs. | No | | | |

**Expected Output**

The following console output is typical for successful completion of the benchmark script:

```
Querying cluster:
100%|██████████████| 10282/10282 [20:44<00:00, 8.26it/s]
```

![image](https://github.com/ZIFODS/Open_ChemSearch-benchmark/assets/122999957/27a5db15-15e3-4de5-8420-c4e1b6e66cc8)
