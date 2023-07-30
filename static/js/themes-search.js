function filterTheme() {
    const input = document.getElementById('filter')
    const inp = input.value.toLowerCase()
    const cardContainer = document.getElementById('card-list')
    const card = cardContainer.getElementsByClassName('theme-cards')

    for (let i = 0; i < card.length; i++) {
        let title = card[i].querySelector('.card-body')
        if (title.innerText.toLowerCase().indexOf(inp) > -1) {
            card[i].style.display = ''
        } else {
            card[i].style.display = 'none'
        }
    }
}