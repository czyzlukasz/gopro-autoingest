# GoPro Auto-ingest

This containerized application implements the "Auto Upload" feature of all recent GoPro cameras without
subscriptions and free of charge!

## Requirements

- Storage facility capable of running a Docker Container. This can be a NAS, PC, laptop, or even a Raspberry Pi.
- Wireless Access Point capable of operating as a Client. This can be a router with OpenWrt installed or an additional
  Wi-Fi card in a PC or laptop.

## Why it works

GoPro cameras implement a Wi-Fi interface that gives users almost full control over the camera. The entire interface
relies on simple HTTP GET requests (except for Wake-on-LAN). Even though GoPro officially supports the API for versions
9 and up, there is a comprehensive documentation done by Konrad Iturbe available
at https://github.com/KonradIT/goprowifihack. This project became possible because we can list all the files, download
videos, remove videos, and shut down the camera.

### Wi-Fi connectivity

Since GoPro expects users to utilize the "GoPro Quik" application for live streaming,
configuration, and control, the camera acts as a Wi-Fi Access Point and accepts all Clients without any explicit
handshake and/or encryption. This can be exploited by creating a Wi-Fi client that connects the GoPro to the local
network and exposes the HTTP API.

## How it works

The container runs two jobs - download and process. They operate independently of each other and can be executed
simultaneously.

### Video download

This job should be run as frequently as possible to prevent the camera from automatically shutting down. The GoPro will
remain powered up as long as the Wi-Fi Client stays connected to the camera. This feature is valuable as it allows the
download process to work without interruption.

Python script first lists all the videos available on the camera. Note that every video consists of one or more
chapters (videos that are about 4GB in size due to FAT32 limitations). All chapters not in the staging area are
sequentially downloaded. The staging area is simply a parking spot for all videos that are downloaded but not yet
processed. Optionally, the downloaded videos are deleted from the camera. The deletion happens only after all chapters
of given video have been successfully downloaded.

### Video processing

Due to the nature of videos produced by GoPro, they require some processing. Primarily, the chapters need to be stitched
together. GoPro also produces metadata that are attached to the .mp4 files in the form of streams. The particular stream
type and count may vary, but the most common streams are TCD, MET, and SOS. Since only TCD is remotely useful, the MET
and SOS streams are discarded. Future project versions may include GPS and IMU metadata extraction. Optionally, videos
that have been successfully processed can be removed from staging area.

