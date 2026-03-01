---
type: "Concept"
hub: "[[Hubs/Kubernetes]]"
tags: [concept, labels]
---
# Labels

Key-value pairs attached to Kubernetes objects, such as Nodes or Pods. Labels are used to organize and select subsets of objects based on criteria.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Nodes.md]] (Added on 2026-03-01 16:43)

*   `--node-labels` - to add when registering the node in the cluster (see label restrictions enforced by the [NodeRestriction admission plugin](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#noderestriction)).

*   For example, if you try to create a Node from the following JSON manifest: `{"kind": "Node", "apiVersion": "v1", "metadata": {"name": "10.240.79.157", "labels": {"name": "my-first-k8s-node"}}}`

*   You can modify Node objects regardless of the setting of `--register-node`. For example, you can set labels on an existing Node or mark it unschedulable.

*   You can set optional node role(s) for nodes by adding one or more `node-role.kubernetes.io/<role>: <role>` labels to the node where characters of `<role>` are limited by the [syntax](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set) rules for labels.

*   Kubernetes ignores the label value for node roles; by convention, you can set it to the same string you used for the node role in the label key.

*   You can use labels on Nodes in conjunction with node selectors on Pods to control scheduling. For example, you can constrain a Pod to only be eligible to run on a subset of the available nodes.



## Further Reading

> Core Node: [[Projects/Second_Brain]]