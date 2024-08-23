const fs = require('fs');
const path = require('path');
const glob = require('glob');

function extractTailwindClasses(jsonData) {
	const tailwindClasses = new Set();

	function extractClassesFromString(str) {
		if (typeof str === 'string') {
			const classes = str.split(' ');
			classes
				.filter((cls) => /^[a-z]/.test(cls) && !cls.includes('.'))
				.forEach((cls) => tailwindClasses.add(cls));
		}
	}

	function traverseObject(obj) {
		if (obj && typeof obj === 'object') {
			for (const key in obj) {
				if (obj.hasOwnProperty(key)) {
					const value = obj[key];
					if (typeof value === 'string') {
						extractClassesFromString(value);
					} else if (Array.isArray(value)) {
						value.forEach(traverseObject);
					} else if (typeof value === 'object') {
						traverseObject(value);
					}
				}
			}
		}
	}

	traverseObject(jsonData);
	return Array.from(tailwindClasses);
}

const processFiles = () => {
	const filePaths = glob.sync(path.join(__dirname, '../static/custom*.{json,yaml,yml}'));

	const tailwindClasses = new Set();

	filePaths.forEach((filePath) => {
		const fileContent = fs.readFileSync(filePath, 'utf-8');
		let jsonData;

		try {
			jsonData = JSON.parse(fileContent);
		} catch (e) {
			// If the file is not a JSON file, try parsing it as YAML
			const yaml = require('yaml');
			jsonData = yaml.parse(fileContent);
		}

		const classes = extractTailwindClasses(jsonData);
		classes.forEach((cls) => tailwindClasses.add(cls));
	});

	const result = Array.from(tailwindClasses).sort();

	const outputFilePath = path.join(__dirname, 'safeList.js');
	const outputContent = `const tailwindClasses = ${JSON.stringify(result, null, 2)};\n\nexport default tailwindClasses;`;
	fs.writeFileSync(outputFilePath, outputContent);
	console.log(`Tailwind classes written to ${outputFilePath}`);
};

processFiles();
