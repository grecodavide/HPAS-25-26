#import "@local/personal:0.1.0": *
// Example of glossary:
// glossary: (
//     example: (
//         short: "EX",
//         long: "Example",
//         description: "This is a toy example"
//     ),
// ),
#show: setup-document.with(
    title: [],
    glossary: (),
)

#let very_low = (
    low: [
        - CAD tampering (browser-portal)
    ],
    medium: [
        - CSRF
    ],
    high: [
        - Path traversal
    ],
    critical: [
        - CAD-embedded malware
    ],
)

#let low = (
    low: [
        - Printer assigned to project
    ],
    medium: [
        - Notification elimination
        - Forging requests
        - Modifying CAD information
        - MES overload
        - Modifying project data
        - Powder management tampering
        - Stop powder resupply
    ],
    high: [
        - Slicer server overloading
        - Slicer server compromised
        - API key leakage
        - Thermal sensor tampering
        - Thermal sensor spoofing
        - Sensor activity disruption
        - Quality control tampering
    ],
    critical: [
        - Obtaining admin access
        - Old OS known vulnerabilities
        - EoP via known vulnerabilities
    ],
)

#let medium = (
    low: [
    ],
    medium: [
        - Contractor information leakage
        - CAD tampering (OT floor)
        - G-code tampering
        - CAD leakage
        - G-code leakage
    ],
    high: [
        - Slicer spoofing
        - MES spoofing
    ],
    critical: [
    ],
)

#let high = (
    low: [
    ],
    medium: [
        - Contractor impersonation
        - Account spoofing
    ],
    high: [
        - Portal overload
    ],
    critical: [
    ],
)

#let very_high = (
    low: [
    ],
    medium: [
    ],
    high: [
    ],
    critical: [
    ],
)

#table(
    columns: (auto,) * 5,
    align: horizon,
    [frequency\\severity], [*Low*], [*Medium*], [*High*], [*Critical*],
    [*Very low*],
    very_low.low,
    very_low.medium,
    very_low.high,
    very_low.critical,

    [*Low*], low.low, low.medium, low.high, low.critical,
    [*Medium*], medium.low, medium.medium, medium.high, medium.critical,
    [*High*], high.low, high.medium, high.high, high.critical,
    [*Very high*],
    very_high.low,
    very_high.medium,
    very_high.high,
    very_high.critical,
)
