# IPv4 Subnet Calculator

## Task 25.1 public verification

The deployed page matched main `c127f856cbd97497412ec35ed66b3b1a58c4b2dc`. All 7 fresh public browser cases passed on 2026-11-07. The release proposal is backed by [the publication audit](../audit/IPV4_SUBNET_CALCULATOR_RELEASE_VERIFICATION.json).

Canonical route `ipv4-subnet-calculator/index.html`.

Enter four decimal octets and a separate prefix, for example 192.0.2.130 and 24. The address-purpose note describes the entered address using selected special-purpose ranges.

IPv4 field at most 32 ASCII characters, prefix at most two decimal digits, output at most 4 KiB. Strict canonical decimal octets, /0–/32, RFC 3021 /31 point-to-point endpoints. No address enumeration.

IPv4 only. /31 endpoints apply to point-to-point links. Conventional host counts do not establish address availability, reachability or routing policy.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

The Task 25 development status was TESTED. Local source revision `593f679c7dd953ce4f4a5aee99d5e4fdc1614215` and [verification evidence](../audit/IPV4_SUBNET_CALCULATOR_VERIFICATION.json).

[IANA special-purpose address registry](https://www.iana.org/assignments/iana-ipv4-special-registry/) and [RFC 3021 point-to-point endpoints](https://www.rfc-editor.org/rfc/rfc3021.html). The in-page address-purpose table lists selected ranges.
