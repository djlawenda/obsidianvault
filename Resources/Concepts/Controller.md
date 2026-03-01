---
type: "Concept"
hub: "[[Hubs/Control_Plane]]"
tags: [concept, controller]
---
# Controller

A control plane component that runs processes, where each process is logically separate but often compiled into a single binary to reduce complexity. Controllers detect and respond to cluster events, bringing the cluster to its desired state.

## Technologies
- 

- [[Technologies/Kube_Controller_Manager]]
- [[Technologies/Cloud_Controller_Manager]]
- [[Technologies/Node_Controller]]
- [[Technologies/Job_Controller]]
- [[Technologies/Endpointslice_Controller]]
- [[Technologies/Serviceaccount_Controller]]
## Excerpts & Key Information


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)

*   Control plane component that runs processes.

*   Logically, each is a separate process, but to reduce complexity, they are all compiled into a single binary and run in a single process.



## Further Reading

> Core Node: [[Projects/Second_Brain]]