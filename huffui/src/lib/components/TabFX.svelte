<script lang="ts">
	import Icon from '@iconify/svelte';
	import heart from '@iconify/icons-mdi/plus';
	import circle from '@iconify/icons-mdi/circle';

	export let type: string;
	export let classList: string;
</script>

{#if type === 'plus'}
	<Icon class={classList} icon={heart} />
{:else if type === 'circle'}
	<Icon class={classList} icon={circle} />
{/if}
