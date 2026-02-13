from diffusers import StableDiffusionPipeline as sdp
import torch, os, time


def generateImage(prompt):

    cwd = os.getcwd()
    os.makedirs(os.path.join(cwd,'Exports',f'{int(time.time())}'),exist_ok=True)
    exportPath = os.path.join(cwd,'Exports',f'{int(time.time())}',f'{int(time.time())}.png')
    pipe = sdp.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    )

    pipe = pipe.to('cuda')

    img = pipe(prompt).images[0]

    img.save(exportPath)


generateImage(input('Enter prompt:'))