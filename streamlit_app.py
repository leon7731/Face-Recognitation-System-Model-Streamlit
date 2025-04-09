import streamlit as st
import requests

RECOGNIZE_API_URL = "http://18.143.150.46:8000/recognize"
UPLOAD_API_URL = "http://18.143.150.46:8000/upload"  


def upload_image_ui(label="Choose an image..."):
    uploaded_file = st.file_uploader(label, type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    return uploaded_file


def send_to_recognize_api(uploaded_file):
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    try:
        response = requests.post(RECOGNIZE_API_URL, files=files)
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def send_to_upload_api(uploaded_file, person_name):
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    data = {"person_name": person_name}
    try:
        response = requests.post(UPLOAD_API_URL, files=files, data=data)
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Upload failed: {e}")
        return None


def face_recognition_tab():
    st.subheader("🔍 Face Recognition")
    uploaded_file = upload_image_ui("Upload image for recognition...")

    if uploaded_file and st.button("Process Image"):
        response = send_to_recognize_api(uploaded_file)
        if response:
            if response.status_code == 200:
                st.success("✅ Image processed successfully!")
                st.image(response.content, caption="Annotated Image", use_container_width=True)
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")


def face_registration_tab():
    st.subheader("🧑‍💼 Face Registration")
    person_name = st.text_input("Enter person's name")
    uploaded_file = upload_image_ui("Upload image for registration...")

    if uploaded_file and person_name and st.button("Upload & Register"):
        response = send_to_upload_api(uploaded_file, person_name)
        if response:
            if response.status_code == 200:
                st.success("✅ Upload successful!")
                st.json(response.json())
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
    elif uploaded_file and not person_name:
        st.warning("⚠️ Please enter a name to register.")


def main():
    st.title("🎯 Face Recognition System")

    tab1, tab2 = st.tabs(["🔍 Recognize Face", "🧑‍💼 Register Face"])
    with tab1:
        face_recognition_tab()
    with tab2:
        face_registration_tab()


if __name__ == "__main__":
    main()
