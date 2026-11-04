# Image Resizer

Static PNG only, up to 5 MiB; PNG signature, chunk structure and dimensions are checked before decode. Input and output width and height must each be 1–4096 pixels and area at most 8,000,000 pixels. Animated PNG is rejected. Choose explicit pixel dimensions or 0.01–400 percent; pixel results are rounded to whole numbers. Aspect lock uses the original ratio and the last edited dimension. Canvas interpolation affects quality; PNG export preserves transparency. Metadata is not deliberately copied, but no metadata-removal guarantee is made.

Image data stays local. Hosting and the existing styling CDN make separate requests. Publication is pending.
