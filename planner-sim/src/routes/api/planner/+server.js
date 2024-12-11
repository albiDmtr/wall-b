import {REPLICATE_API_TOKEN} from '$env/static/private';
import Replicate from "replicate";
import {
  systemPrompt,
  replanPrompt,
  planLanguage,
  envDescription
} from './promptConfig';

const replicate = new Replicate({auth: REPLICATE_API_TOKEN});

let context = [];

export async function POST({ request }) {
  try {
    // Parse the request body
    const body = await request.json();
    if (body.prompt) {
      context = [{
        party: 'user',
        text: body.prompt
      }]
    } else if (body.awakeLine) {
      const lastCode = context.at(-1).text;
      const codeExecuted = lastCode.split('\n').slice(0, body.awakeLine).join('\n');
      context.push({
        party: 'robot',
        text: `${replanPrompt}\n${codeExecuted}`
      });
    } else {
      throw new Error('Request body must contain a prompt or awakeLine');
    }

    const extendedSystemPrompt = `${systemPrompt}\n\n${(
      context.filter((item) => item.party === 'robot').map((item) => item.text).join('\n\n')
    )}`
    console.log(extendedSystemPrompt);

    // <|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|>
    const input = {
        top_p: 0.9,
        prompt: context[0].text,
        min_tokens: 10,
        max_tokens: 712,
        temperature: 0.6,
        prompt_template: `<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n${extendedSystemPrompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n`,
        presence_penalty: 1.15
    };
    
    console.log(context);
    console.log('Running Llama 3 70B...');
    let output = await replicate.run("meta/meta-llama-3-70b-instruct", { input });
    output = output.join("");
    console.log('Inference complete.');
    
    context.push({
      party: 'assistant',
      text: output
    });


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