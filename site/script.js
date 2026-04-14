const fileListElement = document.getElementById("file-list");
const fileFilter = document.getElementById("file-filter");
const fileTitle = document.getElementById("file-title");
const fileContent = document.getElementById("file-content");
const copyButton = document.getElementById("copy-button");
let files = [];
let currentFile = null;

function renderFileList(filter = "") {
  fileListElement.innerHTML = "";
  const normalizedFilter = filter.trim().toLowerCase();

  const visibleFiles = files.filter((file) => {
    return file.path.toLowerCase().includes(normalizedFilter);
  });

  visibleFiles.forEach((file) => {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.textContent = file.path;
    button.type = "button";
    button.addEventListener("click", () => selectFile(file.path));
    if (currentFile === file.path) {
      button.classList.add("active");
    }
    item.appendChild(button);
    fileListElement.appendChild(item);
  });
}

function selectFile(path) {
  currentFile = path;
  const file = files.find((item) => item.path === path);
  if (!file) return;

  fileTitle.textContent = file.path;
  fileContent.textContent = file.content;
  renderFileList(fileFilter.value);
}

function loadFiles() {
  fetch("files.json")
    .then((response) => response.json())
    .then((data) => {
      files = data.files;
      renderFileList();
      if (files.length > 0) {
        selectFile(files[0].path);
      }
    })
    .catch((error) => {
      fileTitle.textContent = "Failed to load files";
      fileContent.textContent = error.message;
    });
}

fileFilter.addEventListener("input", () => renderFileList(fileFilter.value));

copyButton.addEventListener("click", async () => {
  if (!currentFile) return;
  try {
    await navigator.clipboard.writeText(fileContent.textContent);
    copyButton.textContent = "Copied!";
    setTimeout(() => {
      copyButton.textContent = "Copy content";
    }, 1500);
  } catch (err) {
    copyButton.textContent = "Copy failed";
    setTimeout(() => {
      copyButton.textContent = "Copy content";
    }, 1500);
  }
});

loadFiles();
