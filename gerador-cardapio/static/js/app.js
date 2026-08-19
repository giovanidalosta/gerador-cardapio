document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-upload");
    const fileName = document.getElementById("file-name");
    const submitButton = document.getElementById("submit-button");
    const resultMessage = document.getElementById("result-message");
    const previewStatus = document.getElementById("preview-status");
    const emptyPreview = document.getElementById("empty-preview");
    const previewImage = document.getElementById("preview-image");
    const downloadLink = document.getElementById("download-link");

    fileInput.addEventListener("change", function() {
        fileName.textContent = fileInput.files[0] ? fileInput.files[0].name : "Selecione um arquivo .xlsx";
    });

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const file = fileInput.files[0];

        if (!file) {
            resultMessage.textContent = "Por favor, selecione um arquivo Excel.";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        submitButton.disabled = true;
        resultMessage.textContent = "Gerando cardápio...";
        previewStatus.textContent = "Gerando";

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(message => { throw new Error(message || "Erro ao gerar o cardápio."); });
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            previewImage.src = url;
            previewImage.style.display = "block";
            emptyPreview.style.display = "none";
            downloadLink.href = url;
            downloadLink.style.display = "block";
            previewStatus.textContent = "Pronto";
            resultMessage.textContent = "Cardápio gerado com sucesso!";
        })
        .catch(error => {
            resultMessage.textContent = error.message;
            previewStatus.textContent = "Erro";
        })
        .finally(() => {
            submitButton.disabled = false;
        });
    });
});