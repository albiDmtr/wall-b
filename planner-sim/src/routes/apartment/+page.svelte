<script>
    import { onMount } from 'svelte';
    import * as THREE from 'three';
    import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
    import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

    let wrapper;
    let canvas;
    let interpretText = '';
    let llmText = '';
    let text = "Select an action.";
    let llmOutput = 'test\nout\nput';
    let similarObjects = '';
    let similarTarget = '';
    let replanLineNo = 0;

    let downloadImage = () => {};
    let getListOfObjects = () =>  {};
    let interpretScene = () => {};
    const promptLLM = () => {
        llmOutput = "Planning...";
        fetch('/api/planner', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({prompt: llmText}),
        }).then((response) => {
          return response.json();
        }).then((data) => {
          console.log(data);
          llmOutput = data.output;
        }).catch((error) => {
          console.error('Error:', error);
        });
    }
    const replan = () => {
        llmOutput = "Replanning...";
        fetch('/api/planner', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({awakeLine: replanLineNo}),
        }).then((response) => {
          return response.json();
        }).then((data) => {
          console.log(data);
          llmOutput = data.output;
        }).catch((error) => {
          console.error('Error:', error);
        });
    }
    const findSimilar = () => {
        text = "Finding similar objects...";
        fetch('/api/find-similar', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({objects: similarObjects, target: similarTarget})
        }).then((response) => {
          return response.json();
        }).then((data) => {
          console.log(data);
          text = data.output;
        }).catch((error) => {
          console.error('Error:', error);
        });
    }
  
    onMount(() => {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer({ canvas });
      const textureLoader = new THREE.TextureLoader();
      const modelLoader = new GLTFLoader();

      // define API calls
      getListOfObjects = () => {
        renderer.render(scene, camera);
        text = "Getting list of objects...";
        fetch('/api/get-objects', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: renderer.domElement.toDataURL('image/png') }), // Include any required payload
        }).then((response) => {
          return response.json();
        }).then((data) => {
          text = data.objects;
        }).catch((error) => {
          console.error('Error:', error);
        });
      }

      interpretScene = () => {
        renderer.render(scene, camera);
        text = "Interpreting scene...";
        fetch('/api/interpret-scene', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image: renderer.domElement.toDataURL('image/png'),
            question: interpretText
          }),
        }).then((response) => {
          return response.json();
        }).then((data) => {
          text = data.answer;
        }).catch((error) => {
          console.error('Error:', error);
        });
      }

      downloadImage = () =>  {
          renderer.render(scene, camera);
          const dataURL = renderer.domElement.toDataURL('image/png');
          const link = document.createElement('a');
          link.href = dataURL;
          link.download = 'canvas-image.png';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
      }

      renderer.setSize(1200, 800);
      scene.background = new THREE.Color(0x303030);

      // set default camera position
      camera.position.z = -15;
      camera.position.y = 10.5 ;

      // Add OrbitControls
      //const controls = new OrbitControls(camera, renderer.domElement);
      //controls.update();


      // add light
      // Add ambient light
      const ambientLight = new THREE.AmbientLight(0xffffff, 1.5); // soft white light
      scene.add(ambientLight);

      // Add point lights
      const pointLight1 = new THREE.PointLight(0xffffff, 700, 100);
      pointLight1.position.set(0, 18, 0);
      scene.add(pointLight1);

      const pointLight2 = new THREE.PointLight(0xffffff, 700, 100);
      pointLight2.position.set(0, 18, -50);
      scene.add(pointLight2);

      // add objects
      // Add livingroom parquet
      const parquetTexture = textureLoader.load('./textures/parquet.jpg');
      parquetTexture.wrapS = THREE.RepeatWrapping;
      parquetTexture.wrapT = THREE.RepeatWrapping;
      parquetTexture.repeat.set(2, 2)
      const livingroomGroundGeometry = new THREE.PlaneGeometry(40, 60);
      const livingroomGroundMaterial = new THREE.MeshStandardMaterial({ map: parquetTexture, side: THREE.DoubleSide });
      const livingroomGround = new THREE.Mesh(livingroomGroundGeometry, livingroomGroundMaterial);
      livingroomGround.rotation.x = -Math.PI / 2;
      livingroomGround.name = "wall-ground-livingroom";
      scene.add(livingroomGround);

      // Add kitchen floor
      const kitchenFloorTexture = textureLoader.load('./textures/tiles.jpg');
      kitchenFloorTexture.wrapS = THREE.RepeatWrapping;
      kitchenFloorTexture.wrapT = THREE.RepeatWrapping;
      kitchenFloorTexture.repeat.set(2, 2)
      const kitchenGroundGeometry = new THREE.PlaneGeometry(40, 40);
      const kitchenGroundMaterial = new THREE.MeshStandardMaterial({ map: kitchenFloorTexture, side: THREE.DoubleSide });
      const kitchenGround = new THREE.Mesh(kitchenGroundGeometry, kitchenGroundMaterial);
      kitchenGround.rotation.x = -Math.PI / 2;
      kitchenGround.position.set(0, 0, -50);
      kitchenGround.name = "wall-ground-kitchen";
      scene.add(kitchenGround);

      // Add walls
      const wall1Geometry = new THREE.PlaneGeometry(100, 20);
      const wall1Material = new THREE.MeshStandardMaterial({ color: 0xffffff, side: THREE.DoubleSide, transparent: true });
      const wall1 = new THREE.Mesh(wall1Geometry, wall1Material);
      wall1.rotation.y = Math.PI / 2;
      wall1.position.set(20, 10, -20);
      wall1.name = "wall-back";
      scene.add(wall1);

      const wall2Material = new THREE.MeshStandardMaterial({ color: 0xffffff, side: THREE.DoubleSide, transparent: true });
      wall2Material.opacity = 1;
      const wall2 = new THREE.Mesh(wall1Geometry, wall2Material);
      wall2.rotation.y = Math.PI / 2;
      wall2.position.set(-20, 10, -20);
      wall2.name = "wall-front";
      scene.add(wall2);

      const kitchenWallTexture = textureLoader.load('./textures/kitchen_tiles.jpg');
      kitchenWallTexture.wrapS = THREE.RepeatWrapping;
      kitchenWallTexture.wrapT = THREE.RepeatWrapping;
      kitchenWallTexture.repeat.set(3, 3)
      const kitchenWallMaterial = new THREE.MeshStandardMaterial({ map: kitchenWallTexture, side: THREE.DoubleSide });
      const wall3Geometry = new THREE.PlaneGeometry(40, 20);
      const wall3 = new THREE.Mesh(wall3Geometry, kitchenWallMaterial);
      wall3.position.set(0, 10, -70);
      wall3.name = "wall-kitchen";
      scene.add(wall3);

      const wall4 = new THREE.Mesh(wall3Geometry, wall1Material);
      wall4.position.set(0, 10, 30);
      wall4.name = "wall-livingroom";
      scene.add(wall4);

      const wall5Geometry = new THREE.BoxGeometry(12, 20, 2);
      const wall5 = new THREE.Mesh(wall5Geometry, wall1Material);
      wall5.position.set(14, 10, -30);
      wall5.name = "wall-separator-right";
      scene.add(wall5);

      const wall6 = new THREE.Mesh(wall5Geometry, wall1Material);
      wall6.position.set(-14, 10, -30);
      wall6.name = "wall-separator-left";
      scene.add(wall6);

      const ceilingGeometry = new THREE.PlaneGeometry(40, 100);
      const ceiling = new THREE.Mesh(ceilingGeometry, wall2Material);
      ceiling.rotation.x = -Math.PI / 2;
      ceiling.position.set(0, 20, -20);
      ceiling.name = "wall-ceiling";
      scene.add(ceiling);

      
      // Add sofa
      modelLoader.load('./models/sofa.glb', (gltf) => {
        const model = gltf.scene;
        model.scale.set(0.23, 0.23, 0.23);
        model.position.set(15, 0, 5);
        model.name = "sofa";
        scene.add(model);
      }, undefined, (error) => {
        console.error(error);
      });

      // Add bookshelf
      modelLoader.load('./models/bookshelf.glb', (gltf) => {
        const model = gltf.scene;
        model.scale.set(65, 65, 65);

        model.rotation.y = Math.PI;
        model.position.set(5, 0, 29.8);
        model.name = "bookshelf";
        scene.add(model);
      }, undefined, (error) => {
        console.error(error);
      });

      // Add tv stand
      modelLoader.load('./models/tv_stand.glb', (gltf) => {
        const model = gltf.scene;

        model.rotation.y = Math.PI / 2;
        
        model.scale.set(14, 10, 14);
        model.position.set(-19.7, 8, 5);
        model.name = "tv stand";
        scene.add(model);
      }, undefined, (error) => {
        console.error(error);
      });

      // Add plant
      modelLoader.load('./models/plant.glb', (gltf) => {
        const model = gltf.scene;
        
        model.scale.set(9, 9, 9);
        model.position.set(-14, 4.5, -24);

        model.name = "potted plant";
        scene.add(model);
      }, undefined, (error) => {
        console.error(error);
      });

      // Add closet
      modelLoader.load('./models/closet.glb', (gltf) => {
        const model = gltf.scene;

        
        model.scale.set(9, 9, 9);
        model.position.set(15, 12, -20.5);

        model.name = "closet";
        scene.add(model);
      }, undefined, (error) => {
        console.error(error);
      });

      // Add trashcan
      modelLoader.load('./models/trashcan.glb', (gltf) => {
        const model = gltf.scene;

        model.rotation.y = Math.PI / 2;
        
        model.scale.set(8, 6, 8);
        model.position.set(-15, -0.1, 25);

        model.name = "trashcan";
        scene.add(model);
      }, undefined, (error) => {
        console.error(error);
      });


      // Add coffee table
      modelLoader.load('./models/coffee_table.glb', (gltf) => {
        const model = gltf.scene;

        model.rotation.y = Math.PI / 2;
        
        model.scale.set(8, 8, 8);
        model.position.set(2, 3.4, 5);

        model.name = "coffee table";
        scene.add(model);
      }, undefined, (error) => {
        console.error(error);
      });

      // Add newspaper to coffee table
      modelLoader.load('./models/newspaper.glb', (gltf) => {
          const model = gltf.scene;
          
          model.scale.set(0.16, 0.16, 0.16);
          model.rotation.y = Math.PI / 10;

          model.position.set(2, 4.8, 2);

          model.name = "newspaper";
          scene.add(model);
        }, undefined, (error) => {
        console.error(error);
      });

      
      // Kitchen models
      // Add kitchen counter
      modelLoader.load('./models/kitchen_counter.glb', (gltf) => {
          const model = gltf.scene;

          model.scale.set(8, 8, 8);

          model.position.set(17.5, 0, -62);

          model.name = "kitchen counter";
          scene.add(model);
        }, undefined, (error) => {
        console.error(error);
      });

      // Add oven
      modelLoader.load('./models/oven.glb', (gltf) => {
          const model = gltf.scene;

          model.scale.set(0.015, 0.015, 0.015);
          model.position.set(16.5, 0, -51.6);
          model.rotation.y = -Math.PI / 2;

          model.name = "oven";
          scene.add(model);
        }, undefined, (error) => {
        console.error(error);
      });
      
      // Add fridge
      modelLoader.load('./models/fridge.glb', (gltf) => {
          const model = gltf.scene;

          model.scale.set(0.085, 0.085, 0.085);
          model.position.set(16, 0, -48.8);
          model.rotation.y = Math.PI / 2;

          model.name = "fridge";
          scene.add(model);
        }, undefined, (error) => {
        console.error(error);
      });

      // Add kitchen table
      modelLoader.load('./models/table.glb', (gltf) => {
          const model = gltf.scene;

          model.scale.set(0.75, 0.75, 0.75);
          model.position.set(0, 0, -65);
          model.rotation.y = Math.PI / 2;

          model.name = "kitchen table";
          scene.add(model);
        }, undefined, (error) => {
        console.error(error);
      });

      // Add microwave
      modelLoader.load('./models/microwave.glb', (gltf) => {
          const model = gltf.scene;

          model.scale.set(0.07, 0.07, 0.07);
          model.position.set(3, 8.5, -67);

          model.name = "microwave";
          scene.add(model);
        }, undefined, (error) => {
        console.error(error);
      });

        // Add soda
        modelLoader.load('./models/soda.glb', (gltf) => {
          const model = gltf.scene;

          model.scale.set(0.1, 0.1, 0.1);
          model.position.set(-4, 7.7, -63);

          model.name = "soda";
          scene.add(model);
        }, undefined, (error) => {
        console.error(error);
      });

      // Add pizza
          modelLoader.load('./models/pizza.glb', (gltf) => {
          const model = gltf.scene;

          model.scale.set(4, 4, 4);
          model.position.set(-1, 7, -64);

          model.name = "pizza";
          scene.add(model);
        }, undefined, (error) => {
        console.error(error);
      });

      // Add tray
      modelLoader.load('./models/tray.glb', (gltf) => {
          const model = gltf.scene;

          model.scale.set(4.5, 4.5, 4.5);
          model.position.set(17, 6.7, -60);

          model.name = "tray";
          scene.add(model);
        }, undefined, (error) => {
        console.error(error);
      });
  
      // Function to handle keydown events
      const handleKeyDown = (event) => {
        const moveDistance = 0.5;
        const rotationAngle = 0.05;
        const direction = new THREE.Vector3();

        switch (event.key) {
          case 'w':
            direction.set(0, 0, -moveDistance);
            direction.applyAxisAngle(new THREE.Vector3(0, 1, 0), camera.rotation.y);
            camera.position.add(direction);
            break;
          case 's':
            direction.set(0, 0, moveDistance);
            direction.applyAxisAngle(new THREE.Vector3(0, 1, 0), camera.rotation.y);
            camera.position.add(direction);
            break;
          case 'a':
            direction.set(-moveDistance, 0, 0);
            direction.applyAxisAngle(new THREE.Vector3(0, 1, 0), camera.rotation.y);
            camera.position.add(direction);
            break;
          case 'd':
            direction.set(moveDistance, 0, 0);
            direction.applyAxisAngle(new THREE.Vector3(0, 1, 0), camera.rotation.y);
            camera.position.add(direction);
            break;
          case 'i':
            camera.rotation.x -= rotationAngle;
            break;
          case 'k':
            camera.rotation.x += rotationAngle;
            break;
          case 'j':
            camera.rotation.y += rotationAngle;
            break;
          case 'l':
            camera.rotation.y -= rotationAngle;
            break;
          }

          console.log("Camera position: ", camera.position);
          console.log("Camera rotation: ", camera.rotation);
      };

      // Add event listener for keydown events
      window.addEventListener('keydown', handleKeyDown);

      // Animation loop
      const animate = () => {
        requestAnimationFrame(animate);
        //controls.update();
        renderer.render(scene, camera);
      };
      animate();

      // Cleanup event listener on component unmount
      return () => {
        window.removeEventListener('keydown', handleKeyDown);
      };
    });
  </script>
  <canvas bind:this={canvas} width="1200" height="800"></canvas>
  <div class="controls">
    <div class="left">
      <button on:click={downloadImage}>Download scene</button>
      <button on:click={getListOfObjects}>List of objects</button>
      <div class="skill-cont">
        <input type="text" bind:value={interpretText} />
        <button on:click={interpretScene}>Interpret scene</button>
      </div>
      <pre class="scenetxt">{text}</pre>
      <div class="skill-cont">
        <input type="text" bind:value={similarObjects} placeholder="Objects" />
        <input type="text" bind:value={similarTarget} placeholder="Target" />
        <button on:click={findSimilar}>Find similar</button>
      </div>
    </div>
    <div class="right">
      <textarea name="prompt" id="text" bind:value={llmText}></textarea>
      <button on:click={promptLLM}>Plan</button>
      <div class="code-cont">
        {#each llmOutput.split('\n') as line, index}
            <span>{index + 1}</span><code>{line}</code><br>
        {/each}
      </div>
      <div>
        Awake line no.: <input type="number" bind:value={replanLineNo}/>
        <button on:click={replan}>Replan</button>
      </div>
    </div>
  </div>

  <style>
    .controls {
      display: flex;
      justify-content: space-evenly;
      margin-top: 20px;
    }
    canvas {
      display: block;
    }
    .scenetxt {
      width: 500px;
      height: 200px;
      overflow: scroll;
      background-color: rgba(230, 230, 230);
    }
    .code-cont {
        margin: 10px;
        padding: 10px;
        width: 600px;
        background-color: rgb(30, 30, 30);
        white-space: pre-wrap;
        color: white;
    }
    .code-cont code {
      line-height: 1;
    }
    .code-cont span {
      display: inline-block;
      width: 24px;
      font-size: 12px;
      font-family: 'Roboto Mono', monospace;
      line-height: 1;
    }
  </style>