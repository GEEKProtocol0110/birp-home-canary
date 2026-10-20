# BIRP invention brief

[Download the recreated invention brief, version 1.0](BIRP-Invention-Brief-v1.0.pdf).

Created October 20, 2026 for founder/partner discussions. This is a new four-page edition based on the recovered product requirements and the two founder-supplied original visual assets. It is not a recovered copy of the earlier missing PDF.

## Contents

1. Product concept, standalone core, optional connected vision, and collaboration goal.
2. Accurate perimeter-position illustration and proposed first-bench signal flow.
3. Original exploded concept image and a comparison of the first experiment with the broader intended product.
4. A practical path to physical proof, partner evaluation areas, and source links.

The original artwork remains concept art. Hardware performance, customer demand, manufacturing costs, and production scope have not been validated. The brief makes no claim of patent filing, granted rights, or certification.

## Regenerate

Requires Python 3 and ReportLab. From the repository root:

    python3 docs/brief/build_brief.py

Pass an optional absolute output path as the first argument. Source artwork is loaded from website/assets/. The generator uses DejaVu fonts where available and falls back to standard PDF fonts. Render and visually check all pages after changes.

After validating a rebuilt PDF, copy it to website/BIRP-Invention-Brief-v1.0.pdf and publish the hosted site so the download stays current.
