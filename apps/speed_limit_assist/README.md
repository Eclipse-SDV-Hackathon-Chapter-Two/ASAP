# Speed Limit Assist

The Speed Limit Assist warns the Driver, when the Speed exceeds the current detected Speed Limit by the Camera so the Driver can slow down.

## Build

When running `restart-shift2sdv`, or explicitly the `build-apps` script, the Speed Limit Assist will be build and containerized automatically as `ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/speed_limit_assist:latest`.

Of course, you are free to build manually if needed by calling the following command from the speed_limit_assist folder:

```shell
podman build -t speed_limit_assist:latest .
```

## Running

The Speed Limit Assist is automatically started by Ankaios as there is an entry for it in the [shift2sdv_SLA_manifest.yaml](shift2sdv_SLA_manifest.yaml). To use the correct manifest, you need to update the `start-shift2sdv`.

In the test vehicle the Speed Limit Assist container image will be started and managed by Eclipse Ankaios.

## Development

### Run

Start the app inside the devcontainer for local development:

```shell
python3 speed_limit_assist.py
```

### Testing with mock data

Ask the hack coaches for an eCAL recording to play back a recorded driving scenario with eCAL and to receive the vehicle dynamics data in the Speed Limit Assist for development.

Place the downloaded eCAL recording in a `measurements/` folder next to the current file.

Start the eCAL recording within the devcontainer, replace `<recording_folder>` with the recording folder you received from the hack coaches:

```shell
ecal_play -m measurements/<recording_folder>
```

Start the Speed Limit Assist inside the devcontainer as shown above.

For debugging reasons you can see the logs by calling:

```shell
ank-logs speed_limit_assist
```

The warnings will be logged and the exceeded velocity will be displayed.
