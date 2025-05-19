'use strict'

const listingsEl = document.querySelector('.listings')
const searchEl = document.querySelector('.search')
const searchInput = document.querySelector('.search-input')
const searchButton = document.querySelector('.search-button')
const searchForm = document.querySelector('.search-form')
const backBtn = document.querySelector('.back-btn')

let listings = []


////////////////// SEARCH SECTION  /////////////////
showSearch()
hideResults()

async function fetchData(url) {
    try {
        const res = await fetch('https://sina.mhreza.ir/link', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                link: url
            })
        })
        if (!res.ok) {
            alert("آگهی وارد شده پیدا نشد")
            return null
        }
        return await res.json()
    } catch (e) {
        alert("مشکلی پیش امده است، بعدا دوباره امتحان کنید")
    }
    return null
}

function hideSearch() {
    searchEl.style.opacity = 0
    setTimeout(() => searchEl.classList.add('hidden'), 500)
}

function showSearch() {
    searchEl.classList.remove('hidden')
    setTimeout(() => searchEl.style.opacity = 100, 500)
    searchInput.value = ''
    searchInput.focus()
}

function disableButton() {
    searchButton.disabled = true
    searchButton.textContent = 'صبر کنید'
}

function enableButton() {
    searchButton.disabled = false;
    searchButton.textContent = 'پیدا کن';
}

searchButton.disabled = true

searchInput.addEventListener('input', () => {
    searchButton.disabled = !searchInput.checkValidity();
})

searchForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    disableButton()
    const listingData = await fetchData(searchInput.value)
    if (listingData) {
        listings = listingData
        hideSearch()
        showResults()
        renderResults()
    }
    enableButton()
})


////////////////// RESULTS SECTION  /////////////////
backBtn.addEventListener('click', function () {
    hideResults()
    showSearch()
})

function renderResults() {
    let color

    function renderGraph(percentage, strokeWidth, target) {
        if (percentage <= 0.25)
            color = '#E55050'
        if (percentage >= 0.25 && percentage <= 0.5)
            color = '#FA812F'
        if (percentage >= 0.5 && percentage <= 0.75)
            color = '#F3C623'
        if (percentage >= 0.75)
            color = '#169976'
        const graph = new ProgressBar.SemiCircle(target, {
            strokeWidth: strokeWidth,
            trailColor: '#eee',
            trailWidth: strokeWidth,
            color: color,
            duration: 1400,
            easing: 'easeInOut',
        });

        graph.animate(percentage);
    }

    function renderListing(listing, number) {
        const html = `
        <div class="listing" id="listing__${number}">
            <div class="listing-details">
                <div class="listing-name">
                    ${listing.name}
                                    </div>
                <a class="listing-link" href="${listing.url}">
                    لینک آگهی
                </a>
            </div>
            <div class="listing-percent">
                <div class="similarity-text">درصد مشابهت</div>
                <div class="similarity-percent">${listing.percentage}<span style="font-size: 1.25rem">%</span></div>
            </div>
            <div class="listing-graph"></div>            
        </div>
    `
        listingsEl.insertAdjacentHTML('beforeend', html)
        const percentageNumber = document.querySelector(`#listing__${number}`).querySelector('.listing-percent').querySelector('.similarity-percent')
        const listingGraphContainer = document.querySelector(`#listing__${number}`).lastElementChild
        renderGraph(listing.percentage / 100, 14, listingGraphContainer)
        percentageNumber.style.color = color
    }

    listings.sort((listing1, listing2) => -listing1.percentage + listing2.percentage)
    listings.forEach((listing, i) => {
        renderListing(listing, i)
    })
}

function hideResults() {
    backBtn.style.opacity = 0
    setTimeout(() => backBtn.classList.add('hidden'), 500)
    listingsEl.style.opacity = 0
    setTimeout(() => listingsEl.classList.add('hidden'), 500)
    listingsEl.innerHTML = ''
}

function showResults() {
    backBtn.classList.remove('hidden')
    setTimeout(() => backBtn.style.opacity = 100, 500)
    listingsEl.classList.remove('hidden')
    setTimeout(() => listingsEl.style.opacity = 100, 500)
}







