
$(document).ready(function() {
    $('#suggestion').keyup(function(){
        var query = $(this).val();
        $.get('/stocks/suggest/', {suggestion: query}, function(data){
            $('#stocks').html(data);
            });
    });
    $("#tickerForm").on("submit", function(e){
        e.preventDefault();
        $.ajax({
            url: "/stocks/quote/",
            type: "get",
            data: {
                ticker: $("#suggestion").val()
            },
            dataType: 'json',
            success: function(data){
                if(data.result == 'exist'){
                 window.location.href="/stocks/" + data.ticker +"/";
                }else{
                    $("#suggestion").val("");
                    document.getElementById("suggestion").placeholder = "Ticker isn't in my list. Try another.";
                    //$("#id_username").focus();
                    $("#suggestion").on("keydown", function(){
                        document.getElementById("suggestion").placeholder = "Ticker Search";
                    });
                }
            }
        });
    });

    // $("#trendTable a").on("click", function(e){
    //     e.preventDefault();
    //     var trend_ticker =  $(this).attr("id");
    //     console.log('hello');
    //     console.log(trend_ticker);
    //     $.ajax({
    //             url: "/stocks/eda/",
    //             type: "get",
    //             data: {"ticker": trend_ticker},
    //             dataType: "json",
    //             success: function(data){
    //               console.log('returned');
    //                 $("#scatter").tab('show');
    //                 chartType = "scatter";
    //                 dateVal = data.dateVal;
    //                 start = data.start;
    //                 end = data.end;
    //                 vol = data.vol;
    //                 min = data.min;
    //                 max = data.max;
    //                 openVal = data.open;
    //                 highVal = data.high;
    //                 lowVal = data.low;
    //                 closeVal = data.close;
    //                 // realVol = data.realVol.map(function(v) {
    //                 //                             return v.toLocaleString('en');
    //                 //                             });
    //                 // volmn = data.volMin;
    //                 // volmx = data.volMax;
    //                 //console.log(dateVal);
    //                 if (chartPeriod == '1D'){
    //                 // need to call this function because whole doc is not
    //                 // reloaded
    //                     x.style.display = "block";
    //                     intradayChart(dateVal, closeVal, vol, min, max);
    //                 }else {
    //                 //     //dateVal = dateVal.map(function(d) {return new Date(d * 1000);});
    //                 //     start = data.start;
    //                 //     end = data.end;
    //                     if (chartPeriod == '5D' || chartPeriod == '10D'){
    //                         x.style.display = "none";
    //                     }else{
    //                         x.style.display = "block";
    //                     }
    //                     hIntradayChart(dateVal, closeVal, vol, min, max);
    //                 }
    //             },
    //
    //      });
    // });



});

//begin
function intradayChart(x, y, v, mn, mx) {
    document.getElementById("scatter").innerHTML = symbol + ": " + name;
    var chartWidth = document.getElementById("line").parentElement.clientWidth;
    var d3 = Plotly.d3;
            //need to put #
    var gd3 = d3.select("#line")
                .style({
                        width: (chartWidth - 2) +'px' ,
                        height: "350px",
                });
    var gd = gd3.node();
    var data1 = {
                  x: x,
                  y: y,
                  mode: 'lines',
                  type: 'scatter',
                  fill: 'tozeroy',
                  line: {color:'rgb(0,170,230)'},
                  name: 'Price',
                  //hovertext: y,
                  hoverinfo: y+name,
            };
    var data2 = {
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

    var trace = [data1, data2];
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
                        showgrid: false,
                        //autorange: false,
                        tickformat: "%I:%M %p",
                        //tickmode: "auto",
                        linecolor: "#fff",
                        tickfont: { size:10, color:'rgb(0, 120, 180)' },

                    },
                    yaxis: {
                        fixedrange: true,
                        range: [mn, mx],
                        side: "right",
                        separatethousands: true,
                        exponentformat: "none",
                        nticks: 5,
                        overlaying: "y2",
                    },
                    yaxis2: {
                        range: [mn, mx], //[volmn, volmx],
                        fixedrange: true,
                        //overlaying: "y",
                        showgrid: false,
                    },

                };

    Plotly.newPlot(gd, trace, layout, {scrollZoom: true,
                                            displayModeBar: false });

} // end of intradayChart() tickformat: "%I:%M %p,%b %d'%y",

function intradayChart_no_vol(x, y, mn, mx) {
    var chartWidth = document.getElementById("line").parentElement.clientWidth;
    var d3 = Plotly.d3;
            //need to put #
    var gd3 = d3.select("#line")
                .style({
                        width: (chartWidth - 2) +'px' ,
                        height: "350px",
                });
    var gd = gd3.node();

    var data1 = {
                    x: x,
                    y: y,
                    mode: 'lines',
                    type: 'scatter',
                    fill: 'tozeroy',
                    line: {color:'rgb(0,170,230)'},
                    name: 'Price',
            };

    var trace = [data1];
    var layout = {
                    autosize: true,
                    margin:{l:0, t:5, r:45, b:30, pad:0},
                    dragmode: "pan",
                    showlegend: false,
                    xaxis: {
                        //range: [start, end],
                        ticks: "outside",
                        type: "category",
                        fixedrange: false,
                        showgrid: false,
                        //autorange: false,
                        //tickformat: "%I:%M %p,%b %d'%y",
                        //tickformat: "%I:%M %p",
                        nticks: 4,
                        //tickmode: "auto",
                        linecolor: "#fff",
                        tickfont: { size:10, color:'rgb(0, 120, 180)' },

                    },
                    yaxis: {
                        fixedrange: true,
                        range: [mn, mx],
                        side: "right",
                        separatethousands: true,
                        exponentformat: "none",
                        nticks: 5,
                    },

                };
    document.getElementById("scatter").innerHTML = symbol + ": " + name;
    Plotly.newPlot(gd, trace, layout, {scrollZoom: true,
                                            displayModeBar: false });

} //end

function hIntradayChart(x, y, v, mn, mx) {
    document.getElementById("scatter").innerHTML = symbol + ": " + name;

    var chartWidth = document.getElementById("line").parentElement.clientWidth;
    var d3 = Plotly.d3;
    //need to put #
    var gd3 = d3.select("#line")
                .style({
                        width: (chartWidth - 2) +'px' ,
                        height: "350px",
                });
    var gd = gd3.node(); //make global variable

    var data1 = {
                x: x,
                y: y,
                mode: 'lines',
                type: 'scatter',
                fill: 'tozeroy',
                line: {color:'rgb(0,200,255)'},
                name: 'Price',
                //hovertext: y,
                hoverinfo: y+name,

            };
    var data2 = {
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
    var trace = [data1, data2];

    var layout = {
                autosize: true,
                margin:{l:0, t:5, r:45, b:30, pad:0},
                dragmode: "pan",
                showlegend: false,
                xaxis: {
                    ticks: "outside",
                    type: "category",
                    fixedrange: false,
                    showgrid: false,
                    nticks: 4,
                    linecolor: "#fff",
                    side: "bottom",
                    tickfont: {size:10, color:'rgb(0, 120, 180)'},
                    //rangeslider: {range: [start, end]}
                },
                yaxis: {
                        fixedrange: true,
                        range: [mn, mx],
                        side: "right",
                        separatethousands: true,
                        exponentformat: "none",
                        nticks: 5,
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
    Plotly.newPlot(gd, trace, layout, {scrollZoom: true,
                                            displayModeBar: false });

} // end of hIntradayChart()

function hCandleChart(x, o, h, l, c, mn, mx) {
            var chartWidth = document.getElementById("line").parentElement.clientWidth;
            var d3 = Plotly.d3;
            var gd3 = d3.select("#candle")
                        .style({
                                width: (chartWidth - 2) +'px' ,
                                height: "350px"
                           });
            var gd = gd3.node();

            //console.log(x.map(function(d) { return new Date(d); }));
            var fig = PlotlyFinance.createCandlestick(
                    {
                        open: o,
                        high: h,
                        low: l,
                        close: c,
                        dates: x.map(function(d) { return new Date(d); })

                    }
                );

            fig.layout.autosize = true;
            fig.layout.margin = {l:0, t:5, r:45, b:30, pad:0};
            fig.layout.dragmode = "pan";

            fig.layout.xaxis = {
                            nticks: 4,
                            type: "date",
                            ticks: "outside",
                            //tickvals:x,
                            //ticktext:x,
                            fixedrange: true,
                            //autorange: false,

                            showgrid: false,
                            linecolor: "#fff",
                            side: "bottom",
                            tickfont: {size:10, color:'rgb(0, 120, 180)' },

                        };

            fig.layout.yaxis = {
                            range : [mn, mx],
                            fixedrange: false,
                            side: "right",
                            separatethousands: true,
                            nticks: 6,

                        };

            Plotly.newPlot(gd, fig.data, fig.layout, {scrollZoom: true,
                                            displayModeBar: false });

} // end of hCandleChart()


function candleChart(x, o, h, l, c, mn, mx) {
    var chartWidth = document.getElementById("line").parentElement.clientWidth;
    var d3 = Plotly.d3;
    var gd3 = d3.select("#candle")
                .style({
                        width: (chartWidth - 2) +'px' ,
                        height: "300px"
                });
    var gd = gd3.node();
    var fig = PlotlyFinance.createCandlestick(
                    {
                        open: o,
                        high: h,
                        low: l,
                        close: c,
                        dates: x
                            //.map(function(d) { return new Date(d); })
                    }
            );

    fig.layout.autosize = true;
    fig.layout.margin = {l:0, t:5, r:45, b:30, pad:0};
    fig.layout.dragmode = "pan";
    fig.layout.xaxis = {
                            type: "date",
                            range: [start, end],
                            fixedrange: false,
                            showgrid: false,
                            //autorange: false,
                            tickformat: "%I:%M %p",
                            linecolor: "#fff",
                            side: "bottom",
                            tickfont: {size:10, color:'rgb(0, 120, 180)' },
            };
    fig.layout.yaxis = {
                            range : [mn, mx],
                            fixedrange: false,
                            side: "right",
                            separatethousands: true,
                            //tickmode: "auto",
            };

    Plotly.newPlot(gd, fig.data, fig.layout, {scrollZoom: true,
                                            displayModeBar: false });

} // end of candleChart()

function resizeChart(w){
    var activeTab = $(".tab-content").find(".active");
    var id = activeTab.attr('id');
    var d3 = Plotly.d3;

    var gd3;

    gd3 = d3.select("#" + id);

    var gd = gd3.node();
    var update = {
                    width: w -2
            };
    Plotly.relayout(gd, update);
}

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

        x.innerHTML = "<a id= " + trending[i] + " href = /summary/"
                + trending[i] + "/ " + " style= color:" + trendType[i]
                +"; >" + trending[i] + "</a>";

    }
}

$(document).ready(function(){
    //this is for chart tabs
    $(".nav-tabs a").click(function(event){
        event.preventDefault();
        var id = $(this).attr("id"); //get id value
        if (chartType == id){
            //if clicked to same tab as shown chart
            return;
        }
        $(this).tab('show');
        //console.log('chartype ' + chartType, 'chartperiod ' + chartPeriod );
        if (id == "candlestick"){
            chartType = "candlestick";
            //if (chartPeriod == 'd1'){
            //    candleChart(dateVal, openVal, highVal, lowVal, closeVal, min, max);
            //}else {
            hCandleChart(dateVal, openVal, highVal, lowVal, closeVal, min, max);
            //}
        }else if (id == "scatter"){
            chartType = "scatter";
            if(chartPeriod == '1D'){
                intradayChart(dateVal, closeVal, vol, min, max);
            }else{
                hIntradayChart(dateVal, closeVal, vol, min, max);
            }
        }else{
            chartType = "fillingList";

            $.ajax({
                url: "/fillings/",
                type: "POST",
                data: {
                    'ticker': window.symbol,
                },
                dataType: 'json',
                success: function(data){
                    if (data.result == "gotIt"){
                        var fillingNum = data.form.length;
                        var list ="<strong style='color:rgb(0, 172, 230);'>&nbsp &nbsp Recent ";
                        list += fillingNum + " fillings:</strong><ul>";
                        for( i=0; i < fillingNum; i++){
                            list += "<li><a class='fillingSource' href=" + data.dUrl[i] + " target=_blank>" + data.form[i]
                                + ", (" + data.fDate[i] + "): " + data.des[i] + "</a></li>";

                        }
                        list += "</ul>";
                    }else if(data.result == "invalid"){
                        var list = "<br>&nbsp &nbsp There are no fillings for stock index.";
                    }
                    $("#filling").html(list);
                    $(".fillingSource").click(function(){
                        $("#suggestion").focus();
                    });
                }
            });
        }
    });
    //this is for different chartPeriod
    $(".histChart a").click(function(e){
        e.preventDefault();
        var id = $(this).attr("id");

        if (chartPeriod != id)
        {
            document.getElementById(chartPeriod).style.color = "rgb(0,170,0)";
            document.getElementById(id).style.color = "rgb(170,0,0)";
            var x = document.getElementById('candlestick');

            chartPeriod = id;

            //console.log(id + symbol);
            $.ajax({
                    url: "/hChart/",
                    type: "POST",
                    data: {"chartPeriod": id, "ticker": symbol},
                    dataType: "json",
                    success: function(data){
                        $("#scatter").tab('show');
                        chartType = "scatter";
                        dateVal = data.dateVal;
                        start = data.start;
                        end = data.end;
                        vol = data.vol;
                        min = data.min;
                        max = data.max;
                        openVal = data.open;
                        highVal = data.high;
                        lowVal = data.low;
                        closeVal = data.close;
                        // realVol = data.realVol.map(function(v) {
                        //                             return v.toLocaleString('en');
                        //                             });
                        // volmn = data.volMin;
                        // volmx = data.volMax;
                        //console.log(dateVal);
                        if (chartPeriod == '1D'){
                        // need to call this function because whole doc is not
                        // reloaded
                            x.style.display = "block";
                            intradayChart(dateVal, closeVal, vol, min, max);
                        }else {
                        //     //dateVal = dateVal.map(function(d) {return new Date(d * 1000);});
                        //     start = data.start;
                        //     end = data.end;
                            if (chartPeriod == '5D' || chartPeriod == '10D'){
                                x.style.display = "none";
                            }else{
                                x.style.display = "block";
                            }
                            hIntradayChart(dateVal, closeVal, vol, min, max);
                        }
                    },

             });
        }

    });
    //
    // $("#trendTable a").on("click", function(e){
    //     e.preventDefault();
    //     var id = $(this).attr("id");
    //     console.log(id);
    //
    // });

    $(window).resize(function(){
        //updates chartWidth
        newRowWidth = document.getElementById("line").parentElement.clientWidth;
        // to exclude about
        if ( symbol != 1234){
            resizeChart(newRowWidth);
        }
        resizeTrend(newRowWidth);
    });

    //hIntradayChart(dateVal, closeVal, vol, min, max);
    intradayChart(dateVal, closeVal, vol, min, max);
});


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
