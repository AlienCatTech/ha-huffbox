<script lang="ts">
	import Icon from '@iconify/svelte';
	import heart from '@iconify/icons-mdi/heart';
	import { stateStore } from '$lib/stores';
	import { LoadingBox } from '@flexilte/skeleton';

	export let heartRateState: string;
	export let pulseState: string;

	let heartRate: number;
	let pulse: any;
	stateStore.subscribe((states: Record<string, any>) => {
		heartRate = states[heartRateState] ?? 0;
		pulse = states[pulseState] ?? 0;
	});
</script>

{#if heartRate}
	<div class="flex mx-auto items-center">
		<div class="text-8xl">
			{#if pulse}
				<Icon class="w-full text-red-600 glow-icon-error" icon={heart} />
			{:else}
				<Icon class="w-full text-red-600 opacity-0 glow-icon-error" icon={heart} />
			{/if}
		</div>
		<div class="text-5xl glow-text">{heartRate}</div>
	</div>
{:else}
	<LoadingBox />
{/if}
