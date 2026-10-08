# 7. Traffic Bandwidth Prediction and Expected Performance

## 7.1 Existing performance and prediction method

The current servers are struggling because they sit on 100 Mbps interfaces with almost nothing in reserve. The customer interview puts the Web server and the Marketing file server at a 100 Mbps peak each, which is the full capacity of their network cards, with HR-DB at 80 Mbps and CS-FS at 60 Mbps. Every 100BaseT PC shares those paths through the same two 24-port Catalyst 2940 switches, so at peak times the busiest services queue behind each other, which is the slow access HelpYou staff are reporting. The Web server also reports memory and disk-space faults, so bandwidth is one of its limits rather than the only one. [P1, P2]

The client brief gives no measured CPU load, disk latency or application response times, so the interview's bandwidth figures are the one performance measure this proposal can forecast with numbers. The interview labels the Email, DHCP, DC/DNS and Monitoring values as estimates, because those services are new, and the forecast keeps them as planning baselines. The interview also lists IT Admin as the only user group for some of the infrastructure services, which this proposal reads as who administers them. Every PC still consumes DHCP, DNS and domain logon, so the forecast measures those services against the whole head office. [P2]

The forecast formula is: predicted peak = current peak x the five-year staff-growth factor for that service's users x a 1.10 workload allowance, rounded up to the next 10 Mbps. The 10% allowance covers richer content and heavier applications over five years, and the rounding keeps the figures easy to compare. Both are assumptions made for this proposal; the source documents set no multiplier. The growth factors come from HelpYou's five-year head counts.

| Service audience | Growth calculation | Factor |
|---|---|---|
| All head-office staff / shared infrastructure | 108 forecast staff / 40 original staff | 2.70 |
| HR | 10 forecast / 3 original | 3.33 recurring |
| Marketing | 20 forecast / 10 original | 2.00 |
| Customer Service | 30 forecast / 5 original | 6.00 |

*Table 11. Five-year growth factors by service audience.*

The comparison uses the original 40-staff office because the interview gives its traffic figures without saying whether they describe 40 or 70 staff, and the smaller baseline produces the larger, safer growth factor. For the shared infrastructure services, total staff growth serves as the proxy for workload, since every extra person adds logons, lookups and mail. If the IT team measures a 70-staff baseline during month 1, the forecast is recalculated from that. Cairns traffic and any change in application behaviour are checked in the month-2 pilot rather than added to the head-office figures by assumption.

## 7.2 Bandwidth calculations

The table below sets out the forecast for each server service. It shows the current average and peak from the interview, the growth factor and allowance applied, the five-year peak that results, and the benchmark bandwidth the design provides.

| Service | Current average | Current peak | Growth + allowance | 5-year peak | Service benchmark |
|---|---|---|---|---|---|
| Web | 60 | 100 | 2.70 x 1.10 | 300 | 1,000 |
| HR-DB | 40 | 80 | 3.33 x 1.10 | 300 | 1,000 |
| Marketing FS | 50 | 100 | 2.00 x 1.10 | 220 | 1,000 |
| CS-FS | 26 | 60 | 6.00 x 1.10 | 400 | 1,000 |
| Email\* | 25 | 80 | 2.70 x 1.10 | 240 | 1,000 |
| DHCP\* | 20 | 50 | 2.70 x 1.10 | 150 | 1,000 |
| DC / DNS\* | 40 | 90 | 2.70 x 1.10 | 270 | 1,000 |
| Monitoring\* | 60 | 100 | 2.70 x 1.10 | 300 | 1,000 |

*Table 12. Current and predicted server bandwidth with the benchmark design (Mbps).*

All values are Mbps. The starred rows are the figures the interview labels as estimates. The 1,000 Mbps benchmark in the last column is the 1 Gbps the design allocates to each service inside its host's 10 Gbps uplink, so every service has at least two and a half times its forecast peak available. [P2]

Two worked examples show the method. CS-FS = 60 x (30 / 5) x 1.10 = 396 Mbps, rounded up to 400 Mbps. Web = 100 x (108 / 40) x 1.10 = 297 Mbps, rounded up to 300 Mbps. Using each department's own growth matters here: Customer Service grows six-fold, and one multiplier applied to every service would have understated it badly.

The predicted peaks add up to 2,180 Mbps (2.18 Gbps). That total assumes every service peaks at the same moment, which makes it a conservative LAN planning envelope. A single surviving 10 Gbps host path carries about 4.6 times that figure before protocol overhead and backup or replication traffic are counted. The busiest single forecast, CS-FS at 400 Mbps, sits well below its 1 Gbps benchmark.

### Backup, voice and video allowances

Backup traffic comes on top of the eight services above. As an example workload, moving 500 GB of changed data in an eight-hour window needs about 139 Mbps before protocol overhead (500 x 8,000 / 28,800), and about 181 Mbps with 30% overhead added. The real daily change rate is measured in month 1 and the off-site media is sized from the actual dataset. Backups and Hyper-V replication run outside the busiest hours, so interactive application traffic keeps priority on the host links.

For the internet link the design allows for 20 simultaneous video sessions at 4 Mbps in each direction (80 Mbps), ten external voice calls at 0.1 Mbps in each direction (1 Mbps), and a further 100 Mbps download and 50 Mbps upload for everything else happening at once. Together these come to about 181 Mbps download and 131 Mbps upload, well inside the 1000/400 Mbps plan and its 875/339 Mbps typical busy-period speeds. These are design allowances, and the month-4 acceptance tests check them against real calls. File-server traffic stays on the LAN, so the internet calculation leaves it out.

## 7.3 Five-year capacity and implementation

The upgrade pairs faster network paths with right-sized memory, resilient storage and a planned migration of each service. The plan keeps the immediate 70-user Brisbane deployment separate from the 108-user five-year horizon: ports, subnets, licences and storage are sized for the first and reviewed against the second. Department subnet capacity, switch ports, software licences and host storage are checked together at each review, because any one of them can become the limit first. The four-month program runs in the stages below. [P1, P2]

| Stage | Timing | Work and acceptance outcome |
|---|---|---|
| Discovery and approval | Month 1 | Inventory devices and data; confirm the assumptions taken from the client brief, nbn eligibility at both sites, permissions, service dependencies and supplier quotes; obtain the CIO's approval of the design and budget. |
| Build and pilot | Month 2 | Install the switches, firewalls, hosts and NAS; stand up pilot identity, file, email, voice and backup services; prove application and client compatibility before any production data moves. |
| Controlled migration | Month 3 | Move departments in agreed windows; migrate shared data and phone numbers; keep rollback copies and the old service running until each acceptance test passes. |
| Acceptance and handover | Month 4 | Test authorisation, the VPN, the two core paths, recovery, calls and video, and backup restoration; train staff; hand over diagrams and support records; obtain the CIO's acceptance. |

*Table 13. Four-month implementation schedule.*

After handover the IT team reviews capacity monthly, and this proposal recommends a full design review each year. The proposed triggers are sustained busy-period interface load above 70%, CPU above 70%, memory above 80%, or free working storage below 25%. Application latency and error rates are checked alongside load, since a slow application can sit on a lightly loaded link. These thresholds are targets for the CIO to agree, and Zabbix raises the alert when one is crossed.

Day to day, high-priority security and backup alerts are reviewed every morning. Operating-system, application and device updates go through change control, device configurations are backed up, and new firmware is tried on a test device or pilot group first. Each quarter the team reviews access permissions and restores a representative file, VM and database from backup. Once a year the rehearsal widens to losing one host and the internet path, so the recovery plan is exercised end to end. [R27]

Before the project goes to the CIO for sign-off, the acceptance tests prove five things: HR data stays unreadable to every other department, guests reach the internet and nothing else, clients authenticate against either domain controller, files open from both Windows and Linux clients, and a deleted file, a VM and the HR database can each be restored. The tests also measure application response while a large file transfer and video and voice calls run at the same time, and the handover pack records the results.

Capacity grows in steps rather than through replacement. Spare access ports, the hosts' memory and storage headroom, more addresses within the section 5 subnets and additional user licences cover the growth the five-year forecast describes. Three events would call for more than that: reaching the hosts' CPU or platform limit, a much larger HR database, or a stricter recovery target than four hours, any of which means a third host or a different availability design. That is why the five-year answer in this proposal pairs the equipment with the review and upgrade actions above. The monthly review tells the IT team when a limit is near, and the expansion path tells them what to add.

## 7.4 Conclusion

This proposal gives HelpYou a network that handles the move to two floors now and the growth the business forecasts over the next five years. It replaces the 100 Mbps flat network with 1 Gbps to every desk and 10 Gbps between the switches and the servers, puts a FortiGate 70G between the internet and the core stack, separates departments, voice, guests, servers and management into their own VLANs, and gives Cairns and remote staff a controlled way in. Identity, files, email, monitoring and telephony move onto two virtualisation hosts that hold replicas of each other, with daily backups on the NAS and encrypted copies off site. Two core switches on two 10 Gbps links, two domain controllers and the replica pair each remove a different single point of failure from the old design.

Each site keeps one internet service, and this proposal is open about the interruption risk that carries. The first-year cost of $350,601.81 sits within the $500,000 ceiling, with a four-month delivery schedule. That leaves $149,398.19 for the supplier quotes to settle against, and the five-year baseline ownership estimate is $498,211.41. Section 6.9 separates every published price from every allowance, so the CIO can see exactly which figures a quote will firm up. [P1]

The next step sits with the CIO. Once the design and budget are approved, I will obtain the configured quotations, confirm the HR application's compatibility, agree the recovery targets with HelpYou and finalise the diagrams, then start month 1 of the schedule. Installation, testing and acceptance are recorded as each stage completes, so HelpYou can see the network meet each requirement before the CIO signs the project off.
