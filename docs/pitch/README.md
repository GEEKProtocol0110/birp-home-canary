# BIRP partner pitch, version 1.0

Eight slides, dated October 20, 2026. The PPTX has editable native text and a native table. Original images and the new room concept are embedded raster assets. The PDF is a fixed visual export of the reviewed slides; use the PowerPoint to edit content.

This is a concept-stage engineering collaboration pitch, not a validated device, customer traction claim, financing offer or selected licensing agreement. Sources and context are included in speaker notes.

## Files

- [Editable PowerPoint](BIRP-Partner-Pitch-v1.0.pptx)
- [PDF for sharing](BIRP-Partner-Pitch-v1.0.pdf)
- [Invention brief](../brief/BIRP-Invention-Brief-v1.0.pdf)

## Regeneration

The authoring source uses @oai/artifact-tool. It also invokes presentation-skill validators at their runtime paths. Use the Codex primary runtime with those dependencies, DejaVu Sans and Python ReportLab. Set BIRP_WORKSPACE to a workspace containing this repo as birp-home-canary, and create an empty .pitch-build directory plus output/presentation. Put or symlink the runtime node_modules beside build_pitch.mjs before running with the runtime Node binary. Set CODEX_PRIMARY_RUNTIME_PYTHON to its Python executable. Run build_pitch.mjs, then export_pdf.py. The reviewed PowerPoint gets a -reviewed suffix during finalization; rename it to the release name after review. Use a fresh workspace or new receipt/output names to regenerate.

The PDF uses the rendered final slides because native PDF export in this runtime could not resolve its standard font data. All eight slides were individually reviewed, and structure, font and layout checks passed with no warnings.

## New concept image

assets/birp-room-concept.png is a generated lifestyle concept, not an existing product photograph. Created October 20, 2026 with imagegen in new-generation mode, using the original exploded image and logo as design references. Original files remain unchanged in website/assets.

Prompt: Create a wide 16:9 conceptual lifestyle rendering of BIRP installed in a quiet contemporary living room. Show a round white wall-mounted display with a subtle teal halo and a small physical white bird perched at the top of its outside perimeter, outside the screen. Keep the unit and furniture on the right half, with a warm off-white wall and usable negative space on the left. Warm neutral materials, muted forest-green upholstery, soft daylight. No people, text, numbers, labels, logo typography, charts, watermark or promises of an existing product. Preserve the round device and physical perimeter bird. Do not reproduce the exploded assembly. Label as a concept illustration in the deck.
