import {REPLICATE_API_TOKEN} from '$env/static/private';
import Replicate from "replicate";

const replicate = new Replicate({auth: REPLICATE_API_TOKEN});

export async function POST({ request }) {
  try {
    // Parse the request body
    const body = await request.json();

    const userPrompt = `Which of the following objects is another way to describe ${body.target}? Reply with only the name of the object, or 'None' if none of the provided objects are similar.
    Objects: ${body.objects}`;

    const input = {
        prompt: userPrompt,
        prompt_template: `<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n`
    };
    
    console.log('Running Llama 3 8B...');
    let output = await replicate.run("meta/meta-llama-3-8b-instruct", { input });
    output = output.join("").toLowerCase();
    if (output.includes('none') || !body.objects.includes(output)) {
        output = null;
    }

    // Respond with the objects
    return new Response(JSON.stringify({ output: output }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Error:', error);
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
}