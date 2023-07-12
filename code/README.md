>Note: The emulators are using display.

So, if you run the app using a docker container, you need to share the display with the container.
You can achieve this by using xQuartz.

1. Install xQaurtz on your machine.
2. Open xQuartz and go to Preferences -> Security and check "Allow connections from network clients".
3. Restart xQuartz.
4. In the xQuartz terminal, run:
```bash
xhost +127.0.0.1
```
5. Run the docker container with the following command:
```bash
docker run -it --rm -e DISPLAY=host.docker.internal:0 <IMAGE_NAME>:<TAG>
```

Anyway, first you need to build the docker image. You can do it by running the following command:

```bash
docker build -t <IMAGE_NAME>:<TAG> --build-arg MONOREPO_APP_PATH=emulators/<APP_NAME> .
```
