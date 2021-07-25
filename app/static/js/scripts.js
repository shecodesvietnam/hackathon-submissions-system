let creative = document.getElementById("creative").addEventListener("input", calculateTotalGrade)
let accessible = document.getElementById("accessible").addEventListener("input", calculateTotalGrade)
let techOption1 = document.getElementById("techOption1").addEventListener("input", calculateTotalGrade)
let techOption2 = document.getElementById("techOption2").addEventListener("input", calculateTotalGrade)
let techOption3 = document.getElementById("techOption3").addEventListener("input", calculateTotalGrade)
let demo = document.getElementById("demo").addEventListener("input", calculateTotalGrade)
let pitching = document.getElementById("pitching").addEventListener("input", calculateTotalGrade)
let totalGrade = document.getElementById("totalGrade")


function calculateTotalGrade(e) {
    let total = 0
    let creative = document.getElementById("creative").value
    let accessible = document.getElementById("accessible").value
    let techOption1Value = document.getElementById("techOption1").value
    let techOption2Value = document.getElementById("techOption2").value
    let techOption3Value = document.getElementById("techOption3").value
    let demo = document.getElementById("demo").value
    let pitchingValue = document.getElementById("pitching").value

    total += parseInt(creative) + parseInt(accessible) + parseInt(techOption1Value) + parseInt(techOption2Value) + parseInt(techOption3Value) + parseInt(demo) + parseInt(pitchingValue)

    totalGrade.innerHTML = total
}