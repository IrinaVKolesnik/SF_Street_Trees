// ========================================

ShowCaretaker();

function ShowCaretaker() {
    var care_url="/care";
    var care_name_array = new Array();
    var care_count_array = new Array();
    Plotly.d3.json(care_url, function(error, response) {  
        for(var i=0; i<response.length; i++)
        {
            care_name_array=response[0]["caretakers"]
            care_count_array=response[0]["counts"]
        }
        DrawPieChart(care_count_array,care_name_array, "Trees per Caretaker", "stats_div");
    }); 
}

function ShowOldest() {
    var url="/oldest";
    Plotly.d3.json(url, function(error, response) {
        var statDivEle = document.getElementById("stats_div");
        statDivEle.innerHTML = "DATE: "+ response.plant_date;
        statDivEle.innerHTML += "</br>SPECIES: "+ response.species;
        statDivEle.innerHTML += "<br/>ADDRESS: "+ response.address;
    });
}

function ShowTop(subquery, title) {
    var url="/"+subquery;
    Plotly.d3.json(url, function(error, response) {
        var name_array = new Array();
        var count_array = new Array();
        for(var i=0; i<response.length; i++)
        {
            name_array=response[0]["names"]
            count_array=response[0]["counts"]
        }    
        DrawBarChart(count_array, name_array, name_array, title, "stats_div");
    });
}

function ShowTopFoliageVariety() {
    var url="/topfoliagevariety";
    Plotly.d3.json(url, function(error, response) {
        var statDivEle = document.getElementById("stats_div");
        statDivEle.innerHTML = "";
        response.forEach(element => {
            statDivEle.innerHTML += "<br>"; 
            statDivEle.innerHTML += "Species: "+element.foliage;            
            statDivEle.innerHTML += " Count: "+element.species_count;            
        });
    });
}

function ShowTopFoliageAmount() {
    var  foliage_url="/foliage";
    Plotly.d3.json(foliage_url,function(error2, response2) {
        var foliage_name_array = new Array();
        var foliage_count_array = new Array();
        for(var i=0; i<response2.length; i++)
        {
            foliage_name_array=response2[0]["foliages"]
            foliage_count_array=response2[0]["counts"]
        }
    
        DrawPieChart(foliage_count_array, foliage_name_array, "Foliage", "stats_div");
    }); 
}

function ShowAllVariety() {
    var url="/allvariety";
    Plotly.d3.json(url, function(error, response) {
        var statDivEle = document.getElementById("stats_div");
        statDivEle.innerHTML = "";
        response.forEach(element => {
            statDivEle.innerHTML += "<br>"; 
            statDivEle.innerHTML += "Species: "+element.foliage;            
            statDivEle.innerHTML += " Count: "+element.species_count;            
        });
    });
}




//Create a PIE chart that uses your data  
function DrawPieChart(value_array, name_array, title, div_name)
{
    //var value_array = value_array.slice(0,10);
    //var name_array = name_array.slice(0,10);
    //var hovertext_array = hovertext_array.slice(0,10);

    var divElement = document.getElementById(div_name);
    divElement.innerHTML = "";
    var data = [{
        values: value_array,
        labels: name_array,
        type: "pie"
    }];
    var layout = {
        widht: 500,
        height: 800,
        title: title
    };
    Plotly.newPlot(divElement, data, layout);
    divElement.classList.add(div_name);
}

//Create a PIE chart that uses your data  
function DrawBarChart(value_array, name_array, hovertext_array, title, div_name)
{
    var divElement = document.getElementById(div_name);
    divElement.innerHTML = "";
    var data = [{
        y: value_array,
        x: name_array,
        hovertext: hovertext_array,
        type: "bar"
    }];
    var layout = {
        widht: 500,
        height: 800,
        title: title
    };
    Plotly.newPlot(divElement, data, layout);
    divElement.classList.add(div_name);
}
