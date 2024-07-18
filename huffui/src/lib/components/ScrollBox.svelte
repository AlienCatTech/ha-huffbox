<script lang="ts">
	import { stateStore } from '$lib/stores';
	import { populate } from '$lib/common';
	import { onMount } from 'svelte';

	export let state: string;
	let content: string[] = [];
	let lines: string[] = [];
	let link: string = '';
	let pointer: number = 0;
	const MAX_LINE = 9;
	stateStore.subscribe((states: Record<string, any>) => {
		if (states[state] && states[state] != link) {
			link = states[state];
			fetch(link)
				.then((res) => res.json())
				.then((j) => {
					content = j;
				});
		}
	});
	const replaceInj = (text: string) => {
		text = populate(text, {});
		return `<div class="flex">${text}</div>`;
	};

	onMount(() => {
		const addLine = () => {
			if (content.length > 0) {
				const curLine = content[pointer];
				lines = [...lines, replaceInj(curLine)];
				pointer++;
			}
			if (lines.length > MAX_LINE) {
				lines.shift();
			}
			if (pointer >= content.length) {
				pointer = 0;
			}
			setTimeout(addLine, Math.random() * (1000 - 200) + 200);
		};
		addLine();
	});
</script>

<div class="overflow-hidden flex flex-col justify-start h-full w-full p-2 tracking-wide">
	{#each lines as line}
		<div>{@html line}</div>
	{/each}
</div>
