import time
import requests
import logging


def get_form_token(session: requests.Session):
    """ Gets the form_token from the server.
    Uses an active session for requests.
    Returns a token(str) or None."""

    try:
        response = session.get("https://test-rg8.ddns.net/api/get_token")
        response.raise_for_status()
        token = response.text.strip().strip('"')
        logging.info("form_token received")
        return token
    except Exception as e:
        logging.error(f"Couldn't get the form_token: {e}")
        return None


def chunked(lst, size):
    """Splits the list into batches of the specified size.
    Args:
        lst (list): The original proxy list.
        size (int): The size of each batch.
    Generates a sublist(list) up to the size of the elements."""

    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def upload_proxies(proxies: list[str], user_token: str, batch_size: int = 25, delay: int = 30):
    """Uploads the proxy list to the server in batches with repeated attempts in case of errors.
    Args:
        proxies (list[str]): A list of proxy strings.
        user_token (str): A unique user token.
        batch_size (int): The number of proxies in one batch.
        delay (int): The delay between batches is in seconds.
    Returns: A list of responses(list[dict]) from the server with information about saving the proxy."""

    results = []
    MAX_ATTEMPTS = 2

    for batch_num, proxy_batch in enumerate(chunked(proxies, batch_size), start=1):
        for attempt in range(1, MAX_ATTEMPTS + 1):
            session = requests.Session()
            form_token = get_form_token(session)

            if form_token is None:
                logging.warning(f"Skip the batch {batch_num} (attempt {attempt}) — there is no token")
                break

            data = {
                "user_id": user_token,
                "len": len(proxy_batch),
                "proxies": ", ".join(proxy_batch),
            }

            try:
                response = session.post(
                    "https://test-rg8.ddns.net/api/post_proxies",
                    json=data,
                    headers={"Content-Type": "application/json"},
                    cookies=session.cookies,
                    timeout=10
                )

                if response.status_code in (403, 429):
                    reason = "Too Many Requests" if response.status_code == 429 else "Forbidden"
                    logging.warning(f"Batch {batch_num}, attempt {attempt}: {response.status_code} {reason}")
                    if attempt < MAX_ATTEMPTS:
                        logging.info(f"Retry for batch {batch_num} through a new session.")
                        time.sleep(delay)
                        continue
                    logging.error(f"The retry failed (batch {batch_num})")
                    break

                response.raise_for_status()
                result = response.json()
                result["len"] = len(proxy_batch)
                logging.info(f"Sent {len(proxy_batch)} proxy (batch {batch_num}): {result}")
                results.append(result)
                break

            except requests.exceptions.RequestException as e:
                logging.error(f"Network error (batch {batch_num}, attempt {attempt}): {e}")
                if attempt >= MAX_ATTEMPTS:
                    logging.warning(f"Skipping the batch {batch_num} after two unsuccessful attempts")
                    break

        time.sleep(delay)

    return results
