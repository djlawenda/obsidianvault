---
type: "Concept"
hub: "[[Hubs/Control_Plane]]"
tags: [concept, node_controller]
---
# Node Controller

A Kubernetes control plane component that manages various aspects of nodes, including assigning CIDR blocks, monitoring node health, and initiating pod evictions when nodes become unhealthy or unreachable.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   The node controller is a Kubernetes control plane component that manages various aspects of nodes.

*   The node controller has multiple roles in a node's life. The first is assigning a CIDR block to the node when it is registered (if CIDR assignment is turned on).

*   The second is keeping the node controller's internal list of nodes up to date with the cloud provider's list of available machines. When running in a cloud environment and whenever a node is unhealthy, the node controller asks the cloud provider if the VM for that node is still available. If not, the node controller deletes the node from its list of nodes.

*   The third is monitoring the nodes' health. The node controller is responsible for: In the case that a node becomes unreachable, updating the `Ready` condition in the Node's `.status` field. In this case the node controller sets the `Ready` condition to `Unknown`. If a node remains unreachable: triggering API-initiated eviction for all of the Pods on the unreachable node.

*   By default, the node controller waits 5 minutes between marking the node as `Unknown` and submitting the first eviction request.

*   By default, the node controller checks the state of each node every 5 seconds. This period can be configured using the `--node-monitor-period` flag on the `kube-controller-manager` component.

*   In most cases, the node controller limits the eviction rate to `--node-eviction-rate` (default 0.1) per second, meaning it won't evict pods from more than 1 node per 10 seconds.

*   The node eviction behavior changes when a node in a given availability zone becomes unhealthy.

*   The node controller is also responsible for evicting pods running on nodes with `NoExecute` taints, unless those pods tolerate that taint.



## Further Reading

> Core Node: [[Projects/Second_Brain]]