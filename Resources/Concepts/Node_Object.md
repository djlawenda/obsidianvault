---
type: "Concept"
hub: "[[Hubs/Kubernetes]]"
tags: [concept, node_object]
---
# Node Object

A declarative representation of a Kubernetes node in the API. It contains metadata and specifications about the node, such as its name, labels, and capacity.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   After you create a Node object, or the kubelet on a node self-registers, the control plane checks whether the new Node object is valid.

*   For example, if you try to create a Node from the following JSON manifest: `{"kind": "Node", "apiVersion": "v1", "metadata": {"name": "10.240.79.157", "labels": {"name": "my-first-k8s-node"}}}` Kubernetes creates a Node object internally (the representation).

*   The name identifies a Node. Two Nodes cannot have the same name at the same time. Kubernetes also assumes that a resource with the same name is the same object.

*   If the Node needs to be replaced or updated significantly, the existing Node object needs to be removed from API server first and re-added after the update.

*   You can create and modify Node objects using kubectl.

*   When you want to create Node objects manually, set the kubelet flag `--register-node=false`.

*   You can modify Node objects regardless of the setting of `--register-node`. For example, you can set labels on an existing Node or mark it unschedulable.

*   Node objects track information about the Node's resource capacity: for example, the amount of memory available and the number of CPUs.



## Further Reading

> Core Node: [[Projects/Second_Brain]]