// API communication handler
class ConverterHandler {
    async sendConversionRequest(data) {
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        return await response.json();
    }
}