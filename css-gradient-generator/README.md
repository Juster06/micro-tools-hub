# CSS Gradient Generator

Canonical route `css-gradient-generator/index.html`.

Enter an opaque six-digit hex colour and a percentage on each line. Use nondecreasing positions. Equal positions create hard stops. Valid changes update the preview. Radial gradients use a centered circle.

Two to eight opaque #RRGGBB stops with nondecreasing 0–100% positions, two decimal places. Linear angle −360–360 degrees; radial circle centered. Stop text at most 256 units and output at most 4 KiB. Only generated CSS assigned to backgroundImage.

The tool generates a bounded declaration. It does not import arbitrary CSS, use images, or assess text contrast across the gradient.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

Task 25 development. Publication pending.
