let traceId;

function start() {
    const fileUploadForm = document.getElementById('file-upload-form');
    const fileUploadButton = document.getElementById('file-upload-button');
    const regButton = document.getElementById('registration');



    fileUploadForm.addEventListener('change', onFileUpload);
    fileUploadButton.addEventListener('click', () => {
        fileUploadForm.click();
    });
    regButton.addEventListener('click', () => {
        registrationLogin();
    });
    showLogin(() => {
        coreConnect({});
        listFiles();
    });

}

start();