#!/usr/bin/env python3
"""
Comprehensive Vector SVG Library for AeroGrid Solution.
Zero syntax errors, high aesthetic appeal, spacious layouts, and crisp vector typography.
"""

def get_context_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 480" width="100%" height="100%" style="background:#ffffff; font-family:'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cTierGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="cBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#e0f2fe"/>
    </linearGradient>
    <linearGradient id="cAmber" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#fef3c7"/>
    </linearGradient>
    <linearGradient id="cPurple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f3e8ff"/>
    </linearGradient>
    <filter id="cShadow" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
    <marker id="cArrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#0284c7" />
    </marker>
  </defs>

  <!-- Stakeholders Box -->
  <g transform="translate(30, 40)" filter="url(#cShadow)">
    <rect width="250" height="390" rx="10" fill="url(#cTierGrad)" stroke="#38bdf8" stroke-width="2"/>
    <text x="125" y="32" text-anchor="middle" font-size="14" font-weight="bold" fill="#0369a1">Primary Stakeholders</text>
    
    <g transform="translate(20, 60)">
      <rect width="210" height="130" rx="8" fill="url(#cBlue)" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="105" y="30" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">🚁 Drone Operators</text>
      <text x="105" y="55" text-anchor="middle" font-size="10.5" fill="#475569">• Hospital Emergency (Organs)</text>
      <text x="105" y="75" text-anchor="middle" font-size="10.5" fill="#475569">• Campus Security UAVs</text>
      <text x="105" y="95" text-anchor="middle" font-size="10.5" fill="#475569">• Commercial Parcel Delivery</text>
      <text x="105" y="115" text-anchor="middle" font-size="10" font-weight="600" fill="#0284c7">Mobile &amp; Dispatch API</text>
    </g>

    <g transform="translate(20, 220)">
      <rect width="210" height="130" rx="8" fill="url(#cBlue)" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="105" y="35" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">🎛️ Campus Air Traffic</text>
      <text x="105" y="55" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">Controller (ATC)</text>
      <text x="105" y="85" text-anchor="middle" font-size="10.5" fill="#475569">• 3D Live Airspace Radar</text>
      <text x="105" y="105" text-anchor="middle" font-size="10.5" fill="#475569">• Emergency Grounding Override</text>
    </g>
  </g>

  <!-- AeroGrid Cloud Platform (Center Box) -->
  <g transform="translate(340, 30)" filter="url(#cShadow)">
    <rect width="270" height="410" rx="12" fill="url(#cTierGrad)" stroke="#0284c7" stroke-width="2.5"/>
    <text x="135" y="32" text-anchor="middle" font-size="15" font-weight="bold" fill="#0369a1">AeroGrid Cloud Platform</text>
    
    <g transform="translate(25, 55)">
      <rect width="220" height="85" rx="8" fill="url(#cBlue)" stroke="#0284c7" stroke-width="1.6"/>
      <text x="110" y="30" text-anchor="middle" font-size="12" font-weight="bold" fill="#0369a1">Kong API Gateway &amp;</text>
      <text x="110" y="48" text-anchor="middle" font-size="12" font-weight="bold" fill="#0369a1">EMQX MQTT Broker</text>
      <text x="110" y="68" text-anchor="middle" font-size="10" fill="#64748b">TLS 1.3 • Token Auth</text>
    </g>

    <g transform="translate(25, 160)">
      <rect width="220" height="85" rx="8" fill="url(#cPurple)" stroke="#9333ea" stroke-width="1.6"/>
      <text x="110" y="30" text-anchor="middle" font-size="12" font-weight="bold" fill="#581c87">Kafka Event Backbone</text>
      <text x="110" y="50" text-anchor="middle" font-size="10" fill="#6b21a8">High-Throughput Streaming</text>
      <text x="110" y="68" text-anchor="middle" font-size="10" fill="#6b21a8">&gt;15,000 msgs/second</text>
    </g>

    <g transform="translate(25, 265)">
      <rect width="220" height="115" rx="8" fill="url(#cAmber)" stroke="#f59e0b" stroke-width="2"/>
      <text x="110" y="28" text-anchor="middle" font-size="12" font-weight="bold" fill="#78350f">Airspace Deconfliction</text>
      <text x="110" y="46" text-anchor="middle" font-size="12" font-weight="bold" fill="#78350f">&amp; Throttling Engine</text>
      <text x="110" y="70" text-anchor="middle" font-size="10" font-weight="600" fill="#92400e">• 85% Density Throttling</text>
      <text x="110" y="90" text-anchor="middle" font-size="10" font-weight="600" fill="#92400e">• Green Corridor Preemption</text>
    </g>
  </g>

  <!-- Edge & External Infrastructure (Right Box) -->
  <g transform="translate(670, 40)" filter="url(#cShadow)">
    <rect width="250" height="390" rx="10" fill="url(#cTierGrad)" stroke="#16a34a" stroke-width="2"/>
    <text x="125" y="32" text-anchor="middle" font-size="14" font-weight="bold" fill="#15803d">Edge &amp; External Systems</text>
    
    <g transform="translate(20, 50)">
      <rect width="210" height="65" rx="6" fill="url(#cBlue)" stroke="#38bdf8" stroke-width="1.4"/>
      <text x="105" y="28" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0f172a">🛸 50 Autonomous UAVs</text>
      <text x="105" y="48" text-anchor="middle" font-size="10" fill="#475569">MAVLink / 4G Telemetry</text>
    </g>

    <g transform="translate(20, 130)">
      <rect width="210" height="65" rx="6" fill="url(#cBlue)" stroke="#38bdf8" stroke-width="1.4"/>
      <text x="105" y="28" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0f172a">🛬 50 Smart Vertiports</text>
      <text x="105" y="48" text-anchor="middle" font-size="10" fill="#475569">Pad Controllers &amp; Chargers</text>
    </g>

    <g transform="translate(20, 210)">
      <rect width="210" height="65" rx="6" fill="url(#cBlue)" stroke="#38bdf8" stroke-width="1.4"/>
      <text x="105" y="28" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0f172a">📡 Campus Ground Radar</text>
      <text x="105" y="48" text-anchor="middle" font-size="10" fill="#475569">Civil Aviation &amp; Weather SCADA</text>
    </g>

    <g transform="translate(20, 290)">
      <rect width="210" height="65" rx="6" fill="url(#cBlue)" stroke="#38bdf8" stroke-width="1.4"/>
      <text x="105" y="28" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0f172a">💳 Campus ERP &amp; Billing</text>
      <text x="105" y="48" text-anchor="middle" font-size="10" fill="#475569">Cashless Payment Gateway</text>
    </g>
  </g>

  <!-- Connectors -->
  <line x1="280" y1="165" x2="340" y2="135" stroke="#0284c7" stroke-width="1.8" marker-end="url(#cArrow)"/>
  <line x1="280" y1="325" x2="340" y2="155" stroke="#0284c7" stroke-width="1.8" marker-end="url(#cArrow)"/>

  <line x1="475" y1="140" x2="475" y2="160" stroke="#0284c7" stroke-width="2" marker-end="url(#cArrow)"/>
  <line x1="475" y1="245" x2="475" y2="265" stroke="#9333ea" stroke-width="2" marker-end="url(#cArrow)"/>

  <line x1="610" y1="320" x2="670" y2="82" stroke="#0284c7" stroke-width="1.8" marker-end="url(#cArrow)"/>
  <line x1="610" y1="320" x2="670" y2="162" stroke="#0284c7" stroke-width="1.8" marker-end="url(#cArrow)"/>
  <line x1="670" y1="242" x2="610" y2="320" stroke="#0284c7" stroke-width="1.8" marker-end="url(#cArrow)"/>
  <line x1="610" y1="350" x2="670" y2="322" stroke="#0284c7" stroke-width="1.8" marker-end="url(#cArrow)"/>
</svg>"""

def get_use_case_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 630" width="100%" height="100%" style="background:#ffffff; font-family:'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="boundaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="ucGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#e0f2fe"/>
    </linearGradient>
    <linearGradient id="ucSpecialGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fffbeb"/>
      <stop offset="100%" stop-color="#fef3c7"/>
    </linearGradient>
    <linearGradient id="sysGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#0284c7" />
    </marker>
    <marker id="dashedArrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#b45309" />
    </marker>
  </defs>

  <!-- System Boundary Box -->
  <rect x="220" y="25" width="510" height="580" rx="14" fill="url(#boundaryGrad)" stroke="#0284c7" stroke-width="2.5" filter="url(#cardShadow)"/>
  <text x="475" y="55" text-anchor="middle" font-size="16" font-weight="bold" fill="#0369a1" letter-spacing="0.5">AeroGrid System Boundary</text>

  <!-- UC1 -->
  <g id="uc1" filter="url(#cardShadow)">
    <ellipse cx="370" cy="110" rx="115" ry="24" fill="url(#ucGrad)" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="370" y="115" text-anchor="middle" font-size="12.5" font-weight="600" fill="#0f172a">Authenticate Remote ID</text>
  </g>

  <!-- UC2 -->
  <g id="uc2" filter="url(#cardShadow)">
    <ellipse cx="370" cy="175" rx="115" ry="24" fill="url(#ucGrad)" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="370" y="180" text-anchor="middle" font-size="12.5" font-weight="600" fill="#0f172a">Check Vertiport Availability</text>
  </g>

  <!-- UC3 -->
  <g id="uc3" filter="url(#cardShadow)">
    <ellipse cx="370" cy="250" rx="115" ry="26" fill="url(#ucGrad)" stroke="#0284c7" stroke-width="2.2"/>
    <text x="370" y="255" text-anchor="middle" font-size="12.5" font-weight="700" fill="#0369a1">Reserve 3D Flight Corridor</text>
  </g>

  <!-- UC4: Included in UC3 -->
  <g id="uc4" filter="url(#cardShadow)">
    <ellipse cx="610" cy="250" rx="100" ry="24" fill="url(#ucGrad)" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="610" y="255" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Determine Priority Index</text>
  </g>

  <!-- UC5 -->
  <g id="uc5" filter="url(#cardShadow)">
    <ellipse cx="370" cy="330" rx="118" ry="26" fill="url(#ucGrad)" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="370" y="330" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Start Flight Mission &amp;</text>
    <text x="370" y="345" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Stream 3D Telemetry</text>
  </g>

  <!-- UC6: Payment -->
  <g id="uc6" filter="url(#cardShadow)">
    <ellipse cx="610" cy="330" rx="100" ry="24" fill="url(#ucGrad)" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="610" y="335" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Process Payment Fee</text>
  </g>

  <!-- UC7: Monitor Airspace Density -->
  <g id="uc7" filter="url(#cardShadow)">
    <ellipse cx="370" cy="415" rx="115" ry="24" fill="url(#ucGrad)" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="370" y="420" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Monitor Sector Density</text>
  </g>

  <!-- UC8: Dynamic Throttling (Highlighted amber oval) -->
  <g id="uc8" filter="url(#cardShadow)">
    <ellipse cx="610" cy="415" rx="105" ry="26" fill="url(#ucSpecialGrad)" stroke="#f59e0b" stroke-width="2.2"/>
    <text x="610" y="412" text-anchor="middle" font-size="12" font-weight="700" fill="#92400e">Dynamic Airspace</text>
    <text x="610" y="427" text-anchor="middle" font-size="12" font-weight="700" fill="#92400e">Sector Throttling</text>
  </g>

  <!-- UC9: Live Radar View -->
  <g id="uc9" filter="url(#cardShadow)">
    <ellipse cx="490" cy="500" rx="110" ry="24" fill="url(#ucGrad)" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="490" y="505" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">View 3D Radar SCADA</text>
  </g>

  <!-- UC10: Revenue Dashboard -->
  <g id="uc10" filter="url(#cardShadow)">
    <ellipse cx="490" cy="565" rx="110" ry="24" fill="url(#ucGrad)" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="490" y="570" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">View Revenue &amp; Airway Dash</text>
  </g>

  <!-- ================= ACTORS ================= -->
  <!-- 1. DRONE OPERATOR (Stick Figure on Left) -->
  <g id="actorOperator" transform="translate(75, 175)">
    <circle cx="40" cy="30" r="16" fill="#ffffff" stroke="#1e293b" stroke-width="2.5"/>
    <line x1="40" y1="46" x2="40" y2="95" stroke="#1e293b" stroke-width="2.5"/>
    <line x1="12" y1="62" x2="68" y2="62" stroke="#1e293b" stroke-width="2.5"/>
    <line x1="40" y1="95" x2="18" y2="135" stroke="#1e293b" stroke-width="2.5"/>
    <line x1="40" y1="95" x2="62" y2="135" stroke="#1e293b" stroke-width="2.5"/>
    <text x="40" y="158" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">Drone Operator</text>
    <text x="40" y="173" text-anchor="middle" font-size="11" fill="#64748b">(Primary Actor)</text>
  </g>

  <!-- 2. AIR TRAFFIC CONTROLLER (Stick Figure on Bottom Right) -->
  <g id="actorATC" transform="translate(805, 415)">
    <circle cx="40" cy="30" r="16" fill="#ffffff" stroke="#1e293b" stroke-width="2.5"/>
    <line x1="40" y1="46" x2="40" y2="95" stroke="#1e293b" stroke-width="2.5"/>
    <line x1="12" y1="62" x2="68" y2="62" stroke="#1e293b" stroke-width="2.5"/>
    <line x1="40" y1="95" x2="18" y2="135" stroke="#1e293b" stroke-width="2.5"/>
    <line x1="40" y1="95" x2="62" y2="135" stroke="#1e293b" stroke-width="2.5"/>
    <text x="40" y="158" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">Campus ATC Admin</text>
    <text x="40" y="173" text-anchor="middle" font-size="11" fill="#64748b">(Secondary Actor)</text>
  </g>

  <!-- 3. GROUND RADAR SCADA (System Box on Bottom Left) -->
  <g id="actorRadar" transform="translate(25, 415)" filter="url(#cardShadow)">
    <rect x="0" y="0" width="150" height="60" rx="8" fill="url(#sysGrad)"/>
    <text x="75" y="25" text-anchor="middle" font-size="11" font-weight="600" fill="#e0f2fe">«System»</text>
    <text x="75" y="44" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#ffffff">Ground Radar SCADA</text>
  </g>

  <!-- 4. PAYMENT GATEWAY (System Box on Top Right) -->
  <g id="actorPayment" transform="translate(775, 175)" filter="url(#cardShadow)">
    <rect x="0" y="0" width="145" height="60" rx="8" fill="url(#sysGrad)"/>
    <text x="72" y="25" text-anchor="middle" font-size="11" font-weight="600" fill="#e0f2fe">«System»</text>
    <text x="72" y="44" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#ffffff">Payment Gateway</text>
  </g>

  <!-- Associations -->
  <line x1="145" y1="235" x2="255" y2="110" stroke="#475569" stroke-width="1.6"/>
  <line x1="145" y1="235" x2="255" y2="175" stroke="#475569" stroke-width="1.6"/>
  <line x1="145" y1="235" x2="255" y2="250" stroke="#475569" stroke-width="1.8"/>
  <line x1="145" y1="235" x2="255" y2="330" stroke="#475569" stroke-width="1.6"/>

  <line x1="175" y1="445" x2="255" y2="415" stroke="#475569" stroke-width="1.6"/>

  <!-- UC3 to UC4 (<<include>>) -->
  <path d="M 485 250 L 505 250" stroke="#0284c7" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#arrow)"/>
  <text x="495" y="240" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#0369a1">«include»</text>

  <!-- UC5 to UC6 (<<include>>) -->
  <path d="M 488 330 L 505 330" stroke="#0284c7" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#arrow)"/>
  <text x="495" y="320" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#0369a1">«include»</text>

  <line x1="710" y1="330" x2="775" y2="215" stroke="#475569" stroke-width="1.6"/>

  <!-- UC7 to UC8 (<<extend>>) -->
  <path d="M 485 415 L 500 415" stroke="#b45309" stroke-width="1.8" stroke-dasharray="5,3" marker-end="url(#dashedArrow)"/>
  <text x="495" y="403" text-anchor="middle" font-size="10" font-weight="bold" fill="#b45309">«extend»</text>
  <text x="495" y="431" text-anchor="middle" font-size="9" font-weight="bold" fill="#b45309">[Density &gt; 85%]</text>

  <!-- ATC Links -->
  <line x1="810" y1="465" x2="715" y2="425" stroke="#475569" stroke-width="1.5"/>
  <line x1="810" y1="465" x2="600" y2="500" stroke="#475569" stroke-width="1.6"/>
  <line x1="810" y1="465" x2="600" y2="565" stroke="#475569" stroke-width="1.6"/>
</svg>"""

def get_activity_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 820" width="100%" height="100%" style="background:#ffffff; font-family:'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="actBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#e0f2fe"/>
    </linearGradient>
    <linearGradient id="actAmber" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fffbeb"/>
      <stop offset="100%" stop-color="#fef3c7"/>
    </linearGradient>
    <linearGradient id="actGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#dcfce7"/>
    </linearGradient>
    <linearGradient id="actRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff1f2"/>
      <stop offset="100%" stop-color="#ffe4e6"/>
    </linearGradient>
    <filter id="actShadow" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.08"/>
    </filter>
    <marker id="actArrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#0284c7" />
    </marker>
  </defs>

  <!-- Start Node -->
  <circle cx="475" cy="30" r="14" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
  <text x="475" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">Mission Dispatch</text>

  <!-- Step 1: Pre-Flight -->
  <line x1="475" y1="44" x2="475" y2="75" stroke="#0284c7" stroke-width="2" marker-end="url(#actArrow)"/>
  <g transform="translate(325, 75)" filter="url(#actShadow)">
    <rect width="300" height="42" rx="8" fill="url(#actBlue)" stroke="#38bdf8" stroke-width="1.6"/>
    <text x="150" y="26" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Remote ID &amp; Battery Pre-Flight Handshake</text>
  </g>

  <!-- Decision 1: Auth Check -->
  <line x1="475" y1="117" x2="475" y2="145" stroke="#0284c7" stroke-width="2" marker-end="url(#actArrow)"/>
  <g transform="translate(475, 175)">
    <polygon points="0,-25 75,0 0,25 -75,0" fill="url(#actAmber)" stroke="#f59e0b" stroke-width="2"/>
    <text x="0" y="4" text-anchor="middle" font-size="11" font-weight="bold" fill="#78350f">Auth Valid?</text>
  </g>

  <!-- Branch: Auth Failed -->
  <line x1="550" y1="175" x2="680" y2="175" stroke="#e11d48" stroke-width="1.8" marker-end="url(#actArrow)"/>
  <text x="600" y="165" text-anchor="middle" font-size="10" font-weight="bold" fill="#e11d48">[No: Reject]</text>
  <g transform="translate(680, 155)" filter="url(#actShadow)">
    <rect width="180" height="40" rx="8" fill="url(#actRed)" stroke="#f43f5e" stroke-width="1.5"/>
    <text x="90" y="25" text-anchor="middle" font-size="11" font-weight="600" fill="#9f1239">Abort &amp; Log Diagnostic</text>
  </g>

  <!-- Branch: Auth Success -->
  <line x1="475" y1="200" x2="475" y2="230" stroke="#0284c7" stroke-width="2" marker-end="url(#actArrow)"/>
  <text x="495" y="218" font-size="10" font-weight="bold" fill="#16a34a">[Yes: Valid]</text>
  <g transform="translate(325, 230)" filter="url(#actShadow)">
    <rect width="300" height="42" rx="8" fill="url(#actBlue)" stroke="#38bdf8" stroke-width="1.6"/>
    <text x="150" y="26" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Compute Priority Index (Mission Role + SoC + W)</text>
  </g>

  <!-- Step 3: Takeoff -->
  <line x1="475" y1="272" x2="475" y2="300" stroke="#0284c7" stroke-width="2" marker-end="url(#actArrow)"/>
  <g transform="translate(325, 300)" filter="url(#actShadow)">
    <rect width="300" height="42" rx="8" fill="url(#actBlue)" stroke="#38bdf8" stroke-width="1.6"/>
    <text x="150" y="26" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Disengage Vertiport Clamps &amp; Climb to Altitude</text>
  </g>

  <!-- Decision 2: 85% Density Check -->
  <line x1="475" y1="342" x2="475" y2="370" stroke="#0284c7" stroke-width="2" marker-end="url(#actArrow)"/>
  <g transform="translate(475, 405)">
    <polygon points="0,-30 110,0 0,30 -110,0" fill="url(#actAmber)" stroke="#f59e0b" stroke-width="2"/>
    <text x="0" y="-3" text-anchor="middle" font-size="11" font-weight="bold" fill="#78350f">Airspace Sector</text>
    <text x="0" y="12" text-anchor="middle" font-size="11" font-weight="bold" fill="#78350f">Density &gt; 85%?</text>
  </g>

  <!-- Branch: Overload Yes -->
  <path d="M 365 405 L 210 405 L 210 455" stroke="#f59e0b" stroke-width="1.8" marker-end="url(#actArrow)"/>
  <text x="270" y="395" text-anchor="middle" font-size="10" font-weight="bold" fill="#b45309">[Yes: Density &gt; 85%]</text>
  <g transform="translate(90, 455)" filter="url(#actShadow)">
    <rect width="240" height="50" rx="8" fill="url(#actAmber)" stroke="#f59e0b" stroke-width="1.8"/>
    <text x="120" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#78350f">⚡ Dynamic Sector Throttling</text>
    <text x="120" y="38" text-anchor="middle" font-size="10" fill="#92400e">Low-Priority: Speed 25km/h / Hold</text>
  </g>

  <!-- Branch: Overload No (Normal) -->
  <path d="M 585 405 L 740 405 L 740 455" stroke="#16a34a" stroke-width="1.8" marker-end="url(#actArrow)"/>
  <text x="680" y="395" text-anchor="middle" font-size="10" font-weight="bold" fill="#16a34a">[No: Normal Density]</text>
  <g transform="translate(620, 455)" filter="url(#actShadow)">
    <rect width="240" height="50" rx="8" fill="url(#actGreen)" stroke="#16a34a" stroke-width="1.8"/>
    <text x="120" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">🟢 Standard Green Corridor</text>
    <text x="120" y="38" text-anchor="middle" font-size="10" fill="#166534">Optimal Cruise Speed (60-70 km/h)</text>
  </g>

  <!-- Merge into Flight Loop -->
  <path d="M 210 505 L 210 540 L 475 540" stroke="#0284c7" stroke-width="1.8"/>
  <path d="M 740 505 L 740 540 L 475 540" stroke="#0284c7" stroke-width="1.8" marker-end="url(#actArrow)"/>

  <!-- Step: In-Flight Telemetry Streaming -->
  <g transform="translate(325, 555)" filter="url(#actShadow)">
    <rect width="300" height="42" rx="8" fill="url(#actBlue)" stroke="#38bdf8" stroke-width="1.6"/>
    <text x="150" y="26" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Continuous Flight: Stream GPS, Altitude, Speed &amp; SoC</text>
  </g>

  <!-- Step: Land & Settle -->
  <line x1="475" y1="597" x2="475" y2="625" stroke="#0284c7" stroke-width="2" marker-end="url(#actArrow)"/>
  <g transform="translate(325, 625)" filter="url(#actShadow)">
    <rect width="300" height="42" rx="8" fill="url(#actBlue)" stroke="#38bdf8" stroke-width="1.6"/>
    <text x="150" y="26" text-anchor="middle" font-size="12" font-weight="600" fill="#0f172a">Precision Autonomous Landing on Destination Pad</text>
  </g>

  <!-- Step: Billing -->
  <line x1="475" y1="667" x2="475" y2="695" stroke="#0284c7" stroke-width="2" marker-end="url(#actArrow)"/>
  <g transform="translate(325, 695)" filter="url(#actShadow)">
    <rect width="300" height="42" rx="8" fill="url(#actGreen)" stroke="#16a34a" stroke-width="1.6"/>
    <text x="150" y="26" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">💳 Automated Tariff Settlement &amp; Invoice</text>
  </g>

  <!-- End Node -->
  <line x1="475" y1="737" x2="475" y2="765" stroke="#0284c7" stroke-width="2" marker-end="url(#actArrow)"/>
  <circle cx="475" cy="780" r="14" fill="#ffffff" stroke="#0f172a" stroke-width="2.5"/>
  <circle cx="475" cy="780" r="8" fill="#0f172a"/>
  <text x="475" y="810" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">Mission Concluded</text>
</svg>"""

def get_class_diagram_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 680" width="100%" height="100%" style="background:#ffffff; font-family:'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="clsHeadGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
    <filter id="clsShadow" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Class 1: User -->
  <g transform="translate(30, 20)" filter="url(#clsShadow)">
    <rect width="240" height="135" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.6"/>
    <path d="M 0 6 Q 0 0 6 0 L 234 0 Q 240 0 240 6 L 240 28 L 0 28 Z" fill="url(#clsHeadGrad)"/>
    <text x="120" y="19" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#ffffff">User (Abstract)</text>
    <!-- Attributes -->
    <text x="10" y="44" font-size="10.5" fill="#1e293b">- String userId</text>
    <text x="10" y="60" font-size="10.5" fill="#1e293b">- String fullName</text>
    <text x="10" y="76" font-size="10.5" fill="#1e293b">- String emailAddress</text>
    <line x1="0" y1="84" x2="240" y2="84" stroke="#e2e8f0" stroke-width="1"/>
    <!-- Methods -->
    <text x="10" y="100" font-size="10.5" fill="#0369a1">+ authenticate() bool</text>
    <text x="10" y="116" font-size="10.5" fill="#0369a1">+ updateProfile() void</text>
  </g>

  <!-- Class 2: DroneOperator -->
  <g transform="translate(30, 200)" filter="url(#clsShadow)">
    <rect width="240" height="150" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.6"/>
    <path d="M 0 6 Q 0 0 6 0 L 234 0 Q 240 0 240 6 L 240 28 L 0 28 Z" fill="url(#clsHeadGrad)"/>
    <text x="120" y="19" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#ffffff">DroneOperator</text>
    <!-- Attributes -->
    <text x="10" y="44" font-size="10.5" fill="#1e293b">- String pilotLicenseNo</text>
    <text x="10" y="60" font-size="10.5" fill="#1e293b">- String orgCategory</text>
    <text x="10" y="76" font-size="10.5" fill="#1e293b">- float accountBalance</text>
    <line x1="0" y1="84" x2="240" y2="84" stroke="#e2e8f0" stroke-width="1"/>
    <!-- Methods -->
    <text x="10" y="100" font-size="10.5" fill="#0369a1">+ bookCorridor() Reservation</text>
    <text x="10" y="116" font-size="10.5" fill="#0369a1">+ launchMission() bool</text>
    <text x="10" y="132" font-size="10.5" fill="#0369a1">+ triggerRTH() void</text>
  </g>

  <!-- Class 3: UAVDrone -->
  <g transform="translate(350, 20)" filter="url(#clsShadow)">
    <rect width="250" height="165" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.6"/>
    <path d="M 0 6 Q 0 0 6 0 L 244 0 Q 250 0 250 6 L 250 28 L 0 28 Z" fill="url(#clsHeadGrad)"/>
    <text x="125" y="19" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#ffffff">UAVDrone</text>
    <text x="10" y="44" font-size="10.5" fill="#1e293b">- String uavRegId</text>
    <text x="10" y="60" font-size="10.5" fill="#1e293b">- String remoteIdToken</text>
    <text x="10" y="76" font-size="10.5" fill="#1e293b">- float currentSoC</text>
    <text x="10" y="92" font-size="10.5" fill="#1e293b">- float maxPayloadKg</text>
    <line x1="0" y1="100" x2="250" y2="100" stroke="#e2e8f0" stroke-width="1"/>
    <text x="10" y="116" font-size="10.5" fill="#0369a1">+ streamTelemetry() Packet</text>
    <text x="10" y="132" font-size="10.5" fill="#0369a1">+ applySpeedOverride() void</text>
    <text x="10" y="148" font-size="10.5" fill="#0369a1">+ getPriorityRating() float</text>
  </g>

  <!-- Class 4: FlightMission -->
  <g transform="translate(350, 230)" filter="url(#clsShadow)">
    <rect width="250" height="175" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.6"/>
    <path d="M 0 6 Q 0 0 6 0 L 244 0 Q 250 0 250 6 L 250 28 L 0 28 Z" fill="url(#clsHeadGrad)"/>
    <text x="125" y="19" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#ffffff">FlightMission</text>
    <text x="10" y="44" font-size="10.5" fill="#1e293b">- String missionId</text>
    <text x="10" y="60" font-size="10.5" fill="#1e293b">- DateTime departureTime</text>
    <text x="10" y="76" font-size="10.5" fill="#1e293b">- float initialSoC</text>
    <text x="10" y="92" font-size="10.5" fill="#1e293b">- float totalDistanceKm</text>
    <text x="10" y="108" font-size="10.5" fill="#1e293b">- String status</text>
    <line x1="0" y1="116" x2="250" y2="116" stroke="#e2e8f0" stroke-width="1"/>
    <text x="10" y="132" font-size="10.5" fill="#0369a1">+ startMission() void</text>
    <text x="10" y="148" font-size="10.5" fill="#0369a1">+ completeMission() void</text>
    <text x="10" y="164" font-size="10.5" fill="#0369a1">+ computeDistance() float</text>
  </g>

  <!-- Class 5: VertiportHub & LandingPad -->
  <g transform="translate(680, 20)" filter="url(#clsShadow)">
    <rect width="240" height="150" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="1.6"/>
    <path d="M 0 6 Q 0 0 6 0 L 234 0 Q 240 0 240 6 L 240 28 L 0 28 Z" fill="url(#clsHeadGrad)"/>
    <text x="120" y="19" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#ffffff">VertiportHub</text>
    <text x="10" y="44" font-size="10.5" fill="#1e293b">- String hubId</text>
    <text x="10" y="60" font-size="10.5" fill="#1e293b">- String campusZone</text>
    <text x="10" y="76" font-size="10.5" fill="#1e293b">- int totalPads</text>
    <line x1="0" y1="84" x2="240" y2="84" stroke="#e2e8f0" stroke-width="1"/>
    <text x="10" y="100" font-size="10.5" fill="#0369a1">+ checkPadAvail() bool</text>
    <text x="10" y="116" font-size="10.5" fill="#0369a1">+ lockVertiport() void</text>
  </g>

  <!-- Class 6: AirspaceSectorController -->
  <g transform="translate(680, 230)" filter="url(#clsShadow)">
    <rect width="240" height="160" rx="6" fill="#ffffff" stroke="#f59e0b" stroke-width="2"/>
    <path d="M 0 6 Q 0 0 6 0 L 234 0 Q 240 0 240 6 L 240 28 L 0 28 Z" fill="#d97706"/>
    <text x="120" y="19" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#ffffff">AirspaceController</text>
    <text x="10" y="44" font-size="10.5" fill="#1e293b">- String sectorId</text>
    <text x="10" y="60" font-size="10.5" fill="#1e293b">- float maxDensityCap</text>
    <text x="10" y="76" font-size="10.5" fill="#1e293b">- float activeCount</text>
    <line x1="0" y1="84" x2="240" y2="84" stroke="#e2e8f0" stroke-width="1"/>
    <text x="10" y="100" font-size="10.5" fill="#92400e">+ pollRadarSCADA() Data</text>
    <text x="10" y="116" font-size="10.5" fill="#92400e">+ evalCollisionRisk() bool</text>
    <text x="10" y="132" font-size="10.5" fill="#92400e">+ throttleSector() void</text>
  </g>

  <!-- Class 7: BillingTransaction -->
  <g transform="translate(350, 460)" filter="url(#clsShadow)">
    <rect width="250" height="150" rx="6" fill="#ffffff" stroke="#16a34a" stroke-width="1.6"/>
    <path d="M 0 6 Q 0 0 6 0 L 244 0 Q 250 0 250 6 L 250 28 L 0 28 Z" fill="#15803d"/>
    <text x="125" y="19" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#ffffff">BillingTransaction</text>
    <text x="10" y="44" font-size="10.5" fill="#1e293b">- String txnId</text>
    <text x="10" y="60" font-size="10.5" fill="#1e293b">- float totalFee</text>
    <text x="10" y="76" font-size="10.5" fill="#1e293b">- String paymentStatus</text>
    <line x1="0" y1="84" x2="250" y2="84" stroke="#e2e8f0" stroke-width="1"/>
    <text x="10" y="100" font-size="10.5" fill="#14532d">+ processSettlement() bool</text>
    <text x="10" y="116" font-size="10.5" fill="#14532d">+ generateReceipt() Receipt</text>
  </g>

  <!-- Inheritance: DroneOperator -> User -->
  <line x1="150" y1="200" x2="150" y2="155" stroke="#0284c7" stroke-width="1.8"/>
  <polygon points="150,155 144,167 156,167" fill="#ffffff" stroke="#0284c7" stroke-width="1.8"/>

  <!-- Association: DroneOperator -> FlightMission -->
  <line x1="270" y1="280" x2="350" y2="280" stroke="#475569" stroke-width="1.6"/>
  <text x="280" y="272" font-size="10" fill="#475569">1</text>
  <text x="335" y="272" font-size="10" fill="#475569">0..*</text>

  <!-- Association: FlightMission -> UAVDrone -->
  <line x1="475" y1="230" x2="475" y2="185" stroke="#475569" stroke-width="1.6"/>
  <text x="480" y="222" font-size="10" fill="#475569">1</text>
  <text x="480" y="198" font-size="10" fill="#475569">1</text>

  <!-- Association: FlightMission -> BillingTransaction -->
  <line x1="475" y1="405" x2="475" y2="460" stroke="#475569" stroke-width="1.6"/>
  <text x="480" y="420" font-size="10" fill="#475569">1</text>
  <text x="480" y="450" font-size="10" fill="#475569">1</text>

  <!-- Dependency: AirspaceController -> FlightMission -->
  <line x1="680" y1="310" x2="600" y2="310" stroke="#d97706" stroke-width="1.6" stroke-dasharray="5,3"/>
  <text x="635" y="302" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#d97706">Regulates</text>
</svg>"""

def get_microservices_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 780" width="100%" height="100%" style="background:#ffffff; font-family:'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="tierGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="blueCard" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#e0f2fe"/>
    </linearGradient>
    <linearGradient id="amberCard" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#fef3c7"/>
    </linearGradient>
    <linearGradient id="greenCard" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#dcfce7"/>
    </linearGradient>
    <linearGradient id="purpleCard" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f3e8ff"/>
    </linearGradient>
    <filter id="tierShadow" x="-2%" y="-2%" width="104%" height="104%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
    <filter id="elemShadow" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.1"/>
    </filter>
    <marker id="mArrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#0284c7" />
    </marker>
    <marker id="mArrowAmber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#d97706" />
    </marker>
    <marker id="mArrowPurple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#9333ea" />
    </marker>
  </defs>

  <!-- ================= TIER 1: CLIENT & EDGE LAYER ================= -->
  <g transform="translate(30, 20)" filter="url(#tierShadow)">
    <rect width="890" height="110" rx="10" fill="url(#tierGrad)" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="20" y="24" font-size="13" font-weight="bold" fill="#0369a1">1. Edge, Mobile &amp; Sensor Layer</text>

    <!-- Edge Item 1 -->
    <g transform="translate(30, 38)" filter="url(#elemShadow)">
      <rect width="185" height="56" rx="6" fill="url(#blueCard)" stroke="#38bdf8" stroke-width="1.4"/>
      <text x="92" y="24" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">📱 Operator Client App</text>
      <text x="92" y="42" text-anchor="middle" font-size="10.5" fill="#475569">Flutter (iOS / Android)</text>
    </g>

    <!-- Edge Item 2 -->
    <g transform="translate(245, 38)" filter="url(#elemShadow)">
      <rect width="185" height="56" rx="6" fill="url(#blueCard)" stroke="#38bdf8" stroke-width="1.4"/>
      <text x="92" y="24" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">💻 ATC Radar Dashboard</text>
      <text x="92" y="42" text-anchor="middle" font-size="10.5" fill="#475569">React 18 / 3D WebGL</text>
    </g>

    <!-- Edge Item 3 -->
    <g transform="translate(460, 38)" filter="url(#elemShadow)">
      <rect width="185" height="56" rx="6" fill="url(#amberCard)" stroke="#f59e0b" stroke-width="1.4"/>
      <text x="92" y="24" text-anchor="middle" font-size="12" font-weight="bold" fill="#78350f">🛸 50 Autonomous UAVs</text>
      <text x="92" y="42" text-anchor="middle" font-size="10.5" fill="#b45309">MAVLink / 4G Telemetry</text>
    </g>

    <!-- Edge Item 4 -->
    <g transform="translate(675, 38)" filter="url(#elemShadow)">
      <rect width="185" height="56" rx="6" fill="url(#amberCard)" stroke="#f59e0b" stroke-width="1.4"/>
      <text x="92" y="24" text-anchor="middle" font-size="12" font-weight="bold" fill="#78350f">🛬 50 Vertiport Pads</text>
      <text x="92" y="42" text-anchor="middle" font-size="10.5" fill="#b45309">Pad Controllers / Modbus</text>
    </g>
  </g>

  <!-- Downward Arrows from Tier 1 to Tier 2 -->
  <path d="M 152 130 L 152 165" stroke="#0284c7" stroke-width="1.8" marker-end="url(#mArrow)"/>
  <path d="M 367 130 L 367 165" stroke="#0284c7" stroke-width="1.8" marker-end="url(#mArrow)"/>
  <path d="M 582 130 L 582 165" stroke="#d97706" stroke-width="1.8" marker-end="url(#mArrowAmber)"/>
  <path d="M 797 130 L 797 165" stroke="#d97706" stroke-width="1.8" marker-end="url(#mArrowAmber)"/>

  <!-- ================= TIER 2: INGRESS API & MQTT GATEWAY ================= -->
  <g transform="translate(30, 170)" filter="url(#tierShadow)">
    <rect width="890" height="95" rx="10" fill="url(#tierGrad)" stroke="#0284c7" stroke-width="1.8"/>
    <text x="20" y="24" font-size="13" font-weight="bold" fill="#0369a1">2. API Gateway &amp; Ingestion Layer</text>

    <!-- Kong API Gateway -->
    <g transform="translate(60, 36)" filter="url(#elemShadow)">
      <rect width="360" height="48" rx="6" fill="url(#blueCard)" stroke="#0284c7" stroke-width="1.6"/>
      <text x="180" y="22" text-anchor="middle" font-size="12" font-weight="bold" fill="#0369a1">🛡️ Kong Enterprise API Gateway</text>
      <text x="180" y="38" text-anchor="middle" font-size="10" fill="#475569">Reverse Proxy • Rate Limiting • OAuth 2.0 / JWT Auth</text>
    </g>

    <!-- EMQX MQTT Broker -->
    <g transform="translate(470, 36)" filter="url(#elemShadow)">
      <rect width="360" height="48" rx="6" fill="url(#amberCard)" stroke="#f59e0b" stroke-width="1.6"/>
      <text x="180" y="22" text-anchor="middle" font-size="12" font-weight="bold" fill="#92400e">⚡ EMQX Distributed MQTT Gateway</text>
      <text x="180" y="38" text-anchor="middle" font-size="10" fill="#b45309">High-Throughput Sensor Ingestion (&gt;15k msgs/sec)</text>
    </g>
  </g>

  <!-- Downward Arrows from Tier 2 to Tier 3 -->
  <path d="M 240 265 L 240 300" stroke="#0284c7" stroke-width="1.8" marker-end="url(#mArrow)"/>
  <path d="M 650 265 L 650 300" stroke="#d97706" stroke-width="1.8" marker-end="url(#mArrowAmber)"/>

  <!-- ================= TIER 3: DISTRIBUTED EVENT BACKBONE (KAFKA) ================= -->
  <g transform="translate(30, 305)" filter="url(#tierShadow)">
    <rect width="890" height="95" rx="10" fill="url(#tierGrad)" stroke="#9333ea" stroke-width="1.8"/>
    <text x="20" y="24" font-size="13" font-weight="bold" fill="#6b21a8">3. Distributed Event Backbone (Apache Kafka Cluster)</text>

    <!-- Topic 1 -->
    <g transform="translate(25, 36)" filter="url(#elemShadow)">
      <rect width="195" height="46" rx="6" fill="url(#purpleCard)" stroke="#c084fc" stroke-width="1.4"/>
      <text x="97" y="20" text-anchor="middle" font-size="11" font-weight="bold" fill="#581c87">Topic: telemetry.drone.3d</text>
      <text x="97" y="36" text-anchor="middle" font-size="9.5" fill="#6b21a8">2 Hz Telemetry Streams</text>
    </g>

    <!-- Topic 2 -->
    <g transform="translate(240, 36)" filter="url(#elemShadow)">
      <rect width="195" height="46" rx="6" fill="url(#purpleCard)" stroke="#c084fc" stroke-width="1.4"/>
      <text x="97" y="20" text-anchor="middle" font-size="11" font-weight="bold" fill="#581c87">Topic: airspace.density</text>
      <text x="97" y="36" text-anchor="middle" font-size="9.5" fill="#6b21a8">Sector Overload Feeds</text>
    </g>

    <!-- Topic 3 -->
    <g transform="translate(455, 36)" filter="url(#elemShadow)">
      <rect width="195" height="46" rx="6" fill="url(#purpleCard)" stroke="#c084fc" stroke-width="1.4"/>
      <text x="97" y="20" text-anchor="middle" font-size="11" font-weight="bold" fill="#581c87">Topic: commands.override</text>
      <text x="97" y="36" text-anchor="middle" font-size="9.5" fill="#6b21a8">Stepped Speed Throttling</text>
    </g>

    <!-- Topic 4 -->
    <g transform="translate(670, 36)" filter="url(#elemShadow)">
      <rect width="195" height="46" rx="6" fill="url(#purpleCard)" stroke="#c084fc" stroke-width="1.4"/>
      <text x="97" y="20" text-anchor="middle" font-size="11" font-weight="bold" fill="#581c87">Topic: flight.billing</text>
      <text x="97" y="36" text-anchor="middle" font-size="9.5" fill="#6b21a8">Completed Mission Invoices</text>
    </g>
  </g>

  <!-- Downward Arrows from Kafka to Microservices Tier -->
  <path d="M 122 400 L 122 435" stroke="#9333ea" stroke-width="1.8" marker-end="url(#mArrowPurple)"/>
  <path d="M 337 400 L 337 435" stroke="#9333ea" stroke-width="1.8" marker-end="url(#mArrowPurple)"/>
  <path d="M 552 400 L 552 435" stroke="#9333ea" stroke-width="1.8" marker-end="url(#mArrowPurple)"/>
  <path d="M 767 400 L 767 435" stroke="#9333ea" stroke-width="1.8" marker-end="url(#mArrowPurple)"/>

  <!-- ================= TIER 4: AUTONOMOUS MICROSERVICES TIER ================= -->
  <g transform="translate(30, 440)" filter="url(#tierShadow)">
    <rect width="890" height="150" rx="10" fill="url(#tierGrad)" stroke="#16a34a" stroke-width="1.8"/>
    <text x="20" y="24" font-size="13" font-weight="bold" fill="#15803d">4. Autonomous Core Microservices Tier (Docker / Kubernetes Cluster)</text>

    <!-- Svc 1 -->
    <g transform="translate(20, 38)" filter="url(#elemShadow)">
      <rect width="160" height="96" rx="6" fill="url(#greenCard)" stroke="#22c55e" stroke-width="1.4"/>
      <text x="80" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">🔐 Auth &amp; Remote ID</text>
      <text x="80" y="44" text-anchor="middle" font-size="9.5" fill="#166534">FAA Part 89 Remote ID</text>
      <text x="80" y="60" text-anchor="middle" font-size="9.5" fill="#166534">ECDSA Token Verify</text>
      <text x="80" y="78" text-anchor="middle" font-size="9.5" fill="#475569">Go Microservice</text>
    </g>

    <!-- Svc 2 -->
    <g transform="translate(195, 38)" filter="url(#elemShadow)">
      <rect width="160" height="96" rx="6" fill="url(#greenCard)" stroke="#22c55e" stroke-width="1.4"/>
      <text x="80" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">📅 Flight Booking Svc</text>
      <text x="80" y="44" text-anchor="middle" font-size="9.5" fill="#166534">3D Corridor Planning</text>
      <text x="80" y="60" text-anchor="middle" font-size="9.5" fill="#166534">Priority Computation</text>
      <text x="80" y="78" text-anchor="middle" font-size="9.5" fill="#475569">Python / FastAPI</text>
    </g>

    <!-- Svc 3: Highlighted Engine -->
    <g transform="translate(370, 38)" filter="url(#elemShadow)">
      <rect width="170" height="96" rx="6" fill="url(#amberCard)" stroke="#f59e0b" stroke-width="2"/>
      <text x="85" y="22" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#78350f">⚡ Airspace Deconflict</text>
      <text x="85" y="44" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#92400e">&gt;85% Load Throttling</text>
      <text x="85" y="60" text-anchor="middle" font-size="9.5" fill="#b45309">Green Corridor Clear</text>
      <text x="85" y="78" text-anchor="middle" font-size="9.5" fill="#475569">C++ / Go Engine</text>
    </g>

    <!-- Svc 4 -->
    <g transform="translate(555, 38)" filter="url(#elemShadow)">
      <rect width="160" height="96" rx="6" fill="url(#greenCard)" stroke="#22c55e" stroke-width="1.4"/>
      <text x="80" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">📊 3D Telemetry Radar</text>
      <text x="80" y="44" text-anchor="middle" font-size="9.5" fill="#166534">Live Heatmap Stream</text>
      <text x="80" y="60" text-anchor="middle" font-size="9.5" fill="#166534">Collision Avoidance</text>
      <text x="80" y="78" text-anchor="middle" font-size="9.5" fill="#475569">Node.js / WebSocket</text>
    </g>

    <!-- Svc 5 -->
    <g transform="translate(730, 38)" filter="url(#elemShadow)">
      <rect width="140" height="96" rx="6" fill="url(#greenCard)" stroke="#22c55e" stroke-width="1.4"/>
      <text x="70" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">💳 Billing Engine</text>
      <text x="70" y="44" text-anchor="middle" font-size="9.5" fill="#166534">Airway Tariffs</text>
      <text x="70" y="60" text-anchor="middle" font-size="9.5" fill="#166534">Pad Service Fee</text>
      <text x="70" y="78" text-anchor="middle" font-size="9.5" fill="#475569">Java / Spring Boot</text>
    </g>
  </g>

  <!-- Downward Arrows from Microservices to Databases -->
  <path d="M 275 590 L 275 625" stroke="#0284c7" stroke-width="1.8" marker-end="url(#mArrow)"/>
  <path d="M 455 590 L 455 625" stroke="#d97706" stroke-width="1.8" marker-end="url(#mArrowAmber)"/>
  <path d="M 635 590 L 635 625" stroke="#0284c7" stroke-width="1.8" marker-end="url(#mArrow)"/>

  <!-- ================= TIER 5: POLYGLOT PERSISTENCE TIER ================= -->
  <g transform="translate(30, 630)" filter="url(#tierShadow)">
    <rect width="890" height="120" rx="10" fill="url(#tierGrad)" stroke="#0284c7" stroke-width="1.8"/>
    <text x="20" y="24" font-size="13" font-weight="bold" fill="#0369a1">5. Polyglot Persistence Tier</text>

    <!-- DB 1 -->
    <g transform="translate(50, 36)" filter="url(#elemShadow)">
      <rect width="240" height="66" rx="8" fill="url(#blueCard)" stroke="#0284c7" stroke-width="1.6"/>
      <text x="120" y="25" text-anchor="middle" font-size="12" font-weight="bold" fill="#0369a1">🗄️ PostgreSQL RDBMS</text>
      <text x="120" y="44" text-anchor="middle" font-size="10" fill="#334155">ACID Compliant Transactions</text>
      <text x="120" y="58" text-anchor="middle" font-size="9.5" fill="#64748b">Users, Invoices, Vertiports</text>
    </g>

    <!-- DB 2 -->
    <g transform="translate(325, 36)" filter="url(#elemShadow)">
      <rect width="240" height="66" rx="8" fill="url(#amberCard)" stroke="#f59e0b" stroke-width="1.6"/>
      <text x="120" y="25" text-anchor="middle" font-size="12" font-weight="bold" fill="#92400e">⚡ Redis In-Memory Cluster</text>
      <text x="120" y="44" text-anchor="middle" font-size="10" fill="#334155">Sub-Millisecond Sector State</text>
      <text x="120" y="58" text-anchor="middle" font-size="9.5" fill="#64748b">Live Sector Density &amp; Pad Locks</text>
    </g>

    <!-- DB 3 -->
    <g transform="translate(600, 36)" filter="url(#elemShadow)">
      <rect width="240" height="66" rx="8" fill="url(#blueCard)" stroke="#0284c7" stroke-width="1.6"/>
      <text x="120" y="25" text-anchor="middle" font-size="12" font-weight="bold" fill="#0369a1">📈 TimescaleDB / InfluxDB</text>
      <text x="120" y="44" text-anchor="middle" font-size="10" fill="#334155">Time-Series Spatial Telemetry</text>
      <text x="120" y="58" text-anchor="middle" font-size="9.5" fill="#64748b">3D Coordinates, SoC Logs</text>
    </g>
  </g>
</svg>"""
