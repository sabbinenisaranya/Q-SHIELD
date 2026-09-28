import requests


def get_network_telemetry():
    """
    Get the current public IP address and
    approximate geographic information.

    Location is based on IP geolocation and
    should be treated as approximate.

    The function uses multiple services so that
    temporary rate limits do not break Q-SHIELD.
    """

    # --------------------------------------------------
    # DEFAULT RESULT
    # --------------------------------------------------

    result = {
        "ip_address": "UNKNOWN",
        "location": "UNKNOWN"
    }


    # --------------------------------------------------
    # SERVICE 1
    # --------------------------------------------------

    try:

        response = requests.get(
            "https://ipinfo.io/json",
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        ip_address = data.get(
            "ip",
            ""
        )

        city = data.get(
            "city",
            ""
        )

        region = data.get(
            "region",
            ""
        )

        country = data.get(
            "country",
            ""
        )

        location_parts = [

            part

            for part in [
                city,
                region,
                country
            ]

            if part

        ]

        location = ", ".join(
            location_parts
        )


        if ip_address:

            result["ip_address"] = (
                ip_address
            )

            result["location"] = (
                location
                if location
                else "UNKNOWN"
            )

            return result


    except Exception:

        pass


    # --------------------------------------------------
    # SERVICE 2 - FALLBACK
    # --------------------------------------------------

    try:

        response = requests.get(
            "https://ipwho.is/",
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        if not data.get(
            "success",
            False
        ):

            return result


        ip_address = data.get(
            "ip",
            ""
        )

        city = data.get(
            "city",
            ""
        )

        region = data.get(
            "region",
            ""
        )

        country = data.get(
            "country",
            ""
        )


        location_parts = [

            part

            for part in [
                city,
                region,
                country
            ]

            if part

        ]


        location = ", ".join(
            location_parts
        )


        if ip_address:

            result["ip_address"] = (
                ip_address
            )

            result["location"] = (
                location
                if location
                else "UNKNOWN"
            )


    except Exception:

        pass


    return result