<script lang="ts">
	import { stateStore } from '$lib/stores';

	export let type = '';
	export let state;
	let text = '';
	export let classList = '';
	stateStore.subscribe((states: Record<string, any>) => {
		text = states[state] ?? '';
	});
	const buildClass = () => {
		let classString = '';
		if (type.startsWith('h')) {
			classString += `${type} `;
		}
		if (type === 'title') {
			classString += `text-5xl `;
		}
		if (classList) {
			classString += `${classList} `;
		}
		return classString;
	};
</script>

{#if type === 'h1'}
	<h1 class={buildClass()}>
		<div>{text}</div>
	</h1>
{:else if type === 'h2'}
	<h2 class={buildClass()}>
		<div>{text}</div>
	</h2>
{:else if type === 'h3'}
	<h3 class={buildClass()}>
		<div>{text}</div>
	</h3>
{:else if type === 'h4'}
	<h4 class={buildClass()}>
		<div>{text}</div>
	</h4>
{:else if type === 'h5'}
	<h5 class={buildClass()}>
		<div>{text}</div>
	</h5>
{:else if type === 'h6'}
	<h6 class={buildClass()}>
		<div>{text}</div>
	</h6>
{:else}
	<div class={buildClass()}>{text}</div>
{/if}
