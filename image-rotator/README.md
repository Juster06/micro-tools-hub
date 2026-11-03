# Image Rotator

Canonical route: `image-rotator/index.html`.

Static PNG only, up to 5 MiB. PNG signature and IHDR dimensions are inspected before decoding; width and height each 1–4096 pixels and at most 8,000,000 pixels total. Animated PNG and malformed/truncated files are rejected. Rotation is clockwise in 90° increments; horizontal/vertical flips apply to source axes before rotation. Export is PNG and preserves transparency. Browser image decoding, Canvas and PNG encoding are required. Memory use depends on the browser and can exceed the source file size. Original metadata is not deliberately copied; no metadata-removal guarantee is made.

Image contents stay local; hosting and the existing Tailwind CDN are separate network requests. Publication is pending.
