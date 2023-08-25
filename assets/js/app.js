$(document).ready(function () {
  // Function to update the graphs when dropdown selections change
  function updateGraphs() {
    // Get the selected options from the 'Select Channel' dropdown
    var selectedChannels = $("#test").val();

    // Get the selected option from the 'Select Date' dropdown
    var selectedDate = $("#test_2").val();

    // Check if both dropdowns have a valid selection
    if (selectedChannels && selectedChannels.length > 0 && selectedDate) {
      // Fetch the data for the selected .parquet file from the backend
      $.getJSON("/get_data", { filename: selectedDate }, function (data) {
        var datasets = [];

        // Prepare datasets for the selected columns
        for (var i = 0; i < selectedChannels.length; i++) {
          var channelData = data[selectedChannels[i]];
          datasets.push({
            name: selectedChannels[i],
            data: channelData,
          });
        }

        console.log(datasets);

        // Configure the ApexCharts options for the line charts
        var options = {
          series: [{data:datasets}]
          chart: {
            type: "line",
            height: 160,
            width: 300
          },
          yaxis: {
            labels: {
              minWidth: 40
            }
          },
          
        };

        // Render the line charts with the updated data
        for (var j = 1; j <= 5; j++) {
          var chartElementId = "#chart-line" + j;
          var chart = new ApexCharts(
            document.querySelector(chartElementId),
            options
          );
          chart.render();
        }
      });
    }
  }

  // Call the updateGraphs function when dropdown selections change
  $("#test, #test_2").change(function () {
    updateGraphs();
  });

  // Initial graph update
  updateGraphs();
});
