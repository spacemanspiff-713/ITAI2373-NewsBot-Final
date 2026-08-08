async function call(url,payload){let r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});document.querySelector('#output').textContent=JSON.stringify(await r.json(),null,2)}
function analyze(){call('/api/analyze',{text:document.querySelector('#text').value})} function ask(){call('/api/query',{query:document.querySelector('#query').value})}
