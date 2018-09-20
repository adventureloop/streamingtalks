function setupcharts() 
{
	var charts = {}
	charts.internalline = c3.generate({
		bindto: ".internal-line",
		data: {
			columns: [
				['rx'].concat(new Array(100).fill(0)),
				['tx'].concat(new Array(100).fill(0)),
			]
		},
		point: {
			show: false
		},
		axis: {
			y: { show: false },
			x: { show: false }
		},
		legend: { hide: true },
		interaction: {enabled: false},
		transition: { duration: 0 },
	});
	charts.externalline = c3.generate({
		bindto: ".external-line",
		data: {
			columns: [
				['rx'].concat(new Array(100).fill(0)),
				['tx'].concat(new Array(100).fill(0)),
			]
		},
		point: {
			show: false
		},
		axis: {
			y: { show: false },
			x: { show: false }
		},
		legend: { hide: true },
		interaction: {enabled: false},
		transition: { duration: 0 },
	});
	return charts;
}

var ws;

function init()
{
	var charts = setupcharts();

	websocketuri= "ws://" + window.location.hostname + ":8080/ifstatus";

	ws = new WebSocket(websocketuri, "SUPERNET");

	ws.onopen = function (event) {
		console.log("ws connected");
	};

	ws.onmessage = function (event) {
		netdata = JSON.parse(event.data);

		if(!netdata['interfaces'] ||!netdata['interfaces'].length)
			return;

		charts.eth1line.load({
			columns: [
				['rx'].concat(netdata[eth1]["rx"]),
				['tx'].concat(netdata[eth1]["tx"])
			]
		});
	}
}
