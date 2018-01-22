# technician

hardware abstraction layer for opensfera.

It use a local mqtt to
 - receive and execute commands
 - broadcast hardware status

### System status

technician publish on topic `local/status`

message example
```
{
  "data": {
    "h1": 33,
    "t1": 1,
    "lights": "off",
    "fan": "off"
  },
  "event": "sfera_status"
}

```

### System commands

technician subscribe on topic `local/technician`

can receive

|command               | description                                  |
|----------------------|----------------------------------------------|
|lights_on             | turn on the light                            |
|lights_off            | turn off the light                           |
|exhaust_fan_on        | turn on the exhaust fan (to be implemented)  |
|exhaust_fan_off       | turn off the exhaust fan (to be implemented) |

### Config

Configurations are stored in `sfera/config` collection in mongodb.

|field                          | description                                  |
|-------------------------------|----------------------------------------------|
|technician_broadcast_time      | status publish interval (seconds), default 10|


### TODO

- debug
- implement DHT22, FAN
