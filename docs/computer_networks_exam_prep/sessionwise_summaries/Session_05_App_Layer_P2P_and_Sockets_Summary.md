# Computer Networks (BSDCBZC481)
# Session 05: Peer-to-Peer Architectures & Socket Programming
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapter 2 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapter 25 (T2)
- **Lecture Slide Mapping**: CS5: Application Layer — Slides 1 to 31 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Peer-to-Peer (P2P) Architecture: Self-Scalability & Churn Dynamics
  2. Mathematical Derivation of File Distribution Time: Client-Server ($D_{c-s}$) vs. P2P ($D_{P2P}$)
  3. BitTorrent Protocol Mechanics: Torrents, Trackers, Swarms & 256 KB Chunks
  4. BitTorrent Game-Theoretic Policies: Rarest-First Requesting & Tit-for-Tat Optimistic Unchoking
  5. Socket Programming Fundamentals: Application Process vs. OS Kernel Boundaries
  6. TCP Socket Lifecycle: Welcoming Sockets (`ServerSocket`) vs. Connection Sockets (`Socket`)
  7. Java TCP Implementation: Step-by-Step Annotated Client & Server Code
  8. UDP Socket Lifecycle: Connectionless `DatagramSocket` & `DatagramPacket` Multiplexing
  9. Java UDP Implementation: Step-by-Step Annotated Client & Server Code
  10. Master Comparison Matrix: TCP Sockets vs. UDP Sockets
  11. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. Peer-to-Peer (P2P) Architectural Principles (Slide 4)

In contrast to the traditional Client-Server model where dedicated server farms handle all requests:
1. **No Always-On Central Server**: Direct communication occurs between arbitrary end systems called **peers**.
2. **Peers as Consumers and Providers**: Peers request services from other peers, and concurrently contribute upload capacity back to the swarm.
3. **Self-Scalability**: When new peers join, they bring new demand (files to download), but critically, they also **bring new service capacity** (their own upload bandwidth).
4. **Peer Churn**: Peers are intermittently connected, dynamically changing IP addresses as they connect, disconnect, or sleep.

```
CLIENT-SERVER MODEL (Bottleneck at Server):       PEER-TO-PEER (P2P) MODEL (Self-Scaling Swarm):
           [ Server ]                                     [Peer A] <=====> [Peer B]
          /    |     \                                       ^   \         /   ^
         v     v      v                                      |    \       /    |
     [PC 1] [PC 2]  [PC 3]                                   v     v     v     v
                                                          [Peer D] <=====> [Peer C]
```

---

## 3. File Distribution Time: Client-Server vs. P2P (Slides 5–8)

### 3.1 Problem Definition & Parameters
- File Size to distribute: $F$ bits.
- Number of participating clients/peers: $N$.
- Server upload bandwidth: $u_s$ bps.
- Peer $i$ upload bandwidth: $u_i$ bps.
- Peer $i$ download bandwidth: $d_i$ bps.
- Minimum peer download bandwidth: $d_{min} = \min_i(d_i)$.

### 3.2 Client-Server Distribution Time ($D_{c-s}$) (Slide 6)
In the client-server paradigm, the server must upload $N$ distinct copies of the file:
1. **Server Upload Bottleneck**: Time to send $N$ copies sequentially:
   $$T_{\text{server}} = \frac{N \cdot F}{u_s}$$
2. **Client Download Bottleneck**: The peer with the slowest access link ($d_{min}$) requires:
   $$T_{\text{client}} = \frac{F}{d_{min}}$$
3. **Total Client-Server Lower Bound**:
   $$D_{c-s} \ge \max\left(\frac{N \cdot F}{u_s}, \frac{F}{d_{min}}\right)$$

> [!IMPORTANT]
> **Client-Server Scaling Behavior**:
> As $N$ becomes large, $\frac{N \cdot F}{u_s}$ dominates. The minimum distribution time **grows strictly linearly with $N$** ($O(N)$). Distributing a 10 GB file to 100,000 clients collapses a central server unless massive CDNs are deployed.

### 3.3 Peer-to-Peer Distribution Time ($D_{P2P}$) (Slide 7)
In P2P, the server must only upload the initial copy, after which peers upload chunks to each other:
1. **Initial Server Upload**: The server must upload at least one copy of each chunk:
   $$T_{\text{server}} = \frac{F}{u_s}$$
2. **Slowest Peer Download**: The slowest peer still takes at least:
   $$T_{\text{client}} = \frac{F}{d_{min}}$$
3. **Aggregate Swarm Bandwidth Constraint**: Across the entire swarm, $N \cdot F$ bits must be downloaded. The maximum aggregate upload capacity of the entire system is the server's upload rate plus the sum of all peers' upload rates:
   $$\text{Total Upload Capacity} = u_s + \sum_{i=1}^N u_i$$
   $$\text{Aggregate Time} = \frac{N \cdot F}{u_s + \sum_{i=1}^N u_i}$$
4. **Total P2P Lower Bound**:
   $$D_{P2P} \ge \max\left(\frac{F}{u_s}, \frac{F}{d_{min}}, \frac{N \cdot F}{u_s + \sum_{i=1}^N u_i}\right)$$

### 3.4 Asymptotic Comparison (Slide 8)
If each peer has an identical upload bandwidth $u_i = u$:
$$\lim_{N \to \infty} \frac{N \cdot F}{u_s + N \cdot u} = \lim_{N \to \infty} \frac{F}{\frac{u_s}{N} + u} = \frac{F}{u}$$

```
Distribution
Time
  ^
  |                                        / (Client-Server: Linear O(N))
  |                                       /
  |                                      /
  |                                     /
  |                        ____________/
  |_______________________/---------------- (P2P: Asymptotically bounded by F/u)
  +----------------------------------------> Number of Peers (N)
```
While client-server distribution time explodes linearly, **P2P distribution time flattens out**, approaching an asymptotic ceiling of $\max\left(\frac{F}{d_{min}}, \frac{F}{u}\right)$.

---

## 4. The BitTorrent Protocol Deep Dive (Slides 9–12)

BitTorrent is the dominant P2P file-sharing protocol.

### 4.1 Swarm Architecture & Chunking (Slide 9–10)
- **Torrent**: The collection of all peers actively downloading or uploading a specific file.
- **Chunks**: The file is segmented into equal-sized chunks of **$256\,\text{KB}$**.
- **Tracker**: An infrastructure server that maintains the active membership list of all peers currently in the torrent.
- **Peer Lifecycle**:
  1. A new peer (Alice) joins the torrent with zero chunks.
  2. She registers with the tracker, which returns a random subset of peers (typically 50 peers, known as her **neighbors**).
  3. Alice establishes concurrent TCP connections to these neighboring peers.
  4. Once Alice acquires the complete file, she may selfishly depart or altruistically remain to **seed** the torrent.

### 4.2 Chunk Requesting Strategy: Rarest First (Slide 11)
- At any instant, different peers possess different subsets of the file's chunks.
- Alice periodically queries all her neighbors for their chunk bitmasks.
- **Rarest-First Policy**: Alice always requests the chunks that are the **least common (rarest)** among all her neighbors.
- **Benefits**:
  - Ensures rare chunks are duplicated quickly, preventing them from becoming extinct if a peer suddenly goes offline.
  - Leaves the most common chunks for last, ensuring every peer always has useful chunks to trade with others.

### 4.3 Chunk Uploading Policy: Tit-for-Tat & Optimistic Unchoking (Slides 11–12)
BitTorrent prevents "free-riding" through a game-theoretic **Tit-for-Tat (TFT)** incentive mechanism:

```
+-----------------------------------------------------------------------------------------+
|                              BITTORRENT TIT-FOR-TAT RULES                               |
|                                                                                         |
| 1. TOP-FOUR UNCHOKING (Every 10 seconds):                                               |
|    - Alice measures the incoming download rate from all her neighbors.                  |
|    - She unchokes (sends data to) the top 4 peers providing data at the highest rates.  |
|    - All other peers are CHOKED (receive zero bits from Alice).                         |
|                                                                                         |
| 2. OPTIMISTIC UNCHOKING (Every 30 seconds):                                             |
|    - Alice randomly selects one choked peer (Bob) and begins sending chunks to him.     |
|    - If Bob reciprocates by uploading to Alice at a high rate, Bob joins Alice's top 4!|
|    - Allows new peers (who have nothing to trade initially) to bootstrap chunks.        |
|    - Enables continuous discovery of better, faster peering partners across the swarm.  |
+-----------------------------------------------------------------------------------------+
```

---

## 5. Network Sockets & The Application Programming Interface (Slides 13–16)

A **socket** is the software abstraction ("doorway") through which an application process sends and receives messages to and from the network:

```
+-------------------------------------------------------------+
|                     APPLICATION PROCESS                     |
|           (User space: controlled by application developer) |
+-------------------------------------------------------------+
                               |   ^
                    inFromUser |   | outToUser
                               v   |
+-------------------------------------------------------------+
|                           SOCKET                            |
|       (OS API boundary: identified by IP + Port number)     |
+-------------------------------------------------------------+
                               |   ^
                               v   |
+-------------------------------------------------------------+
|              TRANSPORT LAYER (TCP or UDP in Kernel)         |
|             (Buffers, timers, state variables, flow control)|
+-------------------------------------------------------------+
```

### 5.1 Two Core Socket Types
1. **SOCK_STREAM (TCP)**: Provides a reliable, sequenced, bidirectional, full-duplex byte stream connection. Requires a 3-way handshake before data transfer.
2. **SOCK_DGRAM (UDP)**: Provides an unreliable, connectionless datagram service. Packets may arrive out-of-order, duplicated, or not at all. Zero connection setup.

---

## 6. TCP Client-Server Socket Interaction & Implementation (Slides 15–23)

### 6.1 The Two-Socket Architecture of TCP Servers (Slide 16–17)
Unlike UDP, a TCP server maintains two distinct socket objects:
1. **Welcoming Socket (`ServerSocket`)**: Bound to a well-known server port (e.g., 6789). It does NOT exchange data; its sole purpose is to listen for incoming TCP connection requests.
2. **Connection Socket (`Socket`)**: When a client initiates contact, `welcomeSocket.accept()` completes the TCP 3-way handshake and instantiates a brand-new dedicated socket for that specific client!
   - Enables the server to maintain concurrent, multiplexed connections with thousands of distinct clients simultaneously.

```
TCP SERVER (Host B)                                        TCP CLIENT (Host A)
welcomeSocket = ServerSocket(6789)
       |
       | <--- (1) TCP Connection Request (SYN) ------------ clientSocket = Socket("HostB", 6789)
       | ---> (2) TCP Connection Granted (SYN-ACK) --------
       | <--- (3) TCP ACK ---------------------------------
       |
connectionSocket = welcomeSocket.accept()
       |
       | <--- (4) Client sends data (clientSocket) -------- outToServer.writeBytes(...)
       |
read client data from connectionSocket
process / capitalize string
write response to connectionSocket -----------------------> inFromServer.readLine()
       |
close connectionSocket
```

### 6.2 Java Implementation: TCP Client (`TCPClient.java`) (Slides 20–21)
```java
import java.io.*;
import java.net.*;

class TCPClient {
    public static void main(String argv[]) throws Exception {
        String sentence;
        String modifiedSentence;

        // 1. Create input stream to read characters from keyboard
        BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));

        // 2. Create client socket and establish TCP 3-way handshake with server on port 6789
        Socket clientSocket = new Socket("hostname", 6789);

        // 3. Create output stream attached to the socket to transmit bytes to server
        DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());

        // 4. Create input stream attached to socket to receive returned bytes from server
        BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

        // 5. Read line from user, push out to socket
        sentence = inFromUser.readLine();
        outToServer.writeBytes(sentence + '\n');

        // 6. Read transformed response from server and print
        modifiedSentence = inFromServer.readLine();
        System.out.println("FROM SERVER: " + modifiedSentence);

        // 7. Close TCP connection
        clientSocket.close();
    }
}
```

### 6.3 Java Implementation: TCP Server (`TCPServer.java`) (Slides 22–23)
```java
import java.io.*;
import java.net.*;

class TCPServer {
    public static void main(String argv[]) throws Exception {
        String clientSentence;
        String capitalizedSentence;

        // 1. Create welcoming socket on well-known port 6789
        ServerSocket welcomeSocket = new ServerSocket(6789);

        // 2. Continuous loop listening for incoming clients
        while (true) {
            // Blocks waiting for client connection; returns dedicated connectionSocket
            Socket connectionSocket = welcomeSocket.accept();

            // Create input and output streams attached to dedicated connection socket
            BufferedReader inFromClient = new BufferedReader(
                new InputStreamReader(connectionSocket.getInputStream())
            );
            DataOutputStream outToClient = new DataOutputStream(
                connectionSocket.getOutputStream()
            );

            // Read line from client, capitalize it, and send back
            clientSentence = inFromClient.readLine();
            capitalizedSentence = clientSentence.toUpperCase() + '\n';
            outToClient.writeBytes(capitalizedSentence);

            // Close client socket (welcomeSocket remains open to accept next client!)
            connectionSocket.close();
        }
    }
}
```

---

## 7. UDP Client-Server Socket Interaction & Implementation (Slides 24–30)

### 7.1 Key Characteristics of UDP Sockets
- **No Handshaking**: Zero connection establishment latency (0-RTT).
- **Packet-Oriented**: Data is transmitted as independent self-contained units (`DatagramPacket`).
- **Explicit Addressing**: Every outgoing packet must explicitly specify the destination IP and destination port.
- **Single Server Socket**: A UDP server uses a single `DatagramSocket` to receive datagrams from all clients. The sender's IP and port are extracted directly from the incoming packet header.

### 7.2 Java Implementation: UDP Client (`UDPClient.java`) (Slides 27–28)
```java
import java.io.*;
import java.net.*;

class UDPClient {
    public static void main(String args[]) throws Exception {
        // 1. Create keyboard reader
        BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));

        // 2. Create UDP datagram socket (OS binds to arbitrary ephemeral port)
        DatagramSocket clientSocket = new DatagramSocket();

        // 3. Resolve destination hostname using DNS
        InetAddress IPAddress = InetAddress.getByName("hostname");

        byte[] sendData = new byte[1024];
        byte[] receiveData = new byte[1024];

        String sentence = inFromUser.readLine();
        sendData = sentence.getBytes();

        // 4. Encapsulate data + destination IP + destination Port into DatagramPacket
        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 9876);
        clientSocket.send(sendPacket);

        // 5. Receive reply packet
        DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
        clientSocket.receive(receivePacket);

        String modifiedSentence = new String(receivePacket.getData(), 0, receivePacket.getLength());
        System.out.println("FROM SERVER: " + modifiedSentence);

        clientSocket.close();
    }
}
```

### 7.3 Java Implementation: UDP Server (`UDPServer.java`) (Slides 29–30)
```java
import java.io.*;
import java.net.*;

class UDPServer {
    public static void main(String args[]) throws Exception {
        // 1. Create UDP socket bound to port 9876
        DatagramSocket serverSocket = new DatagramSocket(9876);

        byte[] receiveData = new byte[1024];
        byte[] sendData = new byte[1024];

        while (true) {
            // 2. Allocate buffer and block waiting for incoming datagram
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            serverSocket.receive(receivePacket);

            // 3. Extract sender's IP address and Port from the packet header
            InetAddress IPAddress = receivePacket.getAddress();
            int port = receivePacket.getPort();

            // 4. Process data
            String sentence = new String(receivePacket.getData(), 0, receivePacket.getLength());
            String capitalizedSentence = sentence.toUpperCase();
            sendData = capitalizedSentence.getBytes();

            // 5. Transmit reply back to the extracted IP and Port
            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, port);
            serverSocket.send(sendPacket);
        }
    }
}
```

---

## 8. Master Comparison Matrix: TCP vs. UDP Sockets

| Architectural Feature | TCP Sockets (`SOCK_STREAM`) | UDP Sockets (`SOCK_DGRAM`) |
| :--- | :--- | :--- |
| **Connection Setup** | Required ($3\text{-way handshake}$ via `connect()` / `accept()`). | None. Immediate transmission (0-RTT). |
| **Server Socket Model** | **Two sockets**: Welcoming socket (`ServerSocket`) + Connection socket. | **One socket**: Single `DatagramSocket` handles all clients. |
| **Data Transmission Unit**| **Byte stream**: continuous sequence without message boundaries. | **Datagrams**: discrete packets with preserved message boundaries. |
| **Addressing Mechanism** | Destination IP/Port specified once at socket creation. | Destination IP/Port attached explicitly to **every single packet**. |
| **Reliability Guarantees** | $100\%$ reliable, in-order delivery, flow control, congestion control. | Unreliable best-effort; packet loss, reordering, and duplicates possible. |
| **System Overhead** | High: kernel buffers, sequence numbers, timers, state variables. | Minimal: stateless, zero buffer maintenance. |

---

## 9. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The TCP Server Socket Duality Trap**:
   - *Question*: *"A TCP server is communicating with 50 distinct clients simultaneously. How many total sockets are open on the server?"*
   - *Trap*: Answering 1 socket or 50 sockets.
   - *Fact*: **51 sockets!** Exactly $1$ Welcoming Socket (`ServerSocket`) listening on port $X$, plus $50$ distinct Connection Sockets, each dedicated to one active client.
2. **The BitTorrent Free-Rider Trap**:
   - *Question*: *"Why don't all BitTorrent peers simply download chunks without ever uploading (free-riding)?"*
   - *Fact*: The **Tit-for-Tat algorithm** chokes any peer that does not upload at a high rate. Non-contributing peers are starved of bandwidth by the top-four unchoking rule.
3. **The UDP Message Boundary Trap**:
   - *Question*: *"If a UDP client sends three 100-byte packets, how many `receive()` calls must the server execute?"*
   - *Fact*: Exactly **3 calls**. UDP preserves message boundaries. In TCP, three 100-byte writes might be coalesced by Nagle's algorithm and read in a single 300-byte read, or split into arbitrary chunks!

---

## 10. Solved High-Yield Numerical Exam Problems

### Problem 1: Client-Server vs. P2P File Distribution Time
**Problem Statement**:
A content distributor needs to distribute a movie file of size $F = 20\,\text{GB}$ ($20 \times 10^9\,\text{bytes}$) to $N = 1,000$ clients.
- Server upload bandwidth: $u_s = 40\,\text{Mbps}$.
- Each client has a download bandwidth of $d = 10\,\text{Mbps}$ and an upload bandwidth of $u = 2\,\text{Mbps}$.
1. Calculate the minimum distribution time under the **Client-Server approach**.
2. Calculate the minimum distribution time under the **Peer-to-Peer approach**.
3. What is the distribution time under P2P if the swarm expands to $N = 100,000$ peers?

**Step-by-Step Solution**:

1. **Convert File Size to Bits**:
   $$F = 20 \times 10^9 \times 8 = 160 \times 10^9\,\text{bits} = 160\,\text{Gb}$$

2. **Client-Server Minimum Distribution Time ($D_{c-s}$)**:
   $$D_{c-s} \ge \max\left(\frac{N \cdot F}{u_s}, \frac{F}{d_{min}}\right)$$
   - Server upload time:
     $$\frac{N \cdot F}{u_s} = \frac{1,000 \times 160\,\text{Gb}}{40 \times 10^{-3}\,\text{Gbps}} = \frac{160,000}{0.040} = 4,000,000\,\text{seconds} \approx \mathbf{46.3\text{ days}!}$$
   - Client download time:
     $$\frac{F}{d_{min}} = \frac{160\,\text{Gb}}{10 \times 10^{-3}\,\text{Gbps}} = \frac{160}{0.010} = 16,000\,\text{seconds} \approx 4.44\,\text{hours}$$
   $$D_{c-s} = \max(4,000,000\,\text{s}, 16,000\,\text{s}) = \mathbf{4,000,000\,\text{seconds}} \approx \mathbf{46.3\text{ days}}$$

3. **P2P Minimum Distribution Time ($D_{P2P}$)**:
   $$D_{P2P} \ge \max\left(\frac{F}{u_s}, \frac{F}{d_{min}}, \frac{N \cdot F}{u_s + \sum_{i=1}^N u_i}\right)$$
   - Server upload one copy:
     $$\frac{F}{u_s} = \frac{160\,\text{Gb}}{0.040\,\text{Gbps}} = 4,000\,\text{seconds}$$
   - Client download:
     $$\frac{F}{d_{min}} = 16,000\,\text{seconds}$$
   - Swarm aggregate capacity:
     $$\sum_{i=1}^{1,000} u_i = 1,000 \times 2\,\text{Mbps} = 2,000\,\text{Mbps} = 2.0\,\text{Gbps}$$
     $$u_s + \sum u_i = 0.040\,\text{Gbps} + 2.0\,\text{Gbps} = 2.04\,\text{Gbps}$$
     $$\frac{N \cdot F}{u_s + \sum u_i} = \frac{160,000\,\text{Gb}}{2.04\,\text{Gbps}} \approx 78,431\,\text{seconds} \approx 21.79\,\text{hours}$$
   $$D_{P2P} = \max(4,000\,\text{s}, 16,000\,\text{s}, 78,431\,\text{s}) = \mathbf{78,431\,\text{seconds}} \approx \mathbf{21.79\text{ hours}}$$
   - **Performance Comparison**: P2P completes the distribution in under 22 hours, compared to 46 days for client-server ($51\times\text{ faster!}$).

4. **P2P Scaling to $N = 100,000$ Peers**:
   - Aggregate swarm upload rate $= 0.040 + (100,000 \times 0.002) = 200.04\,\text{Gbps}$.
   - Aggregate time:
     $$\frac{100,000 \times 160\,\text{Gb}}{200.04\,\text{Gbps}} = \frac{16,000,000}{200.04} \approx 79,984\,\text{seconds} \approx \mathbf{22.2\text{ hours}}$$
   - Even when increasing users by $100\times$, P2P distribution time increases by only **25 minutes**!

---

## 11. Ultra-Fast Exam Revision Checklist
- [ ] P2P Self-Scalability: New peers bring service capacity ($u_i$) alongside new demand.
- [ ] Client-Server lower bound: $D_{c-s} \ge \max(NF/u_s, F/d_{min})$ ($O(N)$ linear growth).
- [ ] P2P lower bound: $D_{P2P} \ge \max(F/u_s, F/d_{min}, NF/(u_s + \sum u_i))$ (asymptotically bounded by $F/u$).
- [ ] BitTorrent chunk size is $256\,\text{KB}$; Tracker coordinates active peers in swarm.
- [ ] BitTorrent request policy: Rarest-First (maximizes rare chunk replication).
- [ ] BitTorrent upload policy: Tit-for-Tat top 4 unchoking (every 10s) + Optimistic unchoking (every 30s).
- [ ] Socket: Application process API interface to transport layer.
- [ ] TCP Server maintains 2 sockets: Welcoming `ServerSocket` + dedicated connection `Socket`.
- [ ] TCP is byte-stream oriented; UDP is datagram-oriented (preserves message boundaries).
- [ ] UDP sockets require explicit destination IP and port on every outgoing packet.
