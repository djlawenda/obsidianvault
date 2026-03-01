---
type: "Concept"
hub: "[[Hubs/Kubernetes]]"
tags: [concept, extensibility]
---
# Extensibility

The design characteristic that allows a system to be extended or modified by adding new features without altering its core source code.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Kubernetes Overview.md]] (Added on 2026-03-01 16:42)


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)

*   Customization and extensibility: Kubernetes architecture allows for significant customization:

*   Custom schedulers can be deployed to work alongside the default Kubernetes scheduler or to replace it entirely.

*   API servers can be extended with CustomResourceDefinitions and API Aggregation.

*   Cloud providers can integrate deeply with Kubernetes using the cloud-controller-manager.



*   Designed for extensibility Add features to your Kubernetes cluster without changing upstream source code.



## Further Reading

> Core Node: [[Projects/Second_Brain]]