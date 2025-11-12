import os
import time
import requests

FHIR_BASE_URL = os.getenv("FHIR_BASE_URL", "http://fhir-internal:8080/fhir")

def wait_for_fhir_ready(timeout=300):
    print("Waiting for FHIR server to become ready...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{FHIR_BASE_URL}/metadata", timeout=5)
            if r.status_code == 200:
                print("FHIR server is ready.")
                return True
        except Exception:
            pass
        time.sleep(5)
    raise TimeoutError("FHIR server did not become ready in time")

def create_patient():
    patient = {
        "resourceType": "Patient",
        "name": [{"use": "official", "family": "Test", "given": ["FHIR"]}],
        "birthDate": "1980-01-01"
    }
    print("Creating test patient...")
    r = requests.post(f"{FHIR_BASE_URL}/Patient", json=patient)
    r.raise_for_status()
    patient_id = r.json()["id"]
    print(f"Created Patient/{patient_id}")
    return patient_id

def get_summary(patient_id):
    print("Fetching $summary for test patient...")
    r = requests.get(f"{FHIR_BASE_URL}/Patient/{patient_id}/$summary")
    r.raise_for_status()
    if r.status_code == 200:
        print("✅ $summary call succeeded.")
        return True
    raise RuntimeError(f"$summary failed: {r.status_code}")

def delete_patient(patient_id):
    print(f"Deleting Patient/{patient_id}...")
    r = requests.delete(f"{FHIR_BASE_URL}/Patient/{patient_id}")
    r.raise_for_status()
    print("✅ Patient deleted successfully.")

if __name__ == "__main__":
    try:
        wait_for_fhir_ready()
        pid = create_patient()
        get_summary(pid)
        delete_patient(pid)
        print("✅ Smoke test completed successfully.")
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        exit(1)
