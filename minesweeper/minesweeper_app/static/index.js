// This was just demonstration of posting to django using js rather than form submit, keep for later
// const testBtn = document.getElementById("generate-grid");

// async function getGrid(url, data) {
//   try {
//     const response = await fetch(url, {
//      method: 'POST',
//      headers: {
//        'Content-Type': 'application/json'
//        },
//        body: JSON.stringify(data)
//      });
//      let res = await response.json();
//      console.log(res)
//    } catch(error) {
//       console.log(error)
//      } 
//   }



//   testBtn.onclick = ()=>{
//       const obj = JSON.parse('{"row":5, "col":5, "bomb":10}');
//       getGrid("/generate", obj);
//   };