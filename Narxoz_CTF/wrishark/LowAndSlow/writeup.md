# Incident Report — Alert #4471
**DNS Exfiltration & C2 Beaconing via DNS Tunneling**

- **Date:** 2024-05-29
- **Time window:** 16:26:58 – 16:32:33 UTC (364 seconds)
- **Source host:** 10.0.0.42
- **Severity (original):** Low
- **Severity (actual):** Critical
- **Status:** Confirmed compromise — data exfiltrated

---

## Executive Summary

Alert #4471 flagged unusual DNS query volume from 10.0.0.42 and was left uninvestigated for three days. Analysis of the attached packet capture (`Low_and_Slow.pcap`) confirms a multi-stage intrusion: internal network reconnaissance via DNS enumeration, establishment of a covert DNS tunnel to an attacker-controlled domain, exfiltration of a credential or token over DNS to a Tor exit node, and lateral movement scanning of internal services.

The technique — low-rate DNS queries interleaved with benign cover traffic — was specifically designed to evade volume-based detection. The alert was correctly generated; the severity classification was not.

---

## Affected Assets

| Asset | Role | Observed Activity |
|---|---|---|
| 10.0.0.42 | Compromised host | Recon, tunnel, exfil, lateral scan |
| 10.0.0.10–12 | Internal web servers (:80) | Scanned |
| 10.0.0.50 | Internal service (:443) | Scanned (29 packets — more active) |
| 10.0.0.80–81 | Internal services (:3000) | Scanned (likely Grafana) |
| 10.0.0.83–85 | Internal services (:8080) | Scanned |
| 185.220.101.47 | External — Tor exit node | C2 resolver for exfil domain |

---

## Attack Phases

### Phase 1 — Internal Reconnaissance (16:26:58–16:27:46)

10.0.0.42 issued DNS queries at a steady 2-second interval covering a broad set of internal and external hostnames. Internal targets included:

```
portal.corp, gitlab.corp, jira.corp, vpn.corp, mail.corp, backup.corp,
monitor.corp, cdn.corp, sso.corp, api.corp, wiki.corp, update.corp,
ntp.corp, telemetry.corp, ocsp.corp, crl.corp, proxy.corp, fileserver.corp,
printserver.corp, dc01.corp, dc02.corp, exchange.corp, wsus.corp,
grafana.corp, splunk.corp, elastic.corp, confluence.corp, nexus.corp,
harbor.corp, vault.corp, registry.corp, ci.corp, sonar.corp, argocd.corp,
rancher.corp, minio.corp, keycloak.corp
```

This is systematic enumeration of the corporate service landscape — identifying targets before acting.

### Phase 2 — DNS Tunnel Connectivity Test (16:27:38–16:27:46)

Five sequential queries were issued to `tunnel.fake.org` with base64-encoded payloads embedded in subdomain labels:

| Query | Encoded | Decoded |
|---|---|---|
| seq01.dGVzdA.tunnel.fake.org | `dGVzdA` | `test` |
| seq02.aGVsbG8.tunnel.fake.org | `aGVsbG8` | `hello` |
| seq03.d29ybGQ.tunnel.fake.org | `d29ybGQ` | `world` |
| seq04.Zm9v.tunnel.fake.org | `Zm9v` | `foo` |
| seq05.YmFy.tunnel.fake.org | `YmFy` | `bar` |

**Assembled payload:** `testhelloworldfoobar`

This is a channel verification — confirming end-to-end DNS tunnel connectivity before committing to real exfiltration.

### Phase 3 — Data Exfiltration (16:28:46–16:29:18)

Ten sequential queries were issued to `c2.evil.corp`. Unlike the tunnel test, these were routed directly to `185.220.101.47` — a known Tor exit node acting as authoritative resolver. All queries received responses, confirming data was received by the attacker.

The exfil queries were interleaved with cover queries (`ntp.corp`, `telemetry.corp`, `ocsp.corp`, `crl.corp`, `discord.com`, `reddit.com`) to reduce per-unit-time query rate and blend into normal traffic patterns.

| Sequence | Encoded | Decoded fragment |
|---|---|---|
| seq01 | Q1lDTg | CYCN |
| seq02 | RVR7ZA | ET{d |
| seq03 | N2UyZg | 7e2f |
| seq04 | MWEzYg | 1a3b |
| seq05 | OWM0ZQ | 9c4e |
| seq06 | NWY2YQ | 5f6a |
| seq07 | N2I4Yw | 7b8c |
| seq08 | OWQwZQ | 9d0e |
| seq09 | MWYyYQ | 1f2a |
| seq10 | M2I0fQ | 3b4} |

**Assembled exfiltrated data:** `CYCNET{d7e2f1a3b9c4e5f6a7b8c9d0e1f2a3b4}`

This matches a CTF-style flag format and is likely a token, API key, or credential. Its access scope must be determined and it must be revoked immediately.

### Phase 4 — Lateral Movement (16:29:42–16:31:25)

Following exfiltration, 10.0.0.42 initiated TCP connections to internal hosts. Each connection consisted of approximately 9 packets — consistent with a SYN scan or lightweight banner grab rather than sustained sessions.

| Time | Target | Port | Notes |
|---|---|---|---|
| 16:27:48 | 10.0.0.10 | :80 | Web service |
| 16:27:57 | 10.0.0.11 | :80 | Web service |
| 16:28:06 | 10.0.0.12 | :80 | Web service |
| 16:28:15 | 10.0.0.50 | :443 | 29 packets — more interaction |
| 16:29:42 | 10.0.0.80 | :3000 | Likely Grafana |
| 16:29:51 | 10.0.0.81 | :3000 | Likely Grafana |
| 16:30:58 | 10.0.0.83 | :8080 | API/app service |
| 16:31:07 | 10.0.0.84 | :8080 | API/app service |
| 16:31:16 | 10.0.0.85 | :8080 | API/app service |

The connection to 10.0.0.50:443 is notable — 29 packets vs. the ~9 seen for other hosts suggests a more substantive interaction. Logs from that host should be prioritised.

---

## Why This Evaded Detection

The technique is deliberately calibrated to defeat threshold-based alerting:

1. **Low rate.** One DNS query every 2 seconds. No burst, no spike.
2. **Cover traffic.** C2 queries were never sent consecutively. Every malicious query was followed by a plausible benign one (NTP, OCSP, CRL, telemetry) — the kind any healthy host generates.
3. **Domain camouflage.** The exfil subdomain structure (`seq01.PAYLOAD.c2.evil.corp`) superficially resembles legitimate internal hostnames at a glance.
4. **Misclassified severity.** "Unusual DNS query volume" was accurate. "Low severity" was not. The volume anomaly was the signal; the content was the threat.

---

## Indicators of Compromise

| Type | Value |
|---|---|
| Compromised host | `10.0.0.42` |
| C2 resolver (Tor exit) | `185.220.101.47` |
| Exfil domain | `*.c2.evil.corp` |
| Tunnel test domain | `*.tunnel.fake.org` |
| Exfiltrated credential | `CYCNET{d7e2f1a3b9c4e5f6a7b8c9d0e1f2a3b4}` |
| DNS tunneling technique | Base64 payload in subdomain labels, sequential `seqNN` prefix |

---

## Recommended Actions

### Immediate (within hours)

- [ ] **Isolate 10.0.0.42** from the network pending forensic investigation
- [ ] **Revoke `CYCNET{d7e2f1a3b9c4e5f6a7b8c9d0e1f2a3b4}`** — identify what system issued this token and what access it grants
- [ ] **Block 185.220.101.47** at the perimeter firewall
- [ ] **Sinkhole `*.c2.evil.corp` and `*.tunnel.fake.org`** at internal DNS resolvers
- [ ] **Pull logs from 10.0.0.50** — the 29-packet TCP session to :443 warrants priority review

### Short-term (within days)

- [ ] Audit 10.0.0.80–85 for signs of follow-on access following the lateral scan
- [ ] Review DNS resolver logs across the environment for any other hosts querying `c2.evil.corp` or `tunnel.fake.org`
- [ ] Determine initial access vector for 10.0.0.42 (how was it compromised before this capture begins?)
- [ ] Check for persistence mechanisms on 10.0.0.42 (scheduled tasks, cron, startup entries, malicious services)

### Detection Improvements

- [ ] Implement DNS content inspection — flag queries with high-entropy subdomains or sequential `seqNN` prefixes
- [ ] Add SIEM rule: alert on any internal host issuing DNS queries that resolve to known Tor exit nodes
- [ ] Establish DNS baseline per host; alert on new external domains not seen in prior 30 days
- [ ] Re-evaluate alert triage SLA — a 3-day response window allowed this intrusion to progress through recon, exfil, and lateral movement unchecked

---

## Artefacts

- `Low_and_Slow.pcap` — original packet capture covering the full attack window

---

*Writeup prepared from packet-level analysis. All timestamps UTC.*
