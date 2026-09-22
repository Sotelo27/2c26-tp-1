async function save(data, fileName) {
    const filePath = path.join(__dirname, fileName);
    try {
        await fs.promises.writeFile(filePath, JSON.stringify(data, null, 2));
    } catch (err) {
        console.error(`Error writing to ${filePath}:`, err);
    }
}