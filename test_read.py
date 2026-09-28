import sqlite3

from database.database import DATABASE_PATH


connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()


cursor.execute(
    """
    SELECT
        id,
        user_id,
        document_id,
        timestamp,
        device_id,
        ip_address,
        location,
        signature_valid
    FROM signature_events
    """
)


events = cursor.fetchall()


print("\n========================================")
print("       Q-SHIELD STORED EVENTS")
print("========================================")


for event in events:

    print("\nEvent ID:", event[0])
    print("User:", event[1])
    print("Document:", event[2])
    print("Timestamp:", event[3])
    print("Device:", event[4])
    print("IP Address:", event[5])
    print("Location:", event[6])
    print(
        "Signature:",
        "VALID" if event[7] else "INVALID"
    )


connection.close()


print("\n========================================")
print("              READ COMPLETE")
print("========================================")