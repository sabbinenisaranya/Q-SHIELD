from database.database import insert_event


insert_event(
    user_id="USER-001",
    document_id="sample_document.txt",
    timestamp="2026-09-22 12:35:00",
    device_id="DEVICE-001",
    ip_address="192.168.1.10",
    location="Vijayawada",
    signature_valid=True
)


print("Signing event inserted successfully.")