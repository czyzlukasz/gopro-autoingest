# GoPro Auto-ingest

This (soon) containerized application implements the "Auto Upload" feature of all recent GoPro cameras without
subscriptions and for free!

## Requirements

- Storage facility capable of running Docker Container. This can be a NAS, PC, laptop or even a Raspberry Pi
- Wireless Access Point capable of running as a Client. This can be a router with OpenWrt installed or an additional
  Wi-Fi card in a PC or laptop.

### Workflow

- Download all chapters of a video to a _staging_ directory
- Process all videos from a _staging_ directory to the desired _output_ destination
