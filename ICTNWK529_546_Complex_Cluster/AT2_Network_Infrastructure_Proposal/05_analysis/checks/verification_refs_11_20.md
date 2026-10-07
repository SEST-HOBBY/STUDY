# Verification of bibliography references [R11] to [R20]

Checked 7 October 2026. Method: direct fetch of each URL. The session's egress proxy blocks most Australian retailer domains for the normal fetch tool, so those pages were rendered through the remote Cloudflare browser tool instead (the same page content a visitor sees, but the rendering browser sits outside Australia, which is why the Microsoft pages also print "This product is not available in your market"; that line is a geolocation artefact, not a listing problem). Prices are AUD. "Draft" means the price used in sections 6.4 to 6.10 of the draft report.

## Summary table

| Ref | Source and URL | Loads? | Same product/page? | Price shown now (AUD) | Price in draft | Status | Replacement (if needed) |
|---|---|---|---|---|---|---|---|
| R11 | Microsoft AU, SMB security pricing. https://www.microsoft.com/en-au/security/small-medium-business/pricing | Yes | Yes. Defender for Business and the Defender for Business servers add-on are both on the page | Defender for Business AU$4.50 user/month paid yearly; servers add-on AU$4.50 licence/month paid yearly. Page states "Prices shown here and on following pages do not include GST" | AU$4.50 per user or server per month ex GST | ok | none |
| R12 | Synology, RackStation RS2423+ product page. https://www.synology.com/en-global/products/RS2423%2B | Yes | Yes. Page is now titled "RackStation RS2423RP+II / RS2423+" (the RP+ has been revised to RP+II). Specs: 12 x 3.5"/2.5" SATA bays, 2U, redundant PSU on the RP model, 1 x 10GbE + 2 x 1GbE | No price on page (vendor spec page) | none (descriptive reference) | ok | none |
| R13 | Techbuy, Synology RS2423RP+ diskless NAS. https://www.techbuy.com.au/p/529889/HARD_DRIVE_-_EXTERNAL_NAS_DRIVES/Synology/RS2423RP_.asp | Yes | Yes. "Synology RackStation 12-Bay 2U Rackmount NAS (RS2423RP+)", Manuf No RS2423RP+, storage drives installed: No (diskless), in stock | $6,014.25 inc GST (RRP $6,289.00). Footer: "All prices shown on techbuy.com.au are in $AUD and inclusive of GST" | $6,124.25 | price_differs | Same URL, $6,014.25 inc GST |
| R14 | Grandstream, UCM6300 Series IP PBX. https://www.grandstream.com/products/ip-pbxs/ucm-series-ip-pbxs/product/ucm6300-series-ip-pbx | Yes | Yes. Series page covering UCM6301/6302/6304/6308 (series: up to 3000 users and 450 concurrent calls; three Gigabit PoE+ ports; DoC for UCM6302 linked) | No price (vendor page) | none (descriptive reference) | ok | none |
| R15 | Telrex, Grandstream UCM6302. https://www.telrex.com.au/grandstream-ucm6302-2-fxo-2fxs-1000-users | Yes | Yes. "Grandstream UCM6302 IP PBX - 2 FXO, 2 FXS, 3 Gigabit PoE+ Ports - Up to 1000 Users / 150 Concurrent Calls", SKU UCM6302, in stock ("Selling fast, limited stock left") | $605.00 inc (site marks price "inc") | $462 inc GST | price_differs | Same URL, $605.00 inc GST. Only other AU listing found: MyITHub $581.00 inc GST but out of stock (https://www.myithub.com.au/grandstream-ucm6302-2-fxo-2fxs-1000-users) |
| R16 | MyITHub, Grandstream GRP2612P. https://www.myithub.com.au/grandstream-grp2612p-2-4-colour-lcd-display-22-line-keys-2-sip-accounts-poe-support-100mbps-port-ip-phone | Yes | Yes. "Grandstream GRP2612P 4 Line IP Phone, 2 SIP Accounts, 320x240 Colour Screen, HD Audio, Powerable Via POE", SKU GRP2612P, in stock. Spec: "Dual switched auto-sensing 10/100 Mbps Ethernet ports with integrated PoE"; no power adapter included | $83.00 (inc. of GST), was $146.64 | $83 | ok | none |
| R17 | Microsoft AU, Teams Essentials. https://www.microsoft.com/en-au/microsoft-teams/essentials | Yes (normal fetch returned HTTP 503 twice; rendered browser loaded it) | Yes | AU$6.00 user/month, paid yearly (annual subscription). "Prices shown here and on following pages do not include GST" | AU$6 per user per month ex GST | ok | none |
| R18 | Video Conferencing Australia, Logitech MeetUp 2. https://www.videoconferencingaustralia.com.au/product/logitech-meetup-2/ | No. Egress proxy blocks the domain, and the rendered browser is refused by the site's Cloudflare bot protection ("Sorry, you have been blocked") | Could not verify | Could not verify | $1,599 | blocked | MyITHub: Logitech MeetUp 2 (960-001680) $1,307.00 inc GST, in stock, https://www.myithub.com.au/logitech-meetup-2-all-in-one-usb-conference-camera-for-small-meeting-rooms. Alternative: PB Tech AU $1,333.64 inc GST ($1,212.40 ex), "In stock at Supplier", https://www.pbtech.com/au/product/CAMLOG6249502/Logitech-MeetUp-2-4K-All-in-One-USB-Conference-Vid |
| R19 | TP-Link AU, EAP650 V1.30. https://www.tp-link.com/au/business-networking/omada-wifi-ceiling-mount/eap650/v1.30/ | Yes | Yes. Spec table lists 802.1X support, WPA2/WPA3-Personal and Enterprise, SSID to VLAN mapping, wireless isolation between clients, up to 16 SSIDs, management VLAN, SNMP v1/v2c/v3, 802.3at PoE, 1 x Gigabit port | No price (vendor page) | none (descriptive reference) | ok | none |
| R20 | Umart, TP-Link EAP650. https://www.umart.com.au/product/tp-link-ceiling-mount-ax3000-dual-band-wifi-6-access-point-eap650-72658 | Yes | Yes. "TP-Link Ceiling Mount AX3000 Dual Band WiFi 6 Access Point (EAP650)". Delivery and every store listed "Out Of Stock"; page offers "Want a stock alert?" | $179.00 (Umart does not print a GST note on the product page; Australian consumer retail prices are GST-inclusive) | $179 | ok | none required. No in-stock AU listing of the ceiling-mount EAP650 was confirmed: MyITHub lists it at $207.00 inc GST, also out of stock |

## Descriptive claims checked against these references

- 6.4 Anti-Virus [R11]: "AU$4.50 per user or server per month excluding GST" is supported. Arithmetic in 6.9 checks: 78 x 4.50 x 12 x 1.10 = $4,633.20; 14 x 4.50 x 12 x 1.10 = $831.60; combined $5,464.80. All match the draft.
- 6.5 Backup storage [R12, R13]: RS2423RP+ is a 12-bay 2U rackmount with redundant PSU and 1 x 10GbE + 2 x 1GbE; the Techbuy listing is diskless. Supported. Price is $6,014.25, not $6,124.25 (the draft looks like a digit transposition). The 6.9 line "Synology RS2423RP+ diskless NAS 1 x $6,124.25" should become $6,014.25, which lowers the initial implementation subtotal by $110.00 and the 10% contingency by $11.00.
- 6.6 VoIP [R14, R15, R16]: UCM6302 has 2 FXO, 2 FXS, three Gigabit PoE+ ports, up to 1000 users / 150 concurrent calls; GRP2612P has 10/100 Mbps ports and PoE, so the draft's point that PCs should not hang off the phone's passthrough port is supported. The $462 PBX price is not supported by any current listing: Telrex shows $605.00 inc GST (in stock), MyITHub $581.00 inc GST (out of stock). Using Telrex, the 6.9 line becomes 1 x $605.00 (+$143.00 to the subtotal, +$14.30 contingency). 82 x $83 = $6,806.00 is correct.
- 6.6 Teams [R17]: AU$6.00 ex GST is supported. 78 x 6 x 12 x 1.10 = $6,177.60 matches the draft.
- 6.6 MeetUp 2 [R18]: the cited page cannot be reached. Current AU listings are $1,307.00 (MyITHub, in stock) and $1,333.64 (PB Tech, stock at supplier) inc GST, both well under the draft's $1,599. If the reference is swapped to MyITHub, 3 x $1,307.00 = $3,921.00 (draft $4,797.00; subtotal falls by $876.00, contingency by $87.60). If PB Tech is preferred, 3 x $1,333.64 = $4,000.92.
- 6.8 Managed wireless [R19, R20]: EAP650 enterprise authentication (802.1X, WPA2/WPA3-Enterprise), SSID-to-VLAN mapping and client isolation are all in the TP-Link spec table. The $179 price and the "cited retailer currently reports no stock" note are both supported by the Umart page today. 7 x $179 = $1,253.00 is correct.

## Items in the task list that belong to other reference ranges

C1300-12XS port count [R1, R2], FG-70G bundle stock [R6], Dell R360 starting price [R7], Windows Server 2025 Standard 16-core and CAL prices [R8, R10] and the Aussie Broadband Business Assurance 1000/400 plan [R24] sit outside [R11] to [R20] and were not fetched in this pass.

## Net effect on section 6.9 if the verified prices are adopted

| Line | Draft | Verified | Change |
|---|---|---|---|
| Synology RS2423RP+ diskless NAS (1) | $6,124.25 | $6,014.25 | -$110.00 |
| Grandstream UCM6302 (1) | $462.00 | $605.00 | +$143.00 |
| Logitech MeetUp 2 (3) | $4,797.00 | $3,921.00 (MyITHub) | -$876.00 |
| Initial subtotal | $286,999.46 | $286,156.46 | -$843.00 |
| 10% contingency | $28,699.95 | $28,615.65 | -$84.30 |

Recurring lines tied to R11 and R17 are unchanged.
