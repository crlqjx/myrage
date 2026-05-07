# MYRAGE

A simple Python library to instantiate a Tor process and run HTTP requests behind it. Automatically manages Tor sessions, IP rotation, and request routing through SOCKS proxies.

## Features

- Start/stop Tor process programmatically
- Route HTTP/HTTPS requests through Tor network
- Automatic IP rotation after configurable number of requests
- Configure exit nodes by country
- Built-in session management with retries
- Logging support

## Installation

```bash
pip install myrage
```

### Prerequisites

The `tor` command must be available on your system. You can:
- Install Tor from your package manager: `sudo apt-get install tor` (Debian/Ubuntu)
- Use a symlink if Tor is installed in a non-standard location
- Use Nix: `nix-shell -p tor`

## Usage

### Basic Usage

```python
from myrage import Myrage

# Create and start a Tor session
session = Myrage()()

# Make requests through Tor
response = session.get("https://example.com")
print(response.text)

# Get current exit node IP info
ip_info = session.get_ip_info()
print(f"Current IP: {ip_info['query']}")

# Stop the Tor process when done
session.stop()
```

### With Custom Configuration

```python
from myrage import Myrage

# Configure exit nodes and ports
session = Myrage(
    control_port=9050,
    socks_port=9051,
    exit_nodes="{US}, {GB}, {CA}",  # Use exit nodes from specific countries
    strict_nodes=1,  # Strictly use only specified exit nodes
    tor_cmd_path="/usr/bin/tor"  # Custom Tor command path
)()

response = session.get("https://httpbin.org/ip")
print(response.json())

session.stop()
```

### Automatic IP Rotation

IP addresses are automatically rotated after `max_requests` (default: 100):

```python
from myrage import Myrage

session = Myrage(max_requests=50)()  # Rotate IP every 50 requests

for i in range(100):
    response = session.get("https://example.com")
    # IP will be renewed after 50 requests

session.stop()
```

### Manual IP Renewal

```python
from myrage import Myrage

session = Myrage()()

# Get current IP
print(session.get_ip_info())

# Manually renew IP
session.renew_ip()

# Verify new IP
print(session.get_ip_info())

session.stop()
```

### Compare Local IP vs Tor IP

```python
from myrage import Myrage

session = Myrage()()

# Get your local IP (without Tor)
local_ip = session.get_locale_ip_info()
print(f"Local IP: {local_ip['query']}")

# Get Tor exit node IP
tor_ip = session.get_ip_info()
print(f"Tor IP: {tor_ip['query']}")

session.stop()
```

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `control_port` | 9050 | Tor control port |
| `socks_port` | 9051 | Tor SOCKS port |
| `geo_ip_file` | `<package_dir>/geoip` | GeoIP file path |
| `geo_ip_v6_file` | `<package_dir>/geoip6` | GeoIPv6 file path |
| `exit_nodes` | "{BE}, {DE}, {IT}" | Exit node countries (comma-separated) |
| `strict_nodes` | 1 | Strictly use only specified exit nodes |
| `tor_cmd_path` | "/usr/sbin/tor" | Path to Tor executable |

## Exit Node Countries

Use ISO country codes in curly braces. Multiple countries can be specified:
- Single country: `exit_nodes="{US}"`
- Multiple countries: `exit_nodes="{US}, {GB}, {CA}"`
- Exclude countries: `exit_nodes="{US}, {~RU}, {~CN}"`

## License

MIT
