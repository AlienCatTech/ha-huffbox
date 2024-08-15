<script lang="ts">
	import Icon from '@iconify/svelte';
	import file from '@iconify/icons-mdi/file';
	import heart from '@iconify/icons-mdi/heart';
	import lungs from '@iconify/icons-mdi/lungs';
	import oxygenTank from '@iconify/icons-mdi/oxygen-tank';
	import thermostat from '@iconify/icons-mdi/thermostat';

	export let type: string;
	export let classList: string;
</script>

{#if type === 'file'}
	<Icon class={classList} icon={file} />
{:else if type === 'heart'}
	<Icon class={classList} icon={heart} />
{:else if type === 'lungs'}
	<Icon class={classList} icon={lungs} />
{:else if type === 'oxygenTank'}
	<Icon class={classList} icon={oxygenTank} />
{:else if type === 'thermostat'}
	<Icon class={classList} icon={thermostat} />
{:else}
	<Icon class={classList} icon={type} />
{/if}
