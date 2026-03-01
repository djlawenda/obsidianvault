---
type: "Technology"
concept: "[[Concepts/Node_Agent]]"
tags: [technology, kubelet]
---
# kubelet

An agent that runs on each node in the cluster, taking PodSpecs and ensuring that the described containers are running and healthy.

## Excerpts & Key Information


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)

*   An agent that runs on each in the cluster. It makes sure that are running in a .

*   The kubelet takes a set of PodSpecs that are provided through various mechanisms and ensures that the containers described in those PodSpecs are running and healthy. The kubelet doesn't manage containers which were not created by Kubernetes.



## Further Reading

### Source
*   Original reference: [[Processed_Transcripts/Cluster Architecture.md]]

> Core Node: [[Projects/Second_Brain]]