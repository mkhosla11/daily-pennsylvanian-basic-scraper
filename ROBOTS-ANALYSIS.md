# Robots Analysis for the Daily Pennsylvanian

The Daily Pennsylvanian's `robots.txt` file is available at
[https://www.thedp.com/robots.txt](https://www.thedp.com/robots.txt).

## Contents of the `robots.txt` file on 04/20/2025

```
User-agent: *
Crawl-delay: 10
Allow: /

User-agent: SemrushBot
Disallow: /
```

## Explanation

The `robots.txt` file indicates that all user-agents are allowed to crawl the entire site (via `Allow: /`), but they must respect a `Crawl-delay` of 10 seconds between requests. This means we are permitted to scrape the Daily Pennsylvanian website as long as we space out requests appropriately.

However, the crawler specifically blocks `SemrushBot` from accessing any part of the site (`Disallow: /`), meaning SEMrush is not permitted to crawl their pages.

As we are not using SemrushBot and will be implementing a crawl delay of 10 seconds, scraping is allowed under the site's current `robots.txt` policy.
