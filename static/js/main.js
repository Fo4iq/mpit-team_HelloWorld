const imagest = document.querySelectorAll('.imagest')

imagest.forEach(box => {
    box.addEventListener('mouseover', function() {
        this.style.maxWidth = '350px'
    });
    box.addEventListener('mouseout', function() {
        this.style.maxWidth = '300px'
    });
})