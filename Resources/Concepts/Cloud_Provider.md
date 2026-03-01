---
type: "Concept"
hub: "[[Hubs/Kubernetes]]"
tags: [concept, cloud_provider]
---
# Cloud Provider

An interface or integration point that allows Kubernetes to interact with cloud service providers to manage underlying infrastructure resources, such as virtual machines or load balancers.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   `--cloud-provider` - How to talk to a to read metadata about itself.

*   When running in a cloud environment and whenever a node is unhealthy, the node controller asks the cloud provider if the VM for that node is still available. If not, the node controller deletes the node from its list of nodes.

*   If your cluster does not span multiple cloud provider availability zones, then the eviction mechanism does not take per-zone unavailability into account.



## Further Reading

> Core Node: [[Projects/Second_Brain]]