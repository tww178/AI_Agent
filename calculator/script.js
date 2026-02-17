document.getElementById('birthdayButton').addEventListener('click', function() {
    const button = this;
    const container = button.parentElement;

    // Generate random positions within the container
    const newX = Math.random() * (container.offsetWidth - button.offsetWidth);
    const newY = Math.random() * (container.offsetHeight - button.offsetHeight);

    // Apply new positions
    button.style.left = newX + 'px';
    button.style.top = newY + 'px';
    button.style.transform = 'translate(0, 0)'; // Reset transform to use left/top directly

    document.getElementById('bearMessage').classList.remove('hidden');
});