<script lang="ts">
	import { stateStore } from '$lib/stores';
	import { callHass } from '$lib/common';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	export let state: string;
	export let width: string = 'w-full';
	export let height: string = 'h-full';
	export let onClass: string = 'bg-success-500';
	export let offClass: string = 'bg-error-500';
	let data: boolean;
	stateStore.subscribe((states: Record<string, any>) => {
		if (!states[state]) {
			return;
		}
		if (states[state] === 'on' || states[state] === 'locked') {
			data = true;
		} else {
			data = false;
		}
	});
	const handleClick = () => {
		const [domain, entity] = state.split('.');
		callHass('service', {
			domain,
			service: 'toggle',
			data: {
				entity_id: state
			}
		});
	};
</script>

{#if data !== null && data !== undefined}
	{#if data}
		<div on:click={handleClick} class={`${width} ${height} ${onClass}`}></div>
	{:else}
		<div on:click={handleClick} class={`${width} ${height} ${offClass}`}></div>
	{/if}
{:else}
	<ProgressRadial value={undefined} {width} />
{/if}
