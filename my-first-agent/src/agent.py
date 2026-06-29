import Anthropic from "@anthropic-ai/sdk";
import { client } from "./client";

#Step 1: Define tools with JSON Schema
const tools: Anthropic.Tool[] = [
    {
        name: "get_weather",
        description: "Get the current weather for a specific city. Returns temperature in celsius, conditions, and humidity.",
        input_schema: {
            type: "object",
            properties: {
                city: {
                    type: "string",
                    description: "City name, e.g., 'New York', 'London', 'Tokyo'."
                },
            },
            required: ["city"],
        },
    },
    required: ["city"],
];

#Step 2: Implementaion tool handlers
async function executeTool(name: string, input: Record<string, unknown>): Promise<string> {
    switch(name) {
        case "get_weather":{
            conts city = input.city as string;
            // in a real app, call a weather API here.
            const data = {
                city,
                temperature: 22,
                conditions: "Partly cloudy",
                humidity: 65,
            };
            return JSON.stringify(data);
        }
        default:
            throw new Error(`Tool ${name} not found`);
    }
}

// Steps 3: Build the agent loop
async function runAgent(useMessage: string): Promise<String> {
    const messages: Anthropic.MessageParam[] = [
        {
            role: "user",
            content: useMessage,
        },
    ];

    const maxTurns = 10;

    for (let turn = 0; turn < maxTurns; turn++) {
        const response = await client.responses.create({
            model: "claude-sonnet-4-5",
            max_tokens: 1000,
            system: "You are a helpful assistant. Use the get_weather tool to look up weather when asked.",
            messages,
            tools,
        });
        

        #Always append Claude's response to the conversation
        messages.push({
            role: "assistant",
            content: response.content
        });

        # If Claude stopped without calling tools, we have our final answer
        if (response.stop_reason === "end_turn") {
           const textBlock = response.content.find((b) => b.type === "text");
           return (textBlock as Anthropic.TextBlock)?.text??"";
        } 

        #Execute every tool call in the response
        const toolResults: Anthropic.ToolResultBlockParam[] = [];

        for(const block of response.content) {
            if (block.type === "tool_use") {
                try {
                    const result = await executeTool(block.name, block.input as Record<string, unknown>);
                    toolResults.push({
                        type: "tool_result",
                        tool_use_id: block.id,
                        content: result,
                    });
                } catch (error) {
                    toolResults.push({
                        type: "tool_result",
                        tool_use_id: block.id,
                        content: `Error: ${error instanceof Error ? error.message : "Unknown error"}`,
                        is_error: true,
                    });
                }
            }
        }

        #Feed tool reults back as a user message
        messages.push({
            role: "user",
            content: toolResults,
        });
    }

    throw new Error("Agent exceeded Maximum turns");
}