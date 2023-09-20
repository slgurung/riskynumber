//////// for complete reference check version: v2 for both this version and all ajax calls //////////
//begin intradayChart
function intradayChart(x, y, v, mn, mx) {
  //for window resize event, this need to be inside the function
  var lineWidth = lineTab.parentElement.clientWidth;
  var baseHeight = Math.floor(trendWidth/2.6);
  chartTab.style.height = baseHeight + 25 +'px'; //"450px";
  lineTab.style.height = baseHeight + 'px';
  lineTab.style.width = (lineWidth - 2) +'px'
  //////////////////////////////////////////////////////////////////////
  document.getElementById("scatter").innerHTML = symbol + ": " + name;

  var trace1 = {
                x: x,
                y: y,
                mode: 'lines',
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
                  margin:{l:0, t:15, r:45, b:30, pad:0},
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

  Plotly.newPlot(lineTab, data, layout, {scrollZoom: true, displaylogo: false, displayModeBar: true,
            modeBarButtonsToRemove: [ 'autoScale2d', 'zoom2d', 'pan2d', 'select2d', 'lasso2d',
            'hoverCompareCartesian','hoverClosestCartesian', 'toggleSpikelines'] });

} // end of intradayChart() tickformat: "%I:%M %p,%b %d'%y",

//begin updateIntraday
function updateIntraday(x, y, v, mn, mx) {
  //for window resize event, this need to be inside the function
  var lineWidth = lineTab.parentElement.clientWidth;
  var baseHeight = Math.floor(trendWidth/2.6);
  chartTab.style.height = baseHeight + 25 +'px'; //"450px";
  lineTab.style.height = baseHeight + 'px';
  lineTab.style.width = (lineWidth - 2) +'px'
  //////////////////////////////////////////////////////////////////
  document.getElementById("scatter").innerHTML = symbol + ": " + name;
  //////////////////////////////////////////////////////////////////////
  //set color of active chartPeriod & update chartPeriod global var
  document.getElementById(chartPeriod).style.color = "rgb(0,170,0)";
  document.getElementById('1D').style.color = "rgb(170,0,0)";
  chartPeriod = '1D';
  //////////////////////////////////////////////////////////////////////
  var trace1 = {
                x: x,
                y: y,
                mode: 'lines', //this eliminates dot on plot
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
                  margin:{l:0, t:15, r:50, b:30, pad:0},
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
  Plotly.react(lineTab, data, layout, {scrollZoom: true, displaylogo: false, displayModeBar: true,
            modeBarButtonsToRemove: [ 'autoScale2d', 'zoom2d', 'pan2d', 'select2d', 'lasso2d',
            'hoverCompareCartesian','hoverClosestCartesian', 'toggleSpikelines'] });

} // end of updateIntraday() tickformat: "%I:%M %p,%b %d'%y",

function hIntradayChart(x, y, v, mn, mx) {
    var lineWidth = lineTab.parentElement.clientWidth;
    var baseHeight = Math.floor(trendWidth/2.6);
    chartTab.style.height = baseHeight + 25 +'px'; //"450px";
    lineTab.style.height = baseHeight + 'px';
    lineTab.style.width = (lineWidth - 2) +'px'
    /////////////////////////////////////////////////////
    document.getElementById("scatter").innerHTML = symbol + ": " + name;
    //////////////////////////////////////////////////////////////////////
    var trace1 = {
                x: x,
                y: y,
                mode: 'lines',
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
                margin:{l:0, t:15, r:45, b:30, pad:0},
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
            };
            //react() is making chart zoom automatice with double click
    Plotly.newPlot(lineTab, data, layout, {scrollZoom: true, displaylogo: false, displayModeBar: true,
              modeBarButtonsToRemove: [ 'autoScale2d', 'zoom2d', 'pan2d', 'select2d', 'lasso2d',
              'hoverCompareCartesian','hoverClosestCartesian', 'toggleSpikelines'] });

} // end of hIntradayChart()

function hCandleChart(x, o, h, l, c, mn, mx) {
    //for window resize event, this need to be inside the function
    var lineWidth = lineTab.parentElement.clientWidth;
    var baseHeight = Math.floor(trendWidth/2.6);
    chartTab.style.height = baseHeight + 25 +'px'; //"450px";
    candleTab.style.height = baseHeight + 'px';
    candleTab.style.width = (lineWidth - 2) +'px'

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
        dragmode: 'pan',
        margin: {
          r: 40,
          t: 15,
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
          fixedrange: true, //makes non zoomable by scrolling
          domain: [0, 1],
        },
        yaxis: {
          autorange: true,
          domain: [0, 1],
          range: [mn, mx],
          type: 'linear',
          side: "right",
          tickmode: 'auto',
          nticks: 6,
        }
    };
    Plotly.newPlot(candleTab, data, layout, {scrollZoom: false, displaylogo: false, displayModeBar: true,
              modeBarButtonsToRemove: [ 'autoScale2d', 'zoom2d', 'pan2d', 'select2d', 'lasso2d',
              'hoverCompareCartesian','hoverClosestCartesian', 'toggleSpikelines'] });
} // end of hCandleChart()

function candleChart(x, o, h, l, c, mn, mx) {
    //for window resize event, this need to be inside the function
    var lineWidth = lineTab.parentElement.clientWidth;
    var baseHeight = Math.floor(trendWidth/2.6);
    chartTab.style.height = baseHeight + 25 +'px'; //"450px";
    candleTab.style.height = baseHeight + 'px';
    candleTab.style.width = (lineWidth - 2) +'px'

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
        dragmode: 'pan',
        margin: {
          r: 40,
          t: 15,
          b: 0,
          l: 10,
          pad: 0
        },
        showlegend: false,
        xaxis: {
          //autorange: false,
          domain: [0, 1],
          range: [start, end],
          type: 'date',
          fixedrange: true, //this makes non zoomable
        },
        yaxis: {
          //autorange: false, //if range is provide this is false by default
          domain: [0, 1],
          range: [mn, mx],
          type: 'linear',
          side: "right",
          tickmode: 'auto',
          nticks: 6,
        }
    };
    Plotly.newPlot(candleTab, data, layout, {scrollZoom: false, displaylogo: false, displayModeBar: true,
              modeBarButtonsToRemove: [ 'autoScale2d', 'zoom2d', 'pan2d', 'select2d', 'lasso2d',
              'hoverCompareCartesian','hoverClosestCartesian', 'toggleSpikelines'] });
} // end of candleChart()

function resizeTrend(w){
    // trendCell is table row with id trendRow
    console.log('hello');
    for ( i=0; i < colNum; i++){
        trendCell.deleteCell(-1);
    }
    colNum = parseInt(w/60);

    if (tikNum < colNum){
        colNum = tikNum;
    }

    for (i = 0; i < colNum; i++){
        var x = trendCell.insertCell(-1);
        x.innerHTML = "<a id= " + trending[i] + " href = '/stocks/" + trending[i] + "/' " + " style= 'color:" + trendType[i] +";'>" + trending[i] + "</a>";
    }
}

function realtime_quote(data){
  var latestPrice = data.latestPrice;
  var latestTime = data.latestTime;
    
  if (!['^GSPC', '^DJI', '^IXIC'].includes(symbol)){
    var changePercent = data.changePercent;
    var change = data.change;
    var changecolor = data.changecolor;
    var changesymbol = data.changesymbol;
    var week52High = data.week52High;
    var week52Low = data.week52Low;
    $("#add_tik").html("<span class='glyphicon glyphicon-plus-sign'></span>");
    $("#tik").text( symbol +":");
    $("#tik").css( 'color', changecolor);
    $("#lp").text( latestPrice );
    $("#lp").css( 'color', changecolor);
    document.getElementById("udarrow").className = changesymbol;
    $("#udarrow").css( 'color', changecolor);
    $("#chg").text(change);
    $("#cp").text("(" + changePercent + ")");
    $("#cp").css( 'color', changecolor);
    //$("#lv").text( "vol: " + latestVolume );
    // don't need to convert? already converted to current tz
    $("#lt").text("@"+latestTime);
    
    $("#lh").text("52W Range: ["+ week52Low + " - " + week52High+ "]" );
    $("#lh").css( 'color', '#408000');
    
  }else{
    $("#tik").text( symbol +":");
    $("#lp").text( latestPrice );
    $("#lt").text("@"+latestTime);
    
  }

}

function create_stockNews_list(stk_news){
  //var news = {{ stockNews|safe }};
  $("#stockNewsTitle").html('');
  var ul = document.createElement("UL");
  ul.setAttribute("id", "stockNewsTitle");

  document.getElementById("stock_news").appendChild(ul);
  for(i =0; i < stk_news.length; i++){
      var li = document.createElement("LI");
      var a = document.createElement("A");
      li.appendChild(a);
      var newsTitle = document.createTextNode(stk_news[i]["title"]);
      a.setAttribute("href", stk_news[i]["link"]);
      a.setAttribute("target", "_blank");
      a.appendChild(newsTitle);
      document.getElementById("stockNewsTitle").appendChild(li);
  }
}
//maybe don't need this
function create_marketNewslist(mkt_news){
  //var news = {{ businessNews|safe }};
  $("#business_news").html('');
  var ul = document.createElement("UL");
  ul.setAttribute("id", "bizNewsTitle");
  ul.setAttribute("class", "bizNews");
  document.getElementById("business_news").appendChild(ul);
  for(i =0; i < mkt_news.length; i++){
      var li = document.createElement("LI");
      var a = document.createElement("A");
      li.appendChild(a);
      var newsTitle = document.createTextNode(mkt_news[i]["title"]);
      a.setAttribute("href", mkt_news[i]["link"]);
      a.setAttribute("target", "_blank");
      a.appendChild(newsTitle);
      document.getElementById("bizNewsTitle").appendChild(li);
  }
}

//this is much fater than load()
function update_wl_stk(data){
  var stk_list = data.stock_list;
  //faster than load()
  $("#wl_ul").html('');
  var stk_num = stk_list.length;
  var wl_stk_html= "<strong class='watchlist_title'>" + data.wl_name + "</strong>"
  wl_stk_html += '<span class="glyphicon glyphicon-triangle-right wl_arrow"></span>'
  if (stk_num > 0){
    for(var i=0; i<stk_num; i++){
      wl_stk_html += '<li class="wl_li"><a href="#" id= a_' + stk_list[i] + '>'+stk_list[i]
      wl_stk_html += '</a>&nbsp&nbsp<span id= ' + stk_list[i] + ' '
      wl_stk_html += 'class="glyphicon glyphicon-remove-sign wl_cursor remove_tik"'
      wl_stk_html += ' data-toggle="tooltip" data-placement="bottom" title="Remove!"></span></li>'
    }
  }else{
    wl_stk_html += '<strong style="color: rgb(0, 102, 153);">Watchlist is empty! Add some symbols.</strong>';
  }
  $("#wl_ul").html(wl_stk_html);
}

////// Start of document.ready() ///////////
$(document).ready(function() {
    //trigger include 'stocks/ticker.html' at suggested_list
    $('#suggestion').keyup(function(){
        var query = $(this).val();
        $.get('/stocks/symbol/suggested_tickers/', {suggestion: query}, function(data){
            //this injects ticker.html at stock_list id in template
            $('#suggested_list').html(data);
        });
    });
    //trigger include 'stocks/ticker.html' at add_ticker_list
    $('#suggested_watchlist_ticker').keyup(function(e){
        e.preventDefault();
        var query = $(this).val();
        $.get('/stocks/symbol/suggested_tickers/', {suggestion: query}, function(data){
            //this injects ticker.html at stock_list id in template
            $('#add_ticker_list').html(data);
        });
    });

    $("#tickerForm").on("submit", function(e){
        e.preventDefault();
        var ticker = $("#suggestion").val().toLowerCase();
        //to prevent empty ticker value calling ajax
        if (ticker != ''){
          $.ajax({
              url: "/stocks/symbol/search/", //"/stocks/symbol/intraday/",
              type: "get",
              data: { ticker: ticker },
              dataType: 'json',
              success: function(data){
                  $("#suggestion").val(""); //clear input text
                  $('#suggested_list').html(""); //clear suggested list
                  if(data.result == 'success'){
                      /////// this is for non ajax call
                      window.location.href="/stocks/" + ticker +"/";

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
    /// changing search key letters to uppercase as type
    $("#tickerForm").on("keyup", function(event){
      //event.preventDefault();
      $("#suggestion").val($("#suggestion").val().toUpperCase());
    });
    /////////////
    ////// mousedown is trigger before focusout but click is trigger after focusout
    ///////////////
    // This event handler is to clear suggested list if clicked
    // to anyother part of page.
    $("#tickerForm").on("focusout", function(event){
      //event.preventDefault();
      $("#suggestion").val(""); //clear input text
      $('#suggested_list').html(""); //clear suggested list
    });
    //instead of using href in ticker.html, because href click is triggered
    //only after above focusout event which prevent click to work
    $("#suggested_list").on('mousedown', function(event){
      var tagName = event.target.nodeName;
      if(tagName == 'A') {
          var ticker = event.target.getAttribute('id').toLowerCase();
          window.location.href="/stocks/" + ticker +"/";
      }
    });

    //this is div for suggested ticker list
    //when click on ticker, it clear list and display the ticker in input form
    $("#add_ticker_list").on('mousedown', function(e){
        var tn = e.target.nodeName;
        if(tn == 'A') {
          var ticker = e.target.getAttribute('id');
          //console.log(ticker);
          $("#suggested_watchlist_ticker").val(ticker);
          $('#add_ticker_list').html("");
        }
    });

    //this catches click on chart tabs and get correct chart tab id
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
        }else if(id == "filingList"){
            chartType = "filingList";
            filingTab.style.height = lineTab.style.height;

            $.ajax({
                url: "/filings/sec_filing/",
                type: "POST",
                data: {
                    'ticker': window.symbol,
                },
                dataType: 'json',
                success: function(data){
                    if (data.result == "gotIt"){
                        var filing_list = data.filing_list;
                        var filing_num = filing_list.length;
                        var html_str ="<table class='table table-striped filing_table'><tr><th colspan='4' style='text-align:center;'> Recent " + filing_num + " fillings</th></tr>";
                        html_str += "<tr><th></th><th>Filing Date</th><th style='padding-left:20px;'>Form Description</th><th style='padding-left:20px;'>Form Name with Doc Link</th></tr>";
                        for(i=0; i < filing_num; i++){
                            var num = i+1;
                            html_str += "<tr><td style='padding-left:20px;'>"+ num +"</td><td>"+filing_list[i]['filing_date']+"</td><td style='padding-left:20px;'>"+filing_list[i]['description']+"</td>";
                            html_str += "<td style='padding-left:20px;'><a class='fillingSource' href=" + filing_list[i]["url"] + " target=_blank>" +
                                        filing_list[i]["form"] + "</a></td></tr>";

                        }
                        html_str += "</table>";
                    }else if(data.result == "invalid"){
                        var html_str = "<h3 style='text-align:center;'>There are no fillings for stock index!</h3>";
                    }else{
                        var html_str = "<h3 style='text-align:center;'>Couldn't find CIK number for the symbol!</h3>";
                    }
                    $("#filing").html(html_str);
                    $(".fillingSource").click(function(){
                        $("#suggestion").focus();
                    });
                }
            });
        }else if(id == "stkNews"){
            chartType = "stkNews";
            newsTab.style.height = lineTab.style.height;

            $.ajax({
                url: "/newsmedia/stock_news/",
                type: "POST",
                data: {
                    'ticker': window.symbol,
                },
                dataType: 'json',
                success: function(data){
                    if (data.result == "gotIt"){
                        var news_list = data.news_list;
                        var news_num = news_list.length;
                        var html_str ="<table class='table table-striped news_table'><tr><th colspan='2' "
                            html_str += "style='text-align:center; color:rgb(0,170,0);'> <h5>Recent " + 
                                        news_num + " News Headlines</h5></th></tr>";
                       
                        for(i=0; i < news_num; i++){
                            var num = i+1;
                            html_str += "<tr><td style='padding-left:20px;'>"+ num +"</td>";
                            html_str += "<td style='padding-left:20px;'><a class='newsSource' href=" + news_list[i]["link"] +
                                       " target=_blank>" + news_list[i]["title"] + "</a></td></tr>";

                        }
                        html_str += "</table>";
                    }else if(data.result == "invalid"){
                        var html_str = "<h3 style='text-align:center;'>There are no News for stock index!</h3>";
                    }else{
                        var html_str = "<h3 style='text-align:center;'>Couldn't find news for the symbol!</h3>";
                    }
                    $("#news").html(html_str);
                    $(".newsSource").click(function(){
                        $("#suggestion").focus();
                    });
                }
            });





          // chartType = "stkNews";
          // newsTab.style.height = lineTab.style.height;
          // var news_num = stockNews.length;
          
          // var html_str =("<table class='table table-striped news_table'><tr><th colspan='2' style='text-align:center;'> Recent " 
          //   + news_num + " news</th></tr>");
          //     html_str += "<tr><th></th><th>Headlines</th></tr>";
          //     for(i=0; i < news_num; i++){
          //         var num = i+1;
          //         html_str += "<tr><td style='padding-left:20px;'>"+ num +"</td>";
          //         html_str += "<td style='padding-left:20px;'><a class='newsSource' href=" + stockNews[i]["link"] + " target=_blank>" +
          //                     stockNews[i]["title"] + "</a></td></tr>";

          //     }
          //     html_str += "</table>";

          // $("#news").html(html_str);
          // $(".newsSource").click(function(){
          //               $("#suggestion").focus();
          //           });          
      }
    });

    //this is for different chartPeriod
    $(".histChart a").click(function(e){
        e.preventDefault();
        var id = $(this).attr("id");
        console.log(id + ': ' + symbol + ': ' + chartPeriod);
        if (chartPeriod != id)
        {
            document.getElementById(chartPeriod).style.color = "rgb(0,170,0)";
            document.getElementById(id).style.color = "rgb(170,0,0)";
            //var x = document.getElementById('candlestick');
            chartPeriod = id; //update global chartPeriod variable
            //console.log(id + symbol);
            $.ajax({
                url: "/stocks/symbol/hdata/",
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
    //prompt for login to get watchlist if not logged in
    $("#authenticate_watchlist").on('click', function(e){
      e.preventDefault();
      $("#loginModal").modal();
    });
    //getting watchlist page if current page is different when logged in
    $("#mywatchlist").on('click', function(){
      //ar current_url = window.location.href;
      //console.log(current_url.includes('watchlist'));
      //if(current_url.includes('watchlist')){
        $('html, body').animate({
          'scrollTop': $("#watchlist_div").position().top
        });
        $("#suggested_watchlist_ticker").focus();
      //}else{
      //  window.location.href = '/watchlist/';
      //}
    });
    //scroll to add form with click on navbar
    $("#add_to_list").on('click', function(){
      $('html, body').animate({
        'scrollTop': $("#watchlist_div").position().top
      });
      $("#suggested_watchlist_ticker").focus();
    });
    //to draw linechart for ticker in watchlist
    //$("#wl_div a").on('click', function(e) doesn't work after
    //reloading <a> tags.
    $("#wl_div").on('click', 'a', function(e){
      //extracting ticker from id
      var id = $(this).attr("id").split('_')[1];
      $.ajax({
        url:"/watchlist/watchlist_stocks/",
        type: "get",
        data: {"ticker": id},
        dataType: "json",
        success: function(data){
          //$("#suggestion").focus();
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
               realtime_quote(data);
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
    //for tooltip
    $('[data-toggle="tooltip"]').tooltip();
    //to remove ticker in watchlist
    $("#wl_ul").on('click dblclick', ".remove_tik",function(){
        var id = $(this).attr("id");
        //console.log(id);
        $.ajax({
          url:"/watchlist/remove_ticker/",
          type: "get",
          data: {"ticker": id},
          dataType: "json",
          success: function(data){
            update_wl_stk(data);
          },
          error: function(jqXHR, error){
            alert("ERROR: " + error);
          }
        });
    });
    //****************working
    // $("#watchlistForm").on("focusout", function(event){
    //   //event.preventDefault();
    //   $("#suggestion").val(""); //clear input text
    //   $('#suggested_list').html(""); //clear suggested list
    // });
    //to add ticker to watchlist
    $("#watchlistForm").on('submit', function(e){
      //this prevent form submit from the default action
      //otherwise it will look for /watchlist/?add_ticker=ticker
      e.preventDefault();
      var ticker = $("#suggested_watchlist_ticker").val();
      $("#suggested_watchlist_ticker").val('');
      $('#add_ticker_list').html("");
      $("#suggested_watchlist_ticker").focus();
      //console.log(ticker);
      //to prevent empty data causing ajax
      if (ticker != ''){
        $.ajax({
          url:"/watchlist/add_ticker/",
          type: "get",
          data: { ticker: ticker  },
          dataType: 'json',
          success: function(data){
            update_wl_stk(data);
          },
          error: function(jqXHR, error){
            alert("ERROR: " + error);
          }
        });
      }
    });

    //to add ticker  in  realtime quote to watchlist
    $("#add_tik").on("click", function(e){
      e.preventDefault();
      //console.log(symbol);
      $.ajax({
        url: "/watchlist/add_ticker/",
        type: "get",
        data: { ticker: symbol  },
        dataType: 'json',
        success: function(data){
          //console.log(data.user_name);
          //don't need to check this for watchlistForm and wl_ul
          if(data.user_name == ''){
            $("#loginModal").modal();
          }else{
            update_wl_stk(data);
          }
        }
      });
    });
    //scroll to news div wilth click on news menubar
    $("#news_menu").on('click', function() {
      $('html, body').animate({
        'scrollTop': $("#news_div").position().top
      });
    });

    $(window).resize(function(){
        trendWidth = document.getElementById("trendTable").parentElement.clientWidth;
        //to avoid about and howto page chart resize
        if(data_type != 'abouthowto'){
          var lineWidth = lineTab.parentElement.clientWidth;
          var baseHeight = Math.floor(trendWidth/2.6);
          chartTab.style.height = baseHeight + 25 +'px'; //"450px";
          lineTab.style.height = baseHeight + 'px';
          filingTab.style.height = baseHeight + 'px';
          lineTab.style.width = (lineWidth - 2) +'px'
          if (chartType == "scatter"){
            Plotly.relayout(lineTab, {});
          }else if (chartType == "candlestick"){
            //not working for candlelight
            //Plotly.relayout(candleTab, update);
            if (chartPeriod == '1D'){
                candleChart(dateVal, openVal, highVal, lowVal, closeVal, min, max);
            }else{
                hCandleChart(dateVal, openVal, highVal, lowVal, closeVal, min, max);
            }
          }
        }

        resizeTrend(trendWidth);
    });
    //this gets call when user sends request through stocks/<ticker>/ URL
    //but not thru ajax call. If blocks avoid charting for about and how page load
    if (data_type == "intraday"){
      //this is where realtime quote is updated when page for a stock is loaded first time
      realtime_quote(qinfo); // displays real time quote
      intradayChart(dateVal, closeVal, vol, min, max);
            
    }else if(data_type =="daily"){
      //this is where realtime quote is updated when page for a stock is loaded first time
      realtime_quote(qinfo);
      hIntradayChart(dateVal, closeVal, vol, min, max);
      
    }


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
