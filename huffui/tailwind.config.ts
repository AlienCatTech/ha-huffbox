import { join } from 'path';
import type { Config } from 'tailwindcss';
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import { skeleton } from '@skeletonlabs/tw-plugin';
import { scifiTheme } from './src/theme';

export default {
	darkMode: 'class',
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		'./static/*.{json,yaml,yml}',
		join(require.resolve('@skeletonlabs/skeleton'), '../**/*.{html,js,svelte,ts}')
	],
	theme: {
		extend: {
			height: {
				'128': '32rem',
				'160': '40rem',
				'192': '48rem',
				'224': '56rem',
				'320': '80rem'
			},
			width: {
				'128': '32rem',
				'160': '40rem',
				'192': '48rem',
				'224': '56rem',
				'320': '80rem'
			},
			fontSize: {
				'10xl': '9rem',
				'11xl': '10rem',
				'12xl': '11rem'
			},
			fontFamily: {
				barcode: ['Barcode', 'sans-serif'],
				digital: ['Orbitron', 'sans-serif']
			}
		}
	},
	plugins: [
		forms,
		typography,
		skeleton({
			themes: {
				custom: [scifiTheme]
			}
		})
	],
	safelist: [
		{
			pattern: /^(w-|h-|md:|gap-|m-|p-|text-|border|-m-|bg-|tracking-widest|from-|to-)/
		}
	]
} satisfies Config;
