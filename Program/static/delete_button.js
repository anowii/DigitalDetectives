/* Detta är bara en start punkt, den som forstätter arbeta på detta kan ändra det som behövs*/

document.addEventListener("DOMContentLoaded", () => {
    const trashButton = document.querySelector('.trash-button');
    if (trashButton) {
        trashButton.addEventListener('click', () => {
            console.log("Trash button clicked!");
            const confirmed = confirm("Are you sure you want to delete this?");
            if (confirmed) {
                console.log("Item deleted.");
                // Additional deletion logic here
            }
        });
    } else {
        console.warn("Trash button not found in the DOM.");
    }
});