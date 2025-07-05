<script>
    let text = "Hello \nWorld!";
    let userPrompt = "";

    const promptLLM = () => {
        fetch('/api/planner', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({prompt: userPrompt}), // Include any required payload
        }).then((response) => {
          return response.json();
        }).then((data) => {
          console.log(data);
          text = data.output;
        }).catch((error) => {
          console.error('Error:', error);
        });
    }
</script>
<input type="text" bind:value={userPrompt}>
<button on:click={promptLLM}>
Prompt LLM
</button>
<div class="code-cont">
    <code>
        <pre>
            {@html text.replace('\n', '<br>')}
        </pre>
    </code>
</div>

<style>
    code, pre {
        display: block;
        white-space: pre-wrap;
        color: white;
        font-size: 26px;
    }
    .code-cont {
        margin: 10px;
        padding: 10px;
        max-width: 1600px;
        background-color: rgb(30, 30, 30);
    }
</style>