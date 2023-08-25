
  let data;
  function fetchData(selectedChannels, selectedFiles) {
    console.log("Fetching data...");
    console.log(selectedChannels)
    console.log(selectedFiles)
    // Make an AJAX request to the backend with selectedChannel and selectedFile
    const startTime = performance.now();
    $.ajax({
      url: "/fetch_data",
      type: "POST",
      data: JSON.stringify({ channels: selectedChannels, files: selectedFiles }),
      contentType: "application/json",
      success: function (response) {
        data = response;
        console.log("Data received successfully:", response);
        // Render the data received from the backend on the webpage
        displayData(response);
        const endTime = performance.now();
        const elapsedTime = endTime - startTime;
        console.log("Data received in", elapsedTime, "milliseconds");
      },
      error: function(xhr, status, error) {
        console.error("Error fetching data:", error);
      },
    });
  }


    // Function to generate random colors for the chart
   function getRandomColor() {
    const minChannelValue = 0; // Adjust this value to control minimum channel value
    const maxChannelValue = 128;
    let color = '#';
    for (let i = 0; i < 3; i++) {
      const channelValue = Math.floor(Math.random() * (maxChannelValue - minChannelValue) + minChannelValue);
      color += channelValue.toString(16).padStart(2, '0'); // Convert to hex and pad if needed
    }
    return color;
  }


 function displayData(data) {
  document.getElementById('chartContainer').innerHTML = '';
      // Prepare data for the charts
 
      const chartData = [];
      const chartOptions = {
      responsive: true,
      scales: {
    x: {
      type: 'time',
      adapters: {
        date: {
          zone: 'GMT'
        }
      },
      time: {
        unit: 'second'
      },
    },
        y: {
          beginAtZero: true,
        },

      },
      plugins: {
        legend: {
          display: true,
        },
        tooltip: {
        callbacks: {
          label: function (context) {
              const timestamp = new Date(context.parsed.x).toUTCString();
              const value = context.parsed.y;
            return `${timestamp} - ${value}`;
          },
        },
        maxWidth: 300,
      },
        zoom: {
          pan: {
            enabled: true,
            mode: 'xy', // Enable both X and Y pan
            speed: 1,
            threshold: 0.1,
          },
          zoom: {
            wheel: {
              enabled: true,
            },
            pinch: {
              enabled: true,
            },
            mode: 'xy', // Enable both X and Y zoom
            
          },
        },
      },
    
    };

      // Create a map to store values for each channel and date combination
      const channelDateDataMap = new Map();

      // Loop through the data and aggregate values for each channel and date
      data.forEach((item) => {
        const { timestamp, value, channel } = item;


        // Convert the timestamp to a Luxon DateTime instance
        const dateTime = luxon.DateTime.fromISO(timestamp);
        
        // Create a unique identifier for the graph using channel and date
        const graphId = `${channel}-${dateTime.toISODate()}`;

        // Check if the graph already exists in the channelDateDataMap
        if (channelDateDataMap.has(graphId)) {
          channelDateDataMap.get(graphId).push({ x: dateTime, y: value });
        } else {
          // If the graph is not in the map, create a new entry
          channelDateDataMap.set(graphId, [{ x: dateTime, y: value }]);
        }
      });

      // Clear the previous charts
      if (window.chartInstances) {
        Object.values(window.chartInstances).forEach((chart) => {
          chart.destroy();
        });
      }

      // Empty the chartInstances object
      window.chartInstances = {};

      // Loop through the channelDateDataMap to create datasets and chart instances
      channelDateDataMap.forEach((dataPoints, graphId) => {
        const randomColor = getRandomColor();
        chartData.push({
          label: graphId,
          data: dataPoints,
          borderColor: randomColor,
          backgroundColor: randomColor,
          pointRadius: 0,
          showLine: true,
          borderWidth: 0.5
        });

        const chartConfig = {
          type: 'line',
          data: {
            datasets: [chartData[chartData.length - 1]],
          },
          options: chartOptions,
        };
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container';

        const resetButton = document.createElement('button');
        resetButton.textContent = 'Reset Zoom';
        resetButton.onclick = () => resetZoom2(graphId);


        const ctx = document.createElement('canvas');
        ctx.width = 600;
        ctx.height = 400;
        chartContainer.appendChild(resetButton);
        chartContainer.appendChild(ctx);
        document.getElementById('chartContainer').appendChild(chartContainer);
        const newChartInstance = new Chart(ctx, chartConfig);

        // Store the chart instance in the window object
        window.chartInstances[graphId] = newChartInstance;
      });
    }

    function resetZoom2(graphId) {
  if (window.chartInstances && window.chartInstances[graphId]) {
    window.chartInstances[graphId].resetZoom();
  }
}


function updateGraphs() {
    console.log("Updating graphs...");
    // Get the selected start and end times from the dropdowns
    const selectedStartTime = document.getElementById("startTimeSelector").value;
    const selectedEndTime = document.getElementById("endTimeSelector").value;
    const selectedStartHour = parseInt(selectedStartTime.split(":")[0]);
    const selectedEndHour = parseInt(selectedEndTime.split(":")[0]);
    console.log("Selected Start Time:", selectedStartTime);
    console.log("Selected End Time:", selectedEndTime);
    console.log("Converted Start Time:", selectedStartHour);
    console.log("Converted End Time:", selectedEndHour);
    console.log("Data Timestamps:");
    data.forEach((item) => {
    console.log(item.timestamp);
  });

    // Filter data based on the selected time frame
    const filteredData = data.filter((item) => {
        const timestamp = luxon.DateTime.fromISO(item.timestamp, { zone: 'GMT' });
        console.log(timestamp);
        const timestampHour = timestamp.hour;
        console.log(timestampHour);
        return timestampHour >= selectedStartHour && timestampHour <= selectedEndHour;
    });
    console.log(filteredData)

    // Display statistics (max, mean, min) if data is available
    displayStatistics(filteredData);

    // Render the graphs for the selected time frame
    displayData(filteredData);
}

function displayStatistics(data) {
    const statisticsContainer = document.getElementById("statisticsContainer");

    if (data.length > 0) {
        // Calculate max, mean, and min values
        const values = data.map((item) => item.value);
        const max = Math.max(...values);
        const mean = values.reduce((acc, val) => acc + val, 0) / values.length;
        const min = Math.min(...values);

        // Display statistics
        statisticsContainer.innerHTML = `
            <p>Max Value: ${max}</p>
            <p>Mean Value: ${mean.toFixed(2)}</p>
            <p>Min Value: ${min}</p>
        `;
    } else {
        // No data available for the selected time frame
        statisticsContainer.innerHTML = "No data available for the selected time frame.";
    }
}















  