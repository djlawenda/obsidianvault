---
type: "Hub"
tags: [hub, control_plane]
---
# Control Plane

The control plane makes global decisions about the cluster, such as scheduling, and detects and responds to cluster events.

## Concepts
- 

- [[Concepts/Kubernetes_Api]]
- [[Concepts/Key_Value_Store]]
- [[Concepts/Scheduler]]
- [[Concepts/Controller]]
- [[Concepts/Api_Server]]
- [[Concepts/Node_Controller]]
## Excerpts & Key Information


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   Each node is managed by the control plane and contains the services necessary to run Pods.

*   The kubelet on a node self-registers to the control plane

*   After you create a Node object, or the kubelet on a node self-registers, the control plane checks whether the new Node object is valid.

*   The node controller is a Kubernetes control plane component that manages various aspects of nodes.

*   The node controller's internal list of nodes up to date with the cloud provider's list of available machines.

*   By default, the node controller checks the state of each node every 5 seconds. This period can be configured using the `--node-monitor-period` flag on the `kube-controller-manager` component.

*   If there has been an outage and some nodes reappear, the node controller does evict pods from the remaining nodes that are unhealthy or unreachable).



*   The control plane's components make global decisions about the cluster (for example, scheduling), as well as detecting and responding to cluster events (for example, starting up a new when a Deployment's field is unsatisfied.



## Further Reading

> Core Node: [[Projects/Second_Brain]]