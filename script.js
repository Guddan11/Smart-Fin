function calculate() {
    let income = document.getElementById("income").value;
    let expenses = document.getElementById("expenses").value;

    fetch('/api/budget', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ income, expenses })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText =
            "Savings: " + data.savings + " | " + data.message;
    });
}

function scrollToBudget() {
    document.getElementById("budget").scrollIntoView();
}