<script lang="ts">
	import { stateStore } from '$lib/stores';
	import { onMount } from 'svelte';
	import uPlot from 'uplot';

	export let state: string;
	export let stroke: string = 'red';

	let chart: uPlot;
	let data: [number[], number[]] = [[Date.now() / 1000], [70]];

	const options = {
		title: '',
		width: 800,
		height: 300,
		legend: {
			show: false
		},
		series: [
			{},
			{
				stroke,
				width: 5,
				points: {
					show: false
				}
			}
		],
		axes: [
			{
				show: false,
				grid: {
					show: false
				}
			},
			{
				stroke: 'black',
				grid: {
					stroke: '#eee',
					width: 1,
					dash: [1, 0] // Solid horizontal lines
				}
			}
		],
		scales: {
			x: {
				time: false
			},
			y: {
				range: (_u: unknown, dataMin: number, dataMax: number) => {
					if (dataMin === dataMax) {
						return [dataMin - 1, dataMax + 1];
					}
					return [dataMin, dataMax];
				}
			}
		}
	};

	onMount(() => {
		const element = document.getElementById('ecg-chart');
		options.width = element?.parentElement?.scrollWidth!;
		options.height = element?.parentElement?.scrollHeight!;
		if (element) chart = new uPlot(options, data, element);
		window.addEventListener('resize', () => {
			chart.setSize({ width: options.height, height: options.height });
		});
		chart.setSize({ width: options.height, height: options.height });
	});

	// Function to update chart with new data point
	function addDataPoint(timestamp: number, ecgValue: number) {
		const windowSize = 100;
		const animationDuration = 300; // Duration in milliseconds
		const frameDuration = 20; // Duration of each frame in milliseconds
		const numberOfFrames = animationDuration / frameDuration;

		data[0].push(timestamp);
		data[1].push(ecgValue);

		if (data[0].length > windowSize) {
			data[0].shift();
			data[1].shift();
		}

		let frame = 0;
		const initialXMin = chart.scales.x.min;
		const initialXMax = chart.scales.x.max;
		const targetXMin = data[0][0];
		const targetXMax = data[0][data[0].length - 1];

		const animate = () => {
			const easingFactor = frame / numberOfFrames;
			const currentXMin = initialXMin + (targetXMin - initialXMin) * easingFactor;
			const currentXMax = initialXMax + (targetXMax - initialXMax) * easingFactor;

			chart.batch(() => {
				chart.setData(data);
				chart.setScale('x', {
					min: currentXMin,
					max: currentXMax
				});
				chart.setScale('y', {
					min: Math.min(...data[1]),
					max: Math.max(...data[1])
				});
			});

			if (frame < numberOfFrames) {
				frame++;
				requestAnimationFrame(animate);
			}
		};

		animate();
	}

	stateStore.subscribe((states: Record<string, any>) => {
		const now = Date.now() / 1000;
		if (chart) addDataPoint(now, Number(states[state]));
	});
</script>

<div id="ecg-chart" class="max-h-80" />
<div class="u-under" />
