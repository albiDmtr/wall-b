import {REPLICATE_API_TOKEN} from '$env/static/private';
import Replicate from "replicate";
import { context } from 'three/tsl';

const replicate = new Replicate({auth: REPLICATE_API_TOKEN});

export async function POST({ request }) {
  try {
    // Parse the request body
    const body = await request.json();

    const input = {
      image: body.image,
      context: 'I see this. Answer with only a yes or no.',
      question: body.question,
    };
    
    console.log('Starting BLIP-2...');
    const output = await replicate.run("andreasjansson/blip-2:f677695e5e89f8b236e52ecd1d3f01beb44c34606419bcc19345e046d8f786f9", { input });
    console.log('Inference complete.');
    
    const sanitizedOutput = output.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
    let response = false;
    if (sanitizedOutput.includes('yes')) {
        response = true;
    }

    // Respond with the objects
    return new Response(JSON.stringify({ answer: response }), {
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