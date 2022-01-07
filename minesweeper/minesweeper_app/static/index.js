const testBtn = document.getElementById("generate-grid");

async function getGrid(url, data) {
  try {
    const response = await fetch(url, {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
     });
     let res = await response.json();
     console.log(res)
   } catch(error) {
      console.log(error)
     } 
  }

// function getGrid(url, data) {
//     fetch(url, {
//      method: 'POST',
//      headers: {
//        'Content-Type': 'application/json'
//        },
//        body: JSON.stringify(data)
//      }).then((response)=> response.json())
//      .then((data)=>{
//        console.log(data);
//      })

//   }




  testBtn.onclick = ()=>{
      const obj = JSON.parse('{"row":5, "col":5, "bomb":10}');
      // console.log(typeof obj)
      getGrid("/generate", obj);
  };