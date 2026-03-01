This file will contain a high-level overview of the vault's structure and conventions. It serves as a reference for both human and AI agents operating within the vault.

*   **File Naming:** All vault folders and notes use underscore-separated, TitleCased filenames. No spaces or dashes. Acronyms remain uppercase (e.g., `AI_Native_Engineer`, `AWS_ELB`).
*   **Core Node:** Every canonical note should end with the line `> Core Node: [[Projects/Second_Brain]]` to center the graph.
*   **Folder Structure:**
    *   `Inbox/`: Raw capture zone. `Transcripts_to_Process` holds unprocessed text.
    *   `Resources/`: Canonical knowledge.
        *   `Hubs/`: Maps of content (MoCs) for major domains.
        *   `Concepts/`: Evergreen patterns and ideas.
        *   `Technologies/`: Dossiers on specific tools and platforms.
        *   `Processed_Transcripts/`: Archived source material.
    *   `Projects/`: Human-authored, active deliverables. This directory is READ-ONLY for AI agents.
    *   `Areas/`: Long-term responsibilities and research topics.
    *   `Archives/`: Deprecated or historical content.
    *   `Agents/`: Operating manuals and scripts for AI automation.
