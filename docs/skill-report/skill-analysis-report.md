## Skill Analysis: ai-social-media-content

**Source:** https://skills.sh/inferen-sh/skills/ai-social-media-content
**Language:** English
**Security:** Gen Agent Trust Hub: Pass | Socket: Pass | Snyk: Pass

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "Provides hardcoded bash script examples (e.g., `infsh app run...`) rather than an adaptive script." |
| Technical Depth | 4/10 | "Surface-level instructions; only passes raw JSON prompts to the infsh CLI without deep configuration." |
| Decision Intelligence | 2/10 | "No decision making — just lists a fixed set of commands to run." |
| ORM Compatibility | N/A | Skill does not involve databases or ORMs. |
| Security Practices | 9/10 | "Passes validations (Trust Hub, Socket, Snyk). Uses `infsh login` instead of hardcoded API keys." |
| Output Quality | 4/10 | "Output is simply redirected to JSON files (e.g., `> \"carousel_$i.json\"`) without structured artifacts." |
| Error Handling | 1/10 | "No error handling, assumes all infsh API calls and bash loops succeed." |
| Monitoring | N/A | Skill does not involve infrastructure or runtime monitoring. |
| Documentation | 7/10 | "Clear phases for different platforms (TikTok, Instagram, YouTube) and includes a Best Practices section." |
| Freshness | 8/10 | "References recent models like Veo 3, FLUX, and Claude Sonnet 4.5." |
| **TOTAL** | **39/80** | Equivalent to **48.75%** |

**Verdict:** BUILD FROM SCRATCH
