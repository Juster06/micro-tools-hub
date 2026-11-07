# CSS Gradient Generator

Canonical route `css-gradient-generator/index.html`.

Enter an opaque six-digit hex colour and a percentage on each line. Use nondecreasing positions. Equal positions create hard stops. Valid changes update the preview. Radial gradients use a centered circle.

Two to eight opaque #RRGGBB stops with nondecreasing 0–100% positions, two decimal places. Linear angles range from −360 to 360 degrees. Radial gradients use a centered circle. Stop text at most 256 units and output at most 4 KiB. Only generated CSS assigned to backgroundImage.

The tool generates a bounded declaration. It does not import arbitrary CSS, use images, or assess text contrast across the gradient.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

Task 25 status is TESTED. Publication is pending. Local source revision `593f679c7dd953ce4f4a5aee99d5e4fdc1614215` and [verification evidence](../audit/CSS_GRADIENT_GENERATOR_VERIFICATION.json).

[CSS Images gradient syntax](https://drafts.csswg.org/css-images-3/#gradients). The preview uses validated linear or centered radial CSS values.
