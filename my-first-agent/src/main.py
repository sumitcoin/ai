import { runAgent } from "./agent";

async function main() {
    const userMessage = "What is the weather like in London?";
    const response = await runAgent(userMessage);
    console.log(response);
}

main().catch(console.error);