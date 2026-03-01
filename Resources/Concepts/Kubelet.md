---
type: "Concept"
hub: "[[Hubs/Node_Components]]"
tags: [concept, kubelet]
---
# Kubelet

An agent that runs on each node in a Kubernetes cluster. It registers the node with the API server, executes tasks, and manages the lifecycle of Pods and their containers on the node.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   The components on a node include the kubelet, a container runtime, and the kube-proxy.

*   The kubelet on a node self-registers to the control plane

*   Kubernetes checks that a kubelet has registered to the API server that matches the `metadata.name` field of the Node.

*   When the kubelet flag `--register-node` is true (the default), the kubelet will attempt to register itself with the API server. This is the preferred pattern, used by most distros.

*   For self-registration, the kubelet is started with the following options: `--kubeconfig` - Path to credentials to authenticate itself to the API server. `--cloud-provider` - How to talk to a to read metadata about itself. `--register-node` - Automatically register with the API server. `--register-with-taints` - Register the node with the given list of (comma separated `<key>=<value>:<effect>`). No-op if `register-node` is false. `--node-ip` - Optional comma-separated list of the IP addresses for the node. `--node-labels` - to add when registering the node in the cluster. `--node-status-update-frequency` - Specifies how often kubelet posts its node status to the API server.

*   When the Node authorization mode and NodeRestriction admission plugin are enabled, kubelets are only authorized to create/modify their own Node resource.

*   If you have enabled the `TopologyManager` feature gate, then the kubelet can use topology hints when making resource assignment decisions.



## Further Reading

> Core Node: [[Projects/Second_Brain]]