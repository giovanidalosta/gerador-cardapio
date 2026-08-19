// This file contains JavaScript code for client-side functionality, such as handling form submissions and updating the UI dynamically.

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-input");
    const submitButton = document.getElementById("submit-button");
    const resultMessage = document.getElementById("result-message");

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

        fetch("/generate-menu", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao gerar o cardápio.");
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "Cardapio.png";
            document.body.appendChild(a);
            a.click();
            a.remove();
            resultMessage.textContent = "Cardápio gerado com sucesso!";
        })
        .catch(error => {
            resultMessage.textContent = error.message;
        })
        .finally(() => {
            submitButton.disabled = false;
        });
    });
});