# Pluggables Service (Digital Subcarrier Multiplexed)

## Overview

The Pluggables service provides gRPC-based management for optical pluggables and their digital subcarrier groups. It enables configuration and monitoring of coherent optical transceivers with support for multi-carrier operation.

## Key Concepts

### Pluggable
An optical transceiver module installed in a device (router/switch) at a specific physical slot index.

### Digital Subcarrier Group (DSC Group)
A logical grouping of digital subcarriers within a pluggable, representing a coherent optical channel with shared parameters:
- **group_size**: Expected number of subcarriers in the group
- **group_capacity_gbps**: Total capacity in Gbps (e.g., 400G)
- **subcarrier_spacing_mhz**: Frequency spacing between subcarriers (e.g., 75 MHz)

### Digital Subcarrier
Individual frequency channels within a DSC group with configurable parameters:
- **active**: Enable/disable the subcarrier
- **target_output_power_dbm**: Transmit power in dBm
- **center_frequency_hz**: Carrier frequency in Hz (e.g., 193.1 THz)
- **symbol_rate_baud**: Symbol rate in Baud (e.g., 64 GBaud)

## Service API

### gRPC Methods

| Method | Request | Response | Description |
|--------|---------|----------|-------------|
| `CreatePluggable` | `CreatePluggableRequest` | `Pluggable` | Create a new pluggable with optional initial configuration |
| `GetPluggable` | `GetPluggableRequest` | `Pluggable` | Retrieve a specific pluggable by ID |
| `ListPluggables` | `ListPluggablesRequest` | `ListPluggablesResponse` | List all pluggables for a device |
| `DeletePluggable` | `DeletePluggableRequest` | `Empty` | Remove a pluggable from management |
| `ConfigurePluggable` | `ConfigurePluggableRequest` | `Pluggable` | Apply full configuration to a pluggable |

### View Levels

Control the level of detail in responses:
- `VIEW_UNSPECIFIED (0)`: Default, returns full pluggable
- `VIEW_CONFIG (1)`: Returns only configuration data
- `VIEW_STATE (2)`: Returns only state/telemetry data
- `VIEW_FULL (3)`: Returns complete pluggable (config + state)

## Usage Examples

### 1. Creating a Pluggable Without Configuration

```python
from pluggables.client.PluggablesClient import PluggablesClient
from pluggables.tests.testmessages import create_pluggable_request

# Create client
client = PluggablesClient()

# Create pluggable request (auto-assign index)
request = create_pluggable_request(
    device_uuid="550e8400-e29b-41d4-a716-446655440000",
    preferred_pluggable_index=-1  # -1 for auto-assignment
)

# Create pluggable
pluggable = client.CreatePluggable(request)
print(f"Created pluggable at index: {pluggable.id.pluggable_index}")

# Close client
client.close()
```

### 2. Creating a Pluggable With Initial Configuration

```python
from pluggables.tests.testmessages import create_pluggable_request

# Create pluggable with optical channel configuration
request = create_pluggable_request(
    device_uuid="550e8400-e29b-41d4-a716-446655440000",
    preferred_pluggable_index=0,  # Physical slot 0
    with_initial_config=True      # Include DSC group configuration
)

pluggable = client.CreatePluggable(request)

# Verify configuration
assert len(pluggable.config.dsc_groups) == 1
dsc_group = pluggable.config.dsc_groups[0]
assert dsc_group.group_size == 4
assert dsc_group.group_capacity_gbps == 400.0
```

### 3. Listing Pluggables with View Filtering

```python
from common.proto.pluggables_pb2 import View
from pluggables.tests.testmessages import create_list_pluggables_request

# List only configuration (no state data)
request = create_list_pluggables_request(
    device_uuid="550e8400-e29b-41d4-a716-446655440000",
    view_level=View.VIEW_CONFIG
)

response = client.ListPluggables(request)
for pluggable in response.pluggables:
    print(f"Pluggable {pluggable.id.pluggable_index}: {len(pluggable.config.dsc_groups)} DSC groups")
```

### 4. Getting a Specific Pluggable

```python
from pluggables.tests.testmessages import create_get_pluggable_request

# Get full pluggable details
request = create_get_pluggable_request(
    device_uuid="550e8400-e29b-41d4-a716-446655440000",
    pluggable_index=0,
    view_level=View.VIEW_FULL
)

pluggable = client.GetPluggable(request)
print(f"Device: {pluggable.id.device.device_uuid.uuid}")
print(f"Index: {pluggable.id.pluggable_index}")
print(f"DSC Groups: {len(pluggable.config.dsc_groups)}")
```

### 5. Configuring a Pluggable

```python
from pluggables.tests.testmessages import create_configure_pluggable_request

# Apply full configuration (reconfigure optical channels)
request = create_configure_pluggable_request(
    device_uuid="550e8400-e29b-41d4-a716-446655440000",
    pluggable_index=0,
    view_level=View.VIEW_CONFIG,
    apply_timeout_seconds=30
)

# Configuration includes:
# - 1 DSC group with 400G capacity, 75 MHz spacing
# - 2 digital subcarriers at 193.1 THz and 193.175 THz
# - Each subcarrier: -10 dBm power, 64 GBaud symbol rate

pluggable = client.ConfigurePluggable(request)
print(f"Configured {len(pluggable.config.dsc_groups[0].subcarriers)} subcarriers")
```

### 6. Deleting a Pluggable

```python
from pluggables.tests.testmessages import create_delete_pluggable_request

# Delete pluggable from management
request = create_delete_pluggable_request(
    device_uuid="550e8400-e29b-41d4-a716-446655440000",
    pluggable_index=0
)

response = client.DeletePluggable(request)
print("Pluggable deleted successfully")
```

## Configuration Message Structure

### Complete Configuration Example

```python
from common.proto import pluggables_pb2

# Create configuration request
request = pluggables_pb2.ConfigurePluggableRequest()

# Set pluggable ID
request.config.id.device.device_uuid.uuid = "550e8400-e29b-41d4-a716-446655440000"
request.config.id.pluggable_index = 0

# Add DSC group
dsc_group = request.config.dsc_groups.add()
dsc_group.id.pluggable.device.device_uuid.uuid = "550e8400-e29b-41d4-a716-446655440000"
dsc_group.id.pluggable.pluggable_index = 0
dsc_group.id.group_index = 0
dsc_group.group_size = 2
dsc_group.group_capacity_gbps = 400.0
dsc_group.subcarrier_spacing_mhz = 75.0

# Add subcarrier 1
subcarrier = dsc_group.subcarriers.add()
subcarrier.id.group.pluggable.device.device_uuid.uuid = "550e8400-e29b-41d4-a716-446655440000"
subcarrier.id.group.pluggable.pluggable_index = 0
subcarrier.id.group.group_index = 0
subcarrier.id.subcarrier_index = 0
subcarrier.active = True
subcarrier.target_output_power_dbm = -10.0
subcarrier.center_frequency_hz = 193100000000000  # 193.1 THz
subcarrier.symbol_rate_baud = 64000000000  # 64 GBaud

# Add subcarrier 2
subcarrier2 = dsc_group.subcarriers.add()
# ... (similar configuration for second subcarrier)

# Set view level and timeout
request.view_level = pluggables_pb2.VIEW_FULL
request.apply_timeout_seconds = 30
```

## API Reference

For complete API documentation, see:
- Protocol Buffer definitions: `proto/pluggables.proto`
- Client implementation: `src/pluggables/client/PluggablesClient.py`
- Service implementation: `src/pluggables/service/PluggablesServiceServicerImpl.py`
- Test examples: `src/pluggables/tests/test_Pluggables.py`
- Message helpers: `src/pluggables/tests/testmessages.py`
