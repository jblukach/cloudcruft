# cloudcruft

Public IP addresses from a shared pool are automatically assigned using the Dynamic Host Configuration Protocol (DHCP) as resources launch. Addresses occasionally develop a poor reputation on the Internet before being returned. The following organization blindly assumes those addresses, which can result in a negative customer experience.

Cloudcruft captures DNS, IPv4, and IPv6 atomic indicators from Open-Source Intelligence (OSINT) Threat Feeds, storing them in Apache Parquet files for investigations into the past.

### Threat Feeds

I appreciate all the work that goes into maintaining these threat feeds - thank you!

- https://cert.pl
- https://cinsscore.com
- https://feodotracker.abuse.ch
- https://github.com/drb-ra
- https://github.com/elliotwutingfeng
- https://github.com/montysecurity
- https://github.com/stamparm
- https://github.com/Ultimate-Hosts-Blacklist
- https://greensnow.co
- https://jamesbrine.com.au
- https://oisd.nl
- https://openphish.com
- https://osint.digitalside.it
- https://otx.alienvault.com
- https://phishing.army
- https://phishtank.com
- https://report.cs.rutgers.edu
- https://sslbl.abuse.ch
- https://urlabuse.com
- https://zonefiles.io
- https://www.binarydefense.com
- https://www.blocklist.de
- https://www.dan.me.uk
- https://www.nubi-network.com
- https://www.proofpoint.com

### APIs APIs Everywhere

There are a ton of APIs on the Internet that are available to use, but is anything ever free? Why would I want anyone to know what I am investigating or be able to use my data?

Cloudcruft also provides working examples of APIs to allow you to deploy your investigation endpoints.

The **egress** endpoint captures public IP addresses, allowing a query string to monitor your environment for authorized **whoami** network calls.

https://egress.tundralabs.net/?secret_code

The **dns** endpoint checks the domain name against the collected threat feeds.

https://dns.tundralabs.net/4n6ir.com

The **ipv4** endpoint checks the IP address against the collected threat feeds.

https://ipv4.tundralabs.net/134.129.111.111

The **ipv6** endpoint checks the IP address against the collected threat feeds.

https://ipv6.tundralabs.net/::1

The **mx** endpoint checks for DMARC, MX, SPF, TXT, and select DKIM records that can indicate email security issues.

https://mx.tundralabs.net/4n6ir.com

The **spf** endpoint allows the investigation of DNS, IPv4, and IPv6 against the collected threat feeds that could be sending malware and phishing emails.

https://spf.tundralabs.net/4n6ir.com

![Cloud Cruft](images/cloudcruft.png)
