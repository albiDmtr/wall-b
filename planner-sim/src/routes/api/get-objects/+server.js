import {REPLICATE_API_TOKEN} from '$env/static/private';
import Replicate from "replicate";

const replicate = new Replicate({auth: REPLICATE_API_TOKEN});

export async function POST({ request }) {
  try {
    // Parse the request body
    const body = await request.json();

    const input = {
      image: body.image
    };
    
    console.log('Starting Yolo v10...');
    const output = await replicate.run("shubhamai/yolov10:e387e93e8f7f55fa5ae21e94585cfae5361468376c45fc874defa1dd5ca67f5d", { input });
    console.log('Inference complete.');
    
    console.log(output);
    const response = JSON.parse(output).map(obj => obj.name);

    // Respond with the objects
    return new Response(JSON.stringify({ objects: response }), {
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