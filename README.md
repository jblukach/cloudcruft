# cloudcruft

Public IP addresses from a shared pool are automatically assigned using the Dynamic Host Configuration Protocol (DHCP) as resources launch. Addresses occasionally develop a poor reputation on the Internet before being returned. The next organization blindly assumes those addresses, which can result in a negative customer experience. 

Cloud Cruft maintains a thirty-day history to verify an IP's reputation.

### Threat Feeds

I appreciate all the work that goes into maintaining these threat feeds - thank you!

- https://cert.pl
- https://cinsscore.com
- https://ellio.tech
- https://feodotracker.abuse.ch
- https://github.com/drb-ra
- https://github.com/elliotwutingfeng
- https://github.com/mitchellkrogza
- https://github.com/montysecurity
- https://github.com/stamparm
- https://github.com/Ultimate-Hosts-Blacklist
- https://greensnow.co
- https://jamesbrine.com.au
- https://mirai.security.gives
- https://openphish.com
- https://osint.digitalside.it
- https://otx.alienvault.com
- https://phishing.army
- https://phishstats.info
- https://phishtank.com
- https://report.cs.rutgers.edu
- https://securityscorecard.com
- https://sslbl.abuse.ch
- https://talosintelligence.com
- https://urlabuse.com
- https://virtualfabric.com
- https://zonefiles.io
- https://www.binarydefense.com
- https://www.blocklist.de
- https://www.dan.me.uk
- https://www.nubi-network.com
- https://www.proofpoint.com
- https://www.rescure.me

### Step Function

Every Sunday at 11:00 AM UTC, the step function generates a Threat Feed for Cloud/SaaS Providers.

![Step Function](images/stepfunction.png)

At 11:00 AM UTC daily, the Parquet files update with the latest Open Source Threat Intelligence.

### DNS Command

```
https://dns.tundralabs.net/wexe.ink
```

### DNS Output

```json
{
    "domain": {
        "1": "wexe.ink",
        "2427762": "wexe.ink"
    },
    "source": {
        "1": "blackbook",
        "2427762": "zonefiles"
    }
}
```

### DNS Parquet

- Download: https://static.tundralabs.net/dns.parquet
- Verification: https://static.tundralabs.net/dns.sha256
- Last Updated: https://static.tundralabs.net/dns.updated
- Prefix Count: https://static.tundralabs.net/dns.count

### IP Command

```
https://ip.tundralabs.net/49.143.32.6
```

### IP Output

```json
{
    "address": {
        "0": "49.143.32.6",
        "368581": "49.143.32.6"
    },
    "source": {
        "0": "alienvault",
        "368581": "ipsum"
    }
}
```

### IP Parquet

- Download: https://static.tundralabs.net/ip.parquet
- Verification: https://static.tundralabs.net/ip.sha256
- Last Updated: https://static.tundralabs.net/ip.updated
- Prefix Count: https://static.tundralabs.net/ip.count

![Cloud Cruft](images/cloudcruft.png)
