import gpsd


def get_gps_location() -> tuple[float, float] | None:
    try:
        gpsd.connect()
        packet = gpsd.get_current()

        if packet.mode >= 2 and packet.mode <= 3:
            latitude, longitude = packet.position()
            return latitude, longitude
        else:
            print("Unable to get a fix on GPS signal of device.")
            return None

    except Exception as e:
        print("Error occurred while fetching GPS location:", str(e))
        return None


if __name__ == "__main__":
    location = get_gps_location()
    if location is None:
        print("Location not available on this device.")
    else:
        latitude, longitude = location
        if latitude is not None and longitude is not None:
            print(
                f"Your current GPS location: Latitude = {latitude}, Longitude = {longitude}"
            )
        else:
            print("Latitude and longitude not available.")
