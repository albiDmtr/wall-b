import {PUBLIC_REPLICATE_API_TOKEN} from '$env/static/public';
import Replicate from "replicate";

const replicate = new Replicate();

export const getObjects = async (image) => {
    const input = {
        input_media: `data:application/octet-stream;base64,${image}`
    };
    
    const output = await replicate.run("zsxkib/yolo-world:07aee09fc38bc4459409caa872ea416717712f4e6e875f8751a0d0d5bbea902f", { input });
    console.log(output);

    return ["hehe"];
}