import('/node_modules/@canvasjs/charts/canvasjs.min.js').then(()=>console.log('CanvasJS imported'));

const form = document.querySelector('form');

form.addEventListener('submit', (e) => {
	e.preventDefault();

	const formData = new FormData(form);

	const object = {};
	formData.forEach(function(value,key) {
		object[key] = value;
	});
	
	fetch('http://192.168.0.28:5000/getPredictionOutput', {
		method: 'POST',
		headers: {
			'Content-type': 'application/json'
		},
		body: JSON.stringify(object)
	}).then(data => data.json())
		.then(data => {
			createChart(object, data.predict);
		})
});

function createChart(object, prediction) {
	const chartHolder = document.createElement('div');
	chartHolder.setAttribute('id', 'chartContainer')
	chartHolder.setAttribute('style', 'height: 370px; width: 100%;')
	form.insertAdjacentElement('afterend', chartHolder);

	let series = object.series.split(',');
	series = series.map(a => parseFloat(a));

	var chart = new CanvasJS.Chart("chartContainer", {
		animationEnabled: true,
		theme: "light2",
		title:{
			text: "Close price prediction"
		},
		data: [{        
			type: "line",
			indexLabelFontSize: 16,
			dataPoints: [
				{ y: series[0] },
				{ y: series[1] },
				{ y: series[2] },
				{ y: series[3] },
				{ y: series[4] },
				{ y: series[5] },
				{ y: series[6] },
				{ y: series[7] },
				{ y: series[8] },
				{ y: series[9] },
				{ y: series[10] },
				{ y: series[11] },
				{ y: series[12] },
				{ y: series[13] },
				{ y: series[14] },
				{ y: series[16] },
				{ y: series[16] },
				{ y: series[17] },
				{ y: series[18], lineColor: "red", markerType: "triangle", indexLabel: "prediction \u2193", indexLabelOrientation: "vertical" },
				{ y: prediction[0], lineColor: "red", markerColor: "red" },
				{ y: prediction[1], lineColor: "red", markerColor: "red" },
				{ y: prediction[2], markerColor: "red" }
			]
		}]
	});
	chart.render();

}