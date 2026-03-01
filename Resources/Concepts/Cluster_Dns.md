---
type: "Concept"
hub: "[[Hubs/Addons]]"
tags: [concept, cluster_dns]
---
# Cluster DNS

A DNS server within the Kubernetes environment that serves DNS records for Kubernetes services, automatically included in container DNS searches.

## Technologies
- 

## Excerpts & Key Information


> From: [[Processed_Transcripts/Cluster Architecture.md]] (Added on 2026-03-01 16:42)

*   While the other addons are not strictly required, all Kubernetes clusters should have cluster DNS, as many examples rely on it.

*   Cluster DNS is a DNS server, in addition to the other DNS server(s) in your environment, which serves DNS records for Kubernetes services.

*   Containers started by Kubernetes automatically include this DNS server in their DNS searches.



## Further Reading

> Core Node: [[Projects/Second_Brain]]