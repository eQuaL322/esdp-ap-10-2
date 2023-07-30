const originalTexts = document.getElementsByClassName("original-text");
const newDivs = document.getElementsByClassName("words-in-text");

for (let i = 0; i < newDivs.length; i++) {
    const originalText = originalTexts[i];
    const newDiv = newDivs[i];
    const words = originalText.textContent.split(" ");
    const bracketWords = [];

    for (let j = 0; j < words.length; j++) {
        const word = words[j];
        if (word.startsWith("[") && word.endsWith("]")) {
            bracketWords.push(word.slice(1, -1));
            const dropzone = document.createElement("span");
            const taskId = newDiv.getAttribute("data-taskId");
            const wordId = `word-${taskId}-${bracketWords.length}`;
            dropzone.classList.add("dropzone");
            dropzone.setAttribute("id", wordId);
            originalText.innerHTML = originalText.innerHTML.replace(word, dropzone.outerHTML);
        }
    }

    const shuffledWords = shuffleArray(bracketWords);

    newDiv.innerHTML = shuffledWords.map((word, index) => {
        const wordIndex = bracketWords.indexOf(word);
        const taskId = newDiv.getAttribute("data-taskId");
        return `<div draggable="true" class="word-button shadow-sm" id="word-${taskId}-${wordIndex + 1}">${word}</div>`;
    }).join("");

    const draggables = newDiv.querySelectorAll(".word-button");
    const dropzones = originalText.querySelectorAll(".dropzone");

    draggables.forEach(draggable => {
        draggable.addEventListener("dragstart", () => {
            draggable.classList.add("dragging");
        });
        draggable.addEventListener("dragend", () => {
            draggable.classList.remove("dragging");
        });
    });

    dropzones.forEach(dropzone => {
        dropzone.addEventListener("dragover", e => {
            e.preventDefault();
            dropzone.classList.add("hovered");
        });
        dropzone.addEventListener("dragleave", () => {
            dropzone.classList.remove("hovered");
        });
        dropzone.addEventListener("drop", e => {
            e.preventDefault();
            const draggedWord = document.querySelector(".dragging").textContent;
            dropzone.textContent = draggedWord;
            dropzone.classList.remove("hovered");
            const wordId = dropzone.getAttribute("id");
            const wordButton = document.getElementById(wordId);
            if (!wordButton || wordButton.textContent !== draggedWord) {
                dropzone.classList.add("incorrect");
            } else {
                dropzone.classList.add("correct");
                wordButton.classList.add("strikethrough");
            }
        });
    });
}

function shuffleArray(array) {
    const newArray = array.slice();
    for (let i = newArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
    }
    return newArray;
}