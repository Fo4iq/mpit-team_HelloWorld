const textbtn = document.querySelectorAll('.textbtn')

textbtn.forEach(box => {
    box.addEventListener('mouseover', function() {
        box.style.fontSize = '19px'
        this.style.border = '1px solid rgba(255, 255, 255, 0.493)'
        // box.style.boxShadow = 'inset 0px 0px 10px rgba(0, 0, 0, 0.171)'
    });
    box.addEventListener('mouseout', function() {
        box.style.fontSize = '20px'
        this.style.border = 'none'
        // box.style.boxShadow = 'none'
    });
})

const authbtn = document.querySelectorAll('.authbtn')

authbtn.forEach(auths => {
    auths.addEventListener('mouseover', function() {
        this.style.padding = '12px 18px 12px 18px'
    });
    auths.addEventListener('mouseout', function() {
        this.style.padding = '7px 13px 7px 13px'
    });
})