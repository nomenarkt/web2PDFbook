📌 Project Name (Working Title)
Web2PDFBook — "Turn any public documentation website into a structured, navigable PDF book."

🎯 Product Goal (1-liner)
Create a command-line and optionally web-based tool that crawls a public documentation website and generates a single, merged PDF containing all relevant content pages in a structured order.

🧩 Target Use Cases
| User Persona    | Scenario                                                                  |
| --------------- | ------------------------------------------------------------------------- |
| **Developer**   | Wants offline access to documentation while flying or traveling.          |
| **PM or Legal** | Needs a snapshot of product docs for auditing or regulatory archiving.    |
| **Educator**    | Converts API or dev tool docs into printable handouts or coursework PDFs. |

✂️ MVP Scope (must-have features only)
| Feature                                 | Included in MVP? |
| --------------------------------------- | ---------------- |
| Input a base URL                        | ✅ Yes            |
| Crawl all internal links                | ✅ Yes            |
| Filter only valid HTML pages            | ✅ Yes            |
| Render each page as a standalone PDF    | ✅ Yes            |
| Merge PDFs into a single file           | ✅ Yes            |
| Maintain navigation order (if possible) | ✅ Yes            |
| Command-line interface                  | ✅ Yes            |
| Basic error handling & logging          | ✅ Yes            |
| Configurable delay between requests     | ✅ Yes            |
| Automated tests for core modules        | ✅ Yes            |

❌ Out of Scope for MVP (later phases)
| Feature                            | Reason for exclusion        |
| ---------------------------------- | --------------------------- |
| Full site login/cookie auth        | Adds complexity             |
| Sitemap XML parsing                | Optional enhancement        |
| Browser-based GUI                  | Not needed for core utility |
| OCR for scanned/image-heavy pages  | Rare in dev docs            |
| Export to EPUB or Markdown         | Out of initial focus        |
| Upload to cloud or storage buckets | Post-MVP automation         |

📦 Inputs & Outputs
| Input                    | Format                      |
| ------------------------ | --------------------------- |
| Website base URL         | `https://example.com/docs/` |
| Output PDF file path     | `./docs-book.pdf`           |
| (Optional) TOC detection | auto-parsed nav menu        |

🛠️ Risks & Assumptions
-Assumes target sites are mostly static (no JS-heavy navigation).
-Assumes reasonable page load speeds and API quota (if using rendering API).
-Output PDF quality may vary depending on CSS/layout of target docs.

✅ MVP Deliverables
| Deliverable                          | Purpose                               |
| ------------------------------------ | ------------------------------------- |
| **SRS (Software Requirements Spec)** | Formalize this MVP scope and behavior |
| **Architecture diagram**             | Guide modular implementation          |
| **Project structure layout**         | Enforce clean layering                |
| **Python CLI + modular scripts**     | First working app                     |
| **Test plan + CLI test cases**       | Begin testing coverage early          |
| **GitHub-ready repo structure**      | CI/CD ready foundation                |

