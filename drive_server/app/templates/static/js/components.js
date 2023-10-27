const createFile = (uploadId, filename, dateCreated, fileSize, withProgressBar = true) => {
    const filesContainer = document.getElementById('files-container');

    const container = createElement({
        id: `container-${uploadId}`,
        classnames: ['container-fluid', 'p-2', 'border-bottom', 'file-container'],
    });
    const textContainer = createElement({classnames: ['uploaded-file']});
    textContainer.appendChild(createElement({classnames: 'text-black', text: filename}));
    textContainer.appendChild(createElement({classnames: ['text-black'], text: formatDate(dateCreated)}));
    textContainer.appendChild(createElement({classnames: ['text-black'], text: `${formatSize(fileSize)}`}));

    const deleteButton = createElement({
        tag: 'button',
        attributes: {
            type: 'button',
            disabled: true,
            'data-key': filename,
            'data-upload-id': uploadId,
        },
        classnames: ['btn', 'btn-danger', 'd-inline-block'],
        text: '×',
    });
    const downloadButton = createElement({
        tag: 'button',
        attributes: {
            type: 'button',
            disabled: true,
            'data-key': filename,
        },
        classnames: ['btn', 'd-inline-block'],
        text: '⬇',
    });
    deleteButton.addEventListener('click', (e) => (deleteFile(e, filesContainer)));
    textContainer.appendChild(deleteButton);
    downloadButton.addEventListener('click', (e) => (downloadFile(e, filesContainer)));
    textContainer.appendChild(downloadButton);
    container.appendChild(textContainer);

    if (withProgressBar) {
        createProgressBar(uploadId, container);
    }

    filesContainer.appendChild(container);
}

const createProgressBar = (uploadId, container) => {
    const progressBarContainer = createElement({
        id: `progress-bar-container-${uploadId}`,
        classnames: ['progress', 'mt-2'],
    })

    const progressBar = createElement({
        id: `progress-bar-${uploadId}`,
        classnames: ['progress-bar', 'progress-bar-striped', 'progress-bar-animated'],
        attributes: {
            role: 'progressbar',
            'aria-valuenow': '0',
            'aria-valuemin': '0',
            'aria-valuemax': '100',
        }
    });
    progressBar.style.width = '0';
    progressBarContainer.appendChild(progressBar);
    container.appendChild(progressBarContainer);
}

const updateUploadProgress = (uploadId, totalSize, uploadedSize) => {
    document.getElementById(`progress-bar-${uploadId}`).style.width = `${uploadedSize / totalSize * 100}%`;
}

const finishUpload = (uploadId) => {
    const progressContainer = document.getElementById(`progress-bar-container-${uploadId}`);
    const progressBar = document.getElementById(`progress-bar-${uploadId}`);
    progressBar.style.width = '100%';
    progressBar.classList.add('bg-success');
    setTimeout(() => (progressContainer.style.display = 'none'), 1000);
}


const listFiles = async () => {
    let items = await filesList();
    items.forEach((item) => {
        createFile(UUIDv4(), item['Key'], item['LastModified'], item['Size'], false);
    })
}


const onFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!!file) {
        const uploadId = UUIDv4();
        createFile(uploadId, file.name, new Date(), file.size);
        await filesUpload(uploadId, file);
    }
}


const deleteFile = async (e, container) => {
    const ok = await filesDelete({key: e.target.attributes['data-key']});
    if (ok) {
        e.target.removeEventListener('click', deleteFile);
        container.removeChild(
            document.getElementById(`container-${e.target.attributes['data-upload-id']}`),
        );
    }
};

function length_byte(a) {
    // let offset = 0;
    const bit_data = a.value;
    let len = bit_data.byteLength;
    let array = new Uint8Array(len);
    array.set(bit_data);
    return array
}


const downloadFile = async (e) => {
    const file = await fileDownload({key: e.target.attributes['data-key']});
    if (file) {
        let result;
        let summ_mass = Array();
        const reader = await file.getReader();
        while (!(result = await reader.read()).done) {
            let temps = length_byte(result);
            summ_mass.push(temps)
        }
        let a = document.createElement('a');
        let file_ = new Blob([...summ_mass]);
        a.href = URL.createObjectURL(file_);
        a.download = e.target.attributes['data-key'];
        a.click();
    }
};

const hideLogin = (modal) => {
    modal.hide();
}

const login = async (callback) => {
    const username = document.getElementById('login-username').value;
    if (!username) {
        alert('Имя пользователя не введено!');
        return;
    }
    const password = document.getElementById('login-password').value;
    if (!password) {
        alert('Пароль не введен!');
        return;
    }

    const resp = await coreLogin({username, password});
    if (resp !== null) {
        callback();
    }
}

const login_registration = async (callback) => {
    const username = document.getElementById('login-username_').value;
    if (!username) {
        alert('Имя пользователя не введено!');
        return;
    }
    const password = document.getElementById('login-password_').value;
    if (!password) {
        alert('Пароль не введен!');
        return;
    }

    const resp = await addUser({username, password});
    if (resp !== null) {
        callback();
    }
}

const showLogin = async (loginCallback) => {
    const isAuthorized = await coreCurrent();
    if (isAuthorized !== null) {
        console.log('Пользователь авторизован');
        loginCallback()
        return;
    }
    const modal = new bootstrap.Modal(document.getElementById('login-modal'))
    modal.show();
    document.getElementById('login-button').addEventListener(
        'click',
        () => (
            login(() => {
                hideLogin(modal);
                loginCallback();
            })
        )
    );
}

const registrationLogin = async (loginCallback) => {
    const modal = new bootstrap.Modal(document.getElementById('registration-modal'))
    modal.show();
    document.getElementById('registration-button').addEventListener(
        'click',
        () => (
            login_registration(() => {
                hideLogin(modal);
                loginCallback();
            })
        )
    );
}