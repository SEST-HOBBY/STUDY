# Lab 10 demonstration screenshots from the AT1 template

Extracted on 24 Nov 2026 from `ICTNWK529_ICTNWK546_AT1 WORKING ON.docx` (images 27 and 28), which is filed
under `Lab8_Install_and_Configure_ADDS_Services/00_assessment_documents/` on the branch
`sest-dev/laughing-hypatia-qnrqqs`. They are the teacher's examples, from 2021 and carrying another person's
name. They are here only so I can see what my own two snips have to show; they are replaced by mine in the
results document.

| File | What it shows | What my own snip must show |
|---|---|---|
| `10_demo1_ubuntu_nmap_os_scan.png` | A terminal on the domain-joined Ubuntu client (the prompt carries the domain name) running `sudo nmap -O 192.168.2.3`, with the scan report and OS detection result | The same scan run from my Ubuntu client, with my own domain name in the prompt and my own target address |
| `10_demo2_sguil_realtime_events.png` | The Sguil console on Security Onion, RealTime Events tab: `GPL ICMP_INFO PING *NIX` and a run of `ET SCAN ...` alerts from the scanning machine to the monitored machine, and the Agent Status panel with the ossec, pcap and snort agents UP | Sguil with the alerts raised by my scan (source = my scanning machine), my sensor name, and the agents UP |
