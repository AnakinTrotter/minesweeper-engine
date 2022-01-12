// rerenders the grid depending on the game status
function renderGrid(arr) {
    let i = 0;
    let j = 0;
    $(".grid-container").children()
        .each(function () {
            $(this).children()
                .each(function () {
                    $(this).text(arr[i][j]);
                    j++;
                })
            i++;
            j=0;
        });
}

function replaceBomb(arr){
    for (let i = 0; i < arr.length; i++) {
        for(let j = 0; j< arr[i].length; j++){
            if(arr[i][j] == "-"){
                arr[i][j] = "💣";
            }
        }
    }
    return arr;
}

// post method to let the server know the point has been clicked
async function addPoint(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        let res = await response.json();
        console.log(res);
        let grid = res.user_map;
        if(res.game_over){
            if(!res.win)
                alert("Game Over: L");
            else
            {
                alert("Nice");
                replaceBomb(grid);
            }
            $('.grid-cell').off('click');
            // make play again button visible 
        }
        renderGrid(grid);
    } catch (error) {
        console.log(error)
    }
}

// onClick handler for each cell, will create server call to tell the server that the cell has been clicked
$(".grid-cell").click(function () {
    var row = $(this).parent().attr('row-num');
    var col = $(this).attr('col-num');
    // add flag type later idk
    const obj = { "row": row, "col": col, "type": "click" }
    // console.log(row, col)
    addPoint("/add-point", obj)
});