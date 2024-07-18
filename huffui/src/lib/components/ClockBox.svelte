<script lang="ts">
	import { stateStore } from '$lib/stores';
	import { onMount } from 'svelte';

	export let type = '';
	export let state;
	export let content = '';
	let text = '';
	export let classList = '';
	function secondsToHHMMSS(seconds: number): string {
		const hours = Math.floor(seconds / 3600);
		const minutes = Math.floor((seconds % 3600) / 60);
		const remainingSeconds = seconds % 60;

		const pad = (num: number): string => num.toString().padStart(2, '0');

		return `${pad(hours)}:${pad(minutes)}:${pad(remainingSeconds)}`;
	}
	function countdownUntil(timeString: string): string {
		// Parse the input time string
		const [hours, minutes, seconds] = timeString.split(':').map(Number);

		// Create a Date object for the target time
		const now = new Date();
		const targetTime = new Date(
			now.getFullYear(),
			now.getMonth(),
			now.getDate(),
			hours,
			minutes,
			seconds
		);

		// If the target time is earlier than now, set it to tomorrow
		if (targetTime < now) {
			targetTime.setDate(targetTime.getDate() + 1);
		}

		// Calculate the difference in seconds
		const diffSeconds = Math.floor((targetTime.getTime() - now.getTime()) / 1000);

		// Convert seconds to hh:mm:ss format
		const countdownHours = Math.floor(diffSeconds / 3600);
		const countdownMinutes = Math.floor((diffSeconds % 3600) / 60);
		const countdownSeconds = diffSeconds % 60;

		// Pad with zeros and return the formatted string
		const pad = (num: number): string => num.toString().padStart(2, '0');
		return `${pad(countdownHours)}:${pad(countdownMinutes)}:${pad(countdownSeconds)}`;
	}

	function calcu() {
		if (type === 'countdown') {
			text = countdownUntil(content);
		}
	}
	onMount(() => {
		const interval = setInterval(calcu, 1000);

		return () => {
			clearInterval(interval);
		};
	});
	stateStore.subscribe((states: Record<string, any>) => {
		content = states[state] ?? '';
		if (type === 'second') {
			text = secondsToHHMMSS(Number(content));
		}
	});
</script>

<div class={classList}>{text}</div>
