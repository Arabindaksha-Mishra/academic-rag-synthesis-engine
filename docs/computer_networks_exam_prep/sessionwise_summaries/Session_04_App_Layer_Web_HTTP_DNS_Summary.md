# Computer Networks (BSDCBZC481)
# Session 04: Application Layer — HTTP, Electronic Mail & DNS
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapter 2 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapters 25, 26, & 27 (T2)
- **Lecture Slide Mapping**: CS4: Application Layer — Slides 1 to 41 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Principles of Network Applications: Client-Server Paradigms & Application Requirements
  2. The Web & HTTP Architecture: Non-Persistent vs. Persistent Connections, RTT Delays & Pipelining
  3. HTTP Message Formats, Status Codes, Cookies, Web Caching & The Conditional GET Mechanism
  4. Electronic Mail Infrastructure: User Agents (UA), Mail Transfer Agents (MTA) & Message Queues
  5. Simple Mail Transfer Protocol (SMTP, RFC 5321): Command-Response Handshake & Status Codes
  6. The Four Forouzan Mail Architecture Scenarios (Host-to-Host to Modern MAA Protocols)
  7. Architectural Comparison: SMTP vs. HTTP (Push vs. Pull, ASCII Constraints & Delimiters)
  8. Mail Access Protocols: POP3 (Three Phases) vs. IMAP (Hierarchical State) vs. Webmail (HTTP)
  9. Domain Name System (DNS): Distributed Hierarchical Architecture & Root/TLD/Authoritative Tiers
  10. DNS Name Resolution: Iterative vs. Recursive Queries & Caching Dynamics
  11. Resource Record (RR) Syntaxes (A, AAAA, NS, CNAME, MX) & 12-Byte Message Header Dissection
  12. DNS Security Realities: DDoS, Cache Poisoning, and DNSSEC
  13. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. Theoretical Foundations of Application Layer & The Web (HTTP)

### 2.1 Transport Services Required by Applications
Network applications require distinct guarantees across four core dimensions:
1. **Data Integrity / Loss Tolerance**: Applications like file transfer (FTP), email (SMTP), and web browsing (HTTP) mandate $100\%$ reliable data transfer (TCP). Loss-tolerant applications like VoIP and video streaming can tolerate slight packet loss (UDP).
2. **Throughput / Bandwidth**: Bandwidth-sensitive applications require guaranteed minimum throughput (e.g., $5\,\text{Mbps}$ for 4K video); elastic applications make use of whatever throughput is available.
3. **Timing / Latency**: Interactive gaming, virtual reality, and telephony require low delay ($< 100\,\text{ms}$).
4. **Security**: Encryption, data integrity, and endpoint authentication (TLS/SSL).

### 2.2 HTTP Architecture: Non-Persistent vs. Persistent Connections

```
NON-PERSISTENT HTTP/1.0 (Each object requires separate TCP connection):
Client                                                    Server
  |--- TCP SYN -------------------------------------------->|  \
  |<-- TCP SYN-ACK -----------------------------------------|  / 1 RTT (Handshake)
  |--- HTTP GET Object 1 ---------------------------------->|  \
  |<-- HTTP Response 200 OK (Data) -------------------------|  / 1 RTT + Trans Time
  |    (Connection Closed)                                  |
  |--- TCP SYN -------------------------------------------->|  \
  |<-- TCP SYN-ACK -----------------------------------------|  / 1 RTT (Handshake for Object 2)
  |--- HTTP GET Object 2 ---------------------------------->|  \
  |<-- HTTP Response 200 OK (Data) -------------------------|  / 1 RTT + Trans Time

PERSISTENT HTTP/1.1 (Reuses single TCP connection for all objects):
Client                                                    Server
  |--- TCP SYN -------------------------------------------->|  \
  |<-- TCP SYN-ACK -----------------------------------------|  / 1 RTT (Handshake)
  |--- HTTP GET Base HTML --------------------------------->|  \
  |<-- HTTP Response (Base HTML) ---------------------------|  / 1 RTT + Trans Time
  |--- HTTP GET Object 1 (Pipelined) ---------------------->|  \
  |--- HTTP GET Object 2 (Pipelined) ---------------------->|   | 1 RTT for multiple
  |<-- HTTP Response (Object 1) ----------------------------|   | referenced objects!
  |<-- HTTP Response (Object 2) ----------------------------|  /
```

- **Non-Persistent HTTP/1.0**:
  - Requires $2 \times RTT + \text{transmission time}$ per object ($1 \times RTT$ for TCP handshake, $1 \times RTT$ for HTTP request/response).
  - High OS socket overhead (allocating TCP buffers and state per object).
- **Persistent HTTP/1.1**:
  - Keeps TCP connection open after response. Subsequent referenced objects are downloaded over the same connection.
  - With **pipelining**, client sends requests for all referenced objects back-to-back as soon as discovered, saving multiple RTTs.

### 2.3 Web Caching & The Conditional GET Protocol
A web cache (proxy server) satisfies client requests without contacting the origin server:
1. Proxy server checks local cache for requested object.
2. If present, proxy sends a **Conditional GET** to the origin server:
   ```http
   GET /images/logo.png HTTP/1.1
   Host: www.bits-pilani.ac.in
   If-Modified-Since: Thu, 12 Aug 2026 14:30:00 GMT
   ```
3. If the object has not changed, origin server responds with:
   ```http
   HTTP/1.1 304 Not Modified
   ```
   (Contains **zero body data**, saving massive network bandwidth!).
4. If modified, origin server sends `HTTP/1.1 200 OK` with the new object data.

---

## 3. Electronic Mail Infrastructure & Architecture (Slides 4–12)

Electronic mail consists of three major architectural entities:
1. **User Agent (UA)**: The local client interface ("mail reader") used to compose, read, and manage email (Outlook, Apple Mail, Thunderbird).
2. **Mail Server**: Runs continuously in the cloud/enterprise, maintaining a **user mailbox** (storage for incoming mail) and a **message queue** (spool of outgoing messages awaiting transfer).
3. **Simple Mail Transfer Protocol (SMTP)**: The protocol governing transmission of email between mail servers.

```
+---------------+           +-------------------+         +-------------------+           +---------------+
| ALICE's UA    |           | ALICE's SERVER    |         | BOB's SERVER      |           | BOB's UA      |
| (Composes     | -- SMTP ->| [ Message Queue ] |-- SMTP->| [ Bob's Mailbox ] |-- Access->| (Reads        |
|  email)       |           |   (MTA Client)    |         |   (MTA Server)    | (POP/IMAP)|  email)       |
+---------------+           +-------------------+         +-------------------+           +---------------+
```

### 3.1 The Four Architecture Scenarios (Forouzan Taxonomy, Slides 8–12)

| Scenario | Architectural Setup | Scope & Protocols Used |
| :--- | :--- | :--- |
| **Scenario 1 (Slide 8)** | Alice and Bob are registered on the **exact same central computer** (mainframe/server). | Purely internal: Sender UA deposits mail into receiver mailbox directly via file system. **Zero network protocols used**. |
| **Scenario 2 (Slide 9)** | Alice is on a mail server; Bob is on a remote mail server. | Alice's MTA client connects directly over the Internet via SMTP to Bob's MTA server. |
| **Scenario 3 (Slide 10)**| Alice is on a desktop PC connected to a local mail server via LAN; Bob is on a remote mail server. | Alice's UA uses MTA client to send mail to her local mail server; her server's MTA client transfers mail over WAN to Bob's MTA server. |
| **Scenario 4 (Slide 11–12)**| **Modern Internet Architecture**: Both Alice and Bob use personal workstations connected to separate mail servers. | 1. Alice UA $\to$ Alice Mail Server: **SMTP (MTA)**.<br>2. Alice Mail Server $\to$ Bob Mail Server: **SMTP (MTA)**.<br>3. Bob Mail Server $\to$ Bob UA: **Mail Access Protocol (MAA: POP3, IMAP, or HTTP)**. |

> [!IMPORTANT]
> **Why SMTP cannot be used by Bob to retrieve mail from his server**:
> SMTP is strictly a **push protocol** (client pushes data to a receiving server). Bob cannot "push" mail from the server to his computer; he must **pull** messages. Hence, dedicated **Message Access Agents (MAA)** like POP3, IMAP, or HTTP are required.

---

## 4. SMTP Deep Dive & Protocol Interaction (Slides 6, 13–18)

- Defined in **RFC 5321** (originally RFC 821).
- Operates over reliable **TCP on port 25** (server-to-server) or port 587 (client-to-server submission with STARTTLS).
- Direct transfer: Sending mail server establishes a direct TCP connection to the receiving mail server.
- **Three Phases of Transfer**:
  1. Handshaking (Connection establishment & greeting).
  2. Message Transfer (Envelope, headers, body payload).
  3. Connection Closure.

### 4.1 SMTP Command Set (Slide 13)

| Command | Argument | Functional Specification |
| :--- | :--- | :--- |
| `HELO` / `EHLO` | Sender's fully qualified domain | Identifies the client host to the SMTP server (EHLO enables Extended SMTP). |
| `MAIL FROM:` | Sender email address | Initiates mail transaction; identifies the sender envelope return path. |
| `RCPT TO:` | Intended recipient address | Identifies a recipient. Can be repeated multiple times for multiple recipients. |
| `DATA` | None | Informs server that subsequent lines contain the actual message text and headers. |
| `.` | (Period on a single line) | Terminates message data input: `\r\n.\r\n`. |
| `RSET` | None | Aborts the current mail transaction; resets state without closing TCP connection. |
| `VRFY` | Username / Address | Verifies if a mailbox name exists on the receiving server without sending mail. |
| `NOOP` | None | No operation; checks if receiver is still alive and responsive. |
| `QUIT` | None | Requests the server to close the TCP connection gracefully. |

### 4.2 SMTP Status Code Classifications (Slides 14–15)
SMTP responses use 3-digit ASCII status codes:
- **`2xx` (Positive Completion)**:
  - `220`: Service ready.
  - `250`: Requested mail action completed (OK).
  - `221`: Service closing transmission channel (Goodbye).
- **`3xx` (Positive Intermediate Reply)**:
  - `354`: Start mail input; end with `<CRLF>.<CRLF>`.
- **`4xx` (Transient Negative Completion / Temporary Failure)**:
  - `421`: Service not available (server shutting down).
  - `450`: Mailbox unavailable (e.g., mailbox locked or busy).
  - `452`: Insufficient system storage.
- **`5xx` (Permanent Negative Completion / Fatal Error)**:
  - `500`: Syntax error, command unrecognized.
  - `550`: Mailbox unavailable (user not found).
  - `553`: Requested action not taken (mailbox name invalid).

### 4.3 Full Dialogue Trace (Slide 16)
```text
S: 220 hamburger.edu Service Ready
C: HELO crepes.fr
S: 250 Hello crepes.fr, pleased to meet you
C: MAIL FROM: <alice@crepes.fr>
S: 250 alice@crepes.fr... Sender ok
C: RCPT TO: <bob@hamburger.edu>
S: 250 bob@hamburger.edu... Recipient ok
C: DATA
S: 354 Enter mail, end with "." on a line by itself
C: From: alice@crepes.fr
C: To: bob@hamburger.edu
C: Subject: Dinner plans
C:
C: Do you like ketchup?
C: How about pickles?
C: .
S: 250 Message accepted for delivery
C: QUIT
S: 221 hamburger.edu closing connection
```

---

## 5. Architectural Comparison: SMTP vs. HTTP (Slide 18)

| Technical Dimension | Simple Mail Transfer Protocol (SMTP) | Hypertext Transfer Protocol (HTTP) |
| :--- | :--- | :--- |
| **Transmission Direction** | **Push protocol**: Sending host pushes file to receiving mail server. | **Pull protocol**: Client pulls requested file/object from web server. |
| **Data Encoding Format** | **Strict 7-bit ASCII**. Binary data (images, audio) must be encoded via MIME (Base64). | **Binary-safe (8-bit clean)**; transports raw binary streams without transformation. |
| **Message Encapsulation** | Multiple objects (text, attachments) are combined into a **single multipart message**. | Each media object is requested and encapsulated in its **own separate response message**. |
| **End of Message Delimiter**| Determined by searching for the character sequence: `\r\n.\r\n` (CRLF.CRLF). | Determined via `Content-Length` header or `Transfer-Encoding: chunked`. |
| **TCP Port** | Port 25 (Server-to-Server), Port 587 (Submission). | Port 80 (Plain HTTP), Port 443 (HTTPS). |

---

## 6. Mail Access Protocols: POP3 vs. IMAP vs. Webmail (Slides 20–23)

```
+-----------------------------------------------------------------------------------------+
|                                MAIL ACCESS PROTOCOLS                                    |
|                                                                                         |
| 1. POP3 (Post Office Protocol v3 - RFC 1939):                                           |
|    - Port 110. Extremely simple. Downloads messages to local PC.                       |
|    - Two operational modes:                                                             |
|      * Download-and-Delete: Messages removed from server upon retrieval.                |
|      * Download-and-Keep: Messages preserved on server.                                 |
|    - Stateless across client sessions; cannot synchronize folders across devices.       |
|                                                                                         |
| 2. IMAP (Internet Mail Access Protocol - RFC 3501):                                     |
|    - Port 143. Stateful and rich. Messages permanently reside on the mail server.       |
|    - Supports hierarchical remote folders (Inbox, Sent, Archive, Drafts).               |
|    - Seamless multi-device synchronization (phone, laptop, desktop see same state).     |
|    - Allows partial downloading (fetch message header only, without heavy attachments). |
|                                                                                         |
| 3. Web-Based Email (Gmail, Yahoo, Outlook.com):                                         |
|    - Browser communicates with mail server via HTTP/HTTPS.                              |
|    - User's mail server communicates with destination mail server via standard SMTP.    |
+-----------------------------------------------------------------------------------------+
```

---

## 7. Domain Name System (DNS) Architecture (Slides 24–36)

### 7.1 The Scaling Problem: Why DNS Cannot Be Centralized (Slide 25)
DNS translates human-friendly hostnames (`www.bits-pilani.ac.in`) into machine-routable 32-bit IPv4 addresses (`13.127.154.71`) or 128-bit IPv6 addresses.
Centralizing DNS into a single master database is impossible due to:
1. **Single Point of Failure**: If the central database crashes, the entire global Internet goes dark.
2. **Gigantic Traffic Volume**: Billions of hosts making trillions of queries per day (Akamai handles 2.2 Trillion DNS queries/day).
3. **Distant Centralized Geographies**: Severe propagation delay for overseas hosts.
4. **Maintenance Nightmares**: Millions of updates per second across global organizations.

### 7.2 The Three-Tier Distributed Hierarchy (Slides 27–30)

```
                                  [ ROOT DNS SERVERS ]
                       (13 logical root server addresses: a.root-servers.net
                        to m.root-servers.net; 1000+ anycast physical nodes)
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
 [ .com TLD SERVERS ]             [ .edu TLD SERVERS ]              [ .org / .in TLD ]
 (Managed by Verisign)            (Managed by Educause)             (Country-code TLDs)
        |                                 |                                 |
 [ amazon.com Name Server ]       [ bits-pilani.ac.in Server ]      [ wikipedia.org Server ]
 (Authoritative for Amazon)       (Authoritative for BITS)          (Authoritative)
```

1. **Root Name Servers**: Official contact-of-last-resort. Return the IP addresses of the corresponding Top-Level Domain (TLD) servers. Managed by ICANN.
2. **Top-Level Domain (TLD) Servers**: Responsible for generic domains (`.com`, `.org`, `.net`, `.edu`, `.gov`) and country-code domains (`.in`, `.uk`, `.de`, `.jp`).
3. **Authoritative DNS Servers**: An organization's own name server(s) that store the actual definitive mappings of hostnames to IP addresses for that organization.
4. **Local DNS Server (Default Name Server)**: Does not strictly belong to the hierarchy. Each ISP or enterprise operates a local DNS resolver. When a client issues a query, it is sent to the local DNS server, which acts as a proxy, traversing the hierarchy on behalf of the client.

### 7.3 Iterated vs. Recursive Queries (Slides 32–33)

```
ITERATED QUERY (Standard Practice):              RECURSIVE QUERY:
Local DNS does the work; contacted              Contacted server assumes the burden
servers return referrals:                       of querying upstream servers:

Requester                                       Requester
   |                                               |
   | (1) Query gaia.cs.umass.edu                   | (1) Query gaia.cs.umass.edu
   v                                               v
[ Local DNS ] ----(2) Query root--------> [Root] [ Local DNS ] ---> [Root] ---> [TLD] ---> [Auth]
            <---(3) Referral to .edu TLD- [Root]              <---        <---       <---
            ----(4) Query .edu TLD------> [TLD]   (Heavy processing load placed on Root/TLD)
            <---(5) Referral to umass.edu [TLD]
            ----(6) Query umass.edu-----> [Auth]
            <---(7) IP: 128.119.245.12--- [Auth]
   |
   | (8) Returns IP to client
   v
```

> [!TIP]
> **Why the Internet Uses Iterated Queries at the Core**:
> Recursive queries force upper-level servers (Root and TLD) to hold connection state and buffer millions of concurrent transactions. To prevent catastrophic collapse, Root and TLD servers reject recursive requests and provide only iterated referrals.

---

## 8. DNS Resource Records (RR) & Message Formats (Slides 36–38)

A DNS database stores **Resource Records (RRs)** formatted as a 4-tuple:
$$\text{RR} = (\text{Name}, \text{Value}, \text{Type}, \text{TTL})$$

### 8.1 The Five Essential RR Types (Slide 36)

| Type | Name Field | Value Field | Architectural Purpose |
| :--- | :--- | :--- | :--- |
| **A** | Hostname | IPv4 Address ($32\text{-bit}$) | Standard forward hostname-to-IPv4 resolution (e.g., `relay1.foo.com` $\to$ `145.37.93.126`). |
| **AAAA** | Hostname | IPv6 Address ($128\text{-bit}$)| Forward hostname-to-IPv6 resolution. |
| **NS** | Domain Name | Hostname of Authoritative Server| Identifies authoritative name server for the specified domain (e.g., `foo.com` $\to$ `dns.foo.com`). |
| **CNAME**| Alias Hostname | Canonical Hostname | Maps an alias to the real (canonical) hostname (e.g., `www.ibm.com` $\to$ `servereast.backup2.ibm.com`). |
| **MX** | Domain Name | Hostname of Mail Server | Identifies the mail exchange server for that domain (e.g., `bits-pilani.ac.in` $\to$ `mail.bits-pilani.ac.in`). |

### 8.2 The 12-Byte DNS Message Header Structure (Slide 37)
DNS query and reply messages share an identical format:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       IDENTIFICATION (16 bits) | QR | Opcode|AA|TC|RD|RA|Z|RCODE|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     NUMBER OF QUESTIONS (16)   |    NUMBER OF ANSWER RRs (16)  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    NUMBER OF AUTHORITY RRs (16)|   NUMBER OF ADDITIONAL RRs(16)|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    QUESTIONS (Variable Length)                |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 ANSWERS: RRs responding to query               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|             AUTHORITY: RRs for authoritative servers          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            ADDITIONAL INFORMATION: Helpful extra RRs          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **Identification (16 bits)**: Unique query tag; reply echoes this ID to match asynchronous UDP transactions.
- **Flags**:
  - `QR (1 bit)`: 0 = Query, 1 = Reply.
  - `AA (1 bit)`: Authoritative Answer flag.
  - `TC (1 bit)`: Truncated message flag (set if UDP payload exceeded 512 bytes).
  - `RD (1 bit)`: Recursion Desired.
  - `RA (1 bit)`: Recursion Available in reply.
  - `RCODE (4 bits)`: Return code (0 = No error, 3 = Name error / NXDOMAIN).

---

## 9. Open-Book Exam Traps & Examiner Tricks

1. **The SMTP Header vs. Envelope Trap**:
   - *Trap*: Conflating `MAIL FROM:` in SMTP with the `From:` header in the mail body.
   - *Fact*: `MAIL FROM:` is part of the **SMTP transport envelope** (read by servers for delivery/bounces). The `From:` header inside `DATA` is part of the **RFC 2822 mail message body** displayed to the user. They can be completely different (the basis of email address spoofing!).
2. **The CNAME vs. A Record Trap**:
   - *Trap*: Creating a CNAME that points directly to an IP address.
   - *Fact*: A CNAME record **must point to another hostname (canonical name)**, NEVER to an IP address. An A record points to an IP address.
3. **The DNS Transport Layer Trap**:
   - *Question*: *"Does DNS run exclusively over UDP?"*
   - *Fact*: **No!** DNS uses **UDP port 53** for standard client queries ($< 512\,\text{bytes}$). However, DNS switches to **TCP port 53** for:
     1. DNS Zone Transfers between primary and secondary name servers.
     2. Responses exceeding 512 bytes (or DNSSEC signatures) where the `TC` (Truncation) flag is set.

---

## 10. Solved High-Yield Numerical Exam Problems

### Problem 1: Total Web Page Download Latency with Caching
**Problem Statement**:
A client browser requests an HTML base document of size $10\,\text{KB}$. The base document references $8$ small embedded JPEG images (each $5\,\text{KB}$).
The one-way propagation delay between the client and web server is $d_{\text{prop}} = 25\,\text{ms}$ ($RTT = 50\,\text{ms}$).
The link transmission bandwidth is $R = 10\,\text{Mbps}$.
Assume zero processing and queuing delays, and ignore transmission time of TCP control packets.
1. Calculate total elapsed time to download the entire page using **Non-Persistent HTTP/1.0 without parallel connections**.
2. Calculate total elapsed time using **Persistent HTTP/1.1 with Pipelining**.
3. If a local proxy server has a cache hit rate of $75\%$ for the images, and the round-trip time between client and cache is $RTT_{\text{cache}} = 4\,\text{ms}$, calculate the new total download time under persistent HTTP.

**Step-by-Step Solution**:

1. **Non-Persistent HTTP/1.0 (Sequential)**:
   - Total objects $= 1\text{ (base)} + 8\text{ (images)} = 9\text{ objects}$.
   - Each object requires a dedicated TCP 3-way handshake followed by HTTP request/response:
     $$\text{Time per object} = 2 \times RTT + \frac{L_i}{R}$$
   - Base HTML:
     $$d_{trans, base} = \frac{10 \times 10^3 \times 8}{10 \times 10^6} = 0.008\,\text{s} = 8\,\text{ms}$$
     $$T_{\text{base}} = 2 \times 50\,\text{ms} + 8\,\text{ms} = 108\,\text{ms}$$
   - Each image:
     $$d_{trans, img} = \frac{5 \times 10^3 \times 8}{10 \times 10^6} = 0.004\,\text{s} = 4\,\text{ms}$$
     $$T_{\text{img}} = 2 \times 50\,\text{ms} + 4\,\text{ms} = 104\,\text{ms}$$
   - Total sequential time:
     $$T_{\text{total, non-pers}} = T_{\text{base}} + 8 \times T_{\text{img}} = 108\,\text{ms} + (8 \times 104\,\text{ms}) = 108 + 832 = \mathbf{940\,\text{ms}}$$

2. **Persistent HTTP/1.1 with Pipelining**:
   - Connection establishment: $1 \times RTT = 50\,\text{ms}$.
   - Base HTML retrieval: $1 \times RTT + d_{trans, base} = 50\,\text{ms} + 8\,\text{ms} = 58\,\text{ms}$.
   - All 8 images requested pipelined in one burst:
     $$\text{Latency} = 1 \times RTT + \sum_{i=1}^8 d_{trans, img} = 50\,\text{ms} + (8 \times 4\,\text{ms}) = 50 + 32 = 82\,\text{ms}$$
   - Total time:
     $$T_{\text{total, pers}} = 50\,\text{ms} + 58\,\text{ms} + 82\,\text{ms} = \mathbf{190\,\text{ms}} \quad (\mathbf{4.95\times\text{ faster!}})$$

3. **With Local Web Proxy Caching (75% hit rate)**:
   - Out of 8 images: $75\% \times 8 = 6\text{ images}$ cached locally; $2\text{ images}$ fetched from origin.
   - Base HTML fetched from origin: $50\,\text{ms} + 58\,\text{ms} = 108\,\text{ms}$.
   - Cached images from proxy: $1 \times RTT_{\text{cache}} + (6 \times 4\,\text{ms}) = 4\,\text{ms} + 24\,\text{ms} = 28\,\text{ms}$.
   - Origin images: $1 \times RTT_{\text{origin}} + (2 \times 4\,\text{ms}) = 50\,\text{ms} + 8\,\text{ms} = 58\,\text{ms}$.
   - Total time $= 108 + \max(28, 58) = 108 + 58 = \mathbf{166\,\text{ms}}$.

---

### Problem 2: DNS Resolution Latency Trace (Iterative vs. Recursive)
**Problem Statement**:
Host A wishes to resolve the hostname `engineering.nyu.edu`.
The local DNS server has empty caches.
- $RTT$ between Host A and Local DNS $= 2\,\text{ms}$.
- $RTT$ between Local DNS and Root Server $= 40\,\text{ms}$.
- $RTT$ between Local DNS and `.edu` TLD Server $= 30\,\text{ms}$.
- $RTT$ between Local DNS and NYU Authoritative Server $= 20\,\text{ms}$.
1. Calculate total time until Host A receives the IP address under standard **Iterated Resolution**.
2. If the local name server permanently caches the `.edu` TLD server IP address, what is the new lookup latency for subsequent `.edu` queries?

**Step-by-Step Solution**:

1. **Iterated Resolution Trace**:
   - Step 1: Host A queries Local DNS $\to 1 \times RTT_{\text{local}} = 2\,\text{ms}$.
   - Step 2: Local DNS queries Root server $\to 1 \times RTT_{\text{root}} = 40\,\text{ms}$ (receives referral to `.edu` TLD).
   - Step 3: Local DNS queries `.edu` TLD server $\to 1 \times RTT_{\text{TLD}} = 30\,\text{ms}$ (receives referral to NYU authoritative).
   - Step 4: Local DNS queries NYU Authoritative server $\to 1 \times RTT_{\text{auth}} = 20\,\text{ms}$ (receives Type A record).
   - Step 5: Local DNS replies to Host A $\to$ (covered in initial local RTT).
   $$\text{Total Iterated Latency} = 2 + 40 + 30 + 20 = \mathbf{92\,\text{ms}}$$

2. **With TLD Caching Enabled**:
   - The Root server query is completely bypassed!
   $$\text{New Latency} = RTT_{\text{local}} + RTT_{\text{TLD}} + RTT_{\text{auth}} = 2 + 30 + 20 = \mathbf{52\,\text{ms}} \quad (\mathbf{43.5\%\text{ reduction}})$$

---

## 11. Ultra-Fast Exam Revision Checklist
- [ ] HTTP/1.0 is non-persistent ($2 RTT + \text{trans}$ per object); HTTP/1.1 is persistent (reuses TCP connection).
- [ ] Conditional GET: Uses `If-Modified-Since` header; server replies with `304 Not Modified` (zero body) if unchanged.
- [ ] SMTP operates over TCP port 25; strict 7-bit ASCII; message ended by `\r\n.\r\n`.
- [ ] SMTP is a push protocol; POP3/IMAP/HTTP are pull protocols (Message Access Agents).
- [ ] POP3 is simple and download-and-delete/keep; IMAP maintains stateful remote folder hierarchy across devices.
- [ ] DNS is a distributed, hierarchical database: Root $\to$ TLD $\to$ Authoritative.
- [ ] Iterative Query: Local DNS queries each tier sequentially; contacted server returns referrals.
- [ ] Recursive Query: Contacted server takes burden of resolving entire query.
- [ ] RR Types: A (IPv4), AAAA (IPv6), NS (Name Server), CNAME (Canonical Alias), MX (Mail Server).
- [ ] DNS Header: 12 bytes fixed; includes Identification (16 bits), Flags (QR, AA, TC, RD, RA, RCODE).
