<script lang="ts">
	import { LoadingBox } from '@flexilte/skeleton';
	import { stateStore } from '$lib/stores';

	export let state: string;
	export let title: string = '';
	export let unit: string = '';

	let data: number;
	stateStore.subscribe((states: Record<string, any>) => {
		data = states[state];
	});
</script>

{#if data}
	<div class="text-center mx-auto">
		<div class="text-4xl glow-text">{title}</div>

		<div class="text-3xl mt-4 glow-text">
			{data}
			{unit}
		</div>
	</div>
{:else}
	<LoadingBox />
{/if}
