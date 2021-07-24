let creativeOption1 = document.getElementById("creative-0").addEventListener("click", calculateTotalGrade)
let creativeOption2 = document.getElementById("creative-1").addEventListener("click", calculateTotalGrade)
let creativeOption3 = document.getElementById("creative-2").addEventListener("click", calculateTotalGrade)
let accessibleOption1 = document.getElementById("accessible-0").addEventListener("click", calculateTotalGrade)
let accessibleOption2 = document.getElementById("accessible-1").addEventListener("click", calculateTotalGrade)
let accessibleOption3 = document.getElementById("accessible-2").addEventListener("click", calculateTotalGrade)
let accessibleOption4 = document.getElementById("accessible-3").addEventListener("click", calculateTotalGrade)
let techOption1 = document.getElementById("techOption1").addEventListener("input", calculateTotalGrade)
let techOption2 = document.getElementById("techOption2").addEventListener("input", calculateTotalGrade)
let techOption3 = document.getElementById("techOption3").addEventListener("input", calculateTotalGrade)
let demoOption1 = document.getElementById("demo-0").addEventListener("click", calculateTotalGrade)
let demoOption2 = document.getElementById("demo-1").addEventListener("click", calculateTotalGrade)
let demoOption3 = document.getElementById("demo-2").addEventListener("click", calculateTotalGrade)
let pitching = document.getElementById("pitching").addEventListener("input", calculateTotalGrade)
let totalGrade = document.getElementById("totalGrade")


function calculateTotalGrade(e) {
    let total = 0
    let creative = document.getElementsByName("creative");
    let accessibility = document.getElementsByName("accessible");
    let demo = document.getElementsByName("demo");
    let techOption1Value = document.getElementById("techOption1").value
    let techOption2Value = document.getElementById("techOption2").value
    let techOption3Value = document.getElementById("techOption3").value
    let pitchingValue = document.getElementById("pitching").value
      
    for (i = 0; i < creative.length; i++) {
        if (creative[i].checked) {
            total += parseInt(creative[i].value)
        }
    }
      
    for (i = 0; i < accessibility.length; i++) {
        if (accessibility[i].checked) {
            total += parseInt(accessibility[i].value)
        }
    }
 
    for (i = 0; i < demo.length; i++) {
        if (demo[i].checked) {
            total += parseInt(demo[i].value)
        }
    }

    total += parseInt(techOption1Value) + parseInt(techOption2Value) + parseInt(techOption3Value) + parseInt(pitchingValue)

    totalGrade.innerHTML = total
}