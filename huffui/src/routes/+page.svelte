<script lang="ts">
	import { onMount } from 'svelte';
	import { Flexilte } from '@flexilte/core';
	import YAML from 'yaml';
	import { stateStore } from '$lib/stores';
	import type { LayoutConfig } from '@flexilte/core';
	import { components } from '$lib/default';
	import { setModeCurrent } from '@skeletonlabs/skeleton';
	import { fancyLogging } from '$lib/common';
	import { dev } from '$app/environment';
	import { fade } from 'svelte/transition';
	const loadingLayout: LayoutConfig<typeof components> = {
		rows: [
			{
				posX: 'middle',
				posY: 'middle',
				nodeClass: 'h-svh',

				cols: [
					{
						component: 'ImageBox',
						props: {
							url: 'favicon.png'
						},
						posX: 'middle',
						posY: 'middle',
						wrapperClass: 'h-full w-56'
					}
				]
			}
		]
	};

	let layoutConfig: LayoutConfig<typeof components> = {};
	let currentLayout = '';

	async function loadConfig(
		option: string,
		custom: string
	): Promise<LayoutConfig<typeof components>> {
		try {
			const urlDict: Record<string, string> = {
				default: 'default-layout.json',
				'fullscreen-image': 'fullscreen-image.json',
				'fullscreen-text': 'fullscreen-text.json',
				'fullscreen-video': 'fullscreen-video.json',
				custom: custom || '404.json'
			};
			const url = option in urlDict ? urlDict[option] : urlDict['default'];
			currentLayout = option;
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error('Primary API failed');
			}
			if (custom.endsWith('.yaml') || custom.endsWith('.yml')) {
				return YAML.parse(await response.text());
			}

			return await response.json();
		} catch (error) {
			console.error('Failed to load layout');
			return {};
		}
	}

	function transformDict(input: { [key: string]: { [key: string]: any } }): { [key: string]: any } {
		let result: { [key: string]: any } = {};
		for (const key in input) {
			if (input[key] && typeof input[key] === 'object') {
				result[key] = input[key]['state'];
			}
		}
		return result;
	}
	onMount(async () => {
		setModeCurrent(true);

		window.addEventListener('message', async (event) => {
			const { msg, data } = event.data;
			// console.log(msg, data);
			if (!data) {
				return;
			}
			const payload = transformDict(data);
			const newLayout = payload['select.huffbox_select_dashboard'];

			if (Object.keys(layoutConfig).length === 0 || newLayout !== currentLayout) {
				layoutConfig = await loadConfig(newLayout, payload['text.huffbox_custom_layout_link']);
				fancyLogging('init', data);
			}
			stateStore.set(payload);
		});
		if (dev) {
			const mock = {
				'text.huffbox_subject_picture': 'https://placedog.net/500/1500',
				'text.huffbox_subject_name': 'test',
				'text.huffbox_live_chat': 'live-chat.json',
				'text.huffbox_custom_layout_link': 'custom.json',
				'text.huffbox_video_link':
					'https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4',
				'sensor.huffbox_heart_rate': '50',
				'sensor.huffbox_pulse': '50',
				'sensor.huffbox_spo2': '50',
				'sensor.huffbox_resp': '50',
				'sensor.huffbox_temp': '50',
				'lock.huffbox_control_lock': 'locked',
				'light.huffbox_control_light': 'off',
				'fan.huffbox_control_fan': 'on',
				'text.huffbox_banner': 'MEOW',
				'time.huffbox_time': '12:34:56'
			};
			stateStore.set(mock);
			layoutConfig = await loadConfig('default', mock['text.huffbox_custom_layout_link']);
		}
	});
</script>

{#if Object.keys(layoutConfig).length === 0}
	<div transition:fade>
		<Flexilte {components} layoutConfig={loadingLayout} />
	</div>
{:else}
	<div transition:fade>
		<Flexilte {components} {layoutConfig} />
	</div>
{/if}
