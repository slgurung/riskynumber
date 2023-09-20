
//begin intradayChart
function intradayChart(x, y, v, mn, mx) {
  //for window resize event, this need to be inside the function
  var chartWidth = lineTab.parentElement.clientWidth;
  lineTab.style.height = "350px";
  lineTab.style.width = (chartWidth - 2) +'px' ;
  document.getElementById("scatter").innerHTML = symbol + ": " + name;
  //set color of active chartPeriod, this function is called once in begining
  //this is made default color instead
  //set color of active chartPeriod & update chartPeriod global var
  // document.getElementById(chartPeriod).style.color = "rgb(0,170,0)";
  // document.getElementById('1D').style.color = "rgb(170,0,0)";
  // chartPeriod = '1D';
  //////////////////////////////////////////////////////////////////////
  var trace1 = {
                x: x,
                y: y,
                //mode: 'lines',
                type: 'scatter',
                fill: 'tozeroy',
                line: {color:'rgb(0,170,230)'},
                name: 'Price',
                //hovertext: y,
                hoverinfo: "y+x", // 'name' + 'y' not name + y
          };
  var trace2 = {
              x: x,
              y: v,
              yaxis: 'y2',
              //xaxis: 'x2',
              type: "bar",
              marker: {
                      color: 'rgb(0, 115, 150)'
              },
              name: 'Volume',
              // //text: v_text,
              hoverinfo: 'skip' //'y+name',
          };
  var data = [trace1, trace2];
  var layout = {
                  autosize: true,
                  margin:{l:0, t:5, r:45, b:30, pad:0},
                  dragmode: "pan",
                  showlegend: false,
                  xaxis: {
                      range: [start, end],
                      ticks: "outside",
                      type: "date",
                      fixedrange: false,
                      showgrid: true,
                      //autorange: false,
                      tickformat: "%I:%M %p",
                      linecolor: "#fff",
                      tickfont: { size:10, color:'rgb(0, 120, 180)' },
                  },
                  yaxis: {
                      fixedrange: true,
                      range: [mn, mx],
                      side: "right",
                      separatethousands: true,
                      exponentformat: "K",
                      tickmode: 'auto',
                      nticks: 6,
                      overlaying: "y2",
                  },
                  yaxis2: {
                      range: [mn, mx], //[volmn, volmx],
                      fixedrange: true,
                      //overlaying: "y",
                      showgrid: false,
                  },

              };

  Plotly.newPlot(lineTab, data, layout, {scrollZoom: true, displayModeBar: false });

} // end of intradayChart() tickformat: "%I:%M %p,%b %d'%y",

//begin updateIntraday
function updateIntraday(x, y, v, mn, mx) {
  //for window resize event, this need to be inside the function
  var chartWidth = lineTab.parentElement.clientWidth;
  lineTab.style.height = "350px";
  lineTab.style.width = (chartWidth - 2) +'px' ;
  document.getElementById("scatter").innerHTML = symbol + ": " + name;
  //set color of active chartPeriod & update chartPeriod global var
  document.getElementById(chartPeriod).style.color = "rgb(0,170,0)";
  document.getElementById('1D').style.color = "rgb(170,0,0)";
  chartPeriod = '1D';
  //////////////////////////////////////////////////////////////////////
  var trace1 = {
                x: x,
                y: y,
                //mode: 'lines',
                type: 'scatter',
                fill: 'tozeroy',
                line: {color:'rgb(0,170,230)'},
                name: 'Price',
                //hovertext: y,
                hoverinfo: "y+x", // 'name' + 'y' not name + y
          };
  var trace2 = {
              x: x,
              y: v,
              yaxis: 'y2',
              //xaxis: 'x2',
              type: "bar",
              marker: { color: 'rgb(0, 115, 150)' },
              name: 'Volume',
              // //text: v_text,
              hoverinfo: 'skip' //'y+name',
          };

  var data = [trace1, trace2];
  var layout = {
                  autosize: true,
                  margin:{l:0, t:5, r:50, b:30, pad:0},
                  dragmode: "pan",
                  showlegend: false,
                  xaxis: {
                      type: "date",
                      range: [start, end],
                      ticks: "outside",
                      // tickmode: 'auto',
                      // nticks: 5,
                      fixedrange: false,
                      showgrid: true,
                      autorange: false,
                      tickformat: "%I:%M %p",
                      linecolor: "#fff",
                      tickfont: { size:10, color:'rgb(0, 120, 180)' },

                  },
                  yaxis: {
                      fixedrange: true,
                      range: [mn, mx],
                      side: "right",
                      separatethousands: true,
                      exponentformat: "K",
                      tickmode: 'auto',
                      nticks: 6,
                      overlaying: "y2",
                  },
                  yaxis2: {
                      range: [mn, mx], //[volmn, volmx],
                      fixedrange: true,
                      //overlaying: "y",
                      showgrid: false,
                  },

              };
  // more efficient thant newPlot() for plotting in same div
  Plotly.react(lineTab, data, layout, {scrollZoom: true, displayModeBar: false });

} // end of updateIntraday() tickformat: "%I:%M %p,%b %d'%y",

// function intradayChart_no_vol(x, y, mn, mx) {
//   //for window resize event, this need to be inside the function
//   var chartWidth = lineTab.parentElement.clientWidth;
//   lineTab.style.height = "350px";
//   lineTab.style.width = (chartWidth - 2) +'px' ;
//   document.getElementById("scatter").innerHTML = symbol + ": " + name;
//   //////////////////////////////////////////////////////////////////////
//
//     var trace1 = {
//                     x: x,
//                     y: y,
//                     mode: 'lines',
//                     type: 'scatter',
//                     fill: 'tozeroy',
//                     line: {color:'rgb(0,170,230)'},
//                     name: 'Price',
//             };
//
//     var data = [trace1];
//     var layout = {
//                     autosize: true,
//                     margin:{l:0, t:5, r:45, b:30, pad:0},
//                     dragmode: "pan",
//                     showlegend: false,
//                     xaxis: {
//                         //range: [start, end],
//                         ticks: "outside",
//                         type: "category",
//                         fixedrange: false,
//                         showgrid: false,
//                         //autorange: false,
//                         //tickformat: "%I:%M %p,%b %d'%y",
//                         //tickformat: "%I:%M %p",
//                         tickmode: 'auto',
//                         nticks: 5,
//                         linecolor: "#fff",
//                         tickfont: { size:10, color:'rgb(0, 120, 180)' },
//
//                     },
//                     yaxis: {
//                         fixedrange: true,
//                         range: [mn, mx],
//                         side: "right",
//                         separatethousands: true,
//                         exponentformat: "K",
//                         tickmode: 'auto',
//                         nticks: 6,
//                     },
//
//                 };
//     document.getElementById("scatter").innerHTML = symbol + ": " + name;
//     Plotly.newPlot(lineTab, data, layout, {scrollZoom: true,
//                                             displayModeBar: false });
//
// } //end

function hIntradayChart(x, y, v, mn, mx) {
    //for window resize event, this need to be inside the function
    var chartWidth = lineTab.parentElement.clientWidth;
    lineTab.style.height = "350px";
    lineTab.style.width = (chartWidth - 2) +'px' ;
    document.getElementById("scatter").innerHTML = symbol + ": " + name;
    //////////////////////////////////////////////////////////////////////
    var trace1 = {
                x: x,
                y: y,
                //mode: 'lines',
                type: 'scatter',
                fill: 'tozeroy',
                line: {color:'rgb(0,200,255)'},
                name: 'Price',
                //hovertext: y,
                hoverinfo: "y+x",
              };
    var trace2 = {
                x: x,
                y: v,
                yaxis: 'y2',
                //xaxis: 'x2',
                type: "bar",
                marker: {
                        color: 'rgb(0, 115, 150)'
                },
                //name: 'Volume',
                //text: v_text,
                hoverinfo: 'skip' //'x+text+name',
            };
    var data = [trace1, trace2];

    var layout = {
                autosize: true,
                margin:{l:0, t:10, r:45, b:30, pad:0},
                dragmode: "pan",
                showlegend: false,
                xaxis: {
                    type: "category",
                    ticks: "outside",
                    tickmode: 'array',
                    tickvals: tickpos,
                    ticktext: tick_text,
                    //nticks: 5,
                    fixedrange: false,
                    showgrid: true,
                    linecolor: "#fff",
                    side: "bottom",
                    tickfont: {size:10, color:'rgb(0, 120, 180)'},
                    // rangeslider: {
                    //   range: [start, end]
                    // },
                },
                yaxis: {
                    fixedrange: true,
                    range: [mn, mx],
                    side: "right",
                    separatethousands: true,
                    exponentformat: "K",
                    tickmode: 'auto',
                    nticks: 6,
                    overlaying: "y2",
                    },
                yaxis2: {
                    range: [mn, mx], //[volmn, volmx],
                    fixedrange: true,
                    //overlaying: "y",
                    showgrid: false,
                    },
                // shapes: {
                //         type: 'line',
                //         x0: '2017-10-12',
                //         y0: 0,
                //         x1: '2017-10-12',
                //         //yref: 'paper',
                //         y1: 22500,
                //         line: {
                //             color: 'black',
                //             dash: 'dot',
                //             width: 1.5,
                //         },
                // },
            };
    Plotly.react(lineTab, data, layout, {scrollZoom: true, displayModeBar: false });

} // end of hIntradayChart()

function hCandleChart(x, o, h, l, c, mn, mx) {
    //var chartWidth = document.getElementById("line").parentElement.clientWidth;
    var chartWidth = lineTab.parentElement.clientWidth;
    candleTab.style.height = "350px";
    candleTab.style.width = (chartWidth - 2) +'px' ;

    var trace1 = {
        x: x,
        close: c,
        decreasing: {line: {color: '#ff0000'}},
        high: h,
        increasing: {line: {color: '#009900'}},
        line: {color: 'rgba(31,119,180,1)'},
        low: l,
        open: o,
        type: 'candlestick',
        xaxis: 'x',
        yaxis: 'y'
      };
    var data = [trace1];
    var layout = {
        dragmode: 'zoom',
        margin: {
          r: 40,
          t: 10,
          b: 0,
          l: 10,
          pad: 0
        },
        showlegend: false,
        xaxis: {
          type: 'category',
          autorange: true,
          tickmode: 'array',
          tickvals: tickpos,
          ticktext: tick_text,
          //fixedrange: false,
          domain: [0, 1],
          //range: [start, end],
          //rangeslider: {range: [start, end]},
        },
        yaxis: {
          //autorange: true,
          domain: [0, 1],
          range: [mn, mx],
          type: 'linear',
          side: "right",
          tickmode: 'auto',
          nticks: 6,
        }
    };
    Plotly.newPlot(candleTab, data, layout, {scrollZoom: true, displayModeBar: false });
} // end of hCandleChart()


function candleChart(x, o, h, l, c, mn, mx) {
    //var chartWidth = document.getElementById("line").parentElement.clientWidth;
    var chartWidth = lineTab.parentElement.clientWidth;
    candleTab.style.height = "350px";
    candleTab.style.width = (chartWidth - 2) +'px' ;
    //to update label on scatter tab when first chart for symbol is candlestick
    document.getElementById("scatter").innerHTML = symbol + ": " + name;

    var trace1 = {
        x: x,
        close: c,
        decreasing: {line: {color: '#ff0000'}},
        high: h,
        increasing: {line: {color: '#009900'}},
        line: {color: 'rgba(31,119,180,1)'},
        low: l,
        open: o,
        type: 'candlestick',
        xaxis: 'x',
        yaxis: 'y'
      };

    var data = [trace1];
    var layout = {
        dragmode: 'zoom',
        margin: {
          r: 40,
          t: 10,
          b: 0,
          l: 10,
          pad: 0
        },
        showlegend: false,
        xaxis: {
          //autorange: true,
          //domain: [0, 1],
          range: [start, end],
          rangeslider: {range: [start, end]},
          //title: 'Date',
          type: 'date'
        },
        yaxis: {
          //autorange: true,
          //domain: [0, 1],
          range: [mn, mx],
          type: 'linear',
          side: "right",
          tickmode: 'auto',
          nticks: 6,
        }
    };
    Plotly.newPlot(candleTab, data, layout, {scrollZoom: true, displayModeBar: false });
} // end of candleChart()

function resizeTrend(w){
    // trendCell is table row with id trendRow
    for ( i=0; i < colNum; i++){
        trendCell.deleteCell(-1);
    }
    colNum = parseInt(w/60);

    if (tikNum < colNum){
        colNum = tikNum;
    }

    for (i = 0; i < colNum; i++){
        var x = trendCell.insertCell(-1);
        x.innerHTML = "<a id= '" + trending[i] + "' href = '#' style= 'color:" + trendType[i] +";' >" + trending[i] + "</a>";
    }
}

function resizeChart(w){
    var update = {
                width: w -2
            };
    Plotly.relayout(lineTab, update); //global div variable lineTab

}

////// Start of document.ready() ///////////
$(document).ready(function() {
    $('#suggestion').keyup(function(){
        var query = $(this).val();
        $.get('/stocks/suggested_tickers/', {suggestion: query}, function(data){
            //this injects ticker.html at stock_list id in template
            $('#suggested_list').html(data);
        });
    });
    // didn't clear suggested list, maybe change to .change()
    // $('#suggestion').focus(function(){
    //   if($("#suggestion").val() == ""){
    //     $('#suggested_list').html("");
    //   }
    // });
    $("#tickerForm").on("submit", function(e){
        e.preventDefault();
        $.ajax({
            url: "/stocks/intraday/",
            type: "get",
            data: { ticker: $("#suggestion").val() },
            dataType: 'json',
            success: function(data){
                $("#suggestion").val(""); //clear input text
                $('#suggested_list').html(""); //clear suggested list
                if(data.result == 'success'){
                    /////// this is for non ajax call
                    // window.location.href="/stocks/summary/" + data.ticker +"/";
                    //don't use var to save it in global scope
                    dateVal = data.date;
                    closeVal = data.close;
                    vol = data.vol;
                    min = data.min;
                    max = data.max;
                    symbol = data.ticker;
                    name = data.name;
                    start = data.start;
                    end = data.end;
                    openVal = data.open;
                    highVal = data.high;
                    lowVal = data.low;
                    chartType = "scatter";
                    //to draw on current open chart tab
                    // if (chartType == 'scatter'){
                    //   updateIntraday(dateVal, closeVal, vol, min, max);
                    // }else if (chartType == 'candlestick') {
                    //   candleChart(dateVal, openVal, highVal, lowVal, closeVal, min, max);
                    // } else{
                    $("#scatter").tab('show');
                    updateIntraday(dateVal, closeVal, vol, min, max);
                    //}
                    //chartPeriod = "1D"; //don't set this here. It is done by updateIntraday()
                }else if(data.result == "not_found"){
                    document.getElementById("suggestion").placeholder = "Ticker not found! Try another.";
                    //$("#id_username").focus();
                    $("#suggestion").on("keydown", function(){
                        document.getElementById("suggestion").placeholder = "Ticker Search";
                    });
                }else{
                  document.getElementById("suggestion").placeholder = "Error Downloading! Try again.";
                  //$("#id_username").focus();
                  $("#suggestion").on("keydown", function(){
                      document.getElementById("suggestion").placeholder = "Ticker Search";
                  });
                }

            },
            error: function(jqXHR, error){
              alert("ERROR: " + error);
            }
        });
    });

    // This event handler is to clear suggested list if clicked
    // to anyother part of page.
    $("#tickerForm").on("focusout", function(event){
      //event.preventDefault();
      $("#suggestion").val(""); //clear input text
      $('#suggested_list').html(""); //clear suggested list
    });

    //$("#suggested_list a") doesn't work
    ////// mousedown is trigger before focusout but click is trigger after
    //focusout. So, instead of 'click' use 'mousedown' here so that this
    //event is trigger before above 'focusout' event.
    $("#suggested_list").on('mousedown', function(event){
      event.preventDefault();
      //console.log($(this).attr("id")); //gives suggested_list
      //console.log(event.target.nodeName);
      tagName = event.target.nodeName;
      //to trigger ajax when clicked on a tag only not li or ul tag
      if(tagName == 'A') {
        var ticker = event.target.getAttribute('id');
        //console.log(ticker);
        $.ajax({
            url: "/stocks/intraday/",
            type: "get",
            data: { ticker: ticker },
            dataType: 'json',
            success: function(data){
              $("#suggestion").val(""); //clear input text
              $('#suggested_list').html(""); //clear suggested list
              $("#suggestion").focus();
              //don't use var. These are global variables
              if(data.result == 'success'){
                  /////// this is for non ajax call
                  // window.location.href="/stocks/summary/" + data.ticker +"/";
                  //don't use var to save it in global scope
                  dateVal = data.date;
                  closeVal = data.close;
                  vol = data.vol;
                  min = data.min;
                  max = data.max;
                  symbol = data.ticker;
                  name = data.name;
                  start = data.start;
                  end = data.end;
                  openVal = data.open;
                  highVal = data.high;
                  lowVal = data.low;
                  chartType = "scatter";
                  //to draw scatter chart on scatter tab
                  $("#scatter").tab('show');
                  updateIntraday(dateVal, closeVal, vol, min, max);
                  //done in updateIntraday(), if setup before updateIntraday() gives inaccurate result
                  // chartPeriod = "1D";
              }else if(data.result == "not_found"){
                  document.getElementById("suggestion").placeholder = "Ticker not found! Try another.";
                  //$("#id_username").focus();
                  $("#suggestion").on("keydown", function(){
                      document.getElementById("suggestion").placeholder = "Ticker Search";
                  });
              }else{
                document.getElementById("suggestion").placeholder = "Error Downloading! Try again.";
                //$("#id_username").focus();
                $("#suggestion").on("keydown", function(){
                    document.getElementById("suggestion").placeholder = "Ticker Search";
                });
              }
            },
            error: function(jqXHR, error){
              alert("ERROR: " + error);
            }
        });
      }
    });

    //$("#trendTable a") works on original window size but won't detect
    //event after resize of window
    $("#trendTable").on('click dblclick', function(e){
      e.preventDefault();
      //var tikId = $(this).attr("id"); //gives 'trendTable'
      //console.log(tikId);
      //console.log(e.target);
      var tikId = e.target.getAttribute('id');
      //console.log(tikId);
      $.ajax({
          url: "/stocks/intraday/",
          type: "get",
          data: { ticker: tikId  },
          dataType: 'json',
          success: function(data){
            $("#suggestion").focus();
            //don't use var. These are global variables
            if(data.result == 'success'){
                /////// this is for non ajax call
                // window.location.href="/stocks/summary/" + data.ticker +"/";
                //don't use var to save it in global scope
                dateVal = data.date;
                closeVal = data.close;
                vol = data.vol;
                min = data.min;
                max = data.max;
                symbol = data.ticker;
                name = data.name;
                start = data.start;
                end = data.end;
                openVal = data.open;
                highVal = data.high;
                lowVal = data.low;
                chartType = "scatter";
                //to draw scatter chart on scatter tab
                $("#scatter").tab('show');
                updateIntraday(dateVal, closeVal, vol, min, max);
                 //done in updateIntraday(), if setup before updateIntraday() gives inaccurate result
                 //chartPeriod = "1D";
            }else if(data.result == "not_found"){
                document.getElementById("suggestion").placeholder = "Ticker not found! Try another.";
                //$("#id_username").focus();
                $("#suggestion").on("keydown", function(){
                    document.getElementById("suggestion").placeholder = "Ticker Search";
                });
            }else{
              document.getElementById("suggestion").placeholder = "Error Downloading! Try again.";
              //$("#id_username").focus();
              $("#suggestion").on("keydown", function(){
                  document.getElementById("suggestion").placeholder = "Ticker Search";
              });
            }
          },
          error: function(jqXHR, error){
            alert("ERROR: " + error);
          }
      });
    });

    $("#stkindex a").click(function(event){
        var tikId = $(this).attr("id");
        //console.log(tikId);
        $.ajax({
            url: "/stocks/intraday/",
            type: "get",
            data: { ticker:tikId },
            dataType: "json",
            success: function(data){
              $("#suggestion").focus();
              //don't use var. These are global variables
              if(data.result == 'success'){
                  /////// this is for non ajax call
                  // window.location.href="/stocks/summary/" + data.ticker +"/";
                  //don't use var to save it in global scope
                  dateVal = data.date;
                  closeVal = data.close;
                  vol = data.vol;
                  min = data.min;
                  max = data.max;
                  symbol = data.ticker;
                  name = data.name;
                  start = data.start;
                  end = data.end;
                  openVal = data.open;
                  highVal = data.high;
                  lowVal = data.low;
                  chartType = "scatter";
                  //to draw scatter chart on scatter tab
                  $("#scatter").tab('show');
                  updateIntraday(dateVal, closeVal, vol, min, max);
                  //done in updateIntraday(), if setup before updateIntraday() gives inaccurate result
                  // chartPeriod = "1D";
              }else{
                alert("ERROR: data download failed! Try again.");
              }
            },
            error: function(jqXHR, error){
              alert("ERROR: " + error);
            }

        });
    });

    $(".nav-tabs a").click(function(event){
        event.preventDefault();
        var id = $(this).attr("id"); //get id value
        //console.log(id);
        if (chartType == id){
            //if clicked to same tab as shown chart
            return;
        }
        $(this).tab('show');
        if (id == "candlestick"){
            chartType = "candlestick";
            if (chartPeriod == '1D'){
              candleChart(dateVal, openVal, highVal, lowVal, closeVal, min, max);
            }else {
              hCandleChart(dateVal, openVal, highVal, lowVal, closeVal, min, max);
            }
        }else if (id == "scatter"){
            chartType = "scatter";
            if(chartPeriod == '1D'){
                updateIntraday(dateVal, closeVal, vol, min, max);
            }else{
                hIntradayChart(dateVal, closeVal, vol, min, max);
            }
        }else{
            chartType = "fillingList";
            // $.ajax({
            //     url: "/fillings/",
            //     type: "POST",
            //     data: {
            //         'ticker': window.symbol,
            //     },
            //     dataType: 'json',
            //     success: function(data){
            //         if (data.result == "gotIt"){
            //             var fillingNum = data.form.length;
            //             var list ="<strong style='color:rgb(0, 172, 230);'>&nbsp &nbsp Recent ";
            //             list += fillingNum + " fillings:</strong><ul>";
            //             for( i=0; i < fillingNum; i++){
            //                 list += "<li><a class='fillingSource' href=" + data.dUrl[i] + " target=_blank>" + data.form[i]
            //                     + ", (" + data.fDate[i] + "): " + data.des[i] + "</a></li>";
            //
            //             }
            //             list += "</ul>";
            //         }else if(data.result == "invalid"){
            //             var list = "<br>&nbsp &nbsp There are no fillings for stock index.";
            //         }
            //         $("#filling").html(list);
            //         $(".fillingSource").click(function(){
            //             $("#suggestion").focus();
            //         });
            //     }
            // });
        }
    });

    //this is for different chartPeriod
    $(".histChart a").click(function(e){
        e.preventDefault();
        var id = $(this).attr("id");
        //console.log(id + ': ' + symbol);
        if (chartPeriod != id)
        {
            document.getElementById(chartPeriod).style.color = "rgb(0,170,0)";
            document.getElementById(id).style.color = "rgb(170,0,0)";
            //var x = document.getElementById('candlestick');
            chartPeriod = id; //update global chartPeriod variable
            //console.log(id + symbol);
            $.ajax({
                url: "/stocks/hdata/",
                type: "get",
                data: {"chartPeriod": id, "ticker": symbol},
                dataType: "json",
                success: function(data){
                    $("#scatter").tab('show');
                    chartType = "scatter";
                    if(data.result == 'success'){
                        dateVal = data.date;
                        closeVal = data.close;
                        vol = data.vol;
                        min = data.min;
                        max = data.max;
                        start = data.start;
                        end = data.end;
                        openVal = data.open;
                        highVal = data.high;
                        lowVal = data.low;

                        if (chartPeriod == '1D'){
                          //x.style.display = "block";
                          updateIntraday(dateVal, closeVal, vol, min, max);
                        }else {
                            // //dateVal = dateVal.map(function(d) {return new Date(d * 1000);});
                            // start = data.start;
                            // end = data.end;
                            // if (chartPeriod == '5D'){
                            //     //x.style.display = "none";
                            // }else{
                            //     //x.style.display = "block";
                            // }
                            tickpos = data.tickpos;
                            tick_text = data.tick_text;
                            hIntradayChart(dateVal, closeVal, vol, min, max);
                        }
                    }else{
                        alert('Downloading stock data failed! Try again.');
                    }

                },
                error: function(jqXHR, error){
                  alert("ERROR: " + error);
                }
           });
        }
    });


    $(window).resize(function(){
        //updates chartWidth
        newRowWidth = document.getElementById("line").parentElement.clientWidth;
        // to exclude about
        if ( symbol != 1234){
            resizeChart(newRowWidth);
        }
        resizeTrend(newRowWidth);
    });

    //this gets first chart when user starts the page
    intradayChart(dateVal, closeVal, vol, min, max);

}); // end of document.read()



$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
